# cv/

> **Your master CV is the foundation. Write it yourself.**
> `cv/master.md` is compared against by every score, screen check, tailored CV, and cover letter, and nothing is ever added that isn't in it. You are strongly encouraged to draft it in your own words. Run `/cv-master` to import your current resume (format only), get interviewed for missing evidence, and have your draft reviewed.

| File | What | Written by |
|------|------|------------|
| `master.md` | Your master CV: every true, relevant fact | You (step 0, `/cv-master`) |
| `master-<track>.md` | Optional whole-field rewrite for a pivot track | `/tailor`, on your go-ahead |
| `<slug>.md` | Tailored CV for one role | `/tailor` |

Format: see `templates/cv-master.md`. Check it with `python3 scripts/check_setup.py --cv cv/master.md`.

Lines ending in `<!-- claude-drafted -->` were written by Claude at your request. Rewrite them, or delete the marker once you've read the line and stand behind it.
