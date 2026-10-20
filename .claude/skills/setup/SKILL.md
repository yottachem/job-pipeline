---
name: setup
description: One-time startup for a fresh copy of the repo. Runs steps 1-6, each a grill-me interview that captures the personal pieces the template can't ship with (profile, rubric, voice, export format, tracking and privacy, score anchor) and writes them to profile/. Requires step 0 (/cv-master) first. Use for /setup, "/setup <step>", "set up the pipeline", "redo my rubric", or when check_setup.py reports a step incomplete.
---

# Setup (Steps 1-6)

The pipeline logic is shared; the parts that make it yours are not. Each
step below fills one of those parts by interviewing the user with the
`grill-me` method, then writing one file in `profile/`.

## Order and gates

| Step | Name | Writes | Required before | Instructions |
|------|------|--------|-----------------|--------------|
| 0 | Master CV | `cv/master.md` | everything | `/cv-master` skill |
| 1 | Profile | `profile/profile.md` | `/score` | `steps/1-profile.md` |
| 2 | Rubric | `profile/rubric.md` | `/score` | `steps/2-rubric.md` |
| 3 | Voice | `profile/voice.md` | `/cover-letter` | `steps/3-voice.md` |
| 4 | Export format | `profile/export.md` | `/tailor` export, `/cover-letter` export | `steps/4-export.md` |
| 5 | Tracking and privacy | `profile/tracking.md` | `/release`, `/log`, `/dashboard`, first commit of personal data | `steps/5-tracking.md` |
| 6 | Score anchor | anchor section of `profile/rubric.md` | runs at the end of the first `/score` | `steps/6-anchor.md` |

Step 5 asks about repo privacy. If the user plans to commit personal data
before reaching step 5, run step 5 first.

## Running

1. Run `python3 scripts/check_setup.py`. It lists every step as done or
   pending.
2. If step 0 is pending, stop and run `/cv-master`. Every later step reads
   the master CV for its recommended answers, so it has to exist first.
   Remind the user that the master CV is strongly encouraged to be written by
   them.
3. `/setup` with no argument: run the first pending step. `/setup <n>` or
   `/setup <name>`: run that step, even if done (a redo overwrites the
   profile file after showing the user a diff).
4. For the chosen step, read its file in `steps/` and follow it:
   - Run the interview using the `grill-me` skill's method and checkpoint
     rule, with capture file `brainstorms/<date>-setup-<name>.md`.
   - Offer a recommended answer for each question, drawn from
     `cv/master.md` and earlier profile files, unless the step says to ask
     for the user's own words.
   - Draft the profile file from the capture file, show it, and apply the
     user's corrections.
   - When the user approves it, remove the `<!-- SETUP-STUB ... -->` line at
     the top of the file. That line is how `check_setup.py` knows the step
     is done.
5. Rerun `check_setup.py`, report the result in one line, and offer the next
   pending step.

## Rules

- One step per session is fine. Capture files make it safe to stop anywhere.
- Never mark a step done without the user's approval of the written file.
- Don't fill a profile file from guesses to get past the gate. A pending
  step is better than a wrong profile; every score depends on these files.
