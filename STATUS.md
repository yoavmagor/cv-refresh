# Status

| | |
|---|---|
| **Current version** | 1.0.0 (2026-09-23) |
| **State** | Released, feature-complete for v1. Tested with **simulated data only**. |
| **Next milestone** | Real-world trial with the author's own CV, then description tuning |

## Components

| Component | State | Notes |
|---|---|---|
| SKILL.md workflow | ✅ done | 7 steps, ground rules, host table |
| Interview guide | ✅ done | announced batch, skip everywhere, follow-ups, previous roles by name, promotion attribution |
| Writing guide | ✅ done | TL;DR summary, bullets, tailoring freedom and limits, trimming order |
| Review guide | ✅ done | lint + proofread, match-score rubric, chat report template |
| Posting intake | ✅ done | URL / paste / file; LinkedIn handling; untrusted-content rule |
| `extract_cv.py` | ✅ tested | PDF, DOCX, MD/TXT, LinkedIn export detection |
| `extract_style.py` | ✅ tested | PDF and DOCX; detects multi-column originals |
| `render_cv.py` | ✅ tested | mirror / classic / modern / compact; autofit; near-empty-page pull-back; previews |
| `lint_cv.py` | ✅ tested | number audit incl. number words; negative test passes |
| `check_keywords.py` | ✅ tested | before/after coverage |
| `state.py` | ✅ tested | settings, history, export, claude.ai import, zip-slip guard |
| `doctor.py` | ✅ tested | |
| Packaging (`tools/package.py`) | ✅ tested | validates frontmatter, excludes `user-data/` |
| Evals | 🟡 partial | 4 scenarios defined; 1 and 2 run end-to-end; 3 and 4 covered only at component level |

## Test results (v1.0.0, simulated data)

| Scenario | Result |
|---|---|
| **Eval 1: tailored, PDF input, pasted posting** ([example](examples/tailored-jordan/)) | 19/19 objective checks pass. 1 page. Keyword coverage 44% → 94% (must-haves 50% → 100%). Match score 51 → 91. Lint: 0 errors, 0 warnings. |
| **Eval 2: generic, DOCX input, keep layout** ([example](examples/generic-jordan/)) | 18/18 checks pass. The mirror layout reproduced A4, Cambria, the teal centered header, uppercase headings and the original section titles. |
| **Eval 3: LinkedIn export + LinkedIn URL** | Export detected as `linkedin_pdf`; two-column layout flagged. URL fallback not exercised (no live fetch in tests). |
| **Eval 4: returning user** | History save → list → export → re-import round trip works, and the layout question is suppressed once saved. Delta interview not run end-to-end. |
| **Negative test** | A draft with an invented "48%", "dozens", "Optimised" and a changed job title fails all 3 corresponding checks, as intended. |

Issues found and fixed during testing: promotion attribution (added `positions`);
DOCX tab/line-break extraction merging words; "B.Sc., Field" formatting; a near-empty
second page.

## Known limitations

- **Simulated data only so far.** Real CVs are messier: tables, text boxes, odd
  fonts, scanned PDFs.
- **Page count measured with LibreOffice.** Word can differ slightly. Metric-compatible
  fonts keep this small, but a CV that fills page 2 to the last line may reflow in Word.
- **Mirror is single column.** Multi-column designs, photos, icons and logos are not
  carried over. The chat says so when it happens.
- **No OCR.** For scanned PDFs, the skill asks for another format or reads page images directly.
- **Legacy `.doc`** must be converted to `.docx` first.
- **Output is English only**, though right-to-left input (e.g. Hebrew) is detected and translated.
- **claude.ai memory needs the user to re-upload** `cv-refresh-user-data.zip`.
- **The match score is partly judgment-based.** The rubric keeps it consistent, but it
  isn't an ATS simulation.
- **The UK→US spelling check is a word list**, not a dictionary. Claude's proofread
  covers the rest.
- **Claude Code's `AskUserQuestion` may not exist in every version.** The skill falls
  back to numbered text.

## Roadmap

Candidates, not commitments:

1. Run evals 3 and 4 end-to-end, then a trial on a real CV.
2. Optimize the trigger description with skill-creator's description optimizer (needs Claude Code).
3. GitHub Actions CI: regenerate fixtures, render, and run `check_outputs.py` on every PR.
4. Claude Code plugin/marketplace packaging for one-command install.
5. More layouts, or user-supplied layout presets in `user-data/`.
6. Hebrew (right-to-left) output as an opt-in.
7. OCR for scanned PDFs.

Explicitly out of scope by author decision: cover letters, LinkedIn profile edits.
