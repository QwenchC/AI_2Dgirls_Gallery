"""Fail closed on common privacy hazards; never print matched content."""
from pathlib import Path, PurePosixPath
import argparse
import html
import json
import re
import struct
import subprocess
import sys
from urllib.parse import unquote
import zlib

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'artifacts', 'node_modules', '__pycache__'}
TEXT = {'.md', '.json', '.js', '.mjs', '.py', '.html', '.css', '.cmd', '.svg', '.txt', '.yml', '.yaml'}
PATTERNS = {
    'absolute-drive-path': re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/](?!/)'),
    'personal-home-path': re.compile(r'''/(?:Users|home)/[^/\s\\"'<>]+/'''),
    'network-share-path': re.compile(r'\\\\[A-Za-z0-9_.-]+\\'),
    'machine-service-url': re.compile(r'https?://(?:localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|\[::1\])(?=[:/\s]|$)', re.I),
    'provider-secret': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})\b'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'embedded-credential-url': re.compile(r'https?://[^\s/:]+:[^\s/@]+@'),
    'credential-assignment': re.compile(r'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)["']?\s*[=:]\s*["']?[A-Za-z0-9+/=_-]{16,}'''),
}
PNG_ALLOWED = {b'IHDR', b'PLTE', b'IDAT', b'IEND', b'tRNS', b'gAMA', b'cHRM', b'sRGB', b'sBIT', b'bKGD', b'pHYs'}
WEBP_ALLOWED = {b'VP8 ', b'VP8L', b'VP8X', b'ALPH', b'ANIM', b'ANMF'}

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL)

def files(staged):
    if staged:
        for value in git('ls-files', '--stage', '--full-name', '-z').split(b'\0'):
            if value:
                metadata, encoded_name = value.split(b'\t', 1)
                mode, oid, stage = metadata.split()
                name = encoded_name.decode('utf-8')
                category = None
                if stage != b'0':
                    category = 'unmerged-index-entry'
                elif mode == b'120000':
                    category = 'symlink-needs-review'
                elif mode == b'160000':
                    category = 'gitlink-needs-review'
                elif mode not in {b'100644', b'100755'}:
                    category = 'index-entry-mode-needs-review'
                yield name, None if category else git('cat-file', 'blob', oid.decode('ascii')), category
    else:
        pending = [ROOT]
        while pending:
            for p in sorted(pending.pop().iterdir()):
                if p.name.lower() in SKIP:
                    continue
                name = p.relative_to(ROOT).as_posix()
                # Check links before is_file(): broken links and linked directories
                # must not disappear from the inventory or lead outside the root.
                if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
                    yield name, None, 'symlink-needs-review'
                elif p.is_dir():
                    pending.append(p)
                elif p.is_file():
                    yield name, p.read_bytes(), None
                else:
                    yield name, None, 'unsupported-file-type'

def text_forms(content):
    """Inspect common serialized/URL encodings without evaluating source code."""
    yield content
    escape = re.compile(r'\\(?:u([0-9a-fA-F]{4})|x([0-9a-fA-F]{2}))')
    for _ in range(3):
        decoded = html.unescape(unquote(content))
        decoded = escape.sub(lambda m: chr(int(m.group(1) or m.group(2), 16)), decoded)
        decoded = decoded.replace(r'\/', '/').replace(r'\\', '\\')
        decoded = decoded.replace(r'\"', '"').replace(r"\'", "'")
        if decoded == content:
            break
        yield decoded
        content = decoded

def webp_chunks(raw, start, end, nested=False):
    found = []
    image = False
    pos = start
    allowed = {b'ALPH', b'VP8 ', b'VP8L'} if nested else WEBP_ALLOWED
    while pos < end:
        if pos + 8 > end:
            return found + ['invalid-webp-chunk-size'], image
        kind = raw[pos:pos+4]
        length = struct.unpack('<I', raw[pos+4:pos+8])[0]
        payload_start = pos + 8
        payload_end = payload_start + length
        next_pos = payload_end + (length % 2)
        if next_pos > end:
            return found + ['invalid-webp-chunk-size'], image
        if length % 2 and raw[payload_end] != 0:
            found.append('invalid-webp-padding')
        if kind not in allowed:
            found.append('webp-embedded-metadata-or-unknown-chunk')
        if kind in {b'VP8 ', b'VP8L'}:
            image = image or length > 0
        elif kind == b'ANMF' and not nested:
            if length < 16:
                found.append('invalid-webp-frame')
            else:
                frame_issues, frame_image = webp_chunks(raw, payload_start + 16, payload_end, True)
                found.extend(frame_issues)
                if not frame_image:
                    found.append('invalid-webp-missing-image')
                image = image or frame_image
        pos = next_pos
    return found, image

def binary_issues(name, raw):
    if name.lower().endswith('.png'):
        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            return ['invalid-png']
        pos = 8
        end = False
        found = []
        header = False
        image = False
        while pos + 12 <= len(raw):
            length = struct.unpack('>I', raw[pos:pos+4])[0]
            kind = raw[pos+4:pos+8]
            if pos + length + 12 > len(raw):
                return ['truncated-png']
            payload_end = pos + 8 + length
            crc = struct.unpack('>I', raw[payload_end:payload_end+4])[0]
            if zlib.crc32(raw[pos+4:payload_end]) & 0xffffffff != crc:
                found.append('invalid-png-crc')
            if kind == b'IHDR':
                if header or pos != 8 or length != 13:
                    found.append('invalid-png-structure')
                header = True
            elif not header:
                found.append('invalid-png-structure')
            if kind == b'IDAT':
                image = True
            if kind not in PNG_ALLOWED:
                found.append('png-embedded-metadata-or-unknown-chunk')
            pos += length + 12
            if kind == b'IEND':
                if length != 0:
                    found.append('invalid-png-structure')
                end = True
                break
        if not header or not image:
            found.append('invalid-png-structure')
        if not end or pos != len(raw):
            found.append('png-trailing-or-missing-data')
        return found
    if name.lower().endswith('.webp'):
        if len(raw) < 12 or raw[:4] != b'RIFF' or raw[8:12] != b'WEBP' or struct.unpack('<I', raw[4:8])[0]+8 != len(raw):
            return ['invalid-webp']
        found, image = webp_chunks(raw, 12, len(raw))
        if not image:
            found.append('invalid-webp-missing-image')
        return found
    return []

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='Read Git index blobs instead of working files')
    args = parser.parse_args()
    issues = []
    count = 0
    try:
        for name, raw, entry_issue in files(args.staged):
            count += 1
            lower = name.lower()
            parts = PurePosixPath(lower).parts
            if any(p in {'.git', 'artifacts', '.local', '.codex', '.agents', '.claude', '.vscode', '.idea', 'workflows', 'models'} for p in parts) or re.search(r'(^|/)(?:\.env(?:\..*)?|.*local-workflow-audit.*)$', lower) or lower.endswith(('.log', '.key', '.pem', '.p12', '.pfx', '.safetensors', '.ckpt')):
                issues.append({'file': name, 'category': 'private-or-generated-file'})
            if entry_issue:
                issues.append({'file': name, 'category': entry_issue})
                continue
            if PurePosixPath(lower).suffix in TEXT or lower in {'.gitignore', '.gitattributes'}:
                try:
                    content = raw.decode('utf-8-sig')
                except UnicodeDecodeError:
                    issues.append({'file': name, 'category': 'non-utf8-text-needs-review'})
                    continue
                matched = set()
                for form in text_forms(content):
                    matched.update(category for category, pattern in PATTERNS.items() if pattern.search(form))
                issues.extend({'file': name, 'category': category} for category in sorted(matched))
            elif not lower.endswith(('.png', '.webp')):
                issues.append({'file': name, 'category': 'unreviewed-binary-format'})
            for category in sorted(set(binary_issues(name, raw))):
                issues.append({'file': name, 'category': category})
        if not count:
            issues.append({'file': '.', 'category': 'empty-publication-input'})
    except (OSError, ValueError, struct.error, subprocess.CalledProcessError):
        print(json.dumps({'passed': False, 'error': 'Unable to read all publication inputs'}))
        return 1
    print(json.dumps({'mode': 'staged' if args.staged else 'working-tree', 'files': count, 'passed': not issues, 'issues': issues}, ensure_ascii=True, indent=2))
    return bool(issues)

if __name__ == '__main__':
    sys.exit(main())
