#!/usr/bin/env python3
"""Deterministic checks on a cv.json before it is delivered.

Usage:
  python3 lint_cv.py --cv new.cv.json --sources original.txt session_answers.md [...]

Checks
  numbers      every number in the new CV text must appear in a source file
               (original CV text, LinkedIn export, the user's answers). This
               enforces the "never invent numbers" rule.
  spelling_us  common UK spellings (the output is US English)
  pronouns     first-person pronouns in bullets / summary
  weak         weak openers ("responsible for", "helped", ...)
  cliche       filler phrases ("results-driven", "team player", ...)
  mechanics    double spaces, repeated words, mixed bullet punctuation,
               over-long bullets, summary length, date sanity

Exit code 0 always; read "errors" (must fix) and "warnings" (judgment calls).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import emit, extract_text, fail, load_json  # noqa: E402

UK_TO_US = {
    "organise": "organize", "organised": "organized", "organising": "organizing",
    "organisation": "organization", "organisations": "organizations", "organisational": "organizational",
    "optimise": "optimize", "optimised": "optimized", "optimising": "optimizing", "optimisation": "optimization",
    "utilise": "utilize", "utilised": "utilized", "utilising": "utilizing", "utilisation": "utilization",
    "prioritise": "prioritize", "prioritised": "prioritized", "prioritising": "prioritizing",
    "prioritisation": "prioritization", "specialise": "specialize", "specialised": "specialized",
    "specialising": "specializing", "standardise": "standardize", "standardised": "standardized",
    "standardisation": "standardization", "visualise": "visualize", "visualisation": "visualization",
    "visualisations": "visualizations", "analyse": "analyze", "analysed": "analyzed", "analysing": "analyzing",
    "recognise": "recognize", "recognised": "recognized", "realise": "realize", "realised": "realized",
    "summarise": "summarize", "summarised": "summarized", "minimise": "minimize", "minimised": "minimized",
    "maximise": "maximize", "maximised": "maximized", "customise": "customize", "customised": "customized",
    "centralise": "centralize", "centralised": "centralized", "finalise": "finalize", "finalised": "finalized",
    "normalise": "normalize", "normalised": "normalized", "modernise": "modernize", "modernised": "modernized",
    "categorise": "categorize", "categorised": "categorized", "emphasise": "emphasize",
    "synchronise": "synchronize", "synchronised": "synchronized", "containerise": "containerize",
    "containerised": "containerized", "parallelise": "parallelize", "parallelised": "parallelized",
    "monetise": "monetize", "digitise": "digitize", "authorise": "authorize", "authorisation": "authorization",
    "characterise": "characterize", "capitalise": "capitalize", "initialise": "initialize",
    "colour": "color", "colours": "colors", "behaviour": "behavior", "behaviours": "behaviors",
    "favour": "favor", "favourite": "favorite", "labour": "labor", "honour": "honor", "centre": "center",
    "centres": "centers", "programme": "program", "programmes": "programs", "licence": "license",
    "defence": "defense", "offence": "offense", "travelled": "traveled", "travelling": "traveling",
    "modelling": "modeling", "modelled": "modeled", "labelled": "labeled", "labelling": "labeling",
    "cancelled": "canceled", "catalogue": "catalog", "enrolment": "enrollment", "fulfil": "fulfill",
    "judgement": "judgment", "grey": "gray", "ageing": "aging", "learnt": "learned",
    "acknowledgement": "acknowledgment", "analogue": "analog", "tonne": "ton",
}
WEAK = ["responsible for", "helped", "worked on", "assisted with", "involved in", "duties included",
        "tasked with", "participated in", "in charge of"]
CLICHES = ["results-driven", "results driven", "team player", "hard-working", "hardworking", "go-getter",
           "synergy", "think outside the box", "detail-oriented", "passionate", "self-starter",
           "dynamic professional", "proven track record", "best-of-breed", "guru", "ninja", "rockstar",
           "motivated individual", "highly motivated", "excellent communication skills"]
# number words and the digits they stand for (None = only the word itself counts)
NUMBER_WORDS = {"two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
                "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12",
                "dozen": "12", "decade": "10", "dozens": None, "hundred": "100", "hundreds": None,
                "thousand": "1000", "thousands": None, "million": None, "millions": None,
                "billion": None, "decades": None}


def texts(cv: dict) -> list[tuple[str, str]]:
    """(location, text) pairs for every human-readable string in the CV body."""
    out: list[tuple[str, str]] = []
    b = cv.get("basics", {})
    if b.get("headline"):
        out.append(("basics.headline", b["headline"]))
    summary = cv.get("summary") or []
    for i, s in enumerate([summary] if isinstance(summary, str) else summary):
        out.append((f"summary[{i}]", s))

    def role(prefix, r):
        for key in ("title", "company", "company_blurb", "description", "location"):
            if r.get(key):
                out.append((f"{prefix}.{key}", r[key]))
        for j, bl in enumerate(r.get("bullets", []) or []):
            out.append((f"{prefix}.bullets[{j}]", bl))
        for j, pos in enumerate(r.get("positions", []) or []):
            if pos.get("title"):
                out.append((f"{prefix}.positions[{j}].title", pos["title"]))

    for i, r in enumerate(cv.get("experience", []) or []):
        role(f"experience[{i}]", r)
    for i, g in enumerate(cv.get("skills", []) or []):
        out.append((f"skills[{i}]", ", ".join(g.get("items", []))))
    for i, e in enumerate(cv.get("education", []) or []):
        for j, d in enumerate(e.get("details", []) or []):
            out.append((f"education[{i}].details[{j}]", d))
    for i, p in enumerate(cv.get("projects", []) or []):
        if p.get("description"):
            out.append((f"projects[{i}].description", p["description"]))
        for j, bl in enumerate(p.get("bullets", []) or []):
            out.append((f"projects[{i}].bullets[{j}]", bl))
    for i, s in enumerate(cv.get("extra_sections", []) or []):
        for j, item in enumerate(s.get("items", []) or []):
            if isinstance(item, dict):
                role(f"extra_sections[{i}].items[{j}]", item)
            else:
                out.append((f"extra_sections[{i}].items[{j}]", item))
    return out


NUM_RE = re.compile(r"(?<![A-Za-z])\$?\d[\d,.]*\s?(?:%|[kKmMbB]\b|x\b|\+)?")


def numbers_in(text: str) -> list[str]:
    found = []
    for m in NUM_RE.finditer(text):
        token = m.group(0).strip()
        core = re.sub(r"[^\d.]", "", token).strip(".")
        if core:
            found.append((token, core))
    return found


def source_number_cores(source_text: str) -> set[str]:
    cores = set()
    low = source_text.lower()
    for word, digit in NUMBER_WORDS.items():
        if digit and re.search(rf"\b{word}\b", low):
            cores.add(digit)
    for _, core in numbers_in(source_text):
        cores.add(core)
        cores.add(core.replace(".", ""))
        if "." in core:
            cores.add(core.rstrip("0").rstrip("."))
    return cores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cv", required=True)
    parser.add_argument("--sources", nargs="*", default=[],
                        help="original CV / LinkedIn export / answers files (txt, md, pdf, docx, json)")
    args = parser.parse_args()
    cv = load_json(args.cv)
    if not args.sources:
        fail("Pass --sources (original CV text and the user's answers) so numbers can be audited.")
    source_text = "\n".join(extract_text(Path(s))[0] for s in args.sources)
    source_lower = source_text.lower()
    source_cores = source_number_cores(source_text)

    errors, warnings = [], []
    items = texts(cv)
    bullet_ends = []
    for where, text in items:
        low = text.lower()
        for token, core in numbers_in(text):
            if core not in source_cores and core.replace(".", "") not in source_cores:
                errors.append({"check": "numbers", "where": where, "found": token,
                               "message": "Number not found in any source. Remove it unless the user gave it."})
        for word, digit in NUMBER_WORDS.items():
            if not re.search(rf"\b{word}\b", low):
                continue
            if re.search(rf"\b{word}\b", source_lower) or (digit and digit in source_cores):
                continue
            errors.append({"check": "numbers", "where": where, "found": word,
                           "message": "Number word not found in any source."})
        for uk, us in UK_TO_US.items():
            if re.search(rf"\b{uk}\b", low):
                errors.append({"check": "spelling_us", "where": where, "found": uk, "suggest": us})
        if "bullets" in where or where.startswith("summary"):
            if re.search(r"\b(I|me|my|mine|myself)\b", text):
                warnings.append({"check": "pronouns", "where": where,
                                 "message": "First-person pronoun; CVs usually drop them."})
        for phrase in WEAK:
            if re.search(rf"\b{re.escape(phrase)}\b", low):
                warnings.append({"check": "weak", "where": where, "found": phrase,
                                 "message": "Weak opener; lead with what was done or achieved."})
        for phrase in CLICHES:
            if phrase in low:
                warnings.append({"check": "cliche", "where": where, "found": phrase})
        if "  " in text:
            errors.append({"check": "mechanics", "where": where, "message": "Double space."})
        rep = re.search(r"\b(\w+)\s+\1\b", text, re.I)
        if rep and rep.group(1).lower() not in ("that", "had"):
            errors.append({"check": "mechanics", "where": where, "found": rep.group(0), "message": "Repeated word."})
        if "bullets" in where:
            bullet_ends.append(text.rstrip().endswith("."))
            if len(text) > 260:
                warnings.append({"check": "mechanics", "where": where,
                                 "message": f"Long bullet ({len(text)} chars); aim for 1-2 lines."})
    if bullet_ends and 0 < sum(bullet_ends) < len(bullet_ends):
        errors.append({"check": "mechanics", "where": "bullets",
                       "message": "Mixed bullet endings: end all bullets with a period or none."})

    summary = cv.get("summary") or []
    summary = [summary] if isinstance(summary, str) else summary
    words = sum(len(s.split()) for s in summary)
    if not summary:
        errors.append({"check": "summary", "message": "Missing TL;DR summary at the top."})
    elif len(summary) > 2 or words > 110 or words < 30:
        warnings.append({"check": "summary", "message": f"Summary is {len(summary)} paragraph(s), {words} words; "
                                                         "target 1-2 short paragraphs, ~40-100 words."})

    for i, r in enumerate(cv.get("experience", []) or []):
        for j, span in enumerate([r, *(r.get("positions") or [])]):
            start, end = str(span.get("start", "")), str(span.get("end", ""))
            if start and end and end.lower() != "present" and end[:7] < start[:7]:
                where = f"experience[{i}]" + (f".positions[{j - 1}]" if j else "")
                errors.append({"check": "dates", "where": where, "message": "End date before start date."})
        if not r.get("bullets") and not r.get("description"):
            warnings.append({"check": "content", "where": f"experience[{i}]", "message": "Role has no bullets."})

    emit({"ok": not errors, "errors": errors, "warnings": warnings,
          "counts": {"errors": len(errors), "warnings": len(warnings), "strings_checked": len(items)}})


if __name__ == "__main__":
    main()
