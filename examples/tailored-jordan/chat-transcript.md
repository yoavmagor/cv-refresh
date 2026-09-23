# Example session (simulated, condensed)

Everything here is fictional: the user was played from
`evals/fixtures/simulated-user-jordan.md`. The intermediate files are in `work/`
and the delivered CV is in `output/`.

---

**User:** here's my cv (sample-cv-2022.pdf) and a job I want to apply to: *(pastes the Tessellate posting)*

**Claude:** One-time setup question before we start. When I produce your CV, should I:
`[ Keep my current layout ]  [ Show me layout options each time ]`

**User:** Show me layout options each time

**Claude:** Saved. You can say "change my CV layout setting" anytime.

Here's what I found: 3 roles (Harborlight Logistics, Quillstone Retail, Pinecrest
Health Analytics). Your current role at Harborlight has a single placeholder bullet from
2022, so that's the main gap. The posting is a Senior Data Engineer role on a data
platform team, and it needs Spark, dbt and streaming, none of which your CV shows yet.

I have **14 quick questions** about Harborlight: status and title, the company,
your team, what you own, your main projects and any numbers for them, tools, an
outdated line in your summary, and 2 things the posting asks for. Every question
can be skipped, and you can say "enough" anytime.

**Q1/14.** Are you still at Harborlight Logistics? `[ Yes ]  [ No, I left ]  [ Skip ]`
**Q2/14.** Is "Senior Data Engineer" still your title? `[ Yes ]  [ Changed ]  [ Skip ]`

**User:** Yes · Changed: promoted to Data Engineering Team Lead in Jan 2024

*…Q3–Q14 (see `work/answers.md`)…*

**Claude:** Thanks. After reviewing your answers, I have **4 short follow-ups**:
F1. The ~35%: is that the monthly cost of the warehouse?
F2. How many engineers do you mentor?
F3. The data contracts: with which team?
F4. Which of these projects happened after your promotion to Team Lead? (or skip)

**User:** yes · 2 juniors · backend · skip

**Claude:** Got it. Since you skipped F4, I'll list both titles under Harborlight with
shared bullets rather than guess which project belongs to which title.

Want me to go over any earlier roles? `[ Data Engineer, Quillstone Retail (2019–2022) ]  [ BI Developer, Pinecrest Health Analytics (2016–2018) ]  [ None ]`

**User:** Quillstone

**Claude:** **4 questions** about Quillstone Retail… *(P1–P4 in `work/answers.md`)*

**Claude:** Here are 4 layouts for the same content: *(page-1 previews of mirror, classic, modern, compact)*.
Which one? `[ Mirror (closest to your current CV) ]  [ Classic ]  [ Modern ]  [ Compact ]`

**User:** Modern

---

**Claude:**

**Your updated CV is ready**: Jordan_Avery_CV_Tessellate.docx and .pdf (1 page, "modern" layout).

**Match with Senior Data Engineer, Data Platform @ Tessellate Mobility:** 51 → 91 / 100 (strong match)
- Now clearly shown: Spark, dbt, streaming (Kinesis), the lakehouse, data modeling, mentoring, logistics domain
- Still missing: Kafka (you said no; your Kinesis work covers the posting's "or similar"), Kubernetes (you said no)

**What changed**
- Harborlight: both titles (Team Lead since Jan 2024, Senior Data Engineer 2022–2023) with 6 bullets from your answers and a Tech line
- Summary rewritten as a 2-paragraph TL;DR aimed at data platform roles; "6 years" updated to "10 years" as you said
- Quillstone: new Spark bullet near the top; the sales model now reads as dimensional data modeling
- Pinecrest condensed to 2 bullets; SSIS dropped from skills; skills regrouped with the posting's terms first
- Headings renamed to the standard Summary / Experience / Skills, which applicant tracking systems parse best

**Fixes applied**
- "Optimised" → "Optimized" (US spelling)
- "Worked on data quality checks" → "Contributed to data quality checks" (clearer, without overstating)
- The "modern" layout spilled 15% onto a second page, so I tightened spacing to fit one page

**Suggestions (not applied)**
1. If you built or owned the Great Expectations checks at Quillstone (not just contributed), say so and I'll strengthen that bullet.
2. Terraform is listed but you said you use it "some". If an interviewer probes it, be ready with one concrete example, or tell me to drop it.
3. Q12 (awards, talks) was skipped. A talk or blog post on data contracts would stand out for this team.

Anything you'd like changed?
