---
name: grill-me
description: Interview the user one question at a time, checkpointing every answer to a capture file in brainstorms/ so nothing is lost. Used by /cv-master and every /setup step; also use when the user says "grill me", wants to stress-test a plan, or wants interview prep extracted into a doc.
---

# Grill Me

Interview the user about every branch of the topic until you reach shared
understanding. The real goal is to **extract what is in their head into a
durable markdown file**, in their words, so nothing is lost as context fills.

## Setup (before the first question)

1. Create the capture file at `brainstorms/{YYYY-MM-DD}-{topic-slug}.md` (get
   the date with `date +%F`). Setup steps use `setup-<step-name>` as the
   topic slug, for example `brainstorms/2026-11-02-setup-profile.md`.
2. Write a header immediately: title, date, the goal of the session, and an
   empty "Open flags" section.
3. Tell the user where you are saving, in one line. Then ask Q1.

## The checkpoint rule (non-negotiable)

After every answer, before the next question:
- Append an entry to the capture file: the question topic, the key facts and
  decisions from the answer (in their words where wording matters), and any
  flags (things they couldn't answer).
- Correct earlier entries if a later answer changes them.
- Only then ask the next question.

Never batch several answers into one write.

## Interview method

- Ask **one question at a time**. Offer a **recommended answer** drawn from
  what you already know (their master CV, earlier answers) so they can
  confirm, correct, or redirect. For anything that will end up in their CV or
  a cover letter, ask for their own words rather than offering yours.
- Settle upstream decisions before the ones that depend on them.
- If a file in the repo answers the question, read it instead of asking.
- When the user can't answer, record a flag and move on.
- Continue until the user says stop or every branch is covered. Near the
  end, ask: "Anything we haven't touched?"

## Capture file structure

```
# {Topic}: Interview Notes
Date: {date} · Goal: {one line}

## Summary / key decisions
(running synthesis, updated as you go)

## Q&A log
### Q1: {topic}
- Asked: {question}
- Captured: {facts and decisions, in their words where it matters}
- Flags: {open item}

## Open flags
- {item}
```

## At the end

- Reread the capture file for contradictions or gaps and reconcile them.
- Give a short recap: what was captured, what is still flagged, and the next
  step.
- The capture file holds personal information. If `profile/tracking.md` says
  the repo is public, `brainstorms/` must be in `.gitignore`.
