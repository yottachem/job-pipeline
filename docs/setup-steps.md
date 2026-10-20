# Setup steps

> **Your master CV is the foundation. Write it yourself.**
> Step 0 comes before everything else, and every later step reads your master CV to suggest answers. You are strongly encouraged to draft it in your own words; the rest of setup is only as good as what it reads.

The pipeline logic in this repo is shared. Some pieces can't be: what you're targeting, what counts as your core domain, how you write, what your resume looks like. Each of those is one setup step, run as a **grill-me interview**:

- Claude asks **one question at a time** and offers a recommended answer drawn from your master CV and earlier steps, so most questions are confirm-or-correct.
- Every answer is saved to `brainstorms/<date>-setup-<step>.md` immediately, so you can stop at any point and lose nothing.
- At the end, Claude drafts one file for your approval. The step counts as done only when you approve it.

Check status any time: `python3 scripts/check_setup.py`.

**Before step 0: `/start`.** One question: are you a beginner or experienced with AI tools like Claude Code? Your answer is saved in `profile/user.md`. Beginners get each step explained before it starts (what it's for, how long, what file it produces) and one action at a time; experienced users get brief directions. Say "switch to beginner mode" or "switch to experienced mode" any time. The [user guide](user-guide.md) has both tracks.

## Summary

| Step | Writes | Blocks until done | Why it can't ship pre-filled |
|------|--------|-------------------|------------------------------|
| Start | `profile/user.md` | Every command | How much to explain depends on you |
| 0 Master CV | `cv/master.md` | Everything | It's your career, in your words |
| 1 Profile | `profile/profile.md` | `/score` | Targets, throughline, and proof points are yours |
| 2 Rubric | `profile/rubric.md` | `/score` | "Core domain" and "right level" differ for everyone |
| 3 Voice | `profile/voice.md` | `/cover-letter` | Only partly shareable: the method is shared, your voice isn't |
| 4 Export format | `profile/export.md` | Exporting `/tailor` and `/cover-letter` output (recommended) | Your resume's look is yours |
| 5 Tracking and privacy | `profile/tracking.md` | `/release`, `/log`, `/dashboard` | Visibility, sources, and history are personal |
| 6 Score anchor | Anchor in `profile/rubric.md` | Runs at the end of your first `/score` | An anchor is a real role you judged |

---

## Step 0: Master CV (`/cv-master`)

**You write this one.** Claude's role is limited on purpose:

| Claude does | Claude doesn't |
|-------------|----------------|
| Converts your existing resume into the pipeline's format, without changing your wording | Reword your bullets during import |
| Interviews you role by role for scope, outcomes, and numbers | Fill gaps with plausible-sounding claims |
| Reviews your draft and asks questions about weak, vague, or unsupported bullets | Replace your bullets with its own |
| Drafts lines only if you insist, marking each `<!-- claude-drafted -->` | Hide which lines it wrote |

`check_setup.py` keeps listing Claude-drafted lines until you rewrite them or delete the marker yourself.

**Done when:** the format check passes and you confirm the content is yours and true.

## Step 1: Profile

Asks about: target titles and industries, deal-breakers, your **career throughline** (one sentence, in your words: the kind of problem you keep solving), hands-on vs. adjacent domains, 3-5 proof points, the credential a recruiter should see first, claims to avoid or word carefully, and objections you already hear.

**Why it matters:** the throughline is what narrative fit (D4) is scored against. The credential and objections feed the recruiter and hiring manager passes in every screen check.

## Step 2: Rubric

Asks about: whether to keep the default weights (recommended until you have data), which domains are core / adjacent / outside **for you**, your current and target level and how far down or up you'd go, examples of roles whose central problem fits you, which hard gaps apply (work authorization, clearance, license, degree, relocation), and any adjacent fields you're pivoting toward.

**Why it matters:** without this, domain match, seniority, and gap severity would be scored against someone else's career.

## Step 3: Voice

Starts by asking for one to three things **you wrote yourself**: a cover letter, an email, a post. Strongly prefer your own writing; a voice reference written by AI teaches the AI to sound like AI. Then asks which patterns in your writing are deliberate, your punctuation and phrasing rules, how to handle naming a gap, and your exact letter header and sign-off.

**Partly shareable:** the method (one idea per sentence, evidence over adjectives, no describing the company back to itself) ships with the repo. Your voice doesn't.

## Step 4: Export format

Asks about: a reference .docx whose styles to reuse, font and size, right-aligned dates, a rule under the contact block, header style, page length, file naming, and PDF. Ends with a test export of your master CV that you open and approve.

**Check the rendered page, not the file.** Spacing and indentation problems only show up on the page.

## Step 5: Tracking and privacy

Asks about: whether your copy is private (recommended) or public. If public, it switches on the `.gitignore` block that keeps your personal files out of git. It also asks which application sources you use, whether to backfill applications you've already sent, whether you want the dashboard, and which job boards need copy-paste because they sit behind a login.

**Why source matters:** referrals often convert better than direct applications, regardless of fit. `/calibrate` can only show you that if every application records its source.

## Step 6: Score anchor

Runs at the end of your first `/score`. Before showing the math, Claude asks: "How good a fit is this role, 0-100?" If your number and the score differ by more than about 10, you go dimension by dimension. The fix goes into the **definitions** in `rubric.md`, not the one number, and the role is rescored. Then that role becomes your anchor: the reference point that keeps a 70 meaning the same thing in month three as in week one.

If your first role is an outlier (a long shot or a perfect fit), anchor on the next typical one instead.
