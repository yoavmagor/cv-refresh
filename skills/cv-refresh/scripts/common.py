"""Shared helpers for the cv-refresh scripts.

Only the standard library is required here. Optional libraries (python-docx,
pdfplumber, pypdf) are imported lazily so every script can still report a
clear error instead of crashing on import.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def skill_version() -> str:
    """Single source of truth for the version: SKILL.md frontmatter."""
    try:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        head = text.split("---", 2)[1]
        m = re.search(r"^\s*version:\s*['\"]?([0-9][0-9A-Za-z.\-+]*)", head, re.M)
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


def emit(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def fail(message: str, **extra) -> None:
    emit({"ok": False, "error": message, **extra})
    sys.exit(1)


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# LibreOffice (DOCX -> PDF) and page counting
# --------------------------------------------------------------------------

def find_soffice() -> str | None:
    for name in ("soffice", "libreoffice"):
        path = shutil.which(name)
        if path:
            return path
    for candidate in (
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ):
        if os.path.exists(candidate):
            return candidate
    return None


def docx_to_pdf(docx_path, out_dir) -> Path | None:
    """Convert with a throwaway LibreOffice profile (avoids lock/profile errors)."""
    soffice = find_soffice()
    docx_path = Path(docx_path)
    out_dir = Path(out_dir)
    target = out_dir / (docx_path.stem + ".pdf")
    if target.exists():
        target.unlink()
    if soffice:
        env = os.environ.copy()
        if sys.platform.startswith("linux"):
            env.setdefault("SAL_USE_VCLPLUGIN", "svp")
        with tempfile.TemporaryDirectory(prefix="cvr_lo_") as profile:
            cmd = [
                soffice,
                f"-env:UserInstallation={Path(profile).as_uri()}",
                "--headless", "--convert-to", "pdf",
                "--outdir", str(out_dir), str(docx_path),
            ]
            try:
                subprocess.run(cmd, capture_output=True, timeout=240, env=env)
            except (subprocess.TimeoutExpired, OSError):
                pass
    if not target.exists():
        # claude.ai sandboxes ship a wrapper that works around blocked sockets.
        wrapper = Path("/mnt/skills/public/docx/scripts/office/soffice.py")
        if wrapper.exists():
            try:
                subprocess.run(
                    [sys.executable, str(wrapper), "--headless", "--convert-to", "pdf",
                     "--outdir", str(out_dir), str(docx_path)],
                    capture_output=True, timeout=240,
                )
            except (subprocess.TimeoutExpired, OSError):
                pass
    return target if target.exists() else None


def pdf_page_count(pdf_path) -> int | None:
    try:
        import pypdf  # type: ignore
        return len(pypdf.PdfReader(str(pdf_path)).pages)
    except Exception:
        pass
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(str(pdf_path)) as pdf:
            return len(pdf.pages)
    except Exception:
        pass
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            return int(m.group(1))
    return None


def last_page_fill(pdf_path) -> float | None:
    """Fraction of the last page's usable height that holds text (0..1)."""
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            page = pdf.pages[-1]
            first = pdf.pages[0]
            if not page.chars:
                return 0.0
            top_margin = min(c["top"] for c in first.chars) if first.chars else 36
            usable = page.height - 2 * top_margin
            used = max(c["bottom"] for c in page.chars) - top_margin
            return round(max(0.0, min(1.0, used / usable)), 2)
    except Exception:
        return None


def render_previews(pdf_path, out_prefix, dpi: int = 70, first_page_only: bool = False) -> list[str]:
    """PNG previews via pdftoppm (Poppler). Returns [] if unavailable."""
    if not shutil.which("pdftoppm"):
        return []
    args = ["pdftoppm", "-png", "-r", str(dpi)]
    if first_page_only:
        args += ["-f", "1", "-l", "1"]
    subprocess.run(args + [str(pdf_path), str(out_prefix)], capture_output=True)
    parent = Path(out_prefix).parent
    stem = Path(out_prefix).name
    return sorted(str(p) for p in parent.glob(f"{stem}*.png"))


# --------------------------------------------------------------------------
# Text extraction (shared by extract_cv.py and check_keywords.py)
# --------------------------------------------------------------------------

def extract_text(path) -> tuple[str, dict]:
    """Return (text, info). info has format, pages and warnings."""
    path = Path(path)
    suffix = path.suffix.lower()
    info: dict = {"format": suffix.lstrip("."), "pages": None, "warnings": []}
    if suffix == ".pdf":
        text = _pdf_text(path, info)
    elif suffix == ".docx":
        text = _docx_text(path, info)
    elif suffix in (".md", ".markdown", ".txt", ".text"):
        text = path.read_text(encoding="utf-8", errors="replace")
        info["format"] = "md" if suffix in (".md", ".markdown") else "txt"
    elif suffix == ".json":
        text = _json_text(load_json(path))
        info["format"] = "cv.json"
    elif suffix == ".doc":
        info["warnings"].append(
            "Legacy .doc is not supported directly. Convert it to .docx first "
            "(LibreOffice: soffice --headless --convert-to docx file.doc)."
        )
        text = ""
    else:
        info["warnings"].append(f"Unsupported file type: {suffix}")
        text = ""
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text, info


def _pdf_text(path: Path, info: dict) -> str:
    text = ""
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(str(path)) as pdf:
            info["pages"] = len(pdf.pages)
            text = "\n\n".join((p.extract_text(x_tolerance=1.5) or "") for p in pdf.pages)
    except Exception as exc:  # pragma: no cover - depends on environment
        info["warnings"].append(f"pdfplumber failed ({exc.__class__.__name__}); trying fallbacks")
    if not text.strip():
        try:
            import pypdf  # type: ignore
            reader = pypdf.PdfReader(str(path))
            info["pages"] = len(reader.pages)
            text = "\n\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception:
            pass
    if not text.strip() and shutil.which("pdftotext"):
        text = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True).stdout
    if not text.strip():
        info["warnings"].append(
            "No extractable text. The PDF is probably a scanned image; ask the user "
            "for a DOCX/text version or read the page images directly."
        )
    return text


def _docx_text(path: Path, info: dict) -> str:
    try:
        import docx  # type: ignore
    except Exception:
        info["warnings"].append("python-docx missing; using raw XML fallback")
        return _docx_text_raw(path)
    doc = docx.Document(str(path))
    lines: list[str] = []
    body = doc.element.body

    def para_text(p) -> str:
        parts = []
        for run in p.iter():
            if not run.tag.endswith("}r"):
                continue  # only runs carry text; <w:tabs> in pPr are tab-stop definitions
            for node in run:
                tag = node.tag.split("}")[-1]
                if tag == "t":
                    parts.append(node.text or "")
                elif tag == "tab":
                    parts.append("\t")
                elif tag in ("br", "cr"):
                    parts.append("\n")
        return "".join(parts)

    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            lines.append(para_text(child))
        elif tag == "tbl":
            info.setdefault("uses_tables", True)
            for row in child.iter():
                if row.tag.endswith("}tr"):
                    cells = []
                    for cell in row:
                        if cell.tag.endswith("}tc"):
                            paras = []
                            for p in cell.iter():
                                if p.tag.endswith("}p"):
                                    paras.append(para_text(p))
                            cells.append("\n".join(x for x in paras if x.strip()))
                    lines.append("\n".join(c for c in cells if c.strip()))
    for section in doc.sections:
        for part in (section.header, section.footer):
            try:
                extra = "\n".join(p.text for p in part.paragraphs if p.text.strip())
            except Exception:
                extra = ""
            if extra:
                info.setdefault("header_footer_text", True)
                lines.insert(0, extra)
    return "\n".join(lines)


def _docx_text_raw(path: Path) -> str:
    import zipfile
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


def _json_text(cv: dict) -> str:
    """Flatten a cv.json into plain text (for keyword checks and linting)."""
    out: list[str] = []

    def walk(node):
        if isinstance(node, str):
            out.append(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                if key in ("meta", "id", "source"):
                    continue
                walk(value)

    walk(cv)
    return "\n".join(out)
