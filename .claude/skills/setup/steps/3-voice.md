# Step 3: Voice

**Writes:** `profile/voice.md` (and saves samples in `profile/voice-samples/`)
**Why it's only partly shareable:** the method for keeping drafts honest is
shared (below); what the user sounds like is not.
**Reads first:** `cv/master.md` (the Summary is the user's own prose, if they
wrote it).

## Start with a sample the user wrote

Ask for one to three pieces of writing the user wrote themselves: a cover
letter, a professional email, a LinkedIn post. Strongly encourage their own
writing over anything AI-assisted; a voice reference written by a model
teaches the model to sound like a model. Save each to
`profile/voice-samples/` as `.md` or the original file.

If they have nothing, the master CV Summary is the fallback sample. Note
that in the file.

## Interview branches (in order)

1. **What you notice.** Show three or four observations from the samples
   (average sentence length, first person or not, how they open, how they
   name a weakness) and ask which are deliberate.
2. **Hard rules.** Punctuation (em dashes, semicolons, exclamation points),
   words or phrases they never use, contractions, formality.
3. **Naming gaps.** How they want an honest gap handled in a letter (name it
   directly with evidence, or leave it for the interview).
4. **What a letter is about.** Shared default: every paragraph is about the
   user and their fit; never describe the company back to itself. Confirm or
   adjust.
5. **Letter header and sign-off.** Name, contact lines, and closing exactly
   as they want them on every cover letter.

## Shared method (always included in the output)

- One idea per sentence. Split run-ons before export.
- Let accomplishments carry the weight; don't editorialize around them.
- No generic executive language ("results-driven leader", "passionate").
- Reread every draft against the samples before showing it.

## Output format

```markdown
# Voice

## Samples
- profile/voice-samples/<file>: <what it is, who wrote it>

## Observed and confirmed
- ...

## Hard rules
- ...

## Naming gaps
...

## Letter header
<exact lines>

## Sign-off
...

## Shared method
<the four bullets above>
```

**Done when:** the user approves the file. Recommend testing it with
`/cover-letter` on the first real application and refining from there.
