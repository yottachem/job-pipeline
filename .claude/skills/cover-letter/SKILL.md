---
name: cover-letter
description: Draft a cover letter for one role in the user's own voice, grounded in the JD, the CV in play, and the analysis, then export it. Use for /cover-letter <slug> or "write a cover letter for X".
---

# Cover letter

Gate: `python3 scripts/check_setup.py --for cover-letter` (needs step 3,
voice). If the analysis has no `screen_check:` date, run `ats-check` first.

## Inputs
- `profile/voice.md` and the samples it points to. Reread them before
  drafting; the samples are the reference, not your instincts.
- `jds/<slug>.md`, the CV in play, `analyses/<slug>.md`.
- From the analysis: top 3 matches, HM proof bullets, the top HM objection,
  the honest gap worth naming (top 3 gaps / D5), and anything `/tailor`
  marked "not addressable on the CV".
- For `fit_type: pivot`: lead with the bridge line and answer the transition
  objection directly.

## Draft
Write `cover-letters/<slug>.md` following `templates/cover-letter.md` and
the voice rules. Every claim must trace to the CV in play. Every paragraph is
about the user and their fit; never describe the company back to itself.

## Before showing it
Reread every sentence against `voice.md`: split run-ons, remove phrases on
the never-use list, check punctuation rules. Then show the draft and say
which voice rules you checked.

## Export
After the user approves, export with the command in `profile/export.md`
(`--md cover-letters/<slug>.md`). The letter header's contact lines use the
same ` · ` convention as the CV, so they right-align the same way.
