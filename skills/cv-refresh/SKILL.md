---
name: cv-refresh
description: Updates, rewrites or tailors a CV / resume by interviewing the user with short skippable questions about their current or most recent role (and optionally older roles), then produces a 1-2 page DOCX and PDF, proofreads it, and scores it against a job posting when one is given. Use this whenever someone wants to update or refresh their CV or resume, add their latest job to it, tailor it to a job posting or a LinkedIn / job-board URL, get ready for a job search, or check how well their CV fits a job, even if they only say something like "my resume is out of date" or share a CV file together with a job link. Accepts PDF, DOCX and Markdown CVs and LinkedIn profile PDF exports.
license: MIT
compatibility: Claude Code and claude.ai (code execution on). Python 3.9+ with python-docx and pdfplumber or pypdf; LibreOffice for PDF output and the 2-page check; Poppler (pdftoppm) optional for previews.
metadata:
  version: 1.0.0
---

# CV Refresh

People put off updating their CV because it means remembering and wording years of
work from a blank page. This skill removes that friction: it reads the CV they
already have, asks short questions they can answer in seconds (or skip), and
does all the writing, formatting, proofreading and job matching itself.

`SKILL_DIR` below means the directory containing this file. Run scripts with
`python3 SKILL_DIR/scripts/<name>.py`; every script prints JSON.

## Ground rules

These exist because a CV is a document someone signs their name to and a
recruiter may verify. Breaking them costs the user far more than a weaker CV.

1. **Truthful content only.** Every fact must come from the original CV, a LinkedIn
   export the user supplied, or the user's answers in this session or in their
   session history. Never infer skills, tools or responsibilities they didn't state.
2. **Never invent numbers.** Use a number only if it appears in those sources.
   Don't estimate, round up, compute (including "years of experience" from dates)
   or write number words ("a decade", "dozens") that nobody gave you. If the
   original CV has a number that is probably stale (e.g. "6 years of experience"
   written years ago), ask the user for the current value instead of recalculating.
   `lint_cv.py` audits this; fix every number it flags.
3. **Facts that stay fixed:** employer names, official job titles, employment dates,
   degrees and institutions. Everything else is yours to change: wording, order,
   emphasis, headline, which items to keep, whole-document rewrites. Tailoring may
   produce an entirely new version.
4. **Comments live in chat, never in the document.** No Word comments, highlights,
   tracked changes, bracketed placeholders ("[add metric]") or notes-to-self in the
   CV. Every question, suggestion and caveat goes into the conversation.
5. **Two pages maximum**, hard cap, verified by rendering.
6. **US English** output with US spelling. If the source CV is in another language,
   translate faithfully and say so in chat.
7. **Low effort for the user.** Short questions, skip always allowed, never ask
   something the CV or history already answers.

## Workflow

### 0. Set up

1. `python3 SKILL_DIR/scripts/doctor.py`. If it reports missing requirements, give
   the user the install hints before continuing. Without LibreOffice you can still
   deliver a DOCX, but warn that the page count is unverified.
2. `python3 SKILL_DIR/scripts/state.py init`. Keep the returned `work_dir` (scratch
   files for this session), `data_dir`, `persistent`, `settings` and `sessions`.
3. If `needs_layout_question` is true, ask once, before anything else about the CV:
   "Should I keep your current CV's layout as closely as possible, or show you a few
   layout options to pick from each time?" Save the answer with
   `state.py set layout_mode preserve` or `state.py set layout_mode choose`, and tell
   the user in one line that it's saved and they can say "change my CV layout
   setting" anytime.
4. If `sessions` is non-empty, read the most recent session file(s). Previous
   answers are valid sources, and they tell you what not to ask again.

### 1. Gather inputs

- **CV file (required):** PDF, DOCX, Markdown/TXT, or a LinkedIn profile PDF export
  (LinkedIn → profile → More → Save to PDF). If the user provides both a CV and a
  LinkedIn export, the CV is primary and the export fills gaps. Ask for the file if
  none was given.
- **Job posting (optional):** a URL, pasted text or a file. Read
  `references/job-posting-intake.md` before fetching; LinkedIn needs special handling.
  No posting means a generic CV.

Then:

1. `extract_cv.py CV_FILE --out WORK_DIR/original.txt`, and read the whole text file.
   Pay attention to the `format` and `warnings` fields.
2. `extract_style.py CV_FILE --out WORK_DIR/style.json`.
3. Transcribe the original faithfully into `WORK_DIR/original.cv.json` following
   `references/cv-schema.md`. Transcribe only; improving comes later. This file is the
   baseline for "what changed" and for the before/after match score.
4. If there is a posting, build `WORK_DIR/posting.json` (schema in the intake reference).
5. Tell the user in 2-3 lines what you found: the roles you see, which one looks
   current, and what looks missing or outdated.

### 2. Interview about the current / most recent role

Read `references/interview-guide.md` and follow it. In short:

- Plan the whole batch first, then tell the user how many questions you plan to ask
  and on which topics before asking the first one.
- Ask with progress markers ("Q3/11"), using the host's multiple-choice question tool
  when there is one. Every question has a skip option.
- When the batch is done, review all the answers together and ask a follow-up round
  (announce how many) for anything vague, contradictory, or needed for the posting.
- Record every question and answer for the session history as you go.

### 3. Offer interviews on previous roles

List the earlier roles from the CV by name ("Data Engineer, Quillstone Retail,
2019-2022") and ask which, if any, the user wants to be interviewed on. For each one
chosen, run a shorter batch the same way: announce the count, ask, then follow up.

### 4. Write the new CV

Read `references/writing-guide.md`, then write `WORK_DIR/new.cv.json`:

- Always open with a TL;DR summary: one or two short paragraphs directly under the
  header.
- **Generic** (no posting): the strongest, broadly targeted version for the kind of
  roles the user said they want.
- **Tailored** (posting given): rewrite freely toward the posting. Reorder, reword,
  cut, and use the posting's vocabulary for things the user really has, but stay within
  the ground rules.

### 5. Choose the layout and render

Name the output files `First_Last_CV` (generic) or `First_Last_CV_Company` (tailored).
Output folder: claude.ai → `/mnt/user-data/outputs/`; Claude Code → the folder of the
input CV unless the user named another.

- `layout_mode = preserve`: render once with `--template mirror --style WORK_DIR/style.json`.
  This reproduces the original's fonts, sizes, colors, margins, paper size and heading
  style in a clean single column.
- `layout_mode = choose`: render `--template mirror,classic,modern,compact` into
  `WORK_DIR/options/`. Show the user the page-1 previews (or the PDFs), ask which one
  they want, render the chosen template to the output folder, and
  `state.py set last_template NAME`.

```
python3 SKILL_DIR/scripts/render_cv.py --cv WORK_DIR/new.cv.json --out-dir OUT \
  --basename First_Last_CV --template mirror --style WORK_DIR/style.json \
  --max-pages 2 --autofit --previews
```

`--autofit` only tightens typography. If a result still has `within_limit: false`,
cut content using the trimming order in the writing guide and render again. Repeat
until it fits. Then look at the preview images of every page. Fix anything that looks
wrong (orphaned headings, awkward line breaks) before moving on. The renderer already
tries to pull back a last page that is under 20% full. If `autofit_steps` says it
couldn't, trim or add content so no page looks nearly empty.

### 6. Review

Read `references/review-guide.md`. Then:

1. `lint_cv.py --cv WORK_DIR/new.cv.json --sources WORK_DIR/original.txt WORK_DIR/answers.md`
   (plus any LinkedIn export text or history files you used as sources). Fix every error.
   Treat the warnings as judgment calls.
2. Proofread the final text yourself: `extract_cv.py OUT/First_Last_CV.docx --out WORK_DIR/final.txt`.
   Fix spelling, grammar, consistency and tense.
3. If there is a posting: `check_keywords.py --posting WORK_DIR/posting.json --cv WORK_DIR/new.cv.json --before WORK_DIR/original.cv.json`.
   Then score the original and the new CV with the rubric.
4. Re-render after any fix and confirm it is still at most 2 pages.
5. Report in chat using the template in the review guide.

### 7. Deliver and record

1. Deliver the DOCX and PDF (claude.ai: `present_files`; Claude Code: give the paths).
   If the input was Markdown, also write an updated `.md` version.
2. Write the session history file as described in `references/history-format.md`, then
   `state.py save-session WORK_DIR/session.md`.
3. If `persistent` is false (claude.ai), run `state.py export` and deliver
   `cv-refresh-user-data.zip` too. Tell the user to upload it along with their CV next
   time so their settings and history carry over.
4. Offer one round of changes: "Tell me anything you'd like changed." Apply requested
   edits, re-run steps 5-6, and log them in the same session file.

## Host differences

| | Claude Code | claude.ai |
|---|---|---|
| Asking questions | `AskUserQuestion` tool if available, otherwise numbered text | tappable-options tool (max 3 questions per call), open questions as plain text |
| Fetching a posting | WebFetch; a logged-in browser tool if the user offers one | `web_fetch` works only for URLs that appear in the chat; the sandbox network blocks Python downloads |
| Files | real paths on the user's machine | uploads in `/mnt/user-data/uploads`, outputs in `/mnt/user-data/outputs` |
| Settings and history | persist in `SKILL_DIR/user-data/` (or `$CV_REFRESH_HOME`) | reset every chat: export and re-upload the zip |

## Changing settings

If the user says something like "change my CV layout setting" or "always show me
options", run `state.py set layout_mode preserve|choose` and confirm. Personal data
lives only in the data directory (`SKILL_DIR/user-data/` by default). It is
git-ignored and never packaged.

## Files

- `scripts/doctor.py`: environment check with install hints
- `scripts/state.py`: settings, session history, claude.ai import/export
- `scripts/extract_cv.py`: text from PDF / DOCX / MD / LinkedIn export
- `scripts/extract_style.py`: visual style of the original, for the mirror layout
- `scripts/render_cv.py`: cv.json to DOCX + PDF, templates, autofit, previews
- `scripts/lint_cv.py`: number audit, US spelling, weak phrases, mechanics
- `scripts/check_keywords.py`: keyword coverage against the posting, before and after
- `scripts/common.py`, `scripts/sections.py`: shared helpers
- `references/cv-schema.md`: the cv.json format
- `references/interview-guide.md`: planning and asking the questions
- `references/writing-guide.md`: summary, bullets, tailoring, trimming
- `references/review-guide.md`: proofreading, match-score rubric, chat report template
- `references/job-posting-intake.md`: URLs, LinkedIn, pasted text, posting.json
- `references/history-format.md`: the session history file
