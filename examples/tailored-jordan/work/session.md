---
date: 2026-09-23 11:05
skill_version: 1.0.0
mode: tailored
target: Senior Data Engineer, Data Platform @ Tessellate Mobility
posting_url: (pasted text)
input_cv: sample-cv-2022.pdf
layout: modern
outputs: Jordan_Avery_CV_Tessellate.docx, Jordan_Avery_CV_Tessellate.pdf
pages: 1
match_before: 51
match_after: 91
---

# 2026-09-23: Senior Data Engineer, Data Platform @ Tessellate Mobility

Settings: layout_mode was asked for the first time and set to `choose`. The user picked `modern` from 4 options.

## Interview: current role (Harborlight Logistics)
Planned 14 questions. Answered 13, skipped 1.

| # | Question | Answer |
|---|---|---|
| Q1 | Still at Harborlight Logistics? | Yes |
| Q2 | Still "Senior Data Engineer"? Promotions? | Promoted: Senior Data Engineer Apr 2022 – Dec 2023, Data Engineering Team Lead since Jan 2024 |
| Q3 | What does Harborlight do, for whom? | B2B SaaS for freight visibility; mid-size shippers and carriers track shipments and ETAs |
| Q4 | Team size and position? | Lead a team of 4 data engineers |
| Q5 | Groups you work with most? | Data science, product, backend team |
| Q6 | What do you own? | The data platform: ingestion of carrier GPS/telematics and shipment events, the lakehouse, dbt models, internal analytics |
| Q7 | 2-3 things you're proudest of? | Lakehouse on Databricks + Delta Lake replacing Redshift (30 pipelines migrated); near-real-time ETA pipeline with Kinesis + Spark Structured Streaming; dbt with tests + data contracts with backend |
| Q8 | Numbers for those? | Warehouse cost down about 35% monthly; ETA latency from about 1 hour to under 5 minutes |
| Q9 | Tools you use there? | Python, SQL, PySpark, Databricks, Delta Lake, dbt, Airflow (MWAA), AWS (S3, Kinesis, Lambda, Glue), Terraform (some), GitHub Actions, Docker |
| Q10 | Mentoring / hiring / design docs / on-call? | Mentoring, hiring (interviewed and hired 2 engineers), design docs, on-call |
| Q11 | CV says "6 years of experience"; what now? | 10 years |
| Q12 | Awards, talks, patents? | (skipped) |
| Q13 | Used Kafka? (posting: streaming) | No, Kinesis only |
| Q14 | Used Kubernetes? (posting: nice-to-have) | No |

## Follow-ups
| # | Question | Answer |
|---|---|---|
| F1 | The ~35%: monthly warehouse cost? | Yes |
| F2 | How many engineers do you mentor? | 2 junior engineers |
| F3 | Data contracts with which team? | The backend team |
| F4 | Which projects were after the promotion? | (skipped) → both titles rendered under one employer with shared bullets |

## Previous roles
Offered: Data Engineer, Quillstone Retail (2019–2022) · BI Developer, Pinecrest Health Analytics (2016–2018). Chosen: Quillstone Retail.

| # | Question | Answer |
|---|---|---|
| P1 | Did you use Spark at Quillstone? | Yes, Spark on EMR for about a year, clickstream data |
| P2 | dbt at Quillstone? | No |
| P3 | Streaming work there? | (skipped) |
| P4 | Anything the CV undersells? | (skipped) |

## Changes made
| Section | Change | Based on |
|---|---|---|
| Header | Headline "Data Engineer" → "Data Engineering Team Lead · Lakehouse, Streaming & Analytics Engineering" | Q2, Q7, posting |
| Summary | "Profile" rewritten as a 2-paragraph TL;DR; "6 years" → "10 years" | Q4, Q7, Q8, Q11, posting |
| Experience / Harborlight | Stub bullet replaced by both titles + 6 bullets + Tech line | Q2–Q10, F1–F4 |
| Experience / Quillstone | New Spark bullet (2nd); "dimensional sales model" → "dimensional data model for sales reporting"; "Optimised" → "Optimized"; "Worked on" → "Contributed to" | P1, original, review |
| Experience / Pinecrest | 3 bullets merged into 2 | original |
| Skills | Regrouped with posting terms first; added Databricks, Delta Lake, Spark, dbt, Kinesis, EMR, Terraform, GitHub Actions, Docker, data contracts, dimensional data modeling; dropped SSIS | Q9, P1, original, posting |
| Headings | Standard names (Summary / Experience / Skills) instead of Profile / Professional Experience / Technical Skills | writing guide (ATS) |

## Review
- lint_cv: 0 errors, 0 warnings after fixes; all numbers trace to the original CV or answers
- Keyword coverage: must 50% → 100%, nice 33% → 83%, overall 44% → 94%
- Match score: 51 → 91 / 100 (strong match)
- Fixes applied: US spelling (Optimised → Optimized), weak opener rewritten, "data modeling" gap closed by truthful rewording
- Open gaps: Kafka (no; Kinesis shown as streaming experience), Kubernetes (no)
- Layout: "modern" spilled 15% onto page 2; typography tightened to fit 1 page

## Follow-up edits
- none
