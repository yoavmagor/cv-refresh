# Interview guide

The interview is the part the user dreads, so it has to feel quick and finite.
Three things do that: they know how many questions are coming, each question
takes seconds, and skipping is always fine.

## 1. Record as you go

Write every question and the user's exact answer, or `(skipped)`, to
`WORK_DIR/answers.md` as the interview happens:

```
## Current role: Harborlight Logistics
Q1. Are you still at Harborlight Logistics? → Yes
Q2. Is "Senior Data Engineer" still your title? → Promoted to Data Engineering Team Lead, Jan 2024
Q3. ... → (skipped)
## Follow-ups
F1. ...
```

This file is a source for the number audit (`lint_cv.py --sources`), and it
becomes the Q&A section of the session history. Keep the user's wording. Don't
paraphrase their answers into better-sounding facts.

## 2. Plan the batch before asking anything

Draft the full list first. Start from the question bank below and drop every
question that the CV, the LinkedIn export or earlier session history already
answers. Then add posting-gap questions if there is a posting.

- **Typical size:** 8-14 questions for the current role; 4-6 per previous role.
- **With history:** open with "Since your last session on <date>, what changed at
  <company>?" and plan mostly delta questions. Aim for a short batch.
- **Order:** easy facts first (status, title, dates), then team and domain, then
  work and achievements, then tools and skills, then gap questions.

Then announce it, before Q1:

> I have **11 quick questions** about your role at Harborlight Logistics: status and
> title, team, the company's domain, your main projects, tools, and 3 things the job
> posting asks for. Every question can be skipped, and you can say "enough" anytime.

## 3. How to ask

- One idea per question. Short. Answerable in a word or a line.
- Prefer yes/no and multiple choice. Pre-fill guesses from the CV so the user
  confirms instead of composes: "Is your title still 'Senior Data Engineer'?"
  beats "What's your title?".
- Always offer **Skip**. In a choice question it's an option. In an open
  question, add "(or skip)".
- Show progress: `Q4/11`.
- **Host tools.** In claude.ai, use the tappable-options tool for yes/no and choice
  questions (at most 3 per call, 2-4 options each; put Skip among the options).
  Ask open questions as plain text, a few at a time. In Claude Code, use
  `AskUserQuestion` when available (it also lets the user type a custom answer).
  Otherwise use numbered plain text. If the user answers several questions in one
  message, accept that.
- If the user says "enough" or "just write it", stop the batch and work with what
  you have. Don't guilt them into more.

### Numbers

You may offer one optional question for concrete numbers, e.g. "Any numbers you
know for this, like team size, scale, time or money saved? (skip if not)". Use only
numbers the user actually gives. Never suggest example figures they could agree to.
That is still inventing. If the old CV has a number that has probably gone stale
("6 years of experience", "team of 3"), ask: "Your CV says '6 years of experience';
what should it say now? (or skip to drop it)".

## 4. Question bank: current / most recent role

Pick and adapt. Don't ask all of these.

| Topic | Example question | Format |
|---|---|---|
| Status | Are you still at <Company>? | Yes / Left (when?) / Skip |
| Title & dates | Is "<title>" still your title? Any promotions or title changes? | Yes / Changed (to what, when?) / Skip |
| Company domain | In one line, what does <Company> do and for whom? (I'll guess: "<guess>", right?) | Confirm / Correct / Skip |
| Team | How big is your team, and what's your position in it? | IC / Tech lead / Manager / Skip + size |
| Collaboration | Which groups do you work with most? | multi-select: product, data science, backend, customers, execs, other |
| Scope | What do you own or are you responsible for, in a line or two? | open |
| Key work | What are the 2-3 things you built, led or fixed there that you're proudest of? | open |
| Impact | Any numbers you know for those? | open, optional |
| Tools | Which of these do you use there? (list inferred tools and the posting's tools) | multi-select + other |
| Skills | Which of these apply: mentoring, hiring, design docs/architecture, on-call, stakeholder management, cross-team projects? | multi-select |
| Recognition | Any awards, promotions, talks or patents from this role? | open, optional |
| Direction | What roles are you aiming for next? (shapes the summary) | open, short |

## 5. Posting-gap questions (tailored runs)

For each **must-have** in `posting.json` that the CV doesn't clearly show, ask a
yes/no/where question. Ask the same for nice-to-haves that seem plausible for this
person:

> The posting asks for **Apache Spark**. Have you used it? → Yes, current role /
> Yes, an earlier role / No / Skip

"No" is a perfectly good answer. Record it, don't claim the skill, and list it as a
gap in the review. Don't ask leading follow-ups to talk the user into it. If they
have an adjacent skill (Kinesis instead of Kafka), you may present that truthfully.

## 6. Follow-up round

After the batch, read all the answers together and look for:

- vague answers that would make a weak bullet ("worked on the platform"): ask what they
  did, what changed, and for whom
- contradictions with the CV (dates, titles)
- things mentioned in passing that deserve a bullet ("…and I also hired two people")
- a number the user mentioned loosely, to confirm (never to supply)
- after a promotion: which work happened under which title (if skipped, use `positions`)
- remaining posting gaps

Announce the round the same way ("3 short follow-ups"), usually 0-5 questions. If
nothing needs clarifying, say so and move on.

## 7. Previous roles

List each earlier role by title, company and years, and ask which ones to go over
(multi-select with a "None" option). For each chosen role, a 4-6 question batch
covering what changed in how they'd describe it, notable work the CV undersells, and
tools and skills relevant to the posting. Same rules: announce the count, allow
skipping, then follow up.
