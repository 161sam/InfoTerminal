#!/usr/bin/env python3
import re
from pathlib import Path
from urllib.parse import urlparse
import time

ROOT = Path(__file__).resolve().parent.parent
TARGET_FILES = [ROOT / 'README.md'] + list((ROOT / 'docs').rglob('*.md'))

BARE_URL_RE = re.compile(r'(?<!\]\()https?://[^\s)]+')
HEADING_RE = re.compile(r'^(#{1,6})\s')
FENCE_RE = re.compile(r'^```+')
EMP_HEADING_RE = re.compile(r'^\s*([*_])([^*_]+)\1\s*$')
BULLET_RE = re.compile(r'^(\s*)-\s+')


def short_link(url: str) -> str:
    try:
        parsed = urlparse(url)
        host = parsed.netloc or parsed.path
        return host[:30]
    except Exception:
        return 'link'


def detect_lang(code: str) -> str:
    txt = code.strip()
    if re.search(r'^\s*\$ ', txt, re.MULTILINE) or re.search(r'\b(kubectl|helm|curl|make)\b', txt):
        return 'bash'
    if re.search(r'\bimport\b', txt) or re.search(r'^\s*def ', txt, re.MULTILINE):
        return 'python'
    if re.search(r'^\s*select ', txt, re.IGNORECASE):
        return 'sql'
    if txt.startswith('{') or txt.startswith('['):
        return 'json'
    if ':' in txt and re.search(r'^\s*\w+:', txt, re.MULTILINE):
        return 'yaml'
    return 'text'


def process_text(text: str) -> str:
    lines = text.split('\n')
    result = []
    in_code = False
    last_heading_level = 0
    h1_seen = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if not in_code and FENCE_RE.match(line):
            lang = line.strip().lstrip('`')
            if not lang:
                j = i + 1
                code_lines = []
                while j < len(lines) and not FENCE_RE.match(lines[j]):
                    code_lines.append(lines[j])
                    j += 1
                lang = detect_lang('\n'.join(code_lines))
            if result and result[-1].strip() != '':
                result.append('')
            result.append(f"```{lang}")
            in_code = True
            i += 1
            continue
        if in_code:
            if FENCE_RE.match(line):
                result.append('```')
                result.append('')
                in_code = False
            else:
                result.append(line.rstrip())
            i += 1
            continue
        m = EMP_HEADING_RE.match(line)
        if m:
            line = f"### {m.group(2).strip()}"
        hm = HEADING_RE.match(line)
        if hm:
            level = len(hm.group(1))
            if level == 1:
                if h1_seen:
                    level = 2
                else:
                    h1_seen = True
            if level > last_heading_level + 1:
                level = last_heading_level + 1
            last_heading_level = level
            line = re.sub(r'^#{1,6}', '#' * level, line)
            if result and result[-1].strip() != '':
                result.append('')
            result.append(line.rstrip())
            result.append('')
            i += 1
            continue
        b = BULLET_RE.match(line)
        if b:
            line = f"{b.group(1)}* {line[b.end():]}"
        line = BARE_URL_RE.sub(lambda m: f"[{short_link(m.group(0))}]({m.group(0)})", line)
        if line.strip() == '' and result and result[-1].strip() == '':
            i += 1
            continue
        result.append(line.rstrip())
        i += 1
    text = '\n'.join(result)
    return text.strip() + '\n'


def main():
    for path in TARGET_FILES:
        if not path.exists():
            continue
        orig = path.read_text(encoding='utf-8')
        new = process_text(orig)
        if new != orig:
            ts = path.with_suffix(path.suffix + f".bak.{int(time.time())}")
            if not ts.exists():
                path.rename(ts)
            path.write_text(new, encoding='utf-8')

if __name__ == '__main__':
    main()
