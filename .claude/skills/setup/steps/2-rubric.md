# Step 2: Rubric

**Writes:** `profile/rubric.md`
**Why it can't ship pre-filled:** the rubric's structure is shared (see
`CLAUDE.md`), but what counts as a core domain, the right level, and a hard
gap is different for every person. Without this file, D1, D3, and D5 would
be scored against someone else's career.
**Reads first:** `cv/master.md`, `profile/profile.md`.

## Interview branches (in order)

1. **Weights.** Show the default weights and what each dimension measures.
   Recommend keeping the defaults until `/calibrate` has about 15 resolved
   applications to argue from. Change them only if the user has a specific
   reason (for example, a career switcher may want D1 lower and D4 higher).
   Weights must sum to 100.
2. **D1 domain tiers.** Turn `profile.md` domains into three tiers with score
   ranges:
   - Core (80-100): hands-on, recent, central to the throughline.
   - Adjacent (50-79): supervised, older, or neighboring.
   - Outside (0-49): everything else.
   Recommend the tiers; ask the user to move items between them.
3. **D3 level band.** Current level, target level, and the edges: what reads
   as under-leveled (a step down they'd still consider?) and what is a reach
   beyond demonstrated scope (team size, budget, title). Ask whether a step
   down is acceptable and how much.
4. **D4 central problems.** Two or three examples of a role's "central
   problem" that would map cleanly to their throughline, and one that would
   need a stretch. These calibrate narrative-fit judgments.
5. **D5 hard gaps.** Go through the universal list (work authorization,
   security clearance, professional license, required degree field,
   regulated domain experience, relocation, travel) and mark which apply.
   Add any of their own.
6. **Pivot threshold and tracks.** Default: a role is `pivot` when D1 or D4
   is below 60. Ask about adjacent fields they are deliberately pursuing;
   give each a short reusable track slug.

## Output format

```markdown
# Rubric

## Weights
| Dimension | Weight |
|-----------|--------|
| D1 Domain match | 30 |
| D2 Requirement coverage | 25 |
| D3 Seniority and scope | 20 |
| D4 Narrative fit | 15 |
| D5 Gap severity (inverted) | 10 |

Reason for any change from defaults: ...

## D1 domain tiers
- Core (80-100): ...
- Adjacent (50-79): ...
- Outside (0-49): everything else

## D3 level band
- Current: ...  ·  Target: ...
- Under-leveled when: ...  ·  Acceptable step down: ...
- Reach when: ...

## D4 central problems
- Clean fit: ...
- Stretch: ...

## D5 hard gaps
| Gap | Applies to me? | Notes |

## Pivot
- Threshold: 60
- Tracks: `<slug>`: <field, why>

## Anchor
<!-- ANCHOR-PENDING: set by step 6 at the end of the first /score -->
```

**Done when:** the user approves the file and the weights sum to 100. The
anchor stays pending; that is expected.
