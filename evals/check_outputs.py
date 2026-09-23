#!/usr/bin/env python3
"""Objective checks for a cv-refresh run. Use after every change to the skill.

  python3 evals/check_outputs.py --docx OUT.docx --pdf OUT.pdf \
      --original original.cv.json --new new.cv.json \
      --sources original.txt answers.md [--session session.md]

Checks the things that must never regress: page cap, no comments or
placeholders in the document, summary at the top, no invented numbers, US
spelling, fixed facts (employers, titles, start dates, degrees) preserved, and a
complete session history header. Subjective quality still needs a human.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "cv-refresh" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from common import pdf_page_count  # noqa: E402

results: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, evidence: str = "") -> None:
    results.append((name, bool(passed), evidence))


def titles_by_company(cv: dict) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for r in cv.get("experience", []):
        titles = {r["title"]} if r.get("title") else set()
        titles |= {p["title"] for p in r.get("positions", []) if p.get("title")}
        out.setdefault(r.get("company", ""), set()).update(titles)
    return out


def earliest_start(cv: dict, company: str) -> str:
    starts = []
    for r in cv.get("experience", []):
        if r.get("company") == company:
            starts += [str(r["start"])] if r.get("start") else []
            starts += [str(p["start"]) for p in r.get("positions", []) if p.get("start")]
    return min(starts) if starts else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--original", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--sources", nargs="+", required=True)
    ap.add_argument("--session")
    ap.add_argument("--max-pages", type=int, default=2)
    a = ap.parse_args()

    docx, pdf = Path(a.docx), Path(a.pdf)
    check("docx and pdf exist", docx.exists() and pdf.exists())
    pages = pdf_page_count(pdf) if pdf.exists() else None
    check(f"at most {a.max_pages} pages", pages is not None and pages <= a.max_pages, f"pages={pages}")

    with zipfile.ZipFile(docx) as z:
        names = z.namelist()
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    check("no Word comments", not any("comments" in n for n in names), ",".join(n for n in names if "comment" in n))
    check("no highlights or tracked changes", not re.search(r"<w:(highlight|ins|del)\b", xml))
    text = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))
    placeholder = re.search(r"\[(add|insert|todo|tbd|x+)[^\]]*\]|\bTODO\b|\bXX+\b", text, re.I)
    check("no placeholders in document", not placeholder, placeholder.group(0) if placeholder else "")

    orig, new = json.loads(Path(a.original).read_text()), json.loads(Path(a.new).read_text())
    summary = new.get("summary") or []
    summary = [summary] if isinstance(summary, str) else summary
    check("TL;DR summary present (1-2 paragraphs)", 1 <= len(summary) <= 2, f"{len(summary)} paragraph(s)")

    lint = json.loads(subprocess.run(
        [sys.executable, str(SCRIPTS / "lint_cv.py"), "--cv", a.new, "--sources", *a.sources],
        capture_output=True, text=True).stdout)
    nums = [e for e in lint["errors"] if e["check"] == "numbers"]
    spell = [e for e in lint["errors"] if e["check"] == "spelling_us"]
    check("no invented numbers", not nums, json.dumps(nums)[:300])
    check("US spelling", not spell, json.dumps(spell)[:300])

    new_titles = titles_by_company(new)
    extra_items = [i for s in new.get("extra_sections", []) for i in s.get("items", []) if isinstance(i, dict)]
    extra_text = json.dumps(new.get("extra_sections", []))
    for company, titles in titles_by_company(orig).items():
        kept = company in new_titles or company in extra_text
        check(f"employer kept: {company}", kept)
        if company in new_titles:
            check(f"titles kept: {company}", titles <= new_titles[company], f"{titles} vs {new_titles[company]}")
            check(f"start date kept: {company}", earliest_start(orig, company) == earliest_start(new, company),
                  f"{earliest_start(orig, company)} vs {earliest_start(new, company)}")
    for ed in orig.get("education", []):
        match = [e for e in new.get("education", []) if e.get("institution") == ed.get("institution")
                 and e.get("degree") == ed.get("degree")]
        check(f"degree kept: {ed.get('degree')} {ed.get('institution')}", bool(match))
    _ = extra_items

    if a.session:
        head = Path(a.session).read_text().split("---")[1]
        missing = [k for k in ("date", "skill_version", "mode", "target", "input_cv", "layout", "outputs", "pages")
                   if not re.search(rf"^{k}:\s*\S", head, re.M)]
        check("session history header complete", not missing, f"missing={missing}")

    width = max(len(n) for n, _, _ in results)
    for name, ok, ev in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  {ev}")
    failed = sum(not ok for _, ok, _ in results)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
