# Examples

Two complete runs of the skill on **fictional** data (see `evals/fixtures/`). The user
was simulated from `evals/fixtures/simulated-user-jordan.md`.

| Folder | Scenario | Look at |
|---|---|---|
| [`tailored-jordan/`](tailored-jordan/) | Outdated 2022 PDF CV + pasted job posting; "show me options" layout mode; user picked **modern** | [`chat-transcript.md`](tailored-jordan/chat-transcript.md), [`output/`](tailored-jordan/output/), [`work/options/`](tailored-jordan/work/options/) (all 4 layouts) |
| [`generic-jordan/`](generic-jordan/) | Same person, DOCX input, no posting; "keep my layout" mode (**mirror**) | [`output/`](generic-jordan/output/) |

Each `work/` folder holds the intermediate files the skill writes during a session:

| File | What it is |
|---|---|
| `original.txt` | text extracted from the input CV |
| `style.json` | layout detected from the original (drives the mirror template) |
| `original.cv.json` | faithful transcription, the "before" baseline |
| `posting.json` | distilled requirements and keywords (tailored run only) |
| `answers.md` | every question and answer, verbatim; a source for the number audit |
| `new.cv.json` | the rewritten CV that gets rendered |
| `session.md` | the session history record (tailored run) |

To re-check the tailored run:

```bash
T=examples/tailored-jordan
python3 evals/check_outputs.py --docx $T/output/Jordan_Avery_CV_Tessellate.docx \
  --pdf $T/output/Jordan_Avery_CV_Tessellate.pdf --original $T/work/original.cv.json \
  --new $T/work/new.cv.json --sources $T/work/original.txt $T/work/answers.md \
  --session $T/work/session.md
```
