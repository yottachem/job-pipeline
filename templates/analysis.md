---
slug:
company:
role:
scored: YYYY-MM-DD
total_score:
fit_type:        # core | pivot
pivot_track:     # reusable track slug when fit_type: pivot, else blank
screen_check:    # YYYY-MM-DD when the screen check finished; /tailor is gated on this
backfilled:      # true if scored after the outcome was known (excluded from prediction checks)
---

# <Company>, <Role>

**Deal-breaker check:** <none, or which item from profile.md applies>

## Sub-scores

Weights from `profile/rubric.md`.

| Dimension | Weight | Score | Justification (one line) |
|-----------|--------|-------|--------------------------|
| D1 Domain match | | | |
| D2 Requirement coverage | | | |
| D3 Seniority and scope | | | |
| D4 Narrative fit | | | |
| D5 Gap severity (inverted) | | | |

**Weighted total: __ / 100** (anchor: <slug> at <n>)

## Requirement coverage
<!-- Every stated must-have from the JD: met / partial (say why) / unmet -->
- [ ]

## Top 3 matches
1.
2.
3.

## Top 3 gaps
<!-- Mark each: hard (scored) or addressable (address proactively: how) -->
1.
2.
3.

## ATS & Content Check
<!-- Output of scripts/ats_check.py. Mechanical signal only; review with -->
<!-- judgment. Does not affect the weighted total. -->

## Reader lens

### Recruiter pass (top third of page 1 only)

| Check | Result | Note |
|-------|--------|------|
| Positioning line reads as this role's title or function | pass / fix | |
| JD's top ~5 must-have terms appear in the top third | pass / fix | |
| Seniority and years legible at a glance | pass / fix | |
| Credential to surface (profile.md) visible | pass / fix / n/a | |
| Skim-level red flags (level mismatch, tenure, industry, location) | none / fix | |

### Hiring manager pass

**Core problem this hire solves:**

**Proof bullets** (quoted from the CV, and whether they're positioned to be found):
1.
2.
3.

**Likely objections → evidence that answers them:**
1.
2.

**Likely interview probes:**
1.
2.

## Pivot assessment
<!-- Fill only when fit_type: pivot; otherwise write "Core role, n/a." -->

**Bridge line:**

**Translation map:**

| My term | Target field's term |
|---------|---------------------|
| | |

**De-emphasize:**

**Transition objection, and the answer the CV should make unnecessary:**

**Track master check:** <n other analyses in this track; recommend cv/master-<track>.md? yes/no>

## Conversion hypothesis
<!-- One line: does this earn a screen, and why or why not? /calibrate grades -->
<!-- this against the actual outcome. Use: likely / coin-flip / unlikely. -->

## External factors (do not affect the score)
<!-- Source (referral? recruiter?), suspected internal candidate, timing, ATS risk -->
