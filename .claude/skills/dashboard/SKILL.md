---
name: dashboard
description: Rebuild the pipeline dashboard (dashboard/index.html) from applications.csv and open it. Runs automatically at the end of /release and /log. Use for /dashboard, "show my pipeline", "update the dashboard".
---

# Dashboard

Gate: `python3 scripts/check_setup.py --for dashboard`. Skip silently when
called from `/release` or `/log` if `profile/tracking.md` says the dashboard
is disabled.

1. Run `python3 scripts/build_dashboard.py`.
2. If called directly, open `dashboard/index.html` for the user (`open` on
   macOS, `xdg-open` on Linux).
3. If `profile/tracking.md` records a published artifact URL and this
   environment can publish artifacts, republish the file to that same URL.
   Never create a second published copy.
4. Report in one line: applications, resolved, screen rate, and the small-N
   caveat if fewer than 15 are resolved.

The dashboard reads `applications.csv` only. If a number looks wrong, fix the
CSV (through `/log`), not the HTML.
