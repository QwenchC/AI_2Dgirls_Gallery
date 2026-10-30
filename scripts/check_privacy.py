"""Fail closed on common privacy hazards; never print matched content."""
from pathlib import Path, PurePosixPath
import argparse
import json
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'artifacts', 'node_modules', '__pycache__'}
TEXT = {'.md', '.json', '.js', '.mjs', '.py', '.html', '.css', '.cmd', '.svg', '.txt', '.yml', '.yaml'}
PATTERNS = {
    'absolute-drive-path': re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/](?!/)'),
    'personal-home-path': re.compile(r'/(?:Users|home)/[A-Za-z0-9_.-]+/'),
    'network-share-path': re.compile(r'\\\\[A-Za-z0-9_.-]+\\'),
    'machine-service-url': re.compile(r'https?://(?:localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|\[::1\])(?=[:/\s]|$)', re.I),
    'provider-secret': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})\b'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'embedded-credential-url': re.compile(r'https?://[^\s/:]+:[^\s/@]+@'),
    'credential-assignment': re.compile(r'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["']?[A-Za-z0-9+/=_-]{16,}'''),
}
PNG_ALLOWED = {b'IHDR', b'PLTE', b'IDAT', b'IEND', b'tRNS', b'gAMA', b'cHRM', b'sRGB', b'sBIT', b'bKGD', b'pHYs'}
WEBP_ALLOWED = {b'VP8 ', b'VP8L', b'VP8X', b'ALPH', b'ANIM', b'ANMF'}

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL)

def files(staged):
    if staged:
        for value in git('ls-files', '-z').split(b'\0'):
            if value:
                name = value.decode('utf-8')
                yield name, git('show', ':' + name)
    else:
        for p in sorted(ROOT.rglob('*')):
            rel = p.relative_to(ROOT)
            if any(part in SKIP for part in rel.parts) or not p.is_file():
                continue
            if p.is_symlink():
                yield rel.as_posix(), None
            else:
                yield rel.as_posix(), p.read_bytes()

def binary_issues(name, raw):
    if name.lower().endswith('.png'):
        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            return ['invalid-png']
        pos = 8
        end = False
        found = []
        while pos + 12 <= len(raw):
            length = struct.unpack('>I', raw[pos:pos+4])[0]
            kind = raw[pos+4:pos+8]
            if pos + length + 12 > len(raw):
                return ['truncated-png']
            if kind not in PNG_ALLOWED:
                found.append('png-embedded-metadata-or-unknown-chunk')
            pos += length + 12
            if kind == b'IEND':
                end = True
                break
        if not end or pos != len(raw):
            found.append('png-trailing-or-missing-data')
        return found
    if name.lower().endswith('.webp'):
        if raw[:4] != b'RIFF' or raw[8:12] != b'WEBP' or struct.unpack('<I', raw[4:8])[0]+8 != len(raw):
            return ['invalid-webp']
        pos = 12
        found = []
        while pos + 8 <= len(raw):
            kind = raw[pos:pos+4]
            length = struct.unpack('<I', raw[pos+4:pos+8])[0]
            if kind not in WEBP_ALLOWED:
                found.append('webp-embedded-metadata-or-unknown-chunk')
            pos += 8 + length + (length % 2)
        if pos != len(raw):
            found.append('invalid-webp-chunk-size')
        return found
    return []

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='Read Git index blobs instead of working files')
    args = parser.parse_args()
    issues = []
    count = 0
    try:
        for name, raw in files(args.staged):
            count += 1
            parts = PurePosixPath(name).parts
            lower = name.lower()
            if any(p in {'.git', 'artifacts', '.local', '.codex', '.agents', '.claude', '.vscode', '.idea', 'workflows', 'models'} for p in parts) or re.search(r'(^|/)(?:\.env(?:\..*)?|.*local-workflow-audit.*)$', lower) or lower.endswith(('.log', '.key', '.pem', '.p12', '.pfx', '.safetensors', '.ckpt')):
                issues.append({'file': name, 'category': 'private-or-generated-file'})
            if raw is None:
                issues.append({'file': name, 'category': 'symlink-needs-review'})
                continue
            if PurePosixPath(name).suffix in TEXT or name in {'.gitignore', '.gitattributes'}:
                try:
                    content = raw.decode('utf-8-sig')
                except UnicodeDecodeError:
                    issues.append({'file': name, 'category': 'non-utf8-text-needs-review'})
                    continue
                for category, pattern in PATTERNS.items():
                    if pattern.search(content):
                        issues.append({'file': name, 'category': category})
            elif not lower.endswith(('.png', '.webp')):
                issues.append({'file': name, 'category': 'unreviewed-binary-format'})
            for category in set(binary_issues(name, raw)):
                issues.append({'file': name, 'category': category})
    except (OSError, subprocess.CalledProcessError):
        print(json.dumps({'passed': False, 'error': 'Unable to read all publication inputs'}))
        return 1
    print(json.dumps({'mode': 'staged' if args.staged else 'working-tree', 'files': count, 'passed': not issues, 'issues': issues}, ensure_ascii=True, indent=2))
    return bool(issues)

if __name__ == '__main__':
    sys.exit(main())
