"""Self-contained privacy scanner regressions; fixtures never contain real user data."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from urllib.parse import quote
import zlib

spec = importlib.util.spec_from_file_location("privacy_scanner", Path(__file__).with_name("check_privacy.py"))
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


def png_chunk(kind, payload):
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)


def png():
    return bytes([137, 80, 78, 71, 13, 10, 26, 10]) + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(bytes(5))) + png_chunk(b"IEND", b"")


def riff_chunk(kind, payload):
    return kind + struct.pack("<I", len(payload)) + payload + (bytes(1) if len(payload) % 2 else b"")


def webp(chunks):
    payload = b"WEBP" + chunks
    return b"RIFF" + struct.pack("<I", len(payload)) + payload


def git(root, *args, data=None):
    return subprocess.check_output(["git", "-C", str(root), *args], input=data, stderr=subprocess.DEVNULL)


def scan(root, staged=False):
    output = io.StringIO()
    argv = ["check_privacy.py"] + (["--staged"] if staged else [])
    with mock.patch.object(scanner, "ROOT", root), mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(output):
        result = scanner.main()
    return result, json.loads(output.getvalue())


class PrivacyChecks(unittest.TestCase):
    def test_empty_index_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            git(root, "init", "-q")
            result, report = scan(root, True)
            self.assertNotEqual(result, 0)
            self.assertFalse(report["passed"])

    def test_index_symlink_mode_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            git(root, "init", "-q")
            oid = git(root, "hash-object", "-w", "--stdin", data=b"target.txt").decode().strip()
            git(root, "update-index", "--add", "--cacheinfo", "120000," + oid + ",link.txt")
            result, report = scan(root, True)
            self.assertNotEqual(result, 0)
            self.assertIn("symlink-needs-review", {i["category"] for i in report["issues"]})

    def test_index_gitlink_mode_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            git(root, "init", "-q")
            oid = git(root, "hash-object", "-w", "--stdin", data=b"sample").decode().strip()
            git(root, "update-index", "--add", "--cacheinfo", "160000," + oid + ",external")
            result, report = scan(root, True)
            self.assertNotEqual(result, 0)
            self.assertIn("gitlink-needs-review", {i["category"] for i in report["issues"]})

    def test_scans_staged_blob_not_working_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            git(root, "init", "-q")
            value = chr(81) + chr(58) + chr(92) + "ExampleCreator" + chr(92) + "asset"
            (root / "note.txt").write_text(value, encoding="utf-8")
            git(root, "add", "note.txt")
            (root / "note.txt").write_text("clean public note", encoding="utf-8")
            result, report = scan(root, True)
            self.assertNotEqual(result, 0)
            self.assertIn("absolute-drive-path", {i["category"] for i in report["issues"]})
            self.assertNotIn(value, json.dumps(report))

    def test_encoded_paths_and_json_credentials(self):
        drive = chr(81) + chr(58) + chr(92) + "ExampleCreator" + chr(92) + "asset"
        field = "api" + "_key"
        secret = "v" * 24
        fixtures = {
            "encoded.txt": quote(drive, safe=""),
            "unicode.json": json.dumps({"reference": "".join(chr(92) + "u%04x" % ord(c) for c in drive)}),
            "credentials.json": json.dumps({field: secret}),
        }
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, content in fixtures.items():
                (root / name).write_text(content, encoding="utf-8")
            result, report = scan(root)
            self.assertNotEqual(result, 0)
            affected = {i["file"] for i in report["issues"]}
            self.assertEqual(affected, set(fixtures))
            rendered = json.dumps(report)
            self.assertNotIn(drive, rendered)
            self.assertNotIn(secret, rendered)
            self.assertTrue(all(set(i) == {"file", "category"} for i in report["issues"]))

    def test_valid_png_and_corrupt_crc(self):
        good = png()
        self.assertEqual(scanner.binary_issues("image.png", good), [])
        bad = good[:-1] + bytes([good[-1] ^ 1])
        self.assertIn("invalid-png-crc", scanner.binary_issues("image.png", bad))

    def test_png_without_image_fails(self):
        header = bytes([137, 80, 78, 71, 13, 10, 26, 10])
        self.assertTrue(scanner.binary_issues("image.png", header + png_chunk(b"IEND", b"")))

    def test_webp_nested_metadata_fails(self):
        frame = bytes(16) + riff_chunk(b"EXIF", b"private fixture")
        self.assertTrue(scanner.binary_issues("image.webp", webp(riff_chunk(b"ANMF", frame))))

    def test_webp_nested_overflow_fails(self):
        frame = bytes(16) + b"VP8 " + struct.pack("<I", 100)
        self.assertTrue(scanner.binary_issues("image.webp", webp(riff_chunk(b"ANMF", frame))))

    def test_webp_nonzero_padding_fails(self):
        chunk = riff_chunk(b"VP8 ", b"x")[:-1] + b"y"
        self.assertTrue(scanner.binary_issues("image.webp", webp(chunk)))

    def test_webp_empty_fails(self):
        self.assertTrue(scanner.binary_issues("image.webp", webp(b"")))

    def test_public_files_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("Public documentation with https://example.org/guide", encoding="utf-8")
            (root / "image.png").write_bytes(png())
            result, report = scan(root)
            self.assertEqual(result, 0)
            self.assertTrue(report["passed"])
            git(root, "init", "-q")
            git(root, "add", "README.md", "image.png")
            result, report = scan(root, True)
            self.assertEqual(result, 0)
            self.assertTrue(report["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
