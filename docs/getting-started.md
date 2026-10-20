# Getting started

> **Your master CV is the foundation. Write it yourself.**
> Everything in this pipeline compares against `cv/master.md`. You are strongly encouraged to draft it in your own words. Claude helps with format, asks questions that surface missing evidence, and reviews, but doesn't write your bullets unless you insist.

## What you need

| Requirement | Why | Install |
|-------------|-----|---------|
| Claude Code | Runs the pipeline | [claude.com/claude-code](https://claude.com/claude-code) |
| Python 3.10+ | Helper scripts | Usually preinstalled; `python3 --version` |
| pandoc | Markdown to .docx | [pandoc.org/installing.html](https://pandoc.org/installing.html) |
| python-docx | .docx layout fixes | `pip install -r requirements.txt` |
| git and a GitHub account | Your private copy | [github.com](https://github.com) |
| Word or LibreOffice (optional) | PDF export, checking the rendered page | |

## 1. Make your own private copy

1. On this repo's GitHub page, click **Use this template → Create a new repository**.
2. Set it to **Private**. Your copy will hold your CV, contact details, job history, and interview notes.
3. Clone it:
   ```
   git clone https://github.com/<you>/<your-repo>.git
   cd <your-repo>
   pip install -r requirements.txt
   ```
4. Check the setup status:
   ```
   python3 scripts/check_setup.py
   ```
   Every step shows `pending`. That's expected.

## 2. Step 0: your master CV

Open Claude Code in the repo folder and run `/cv-master`.

You'll choose a starting point:
- **Import** your current resume (.docx, .pdf, or pasted text). Claude converts the *format* only; your wording stays as is.
- **Write from scratch** in `templates/cv-master.md`, copied to `cv/master.md`.
- **Already done**, if you wrote `cv/master.md` yourself.

Then Claude interviews you role by role: scope, what changed because you were there, numbers you can stand behind, work that isn't on the page yet. Every answer is saved to `brainstorms/` as you go. **You** then revise `cv/master.md` with that material. Claude reviews the result and asks questions; it doesn't rewrite.

The master CV is a superset. Put every true, relevant fact in it, even if it runs longer than a resume you'd submit. Tailoring selects from it.

`examples/sample-master.md` shows the format with a fictional person. Don't copy its content.

## 3. Steps 1-5: setup interviews

Run `/setup`. Each step is a short interview that ends with one file in `profile/` for you to approve. You can stop after any step; `/setup` picks up at the next pending one.

Do step 5 (tracking and privacy) first if you plan to commit and push before finishing setup.

See [setup-steps.md](setup-steps.md) for what each step asks.

## 4. Your first job

Find a job you're considering and run:
```
/score https://company.example/careers/some-role
```
or paste the job description after `/score`.

You'll get a scored analysis in `analyses/`, a screen check (ATS, recruiter skim, hiring manager read), a visual CV review in your browser, and a decision: tailor, tailor as a pivot, or stop. The first run ends with step 6, which sets your score anchor.

## 5. Keep it current

| When | Run |
|------|-----|
| You submit an application | `/release <slug>` |
| You hear back, or don't | `/log <slug> <outcome>` |
| A fact on your CV changes | `/cv-master` (you edit, Claude reviews) |
| About 15 applications have resolved | `/calibrate` |

Commit often. Your history of scores, tailored CVs, and outcomes is the data `/calibrate` learns from.
