# User guide

What to do, when, and where, from your first session to your fiftieth application.

> **Your master CV is the foundation. Write it yourself.**
> Every score, check, tailored CV, and cover letter compares against `cv/master.md`, and nothing is ever added that isn't in it. You are strongly encouraged to draft it in your own words. Claude formats it, interviews you for evidence you left out, and reviews it, but doesn't write your bullets unless you insist.

---

## First: which describes you?

| | You are... | Read |
|---|-----------|------|
| **A. Beginner** | New to Claude Code, the terminal, or GitHub. You've mostly used AI through a chat window, or not at all. | [Beginner track](#beginner-track) |
| **B. Experienced** | You use Claude Code or similar tools and you're comfortable with git and the terminal. | [Experienced track](#experienced-track) |

Not sure? Choose **Beginner**. It's easier to skip an explanation than to recover from a missing one.

Claude asks you this same question when you run `/start`. Your answer is saved in `profile/user.md` and sets how much Claude explains at every later step. You can change it any time by saying "switch to beginner mode" or "switch to experienced mode".

---

## The whole process at a glance

### One time: setup (one to three sittings)

| # | Step | When | Where | You do | Claude does | Time |
|---|------|------|-------|--------|-------------|------|
| 1 | Make your private copy | Before anything else | GitHub website | Click **Use this template**, choose **Private** | | 2 min |
| 2 | Put it on your computer | Once | GitHub Desktop or terminal | Clone the copy | | 5 min |
| 3 | Open it in Claude Code | Every session | Claude desktop app, terminal, or VS Code | Open the repo folder | Loads the pipeline | 1 min |
| 4 | `/start` | First session | Claude Code | Answer one question: beginner or experienced | Checks your tools and offers to install what's missing | 5-10 min |
| 5 | `/cv-master` | First session, after `/start` | Claude Code, plus your editor or Word | Bring your resume. Answer the interview. **Write and revise `cv/master.md` yourself** | Converts the format, interviews you, reviews your draft with questions | 1-3 hours over 1-2 sittings |
| 6 | `/setup` steps 1-5 | After the master CV. One step per sitting is fine | Claude Code; step 4 also needs Word, Google Docs, or LibreOffice | Answer questions, approve each file | Asks one question at a time, saves every answer, drafts the file | 15-30 min each |
| 7 | Save your work | End of every session | GitHub Desktop, terminal, or ask Claude | Commit and push | Can do it for you if you ask | 1 min |

### Every job you consider

| # | Step | When | Where | You do | Claude does | Time |
|---|------|------|-------|--------|-------------|------|
| 8 | `/score <link or pasted JD>` | When a job looks interesting | Claude Code; the CV review opens in your browser | Give the link or paste the description. Choose: tailor, tailor as a pivot, or stop | Saves the JD, scores fit, runs the screen check. **The first time, also sets your score anchor (setup step 6)** | 5-10 min |
| 9 | `/tailor <slug>` | When you decide to apply | Claude Code, then Word to check the file | Approve or reject each flagged change. Open the .docx and check it on the page | Rewords and reorders from your master CV, never adds claims; exports the .docx | 15-30 min |
| 10 | `/cover-letter <slug>` | If the job asks for one | Claude Code, then Word | Read it aloud. Does it sound like you? | Drafts in your voice from your samples | 10-20 min |
| 11 | **Submit** | When you're ready | The employer's site | **You submit.** Claude never submits or sends anything | | |
| 12 | `/release <slug>` | Right after you submit | Claude Code | Confirm which files you sent | Freezes a copy of what you submitted; updates the dashboard | 2 min |
| 13 | `/log <slug> <outcome>` | When you hear back, or after 3 weeks of silence | Claude Code | Say what happened | Records it; at a screen or later, offers interview prep | 2 min |

### Now and then

| Step | When | Where |
|------|------|-------|
| `/dashboard` | Whenever you want to see the pipeline | Claude Code; opens in your browser |
| `/ats-check <slug>` | After you edit a tailored CV by hand | Claude Code |
| `/cv-master` | Whenever a fact changes (new role, new result, corrected date) | Claude Code and your editor |
| `/calibrate` | After about 15 applications have an outcome | Claude Code |
| `/setup <step>` | When something about you changes (targets, level, voice) | Claude Code |

---

## Beginner track

### What you need

| Item | What it is | Get it |
|------|-----------|--------|
| GitHub account | Free website that stores your copy of this project | [github.com/signup](https://github.com/signup) |
| Claude plan that includes Claude Code | The AI assistant that runs the pipeline | [claude.com/claude-code](https://claude.com/claude-code) |
| Claude desktop app | Where you'll talk to Claude Code | Same page |
| GitHub Desktop | Copies your project to your computer and saves changes back, without the terminal | [desktop.github.com](https://desktop.github.com) |
| A way to open .docx files | To check your exported resume | Word, Google Docs, or LibreOffice |

You also need Python, pandoc, and python-docx. You don't have to install these yourself: in step 4, `/start` checks for them and offers to install anything missing.

### A few words you'll see

| Word | Meaning |
|------|---------|
| **Repo** (repository) | A project folder that GitHub keeps a history of. Your copy of this project is a repo. |
| **Clone** | Download a repo to your computer. |
| **Commit** and **push** | Save a snapshot of your changes, then upload it to GitHub. |
| **Markdown** (.md) | Plain text with light formatting: `#` for headings, `-` for bullets. Your master CV is a markdown file. |
| **Slash command** | A command you type in Claude Code that starts with `/`, like `/start`. |
| **Slug** | The short name the pipeline gives each job, like `acme-director-engineering`. |
| **JD** | Job description. |
| **ATS** | Applicant tracking system: the software that screens resumes before a person reads them. |

### Step by step

**1. Make your private copy.**
On this project's GitHub page, click the green **Use this template** button, then **Create a new repository**. Give it a name (for example `my-job-search`) and choose **Private**. It will hold your resume, contact details, and every job you apply to, so private matters.

**2. Put it on your computer.**
Open GitHub Desktop, sign in, choose **File → Clone repository**, pick your new repo, and note the folder it saves to.

**3. Open it in Claude Code.**
Open the Claude desktop app, start a Claude Code session, and select the folder from step 2. (Terminal users: `cd` into the folder and run `claude`. VS Code users: open the folder and open the Claude Code panel.)

**4. Type `/start` and press Enter.**
Answer **A** to the first question. Claude explains what's coming, then checks your tools. When it asks to install something, it tells you what and why; approve it if that matches.

> **About permission prompts.** Claude Code asks before it runs a command or changes a file. Read the prompt. If it matches what Claude just told you it was about to do, approve it. If it doesn't, decline and ask what it's for.

**5. Build your master CV: `/cv-master`.**
Have your current resume ready (a .docx, a PDF, or text you can paste).
- Claude converts it to the pipeline's format **without changing your words**.
- Then it interviews you, one question at a time, about each role: what you were responsible for, what changed because you were there, numbers you can stand behind. Every answer is saved in the `brainstorms/` folder as you go.
- **Then you revise `cv/master.md` yourself**, using those notes. Open it in any text editor (TextEdit or Notepad works; VS Code is nicer). Claude will show you where it is.
- Claude reviews your draft and asks questions about anything weak or vague. It doesn't rewrite your bullets. If you ask it to draft a line anyway, it marks that line so you remember to make it your own.

Take your time here. Everything later depends on this file.

**6. Run `/setup`, one step at a time.**
Each step is a short interview that ends with one file for you to approve:

| Step | About |
|------|-------|
| 1 Profile | The jobs you want, and what your career is really about |
| 2 Rubric | What counts as a strong fit for you |
| 3 Voice | How you write. Bring something you wrote yourself, like a cover letter or an email |
| 4 Export format | How your resume file should look. You'll open a test file and approve it |
| 5 Tracking and privacy | Keeping your copy private, and any jobs you've already applied to |

You can stop after any step. Next time, type `/setup` and it picks up where you left off.

**7. Save your work.**
In GitHub Desktop: write a short summary (for example "Finished setup step 2"), click **Commit to main**, then **Push origin**. Or type "commit and push my changes" to Claude.

**8. Score your first job: `/score`.**
Type `/score` followed by a link to the job posting, or paste the whole job description after it. If the job site needs a login (LinkedIn often does), copy the description text and paste it instead.

You'll get:
- a fit score from 0 to 100, with the five parts that make it up
- a "screen check": how an ATS, a recruiter skimming for 10 seconds, and a hiring manager reading closely would each see your CV
- a review page in your browser that highlights your CV
- a choice: tailor your CV for this job, or stop here

The first time, Claude also asks how good a fit *you* think the job is. That sets your **anchor**, so later scores mean something consistent.

> **The score is about fit, not your odds.** A high score means your background matches the job as written. It doesn't predict a call back; referrals and timing matter more. Use it to choose where to spend effort, and look for someone who can refer you.

**9 to 13. Apply and track.**
- `/tailor <slug>` makes a version of your CV for this job. Every change is flagged. Approve only changes you could explain in an interview.
- `/cover-letter <slug>` if the job asks for one.
- **You submit the application yourself.**
- `/release <slug>` right after you submit.
- `/log <slug> rejected` (or `recruiter_screen`, `hm_interview`, `offer`) when you hear back.

### Troubleshooting

| Problem | Fix |
|---------|-----|
| A command says it's "blocked" | A setup step isn't done yet. The message names it; run that step. |
| `/score` can't read the job link | Paste the job description text after `/score` instead. |
| The resume file looks wrong | Run `/setup 4` again and describe what's off. |
| You closed Claude mid-interview | Nothing is lost. Run the same command again; your answers are in `brainstorms/`. |
| You want less (or more) explanation | Say "switch to experienced mode" (or "beginner mode"). |
| Something else | Ask Claude: "What should I do next?" It can read this guide and your setup status. |

---

## Experienced track

```bash
gh repo create my-job-pipeline --private --template yottachem/job-pipeline --clone
cd my-job-pipeline
pip install -r requirements.txt    # python-docx; also needs pandoc and Python 3.10+
claude
```

Then, in Claude Code:

```
/start              # answer B
/cv-master          # import resume (format only), evidence interview, you edit cv/master.md
/setup              # steps 1-5; run 5 first if you'll push before finishing
/score <url|JD>     # ends with step 6 (anchor) on the first run
```

Notes:
- **Layout:** pipeline rules in `CLAUDE.md`; one skill per command in `.claude/skills/`; setup interviews in `.claude/skills/setup/steps/`. Personal context lives in `profile/`.
- **Gates:** every command runs `scripts/check_setup.py --for <command>`. A profile file is "done" when its `<!-- SETUP-STUB` first line is gone.
- **Scripts** are stdlib-only and usable without Claude: `ats_check.py`, `build_cv_review.py`, `export_docx.py` (needs pandoc and python-docx), `build_dashboard.py`, `check_setup.py --cv cv/master.md`.
- **Master CV format** is strict because the scripts parse it; see `templates/cv-master.md`. Lines marked `<!-- claude-drafted -->` are reported until you rewrite them or delete the marker.
- **Rubric:** weights, domain tiers, level band, hard gaps, and pivot threshold are in `profile/rubric.md`. Leave the weights alone until `/calibrate` has about 15 resolved rows.
- **CSV:** `applications.csv` has 12 columns (schema in `CLAUDE.md`). `/calibrate` uses the frozen `applications/.../analysis.md` scores, not the live analyses.
- **Public copy:** setup step 5 enables the personal-data block in `.gitignore`. Anything committed before that stays in history.
- **Dashboard:** a static `dashboard/index.html`. If your environment can publish artifacts, step 5 can record a URL to republish to.

---

## Related docs

| Doc | For |
|-----|-----|
| [Setup steps](setup-steps.md) | What each setup interview asks and why it can't ship pre-filled |
| [Pipeline](pipeline.md) | Each command in detail, the screen check, core vs. pivot |
| [Scoring](scoring.md) | The rubric, the gap rules, calibration |
| [Privacy](privacy.md) | Keeping your data private |
