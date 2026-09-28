# cv.json format

The renderer, the linter and the keyword checker all read this one structure. You
write two instances per session: `original.cv.json`, a faithful transcription, and
`new.cv.json`, the rewrite. Omit any field you don't need. Unknown fields are ignored.

```json
{
  "meta": {
    "target": {"type": "posting", "title": "Senior Data Engineer", "company": "Tessellate Mobility"},
    "section_order": ["summary", "experience", "skills", "education", "military", "languages"],
    "section_titles": {"experience": "Professional Experience", "skills": "Technical Skills"}
  },
  "basics": {
    "name": "Jordan Avery",
    "headline": "Data Engineering Team Lead",
    "location": "Tel Aviv, Israel",
    "phone": "",
    "email": "jordan.avery@example.com",
    "links": [{"label": "LinkedIn", "url": "https://linkedin.com/in/jordan-avery-example",
               "display": "linkedin.com/in/jordan-avery-example"}]
  },
  "summary": [
    "First paragraph of the TL;DR.",
    "Optional second paragraph."
  ],
  "experience": [
    {
      "company": "Harborlight Logistics",
      "title": "Data Engineering Team Lead",
      "start": "2024-01",
      "end": "present",
      "location": "Tel Aviv, Israel",
      "company_blurb": "B2B SaaS for freight visibility",
      "bullets": ["Led ...", "Built ..."],
      "tech": ["Python", "Databricks"]
    }
  ],
  "skills": [{"group": "Languages", "items": ["Python", "SQL"]}],
  "education": [{"institution": "Ben-Gurion University of the Negev", "degree": "B.Sc.",
                 "field": "Industrial Engineering and Management", "start": "2012", "end": "2016",
                 "details": []}],
  "certifications": [{"name": "...", "issuer": "...", "year": "2023"}],
  "projects": [{"name": "...", "description": "...", "link": "github.com/...", "bullets": []}],
  "languages": [{"language": "Hebrew", "level": "Native"}, {"language": "English", "level": "Fluent"}],
  "extra_sections": [
    {"key": "military", "title": "Military Service",
     "items": [{"title": "Operations Analyst", "company": "IDF", "start": "2009", "end": "2012", "bullets": []}]},
    {"key": "earlier", "title": "Earlier Experience", "style": "lines",
     "items": ["BI Developer, Pinecrest Health Analytics (2016 – 2018)"]}
  ]
}
```

## Field notes

- **Dates:** `YYYY-MM` or `YYYY`, or `present`. They render as "Jan 2024 – Present".
  Keep the original's precision. Don't add a month that the original doesn't have.
- **Promotions:** if the user said which work belongs to which title, use separate
  `experience` entries with the same `company`, newest first. If they didn't, don't
  guess. Use one entry with `positions`, and the bullets apply to the whole tenure:
  ```json
  {"company": "Harborlight Logistics", "company_blurb": "B2B SaaS for freight visibility",
   "positions": [{"title": "Data Engineering Team Lead", "start": "2024-01", "end": "present"},
                 {"title": "Senior Data Engineer", "start": "2022-04", "end": "2023-12"}],
   "bullets": ["..."]}
  ```
- **`company_blurb`:** a short, factual line about what the company does. Include it
  only when the user or the CV said it. It helps with lesser-known employers.
- **`tech`:** optional "Tech:" line under a role. Use it when tools matter for the
  target; otherwise leave tools in `skills`.
- **Inline markup in text** (bullets, `summary` paragraphs, `extra_sections` "lines"
  items): wrap a word or short phrase in `**double asterisks**` to render it bold —
  use this for the 1-2 key nouns per bullet (the tool, platform, or result), not for
  whole sentences (see `references/writing-guide.md`). A bare URL or `github.com/...`
  reference is rendered as a clickable link automatically; don't wrap it in markdown
  link syntax.
- **`section_order`:** canonical keys `summary, experience, skills, projects, education,
  certifications, languages`, plus the `key` of any extra section. The summary is
  always rendered first, right under the header. Sections that exist in the data but
  aren't listed are appended after the listed ones.
- **`section_titles`:** override headings, e.g. to mirror the original's wording.
- **`extra_sections`:** anything else (military service, volunteering, awards,
  publications, earlier experience). Items can be strings (`style`: `bullets`, the
  default, or `lines`) or role-like objects (title, company, start, end, bullets).
- **Header and contact details** go in `basics` and are rendered in the document body,
  not in the page header or footer. Some applicant tracking systems skip those areas.
- **Links (`basics.links[].url`, `projects[].link`):** only set `url` when you actually
  have one, from a source or the user. Leave it `""` when you don't — the renderer shows
  the label as plain, non-clickable text instead of guessing a destination from it (a
  guessed URL is a fabricated fact). A bare URL or `github.com/...` reference typed
  directly into a bullet or an `extra_sections` `lines` item is auto-linkified by the
  renderer and shown underlined in the accent color, so it doesn't need a separate field.
  Verify every link resolves before delivering (`references/review-guide.md`).
