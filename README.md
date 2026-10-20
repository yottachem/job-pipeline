# Job Pipeline

A [Claude Code](https://claude.com/claude-code) workflow for job seekers. For each job you consider, it:

- scores your fit against the job description with a fixed, weighted rubric
- reads your CV the way an ATS, a recruiter, and a hiring manager would, and turns what they'd miss into a fix list
- tailors your CV to close those gaps **without inventing anything**
- drafts a cover letter in your voice
- freezes what you submitted and tracks the outcome, so you can learn whether your scores predict anything

Everything runs in your own copy of this repo. Your CV, applications, and notes stay in files you control.

> **Your master CV is the foundation. Write it yourself.**
> Every score, check, tailored CV, and cover letter compares against one file: `cv/master.md`. You are strongly encouraged to draft it yourself, in your own words. Claude will convert your existing resume into the right format, interview you for evidence you left out, and flag weak bullets, but it won't write your bullets unless you insist. When it does, it marks every line it drafted until you rewrite or approve it.

## Why write the master CV yourself

- **The pipeline never invents claims,** so it can only be as accurate and specific as your master CV.
- **Interviewers probe what's on your resume.** Bullets you wrote are bullets you can defend for two minutes.
- **AI-written resumes read alike.** Your own phrasing is part of what makes you recognizable as a person.
- **It sets your voice.** Your cover letters are checked against writing you did yourself.

## What the score is, and what it isn't

The fit score (0-100) measures how well your background matches the job **as written**. It is not a probability of getting an interview. Referrals, timing, internal candidates, and ATS filters are invisible to it.

In the author's own job search, fit scores did not separate the applications that got a screen from the ones that didn't. How the application went in (direct vs. referral) did. That's why every application records its source, and why `/calibrate` exists: after about 15 resolved applications, you can check what predicts screens for *you*. Use the score to choose targets and find what to fix, then look for a warm path in.

More in [docs/scoring.md](docs/scoring.md).

## How it works

```
Step 0  /cv-master     You write your master CV (Claude formats, interviews, reviews)
Steps 1-6  /setup      Short interviews that capture the parts only you can supply
                       (profile, rubric, voice, export format, tracking, score anchor)

Then, per job:
/score <url>           Retrieve JD → score → screen check → decision
/tailor <slug>         Close the gaps the screen check found, no new claims
/cover-letter <slug>   Draft in your voice
/release <slug>        Freeze what you submitted
/log <slug> <outcome>  Record what happened
/calibrate             Learn what actually predicts a screen for you
```

## Setup at a glance

The pipeline logic is shared. The parts that make it yours can't ship pre-filled, so each one is a short **grill-me** interview: Claude asks one question at a time, offers a recommended answer drawn from your master CV, saves every answer to `brainstorms/` as you go, and drafts the file for your approval.

| Step | What | Command | You'll be asked about |
|------|------|---------|-----------------------|
| 0 | **Master CV (you write it)** | `/cv-master` | Your existing resume, then the evidence behind each role |
| 1 | Profile | `/setup 1` | Target roles, career throughline, domains, proof points, claims to avoid |
| 2 | Rubric | `/setup 2` | Weights, what counts as core vs. adjacent for you, your level, hard gaps |
| 3 | Voice | `/setup 3` | Writing samples you wrote yourself, punctuation and phrasing rules |
| 4 | Export format | `/setup 4` | Font, layout, page length, file names; a test export you approve |
| 5 | Tracking and privacy | `/setup 5` | Repo visibility, application sources, past applications, dashboard |
| 6 | Score anchor | runs after your first `/score` | Whether the first score matches your gut, and why not |

Details: [docs/setup-steps.md](docs/setup-steps.md).

## Get started

1. **Copy this repo.** Click **Use this template** and create a **private** repository. It will hold your CV, contact details, and application history. See [docs/privacy.md](docs/privacy.md).
2. **Clone it and install the requirements:**
   ```
   git clone https://github.com/<you>/<your-repo>.git
   cd <your-repo>
   pip install -r requirements.txt     # python-docx, for exports
   ```
   You also need [Claude Code](https://claude.com/claude-code), Python 3.10+, and [pandoc](https://pandoc.org/installing.html).
3. **Open Claude Code in the repo folder and run `/cv-master`.** Bring your current resume.
4. **Run `/setup`** and work through steps 1-5. One step per sitting is fine; nothing is lost between sessions.
5. **Run `/score` on a real job.** It finishes with step 6.

Full walkthrough: [docs/getting-started.md](docs/getting-started.md).

## Documentation

| Doc | Read it for |
|-----|-------------|
| [Getting started](docs/getting-started.md) | Install, copy, first session |
| [Setup steps](docs/setup-steps.md) | What each setup interview asks, what it writes, and why it can't ship pre-filled |
| [Pipeline](docs/pipeline.md) | Day-to-day commands and what each one produces |
| [Scoring](docs/scoring.md) | The rubric, the gap rules, core vs. pivot, calibration |
| [Privacy](docs/privacy.md) | Keeping your data private |

## What's in the repo

| Path | Shared or yours |
|------|-----------------|
| `CLAUDE.md`, `.claude/skills/`, `scripts/`, `templates/`, `docs/` | Shared pipeline logic |
| `cv/`, `profile/` | Yours, written during setup |
| `jds/`, `analyses/`, `cover-letters/`, `applications/`, `applications.csv`, `outcomes.md`, `calibration/`, `brainstorms/` | Yours, written as you use it |
| `examples/` | A fictional CV and JD, for format reference only |

## About

Built by Joshua Ritchey while running his own job search with Claude Code, then generalized for others. Issues and suggestions are welcome through GitHub Issues.
