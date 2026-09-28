# Review guide

The review has two outputs. The first is a corrected CV: you fix the problems you
find rather than just listing them. The second is a report in chat. Nothing from the
review goes into the document itself.

## 1. Automated checks

```
python3 SKILL_DIR/scripts/lint_cv.py --cv WORK_DIR/new.cv.json \
  --sources WORK_DIR/original.txt WORK_DIR/answers.md [other source files]
```

- `numbers` errors: remove the number, or restore the exact figure from a source. If
  the user may know the real value, ask in chat. Don't guess.
- `spelling_us` errors: apply the suggested US spelling.
- `mechanics` and `dates` errors: fix them.
- Warnings (pronouns, weak openers, clichés, long bullets, summary length): fix unless
  there's a good reason not to, such as a quoted award name.

## 2. Human-quality proofread

Extract the final DOCX text (`extract_cv.py OUT/<name>.docx --out WORK_DIR/final.txt`)
and read all of it, top to bottom. Check for:

- spelling, including names of tools and companies (PostgreSQL, not Postgres SQL)
- grammar, agreement and articles; tense (current role present, past roles past)
- consistency: date format, capitalization, bullet punctuation, serial commas
- repetition: the same verb starting three bullets in a row, the same claim twice
- clarity: any bullet a recruiter outside the team wouldn't understand
- truthfulness, one last time: does every claim trace back to a source?

Apply the fixes, re-render, and confirm the page count again.

## 3. Verify every link is real and reachable

Anything that will render as a clickable link — every `basics.links[].url`,
`projects[].link`, and any bare URL inside a bullet or extra-section line (see
`references/cv-schema.md`) — must be checked before delivery, not just typed in.

1. **Never fabricate one first.** If a source or the user didn't give you a URL, leave
   the field empty (it renders as plain, non-clickable text — see `render_cv.py`'s
   `header()`) and ask once rather than guess one from a label like "LinkedIn" or
   "GitHub". A guessed URL is a fabricated fact, same as an invented number.
2. **Then fetch each one** with the host's tool (`WebFetch` in Claude Code, `web_fetch`
   in claude.ai) to confirm it resolves. Treat these as expected, not failures:
   - LinkedIn blocks automated fetches (HTTP 999 or similar) for any URL, valid or not —
     it doesn't tell you the profile is broken. A LinkedIn URL the user typed or that
     came from their own LinkedIn export is trustworthy without a fetch.
   - A GitHub profile or repo page can come back as "content failed to load" from a
     markdown-conversion fetch tool even when the page is real, because GitHub renders
     client-side. Confirm with `gh api users/<name>` or `gh api repos/<owner>/<repo>`
     instead when `gh` is available.
   A genuine 404, parked-domain page, or login wall on something meant to be public is
   a real problem: tell the user in chat rather than silently dropping or editing the
   link yourself — they may know it's temporarily down, or need to give you the fix.

## 4. Match score (only when a posting was given)

```
python3 SKILL_DIR/scripts/check_keywords.py --posting WORK_DIR/posting.json \
  --cv WORK_DIR/new.cv.json --before WORK_DIR/original.cv.json
```

Score **both** the original and the new CV out of 100 with this rubric, so the user
sees what the update achieved:

| Component | Points | How to judge |
|---|---|---|
| Must-have requirements evidenced | 45 | the share of must-haves the CV clearly shows (a keyword mention alone counts half) |
| Nice-to-haves evidenced | 15 | same, for the nice-to-haves |
| Keyword coverage | 15 | `overall_coverage_pct` from the script × 0.15 |
| Seniority & scope fit | 15 | years, level, leadership and scale compared with the posting |
| Domain fit | 10 | industry / problem-space overlap |

Bands: 85+ strong match · 70-84 good · 55-69 partial · under 55 a stretch.
Be honest: a truthful CV can't close a real gap, and the score should show that.

## 5. Chat report template

Keep it scannable. Use this structure and drop the parts that don't apply:

```
**Your updated CV is ready**: Jordan_Avery_CV_Tessellate.docx and .pdf (2 pages, "modern" layout).

**Match with Senior Data Engineer @ Tessellate Mobility:** 58 → 84 / 100 (good match)
- Now clearly shown: Spark, dbt, streaming (Kinesis), lakehouse, mentoring
- Still missing: Kafka (you said no; Kinesis is presented as the streaming experience), Kubernetes

**What changed**
- New Team Lead role and Senior Data Engineer role at Harborlight, built from your answers
- Summary rewritten as a 2-paragraph TL;DR aimed at data platform roles
- Quillstone bullets reordered to lead with Spark and Airflow; Pinecrest shortened to 2 bullets
- "Profile" is now "Summary"; skills regrouped with posting keywords first

**Fixes applied**
- "Optimised" → "Optimized" (US spelling)
- "Worked on data quality checks" → rewritten with a stronger verb

**Links checked:** LinkedIn, GitHub, portfolio.example.com — all resolve.

**Suggestions (not applied)**
1. If you have a public talk, blog post or open-source work on data contracts, add a link; it's a differentiator here.
2. The posting stresses Kubernetes as a nice-to-have. Worth a line in your cover email if you've used it outside work.

Anything you'd like changed?
```

Suggestions must be actionable, specific to this CV and posting, and never pressure
the user to claim things they don't have.
