# Step 6: Score anchor

**Writes:** the `## Anchor` section of `profile/rubric.md` (replacing the
`<!-- ANCHOR-PENDING ... -->` line), and possibly revised definitions
elsewhere in that file.
**Why it can't ship pre-filled:** an anchor is a real role the user has
scored and judged. It is what keeps score 70 meaning the same thing in month
three as in week one.
**When:** automatically at the end of the first `/score` run (the score skill
detects the pending marker). Can be rerun with `/setup 6` against any scored
role.

## Interview branches (in order)

1. **Gut check.** Show the five sub-scores and the total. Before explaining
   them, ask: "Without looking at the math, how good a fit is this role,
   0-100?" Record the answer.
2. **Disagreement by dimension.** If the gut number and the total differ by
   more than about 10 points, go dimension by dimension: which sub-score
   feels wrong, and why?
3. **Fix the definition, not the number.** For each disagreement, decide
   whether the rubric definition is wrong (edit the tier, level band, or
   hard-gap list in `rubric.md`) or the gut is reacting to something the
   rubric deliberately excludes (referral, company brand, compensation).
   Excluded factors stay excluded; note them in the analysis's external
   factors section.
4. **Rescore if definitions changed.** Rerun scoring for this role against
   the edited rubric and show the new total.
5. **Lock the anchor.** Record the role, the final score, and one line on
   why it's a good reference point (a typical target, not an outlier).

## Output format

```markdown
## Anchor
- Role: <slug> (<Company>, <Role>)
- Score: <n>/100, set <YYYY-MM-DD>
- Why it's a good reference: ...
- Definition changes made while anchoring: ...
```

**Done when:** the anchor is recorded and the user agrees future scores
should be read relative to it. If the first role scored is an outlier (a
long shot or a perfect fit), say so and recommend anchoring on the next
typical one instead; leave the marker in place until then.
