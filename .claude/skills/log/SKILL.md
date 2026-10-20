---
name: log
description: Record an application outcome (rejection, screen, interview, offer, withdrawal) in outcomes.md and applications.csv, grade the conversion hypothesis, and refresh the dashboard. Use for /log <slug> <outcome>, "I got rejected from X", "X wants to schedule a screen".
---

# Log outcome

Gate: `python3 scripts/check_setup.py --for log`.

Outcome ladder: `no_response → rejected → recruiter_screen → hm_interview →
onsite → offer`. Off-ladder: `withdrawn`, `stalled`, `not_applied`, plus any
additions in `profile/tracking.md`.

## Steps
1. Match the slug in `applications.csv`. If the user names a company with
   several rows, ask which.
2. Append an entry at the top of `outcomes.md`:
   ```
   ## YYYY-MM-DD: <slug> → <outcome>
   <What happened, how it arrived, any reason given.>
   Fit score: <n> (<fit_type>), source: <source>.
   _Hypothesis check: held / missed. <One line on why, for /calibrate.>_
   ```
   Read the frozen `applications/.../analysis.md` hypothesis where a release
   exists; otherwise `analyses/<slug>.md`.
3. Update `outcome` and `outcome_date` in `applications.csv`. If the outcome
   is `recruiter_screen` or later, set `reached_screen` to `yes`; it stays
   `yes` even if the role later ends in rejection. Real CSV parser, build the
   output in memory, verify 12 fields per row before writing.
4. At `recruiter_screen` or later, offer to create a dated interview note in
   `applications/<company-slug>/<role-slug>/interviews/` (for example
   `2026-11-04-recruiter-call.md`) for prep and debrief. Offer the
   `grill-me` skill for interview prep.
5. Refresh the dashboard (`dashboard` skill).
