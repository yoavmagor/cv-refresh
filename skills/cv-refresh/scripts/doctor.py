#!/usr/bin/env python3
"""Check that everything cv-refresh needs is available and print install hints."""
from __future__ import annotations

import importlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import emit, find_soffice, skill_version  # noqa: E402


def has_module(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def main() -> None:
    checks = {
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 9),
        "python-docx": has_module("docx"),
        "pdfplumber": has_module("pdfplumber"),
        "pypdf": has_module("pypdf"),
        "libreoffice": find_soffice(),
        "pdftoppm": shutil.which("pdftoppm"),
    }
    hints = []
    if not checks["python-docx"]:
        hints.append("pip install python-docx   (required: builds the DOCX)")
    if not (checks["pdfplumber"] or checks["pypdf"]):
        hints.append("pip install pdfplumber    (required for PDF input and style detection)")
    if not checks["libreoffice"]:
        hints.append("Install LibreOffice for PDF output and the 2-page check "
                     "(macOS: brew install --cask libreoffice; Debian/Ubuntu: apt install libreoffice-writer)")
    if not checks["pdftoppm"]:
        hints.append("Optional: install Poppler for page previews (macOS: brew install poppler)")
    blocking = not checks["python_ok"] or not checks["python-docx"] or not (checks["pdfplumber"] or checks["pypdf"])
    emit({
        "ok": not blocking,
        "skill_version": skill_version(),
        "checks": checks,
        "pdf_output_available": bool(checks["libreoffice"]),
        "hints": hints,
    })


if __name__ == "__main__":
    main()
