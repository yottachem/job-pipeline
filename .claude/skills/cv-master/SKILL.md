---
name: cv-master
description: Step 0 of setup, required before anything else. Helps the user build or revise cv/master.md, the master CV that every score, check, tailored CV, and cover letter compares against. The user drafts it; Claude converts format, interviews for evidence, and reviews. Use for /cv-master, "build my master CV", "import my resume", "review my master CV", or when check_setup.py reports step 0 incomplete.
---

# CV Master (Step 0)

If `profile/user.md` still starts with `<!-- SETUP-STUB`, run the `start`
skill first. Then follow its "How Claude works with you" block throughout.

`cv/master.md` is the ground truth for the whole pipeline. Nothing downstream
can be more accurate or specific than it is, and tailoring never adds claims
that aren't in it.

## The deal: the user writes it

Say this to the user at the start of every first session, in your own short
words:

> Your master CV is strongly encouraged to be written by you. I'll convert
> your existing resume into the right format, ask questions that surface
> evidence you left out, and flag weak or vague bullets. I won't write your
> bullets unless you ask me to, and if you do, I'll mark every line I drafted
> so you can rewrite it. Interviewers probe what's on your resume; bullets you
> wrote are bullets you can defend.

Hold to it:
- **Never reword the user's text during import.** Import changes format only.
- **Ask, don't rewrite.** In review, a weak bullet gets a question ("What
  changed because you did this? Is there a number?"), not a replacement.
- **If the user insists on a draft**, draft only from facts they gave you
  (their words in the capture file), and end every drafted line with
  `<!-- claude-drafted -->`. Tell them `check_setup.py` will keep listing
  those lines until they rewrite or approve them (approving means deleting
  the marker themselves).

## Modes

| Invocation | Does |
|------------|------|
| `/cv-master` | Start or continue: detect state, pick the next stage below |
| `/cv-master import <file or pasted text>` | Stage 2 only |
| `/cv-master interview [role]` | Stage 3, optionally for one role |
| `/cv-master review` | Stage 5 |

## Stages

### 1. Starting point
Run `python3 scripts/check_setup.py --cv cv/master.md`. If the file doesn't
exist, ask which start the user wants:
- **Import** an existing resume (.docx, .pdf, or pasted text). Recommended
  for most people.
- **Write from scratch:** copy `templates/cv-master.md` to `cv/master.md` and
  let them fill it in their editor.
- **Already done:** they wrote `cv/master.md` themselves; go to stage 4.

Show `examples/sample-master.md` as a format reference only. It is fictional;
none of its content should be copied.

### 2. Import (format only)
- Read the source. For .docx use `pandoc <file> -t markdown`; for .pdf use
  any available text extractor, or ask the user to paste the text.
- Rewrite into the format in `templates/cv-master.md` without changing the
  user's wording. Formatting fixes allowed: headings, the `·` separators,
  date format, bullet markers, removing tables and columns.
- List anything that didn't fit the format (a sidebar, a skills graphic, a
  two-column layout) and ask where it should go.

### 3. Evidence interview (grill-me)
Run the `grill-me` method with capture file
`brainstorms/<date>-cv-master.md`. Go role by role, newest first. For each:
- Scope: team size, budget, products, customers, reporting line.
- What changed because they were there? Before and after.
- Numbers they can stand behind (and where the number comes from).
- Work they're proud of that isn't on the page.
- Tools, methods, regulations, and domains used hands-on vs. supervised.

Then across the whole career: recurring themes (feeds the throughline in
step 1), credentials, patents, publications, awards, volunteer or side work.

The master CV is a **superset**. It should hold every true, relevant fact,
even if that makes it longer than any resume they would submit. Tailoring
selects from it.

### 4. The user drafts
Point the user to their capture file and let them revise `cv/master.md`
themselves. Offer to show which captured notes map to which role. Wait for
them to say they are done. Do not draft unless asked (see "The deal").

### 5. Review
Run `python3 scripts/check_setup.py --cv cv/master.md`, which validates the
format and reports content flags (weak verbs, passive voice, buzzwords,
quantified-impact ratio, em dashes). Then read it as an interviewer would and
list, as questions:
- Bullets the user couldn't talk about for two minutes.
- Numbers without an obvious source.
- Vague bullets ("improved processes") with no outcome.
- Facts that conflict with each other (dates, titles, team sizes).
- Evidence from the capture file that never made it onto the page.

Every review item is a question for the user. Record answers in the capture
file; the user makes the edits.

### 6. Done
Done when:
- `check_setup.py --cv` passes the format check, and
- the user confirms, in their own words, that the content is theirs and true.

Then tell them the next step: `/setup` (step 1, profile).

## Later revisions

When a fact changes in `cv/master.md` (new role, corrected date, new
result), list every `cv/master-<track>.md` and say each one needs the same
change. Tailored CVs already released stay frozen.
