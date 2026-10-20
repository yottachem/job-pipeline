# Step 1: Profile

**Writes:** `profile/profile.md`
**Why it can't ship pre-filled:** the targets, throughline, and proof points
are the user's. Scoring D1, D3, and D4, and the recruiter pass in every
screen check, read this file.
**Reads first:** `cv/master.md`, `brainstorms/*-cv-master.md` if present.

## Interview branches (in order)

1. **Targets.** Titles and functions they are pursuing (rank them), industries,
   locations and remote preference, company stage and size. Recommend from
   the master CV's recent roles; let them correct.
2. **Deal-breakers.** Anything that rules a role out regardless of fit
   (relocation, travel, compensation floor, on-site days, sector). These are
   recorded, not scored; `/score` notes them at the top of the analysis.
3. **Throughline.** One sentence: the kind of problem their career keeps
   solving. Propose one from the master CV, then ask them to rewrite it in
   their words. D4 scores against this sentence, so it matters more than any
   other line in the file.
4. **Domains.** Hands-on domains (did the work) vs. supervised or adjacent
   domains (directed or worked alongside). Step 2 turns these into scoring
   tiers.
5. **Proof points.** Three to five results that best prove the throughline,
   each tied to a role in the master CV. If one isn't in the master CV, flag
   it and send them back to `/cv-master` to add it.
6. **Credential to surface.** The degree, license, clearance, or
   certification a recruiter should see in the first skim (or "none").
7. **Claim rules.** Anything that must never be claimed or must be worded
   carefully: confidential employers or products, NDA limits, titles that
   were acting or interim, shared credit, technical descriptions that are
   easy to get wrong. Ask for exact wording where it matters.
8. **Known objections.** What do interviewers or recruiters already push
   back on (employment gap, short tenure, overqualified, industry switch)?
   And what is the honest answer?

## Output format

```markdown
# Profile

## Targets
| Rank | Title / function | Industries | Notes |

Locations: ...  ·  Remote: ...  ·  Stage/size: ...

## Deal-breakers
- ...

## Throughline
<one sentence, user's words>

## Domains
- Hands-on: ...
- Supervised / adjacent: ...

## Proof points
1. <result>: <role in master CV>

## Credential to surface
...

## Claim rules
- Never claim: ...
- Word carefully: ... → use "<exact wording>"

## Known objections
| Objection | Honest answer | Evidence in master CV |
```

**Done when:** the user approves the file and the throughline is in their
own words.
