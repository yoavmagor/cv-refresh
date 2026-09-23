# Release notes

User-facing notes for each release. Technical details are in [CHANGELOG.md](CHANGELOG.md).

---

## v1.0.0 (2026-09-23)

First release. Give Claude your CV (and optionally a job posting), answer a few quick
questions, and get back an updated 1-2 page CV as DOCX and PDF.

**Highlights**
- **Short, skippable interview.** You're told how many questions are coming before the
  first one. Most are yes/no or one line, and anything can be skipped. A short follow-up
  round catches gaps, and you can choose which earlier jobs, if any, to revisit.
- **Generic or tailored.** Without a posting you get a strong all-purpose CV. With one,
  the CV is rewritten toward that job and you get a before/after match score and a list
  of remaining gaps.
- **Honest by design.** Nothing is invented, especially numbers. Your employers, titles,
  dates and degrees are never altered. A built-in check verifies every number against
  your CV and your answers.
- **Your layout or a new one.** On first use, choose between keeping your current CV's
  look or picking from four layouts each time. The choice is remembered.
- **Proofread and reviewed.** Spelling and grammar are fixed automatically. Suggestions,
  the match score and questions all come in chat. Nothing is left as comments inside
  your document.
- **A TL;DR at the top.** Every CV opens with a short summary paragraph or two.
- **It remembers.** Each session's questions, answers and changes are kept, so next time
  it only asks what's new. In claude.ai, keep the `cv-refresh-user-data.zip` it gives
  you and upload it next time.

**Works with:** Claude Code and claude.ai. Accepts PDF, DOCX, Markdown, or a LinkedIn
profile PDF export. Job postings can be a link or pasted text. For LinkedIn job links
you may need to paste the text, because LinkedIn often hides postings behind a login.

**Known limitations:** tested with simulated data so far; English output only; the
"keep my layout" mode reproduces fonts, colors and spacing in a single column (photos,
icons and multi-column designs aren't carried over); no OCR for scanned PDFs. See
[STATUS.md](STATUS.md#known-limitations).
