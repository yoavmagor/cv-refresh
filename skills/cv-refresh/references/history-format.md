# Session history format

Each run leaves one Markdown file. It serves three purposes: the user can see exactly
what was asked and changed, the next session can skip what's already known, and the
answers act as a verified source for the number audit. Write it to
`WORK_DIR/session.md`, then run `state.py save-session WORK_DIR/session.md`.

It contains personal data. It lives only in the data directory, which is git-ignored
and never packaged.

```markdown
---
date: 2026-09-23 11:05
skill_version: 1.0.0
mode: tailored
target: Senior Data Engineer @ Tessellate Mobility
posting_url: (pasted text)
input_cv: sample-cv-2022.pdf
layout: modern
outputs: Jordan_Avery_CV_Tessellate.docx, Jordan_Avery_CV_Tessellate.pdf
pages: 2
match_before: 58
match_after: 84
---

# 2026-09-23: Senior Data Engineer @ Tessellate Mobility

## Interview: current role (Harborlight Logistics)
Planned 11 questions. Answered 10, skipped 1.

| # | Question | Answer |
|---|---|---|
| Q1 | Still at Harborlight Logistics? | Yes |
| Q2 | Still "Senior Data Engineer"? | Promoted to Data Engineering Team Lead, Jan 2024 |
| Q7 | Any numbers for the lakehouse migration? | 30 pipelines migrated; monthly warehouse cost down ~35% |
| Q9 | Used Kafka? | No |
| Q10 | Recognition from this role? | (skipped) |

## Follow-ups
| # | Question | Answer |
|---|---|---|
| F1 | The 35%: monthly warehouse spend? | Yes, compute + storage for analytics |

## Previous roles
Offered: Quillstone Retail (2019–2022), Pinecrest Health Analytics (2016–2018). Chosen: Quillstone Retail.

| # | Question | Answer |
|---|---|---|
| P1 | Did you use Spark at Quillstone? | Yes, Spark on EMR for ~1 year, clickstream |

## Changes made
| Section | Change | Based on |
|---|---|---|
| Experience | Added "Data Engineering Team Lead" (2024–present) with 4 bullets | Q2, Q4–Q8 |
| Experience / Quillstone | New first bullet: Spark on EMR for clickstream | P1 |
| Summary | Rewritten as a 2-paragraph TL;DR for data platform roles | Q12, posting |
| Skills | Regrouped; posting keywords first; SSIS dropped | posting |

## Review
- Fixes applied: Optimised → Optimized; 1 weak opener rewritten
- Suggestions given: 2 (see chat)
- Open gaps: Kafka (no), Kubernetes (no)

## Follow-up edits
- (requests after delivery and what was done)
```

Keep answers in the user's words, shortened if long. Every row under "Changes made"
should point to the question, the posting or the original text that justifies it.
