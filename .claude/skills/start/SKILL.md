---
name: start
description: First thing a new user runs. Asks one question (beginner or experienced with AI tools like Claude Code), records the answer in profile/user.md so every later step explains things at the right level, orients the user, and hands off to /cv-master. Use for /start, "how do I begin", "I'm new", "switch to beginner mode", "switch to experienced mode", or whenever profile/user.md is still a stub.
---

# Start

## 1. The question (always first)

If `profile/user.md` still begins with `<!-- SETUP-STUB`, ask this before
anything else, as one question with two choices:

> Before we begin: how familiar are you with AI tools like Claude Code?
>
> **A. Beginner.** I'm new to Claude Code, the terminal, or GitHub, or I've
> mostly used AI through a chat window. Walk me through each step.
>
> **B. Experienced.** I use Claude Code or similar tools and I'm comfortable
> with git and the terminal. Keep it brief.

If the answer is unclear ("somewhere in between"), choose beginner. It's
easier to skip an explanation than to recover from a missing one. The user can
switch any time by saying "switch to beginner mode" or "switch to experienced
mode"; rerun this skill to rewrite the file.

## 2. Record it

Write `profile/user.md` without the stub line:

```markdown
# About you

- Experience: beginner | experienced
- Answered: YYYY-MM-DD
- Name to use: <optional, ask only if beginner>

## How Claude works with you
<copy the matching block below>
```

**Beginner block:**
- Before each command or step, say in plain words what it will do, which
  files it will create or change, and roughly how long it takes.
- One action at a time. Wait for the user's OK before the next one.
- Explain any term the first time it comes up, in one line (repo, commit,
  markdown, slug, ATS).
- Before a permission prompt appears, say what Claude is asking to do and
  why it's needed.
- After writing a file, say where it is and how to open it.
- Offer to save progress to git (commit) at the end of each session, and
  say what that means.
- End every session with what comes next and the exact command to type.
- Point to the matching section of `docs/user-guide.md` (Beginner track).

**Experienced block:**
- Be brief. Don't explain git, markdown, the terminal, or slash commands.
- Batch related actions; stop only at decisions the user has to make.
- Refer to files by path. Don't narrate routine tool use.
- The user commits and pushes; don't offer unless asked.
- Point to `docs/user-guide.md` (Experienced track) only when asked.

## 3. Orient

- **Beginner:** explain in four or five short lines what the pipeline does,
  that setup takes one to three sittings, that nothing is lost between
  sessions, and that Claude will never send or submit anything on their
  behalf. Then check the tools: run `python3 --version`, `pandoc --version`,
  and `python3 -c "import docx"`. For anything missing, explain what it is
  and offer to install it, with the user's OK on each install.
- **Experienced:** one line on the flow (`/cv-master` → `/setup` → `/score`)
  and the same tool check, reported as a single list.

Both: say that the master CV comes first and that they are strongly
encouraged to write it themselves (Claude formats, interviews, and reviews,
but doesn't write their bullets).

## 4. Hand off

Run `python3 scripts/check_setup.py` and show the result. Then offer to start
`/cv-master` now.
