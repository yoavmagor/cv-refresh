# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). The version's single source of truth is
`metadata.version` in `skills/cv-refresh/SKILL.md`.

For a user-facing summary of each release, see [RELEASE_NOTES.md](RELEASE_NOTES.md).

## [Unreleased]

### Added
- Ground rule: never fabricate a link (`basics.links[].url`, `projects[].link`, or a
  URL in a bullet) from a label. Missing URLs render as plain text and get asked about
  once instead of guessed.
- Review guide step: verify every link that will render as clickable actually resolves
  before delivery, using the host's fetch tool, with documented false-negative cases
  (LinkedIn blocks automated fetches; GitHub's profile page is client-rendered — use
  `gh api` for those instead of trusting a fetch-tool error).
- `render_cv.py`: bare URLs and `github.com/...` references typed directly into a
  bullet or an `extra_sections` `lines` item are now auto-linkified as clickable,
  underlined, accent-colored hyperlinks (`add_text_with_links`).
- `render_cv.py`: every template now gets a colored rule under the header and under
  each section heading, and the company/institution name on a role or education line
  renders in the template's accent color, so the default output no longer reads as flat
  black-and-white. `classic` and `compact` each got a distinct accent color instead of
  near-black; `modern`'s section-heading rule was turned on.

### Fixed
- `render_cv.py`: the header would silently fabricate a URL (e.g. `https://LinkedIn`)
  for a link whose `url` was empty, using the display label as a fallback. It now
  renders as plain, non-clickable text instead.

## [1.0.0] - 2026-09-23

### Added
- `SKILL.md` workflow: setup, inputs, current-role interview, optional previous-role
  interviews, writing, layout and rendering, review, delivery and history.
- Ground rules: truthful content only, no invented numbers, fixed facts (employers,
  titles, dates, degrees), feedback in chat only, 2-page cap, US English.
- References: `interview-guide.md`, `writing-guide.md`, `review-guide.md`,
  `job-posting-intake.md`, `cv-schema.md`, `history-format.md`.
- `scripts/extract_cv.py`: text from PDF, DOCX, Markdown/TXT; LinkedIn profile export
  and right-to-left script detection.
- `scripts/extract_style.py`: fonts, sizes, colors, margins, paper size, header
  alignment, heading case/rule and section order from PDF or DOCX; multi-column flag.
- `scripts/render_cv.py`: cv.json → DOCX (named styles) → PDF via LibreOffice; layouts
  `mirror`, `classic`, `modern`, `compact`; typographic autofit to the page cap;
  pull-back of a near-empty last page; PNG previews; `positions` for multiple titles
  at one employer.
- `scripts/lint_cv.py`: number audit against source files (digits and number words),
  UK→US spelling, pronouns, weak openers, clichés, mechanics, dates, summary length.
- `scripts/check_keywords.py`: whole-term keyword coverage with aliases, before vs after.
- `scripts/state.py`: data-dir resolution (`$CV_REFRESH_HOME`, `SKILL_DIR/user-data`,
  claude.ai temp), settings (`layout_mode`, `last_template`), session history,
  export/import zip for claude.ai with a path-traversal guard.
- `scripts/doctor.py`: dependency check with install hints.
- Evals: 4 scenarios, generated fictional fixtures, a simulated-user persona,
  `check_outputs.py` objective assertions.
- Examples: full tailored (PDF, "modern") and generic (DOCX, "mirror") runs with all
  intermediate files.
- Tooling: `tools/package.py` (validate + build `.skill`/zip),
  `tools/install-claude-code.sh`.
- Docs: README, DESIGN (with the recreation prompt), STATUS, CHANGELOG, RELEASE_NOTES,
  MIT LICENSE.

[Unreleased]: https://github.com/<your-github-user>/cv-refresh/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/<your-github-user>/cv-refresh/releases/tag/v1.0.0
