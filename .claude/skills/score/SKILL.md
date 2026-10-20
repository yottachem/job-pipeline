---
name: score
description: Score fit between the master CV and one job description, then run the mandatory screen check and stop on a decision. Use for /score <url | slug | pasted JD>, "score this job", "how well do I fit this role", or when the user pastes a job description.
---

# Score

Runs: retrieve the JD → score → screen check → decision block. The screen
check is never skipped; a score without it is an incomplete run.

## 0. Gate
`python3 scripts/check_setup.py --for score`. If blocked, stop and offer the
missing step. Read `profile/profile.md` and `profile/rubric.md` before
scoring.

## 1. Register the job
- Build the slug `<company>-<role-slug>` (lowercase, hyphenated).
- If `applications.csv` has no row for it, add one (real CSV parser, 12
  fields): company, role, url, `date_applied` blank, `outcome` blank. Ask the
  user for `source` from the vocabulary in `profile/tracking.md` if it isn't
  obvious; default `direct`.
- Never overwrite an existing `analyses/<slug>.md` unless asked. To rescore,
  append a dated `## Revision YYYY-MM-DD` section.

## 2. Retrieve the JD
- Live URL: fetch it.
- Dead URL (postings come down when roles close): search for a cached or
  aggregator copy.
- Neither works, or the board needs a login: set `jd_status` to `jd_missing`
  and ask the user to paste the text.
- Save to `jds/<slug>.md` using `templates/jd.md`, keeping the original
  wording. Set `jd_status` in the CSV.

## 3. Score
Write `analyses/<slug>.md` from `templates/analysis.md`, following the rubric
and scoring discipline in `CLAUDE.md`:
- Deal-breaker check against `profile.md` first (recorded, not scored).
- Five sub-scores with one-line justifications, using the tiers, level band,
  and hard-gap list in `rubric.md`, and the throughline in `profile.md`.
- Weighted total using `rubric.md` weights. Compare it with the anchor; if
  the comparison feels wrong, recheck the sub-scores before writing.
- Requirement coverage list, top 3 matches, top 3 gaps (each marked hard or
  addressable).
- One-line conversion hypothesis: likely / coin-flip / unlikely, and why.
- External factors, including source.
- Update `fit_score` in the CSV.

## 4. Screen check
Continue straight into the `ats-check` skill (all of it, including the
visual review and fit-type classification). Then set `fit_type` in the CSV.

## 5. Anchor (first run only)
If `check_setup.py` reported the anchor pending, run setup step 6
(`.claude/skills/setup/steps/6-anchor.md`) on this role now.

## 6. Decision block
Stop and give the user one short block:
- Total score (and anchor for reference), `fit_type` / `pivot_track`
- Recruiter-pass fix count, top hiring-manager objection
- Conversion hypothesis
- Options: tailor (core mode), tailor (pivot mode, offered when
  `fit_type: pivot`; the user can override), create a track master first
  (when recommended), or stop here.

Don't proceed to `/tailor` without the user's answer.
