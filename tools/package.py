#!/usr/bin/env python3
"""Validate the skill and build uploadable packages (standard library only).

  python3 tools/package.py            -> dist/cv-refresh.skill and dist/cv-refresh.zip

Both files are the same zip with the skill folder at the root, which is the layout
claude.ai expects ("Upload skill"). Personal data (user-data/) and caches are never
included.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "cv-refresh"
DIST = ROOT / "dist"
EXCLUDE_DIRS = {"user-data", "__pycache__", "node_modules", ".git"}
EXCLUDE_FILES = {".DS_Store"}
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def validate() -> str:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit("SKILL.md: missing YAML frontmatter")
    front = m.group(1)
    top_keys = {line.split(":", 1)[0] for line in front.splitlines() if line and not line.startswith(" ")}
    if top_keys - ALLOWED_KEYS:
        sys.exit(f"SKILL.md: unexpected frontmatter keys {sorted(top_keys - ALLOWED_KEYS)}")
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    version = re.search(r"^\s+version:\s*['\"]?([\w.\-+]+)", front, re.M)
    if not name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1).strip()):
        sys.exit("SKILL.md: name must be kebab-case")
    if name.group(1).strip() != SKILL.name:
        sys.exit("SKILL.md: name must match the folder name")
    if not desc or len(desc.group(1)) > 1024 or re.search(r"[<>]", desc.group(1)):
        sys.exit("SKILL.md: description missing, over 1024 chars, or contains angle brackets")
    nested = [p for p in SKILL.rglob("SKILL.md") if p != SKILL / "SKILL.md"
              and not EXCLUDE_DIRS & set(p.relative_to(SKILL).parts)]
    if nested:
        sys.exit(f"Only one SKILL.md allowed; found extra: {nested}")
    for ref in re.findall(r"`((?:references|scripts)/[\w.\-]+)`", text):
        if not (SKILL / ref).exists():
            sys.exit(f"SKILL.md references a missing file: {ref}")
    return version.group(1) if version else "unknown"


def build() -> list[Path]:
    DIST.mkdir(exist_ok=True)
    files = sorted(
        p for p in SKILL.rglob("*")
        if p.is_file()
        and not EXCLUDE_DIRS & set(p.relative_to(SKILL).parts)
        and p.name not in EXCLUDE_FILES
        and p.suffix != ".pyc"
    )
    outputs = []
    for target in (DIST / "cv-refresh.skill", DIST / "cv-refresh.zip"):
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(f, (Path(SKILL.name) / f.relative_to(SKILL)).as_posix())
        outputs.append(target)
    return outputs


if __name__ == "__main__":
    ver = validate()
    outs = build()
    print(f"cv-refresh {ver}: valid")
    for o in outs:
        print(f"  built {o.relative_to(ROOT)} ({o.stat().st_size // 1024} KB)")
