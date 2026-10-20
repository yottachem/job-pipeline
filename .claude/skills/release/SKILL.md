---
name: release
description: Freeze what was actually submitted for one role into a permanent case file, stamp the application date, and refresh the dashboard. Use for /release <slug>, "I submitted the application for X", or "archive this application".
---

# Release

Gate: `python3 scripts/check_setup.py --for release`.

A release is a one-time snapshot of what was submitted. It locks the score
and conversion hypothesis as they stood at decision time, so `/calibrate`
grades the prediction that actually existed, not a later revision.

## Steps
1. If `applications/<company-slug>/<role-slug>/` already exists, stop and
   ask before doing anything. Releases are not syncs.
2. Confirm with the user which files they actually submitted (tailored CV
   docx? master? cover letter or not?).
3. Create the folder and copy:

   ```
   applications/<company-slug>/<role-slug>/
   ├── jd.md              # from jds/<slug>.md
   ├── analysis.md        # from analyses/<slug>.md
   ├── cv.docx            # the exact file submitted
   ├── cover-letter.docx  # if one was submitted
   └── interviews/        # created empty; filled by /log later
   ```
4. In `applications.csv`, set `date_applied` to today if blank (ask if the
   user submitted on a different date). Real CSV parser, 12 fields.
5. Refresh the dashboard (`dashboard` skill).
6. Tell the user what was frozen, in one short list.

Never edit files in `applications/` after release.
