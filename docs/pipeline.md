# Pipeline

> **Your master CV is the foundation. Write it yourself.**
> Every command below compares against `cv/master.md`, and none of them adds a fact that isn't in it. You are strongly encouraged to draft it in your own words. To add or correct a fact, edit the master CV (`/cv-master` reviews it), then rerun the command.

## Per-job flow

```
/score <url | pasted JD>
   │  JD saved to jds/, analysis to analyses/, row added to applications.csv
   │  screen check: ATS + recruiter skim + hiring manager read + core/pivot
   │  visual CV review opens in your browser
   ▼
decision: tailor │ tailor as pivot │ build a track master │ stop
   ▼
/tailor <slug> [pivot]       cv/<slug>.md, every change flagged for your approval
   ▼
/cover-letter <slug>         cover-letters/<slug>.md, in your voice
   ▼
(you submit it yourself)
   ▼
/release <slug>              frozen case file in applications/
   ▼
/log <slug> <outcome>        outcomes.md, applications.csv, dashboard
```

Claude never submits an application or sends a message. You do.

## Commands

| Command | Produces | Notes |
|---------|----------|-------|
| `/start` | `profile/user.md` | First run: beginner or experienced? Sets the explanation level |
| `/cv-master` | `cv/master.md` | Step 0. You write; Claude formats, interviews, reviews |
| `/setup [step]` | `profile/*.md` | Steps 1-6 |
| `/score <url, slug, or JD>` | `jds/<slug>.md`, `analyses/<slug>.md`, CSV row | Always includes the screen check. Ends on a decision |
| `/ats-check <slug>` | Updates the analysis, new visual review | Rerun after editing a CV |
| `/tailor <slug>` | `cv/<slug>.md`, exported .docx | Rewords and reorders only; same shape as your resume |
| `/tailor <slug> pivot` | Same | Wider reframing for an adjacent field, still no new claims |
| `/cover-letter <slug>` | `cover-letters/<slug>.md`, .docx | Checked against your voice samples |
| `/release <slug>` | `applications/<company>/<role>/` | One-time snapshot of what you submitted |
| `/log <slug> <outcome>` | `outcomes.md`, CSV, dashboard | Offers an interview prep note at screen or later |
| `/calibrate` | `calibration/calibration-<date>.md` | Meaningful after about 15 resolved applications |
| `/dashboard` | `dashboard/index.html` | Rebuilt automatically by `/release` and `/log` |

## The screen check

Every `/score` runs it, and `/tailor`, `/cover-letter`, and `/release` require it.

| Reader | What it checks |
|--------|----------------|
| **ATS** (`scripts/ats_check.py`) | Keyword overlap with the JD, weak verbs, passive voice, buzzwords, quantified-impact ratio, structure, contact info |
| **Recruiter** (6-30 second skim of the top third of page 1) | Does the positioning line read as this role? Are the top must-have terms there? Is seniority obvious? Is your key credential visible? Any red flag? |
| **Hiring manager** (full read) | The core problem this hire solves, the 3 bullets that prove you can solve it, the objections they'll raise and your evidence, likely interview probes |

Each recruiter "fix", weakly placed proof bullet, and unanswered objection becomes a work item for `/tailor`. Anything a CV can't fix goes to the cover letter or interview prep.

## Core vs. pivot

A role is a **pivot** when domain match or narrative fit falls below your threshold (default 60), or when the function or industry sits outside your throughline. Pivots get a **bridge line** (why this is a logical next step, not a restart), a **translation map** (your terms to theirs), and a pivot-mode tailor. When two or more roles share a pivot track, the pipeline suggests a **track master**: a whole-field rewrite of your master CV that later roles start from.

## Working vs. frozen files

| Working (revised in place) | Frozen (written once) |
|----------------------------|-----------------------|
| `cv/`, `jds/`, `analyses/`, `cover-letters/` | `applications/<company>/<role>/` |

The frozen copy keeps the score and prediction exactly as they stood when you applied, so `/calibrate` grades the real prediction, not a later revision.

## Helper scripts

All deterministic, no AI calls. Run from the repo root.

| Script | Does |
|--------|------|
| `check_setup.py` | Setup status, command gates, master CV format check |
| `ats_check.py` | Mechanical CV vs. JD checklist |
| `build_cv_review.py` | Visual CV review page (highlights plus diff against master) |
| `export_docx.py` | Markdown to a clean single-column .docx |
| `build_dashboard.py` | Dashboard from `applications.csv` |
