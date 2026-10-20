---
name: ats-check
description: The screen check. Reads the CV in play the way an ATS, a recruiter, and a hiring manager would, classifies the role as core or pivot, and builds a visual review page. Runs automatically inside /score and is a prerequisite for /tailor, /cover-letter, and /release. Use for /ats-check <slug>, or to recheck after editing a CV.
---

# Screen check

**CV in play:** `cv/<slug>.md` if it exists (recheck after tailoring);
otherwise `cv/master-<track>.md` if the role's `pivot_track` has one;
otherwise `cv/master.md`.

Gate: `python3 scripts/check_setup.py --for ats-check`.

## 1. ATS (mechanical)
Run `python3 scripts/ats_check.py --cv <cv in play> --jd jds/<slug>.md --json /tmp/<slug>-ats.json`.
Paste its output into `## ATS & Content Check`. It is a mechanical signal:
missing-keyword lists include generic words, and a flag is a candidate to
look at, not a verdict. Review with the same discipline as the scores.

## 2. Reader lens (judgment)
Fill `## Reader lens`.

**Recruiter pass (the 6-30 second skim).** Judge only the top third of page
1: name, Summary, first role. Mark each check pass or fix:
- Does the positioning line read as this role's title or function?
- Do the JD's top ~5 must-have terms appear there, not just on page 2?
- Are seniority and years legible at a glance?
- Is the credential from `profile.md` ("Credential to surface") visible?
- Any skim-level red flag: level mismatch (overqualified or reach), short
  tenure, industry mismatch, location?

**Hiring manager pass (the full read).**
- The core problem this hire solves, in one line, inferred from the JD (not
  the JD's own summary sentence).
- The 3 CV bullets that best prove it, quoted, and whether they're positioned
  where the hiring manager will find them.
- The 2-3 most likely objections, each with the specific evidence that
  answers it. Check `profile.md` "Known objections" first.
- 2-3 likely interview probes.

Every recruiter "fix", weakly positioned proof bullet, and unanswered
objection becomes a work item for `/tailor`.

## 3. Fit type and pivot assessment
Classify per `CLAUDE.md` (pivot threshold from `rubric.md`) and set
`fit_type` and `pivot_track` in the analysis frontmatter. Reuse an existing
track slug (from `rubric.md` or other analyses) before inventing one.

For `pivot`, fill `## Pivot assessment`:
- **Bridge line:** one sentence on why this move is a logical next step, not
  a restart. The Summary and cover letter must carry it.
- **Translation map:** the user's experience in their terms → the same thing
  in the target field's vocabulary.
- **De-emphasize:** what on the current CV reads as noise to this reader.
- **Transition objection:** the "why are you leaving your field?" question,
  and the answer the CV should make unnecessary.
- **Track master check:** count analyses with the same `pivot_track`. At 2+
  (including this one) with no `cv/master-<track>.md`, recommend creating one.
  Don't create it without the user's go-ahead.

## 4. Visual review
Run:
```
python3 scripts/build_cv_review.py --cv <cv in play> --jd jds/<slug>.md \
    --master cv/master.md --title "<Company>, <Role>" --out /tmp/<slug>-review.html
```
Open the file for the user (`open` on macOS, `xdg-open` on Linux), or publish
it as an artifact if the environment supports that. It is a review aid, not a
record: don't commit it.

## 5. Finish
Set `screen_check: YYYY-MM-DD` in the analysis frontmatter. When called on
its own (not from `/score`), end with the same decision block as `/score`.
