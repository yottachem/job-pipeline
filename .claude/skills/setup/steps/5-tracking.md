# Step 5: Tracking and privacy

**Writes:** `profile/tracking.md`, and edits `.gitignore` if the repo is
public.
**Why it can't ship pre-filled:** where the user's data lives, who can see
it, and what they already applied to are personal decisions.
**Reads first:** `.gitignore`, `applications.csv`.

## Interview branches (in order)

1. **Repo visibility.** Is their copy of this repo private or public?
   Recommend private: the repo will hold their CV, contact details,
   application history, and interview notes. Check with
   `gh repo view --json visibility` if `gh` is available.
   - **Private:** commit everything; history is useful.
   - **Public:** uncomment the personal-data block in `.gitignore`, then run
     `git status` to confirm `cv/`, `profile/`, `brainstorms/`, `jds/`,
     `analyses/`, `cover-letters/`, `applications/`, `applications.csv`,
     `outcomes.md`, `calibration/`, and `dashboard/index.html` are no longer
     tracked. If any were committed already, warn that they remain in git
     history and explain the options (make the repo private, or rewrite
     history).
2. **Sources.** The default source vocabulary is `direct`, `referral`,
   `recruiter`, `agency`, `network`. Ask whether they need others. Source is
   recorded on every application because it often predicts a screen better
   than fit does; `/calibrate` splits by it.
3. **Backfill.** Have they already applied to roles they want tracked? For
   each: company, role, date, source, outcome so far, and the JD if they
   still have it. Add rows to `applications.csv` (real CSV parser, 12
   fields). Offer `/score` on any with a JD; scored-after-the-fact roles are
   marked in the analysis frontmatter as `backfilled: true` and excluded from
   calibration's prediction checks (the hypothesis wasn't made in advance).
4. **Dashboard.** Do they want the pipeline dashboard? It is a local HTML
   file (`dashboard/index.html`) rebuilt by `/dashboard`, `/release`, and
   `/log`. If their Claude environment can publish artifacts, ask whether to
   publish it there too, and record the URL.
5. **Outcome ladder.** Confirm the default ladder in `CLAUDE.md`, or add
   off-ladder states they need.
6. **JD sources.** Where do they find jobs? Note boards that need a login
   (Claude can't fetch those; paste the JD text instead).

## Output format

```markdown
# Tracking

## Privacy
- Repo visibility: private / public
- .gitignore personal-data block: active / inactive

## Sources
direct, referral, recruiter, agency, network, ...

## Backfill
- <n> rows added on <date>; <n> scored after the fact (backfilled: true)

## Dashboard
- Enabled: yes / no
- Published URL: ...

## Outcome ladder additions
- ...

## JD sources
- <board>: fetchable / paste
```

**Done when:** the user approves the file and, for a public repo,
`git status` confirms personal paths are ignored.
