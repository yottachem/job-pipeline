# Privacy

> **Your master CV is the foundation. Write it yourself.**
> It is also the most personal file in the repo, next to your application history. Keep your copy private.

## What your copy will contain

| Path | Contains |
|------|----------|
| `cv/` | Your master CV, tailored CVs, contact details |
| `profile/` | Targets, deal-breakers, objections you hear, writing samples |
| `brainstorms/` | Interview notes from setup and interview prep, in your words |
| `jds/`, `analyses/`, `cover-letters/` | Every job you considered and how you assessed it |
| `applications/`, `applications.csv`, `outcomes.md` | What you submitted, where, and what happened |
| `calibration/`, `dashboard/index.html` | Your conversion rates |

## Recommended: a private repo

When you click **Use this template**, choose **Private**. Then commit everything. Your history of scores and outcomes is what `/calibrate` learns from.

Check your visibility any time:
```
gh repo view --json visibility
```

## If your copy must be public

Setup step 5 handles this. It uncomments the personal-data block in `.gitignore` so those paths are never committed, and confirms with `git status`.

If personal files were committed **before** the block was switched on, they stay in git history even after you delete them. Your options:
- make the repo private, or
- rewrite history (for example with `git filter-repo`), then force-push, or
- delete the repo and start a fresh copy.

## What Claude does and doesn't do

- Claude reads and writes files in your repo folder.
- Claude fetches job postings from URLs you give it.
- Claude **never** submits applications, sends emails, or posts anything. Every outward step is yours.

Your data is handled under the terms of the Claude plan you use with Claude Code.
