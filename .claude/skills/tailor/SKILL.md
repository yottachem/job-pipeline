---
name: tailor
description: Tailor the CV for one role from the screen check's work items, without inventing claims or restructuring the resume, then recheck and export. Use for /tailor <slug>, /tailor <slug> pivot, "tailor my CV for X", or to build a pivot-track master CV.
---

# Tailor

Gate: `python3 scripts/check_setup.py --for tailor`. If the analysis has no
`screen_check:` date, run the `ats-check` skill first and show the result.

## Rules (both modes)
- **No invented claims.** Every fact must already be in `cv/master.md` (or
  the track master). If the user wants to add a fact, it goes into
  `cv/master.md` first, through `/cv-master`.
- **Same shape.** Never split one bullet into two, merge two into one, or
  convert the Summary between prose and bullets. Tailoring rewords, reorders
  within a role, and re-emphasizes. The result should read as the same
  resume, reworded.
- Respect `profile.md` claim rules and `voice.md` hard rules.
- **Work from the screen check's list.** Every recruiter-pass "fix", weakly
  positioned proof bullet, and unanswered objection is either addressed by a
  specific change or marked "not addressable on the CV" (routed to the cover
  letter or interview prep).
- **Flag every change** inline for the user's confirmation:
  `*Flag: <what changed> (resolves: <screen-check item>)*` on its own line
  after the changed bullet. Flags are stripped at export.

## Core mode (`/tailor <slug>`)
Generate `cv/<slug>.md` from the CV in play: reorder bullets within roles,
reword to the JD's vocabulary where the underlying fact is identical, sharpen
the Summary's positioning line toward the role.

## Pivot mode (`/tailor <slug> pivot`)
Same rules, with a wider reframing allowance:
- Rewrite the Summary around the bridge line, still one prose paragraph of
  similar length, leading with the transferable capability in the target
  field's vocabulary.
- Apply the translation map throughout wherever the fact is identical.
- Move de-emphasized bullets to the bottom of their role. Never delete them;
  a deletion is a structural change for the user to decide.
- Reorder the Skills section so the target field's skills lead.
- Reword role subtitles to name target-relevant context when factually true.
- The finished CV should make the transition objection unnecessary to ask.

## Track masters
`cv/master-<track>.md` is a pivot-mode rewrite of `cv/master.md` for a
whole destination field, the starting point for every role in that track.
Create one only on the user's go-ahead, by pivot-mode tailoring against the
common requirements across that track's analyses (not one JD). Its header
comment lists the analyses it was built from. `cv/master.md` remains the
source of truth for facts.

## Recheck and export
1. Rerun the ATS script and the recruiter pass against `cv/<slug>.md`;
   append a dated `### Recheck (tailored CV)` under each section showing what
   moved. Call out anything still marked "fix".
2. Walk the user through the flags. Once they approve, remove the approved
   flags (or leave them; the exporter strips them).
3. Export with the command in `profile/export.md`. If step 4 isn't done,
   offer `/setup 4` first.
4. Ask the user to open the exported file and check it on the page.
