#!/usr/bin/env python3
"""Extract plain text from a CV (PDF, DOCX, Markdown/TXT, LinkedIn profile PDF).

Usage:
  python3 extract_cv.py INPUT [--out TEXT_FILE]

Writes the full text to TEXT_FILE (default: INPUT stem + .extracted.txt in the
current directory) and prints a JSON summary. Read the text file in full
before building cv.json -- the summary is only a guide.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import emit, extract_text, fail  # noqa: E402
from sections import canonical_section  # noqa: E402


def looks_like_linkedin_export(text: str) -> bool:
    """LinkedIn's 'Save to PDF' profile export has a recognizable skeleton."""
    signals = [
        bool(re.search(r"\bPage \d+ of \d+\b", text)),
        "linkedin.com/in/" in text.lower(),
        bool(re.search(r"^\s*Top Skills\s*$", text, re.M)),
        bool(re.search(r"^\s*Contact\s*$", text, re.M)),
    ]
    return sum(signals) >= 3


def guess_headings(text: str) -> list[str]:
    found = []
    for line in text.splitlines():
        clean = line.strip().strip(":")
        if 2 < len(clean) <= 40 and canonical_section(clean):
            found.append(clean)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        fail(f"File not found: {src}")
    text, info = extract_text(src)
    out = Path(args.out) if args.out else Path.cwd() / f"{src.stem}.extracted.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    linkedin = info["format"] == "pdf" and looks_like_linkedin_export(text)
    warnings = list(info["warnings"])
    if linkedin:
        warnings.append(
            "Looks like a LinkedIn profile export: section order is Contact/Top Skills/"
            "Summary/Experience/Education, page footers ('Page N of M') are noise, and "
            "multiple titles at one company are listed under a single company heading."
        )
    if info.get("uses_tables"):
        warnings.append("The DOCX uses tables for layout; reading order may be scrambled -- check it.")
    if info.get("header_footer_text"):
        warnings.append("Some content sits in the page header/footer (often contact details).")
    if re.search(r"[\u0590-\u05FF\u0600-\u06FF]", text):
        warnings.append("Right-to-left script detected. Output is US English only; translate faithfully.")

    emit({
        "ok": bool(text.strip()),
        "source_file": str(src),
        "format": "linkedin_pdf" if linkedin else info["format"],
        "pages": info["pages"],
        "chars": len(text),
        "words": len(text.split()),
        "text_file": str(out),
        "headings_found": guess_headings(text),
        "warnings": warnings,
    })


if __name__ == "__main__":
    main()
