---
name: calibrate
description: Compare predicted fit scores and conversion hypotheses against actual outcomes to learn whether the rubric predicts anything for this user, and what does. Use for /calibrate, "is my scoring working", "what's converting".
---

# Calibrate

Gate: `python3 scripts/check_setup.py --for calibrate`.

## Data rules
- **Resolved** = has an outcome. Rows with no response 3+ weeks after
  applying count as "no screen" (say which rows you treated that way).
- **Use the frozen score:** `applications/<company-slug>/<role-slug>/analysis.md`
  where a release exists, not the live `analyses/<slug>.md`, which may have
  been revised since.
- Exclude `not_applied`. Exclude `backfilled: true` analyses from hypothesis
  checks (the prediction wasn't made in advance) but keep them in rate tables.
- Report "not enough data yet" honestly when N is below about 15. Don't
  recommend reweighting below that.

## Questions to answer
1. **Do higher scores convert more often?** Screen rate by score band
   (0-39, 40-59, 60-79, 80-100). Mean total, converted vs. not.
2. **Is the rubric calibrated?** How many "likely" hypotheses converted vs.
   "coin-flip" and "unlikely"? Systematically optimistic or pessimistic?
3. **Which dimensions separate?** Mean of each sub-score, converted vs. not,
   and the gap. A heavily weighted dimension that doesn't separate is worth
   noting.
4. **Source.** Screen rate by source (direct, referral, recruiter, ...).
   Source often predicts better than fit; if it does here, say so plainly.
5. **Patterns in the misses.** For example, high domain fit but no screen on
   direct applications points to a resume-skim problem, not a fit problem.
6. **Core vs. pivot.** Screen rate and mean score by `fit_type`, and by
   `pivot_track` where a track has enough rows. Does the rubric under- or
   over-predict pivots?
7. **Reader lens.** Did roles released with unresolved recruiter-pass fixes
   die before a screen more often than roles with none?

## Output
Write `calibration/calibration-YYYY-MM-DD.md` with a table per question, then
up to three recommendations. Typical ones: keep the weights (with the
reason), adjust a specific definition in `profile/rubric.md`, or change
behavior (for example, use the score to pick targets and then find a warm
path in). Any rubric change is the user's decision; offer `/setup 2` to make
it.
