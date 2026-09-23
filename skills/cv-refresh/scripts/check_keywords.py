#!/usr/bin/env python3
"""Keyword coverage of a CV against a job posting (one input to the match score).

Usage:
  python3 check_keywords.py --posting posting.json --cv new.cv.json [--before original.cv.json]

posting.json must contain "keywords": [{"term": "Airflow", "aliases": ["Apache Airflow"],
"priority": "must" | "nice"}]. CV inputs may be cv.json, PDF, DOCX, MD or TXT.
Matching is case-insensitive on whole terms, so "Go" does not match "Google"
and "C++" / "CI/CD" / "Node.js" work as written.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import emit, extract_text, fail, load_json  # noqa: E402


def term_pattern(term: str) -> re.Pattern:
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9+#])", re.I)


def coverage(keywords: list[dict], text: str) -> dict:
    rows = []
    for kw in keywords:
        terms = [kw["term"], *kw.get("aliases", [])]
        hits = sum(len(term_pattern(t).findall(text)) for t in terms)
        rows.append({"term": kw["term"], "priority": kw.get("priority", "nice"), "hits": hits, "found": hits > 0})

    def pct(priority):
        subset = [r for r in rows if r["priority"] == priority]
        return round(100 * sum(r["found"] for r in subset) / len(subset)) if subset else None

    return {
        "must_coverage_pct": pct("must"),
        "nice_coverage_pct": pct("nice"),
        "overall_coverage_pct": round(100 * sum(r["found"] for r in rows) / len(rows)) if rows else None,
        "missing_must": [r["term"] for r in rows if r["priority"] == "must" and not r["found"]],
        "missing_nice": [r["term"] for r in rows if r["priority"] != "must" and not r["found"]],
        "terms": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posting", required=True)
    parser.add_argument("--cv", required=True)
    parser.add_argument("--before")
    args = parser.parse_args()
    posting = load_json(args.posting)
    keywords = posting.get("keywords") or []
    if not keywords:
        fail("posting.json has no 'keywords' list")
    result = {"ok": True, "after": coverage(keywords, extract_text(Path(args.cv))[0])}
    if args.before:
        result["before"] = coverage(keywords, extract_text(Path(args.before))[0])
        for key in ("must_coverage_pct", "nice_coverage_pct", "overall_coverage_pct"):
            b, a = result["before"][key], result["after"][key]
            result.setdefault("delta", {})[key] = None if a is None or b is None else a - b
        # keep the output short: per-term rows only for the new CV
        result["before"].pop("terms", None)
    emit(result)


if __name__ == "__main__":
    main()
