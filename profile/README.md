# profile/

Your personal context. The pipeline logic in this repo is shared; these files
are what make it yours. Each one is written by a `/setup` step: a short
interview (grill-me) that captures your answers, then drafts the file for your
approval.

| File | Step | What it holds |
|------|------|---------------|
| `user.md` | Start (`/start`) | Beginner or experienced, and how Claude should explain things |
| `../cv/master.md` | 0 (`/cv-master`) | Your master CV. Strongly encouraged to be written by you. |
| `profile.md` | 1 | Targets, throughline, domains, proof points, claim rules |
| `rubric.md` | 2, 6 | Scoring weights, domain tiers, level band, hard gaps, anchor |
| `voice.md` | 3 | How your cover letters should sound |
| `voice-samples/` | 3 | Writing you did yourself, used as the voice reference |
| `export.md` | 4 | DOCX export command and format choices |
| `tracking.md` | 5 | Repo privacy, source vocabulary, dashboard |
| `reference.docx` | 4, optional | Your resume's styles, for the exporter |

A file whose first line is `<!-- SETUP-STUB ... -->` is not set up yet.
Check status any time with `python3 scripts/check_setup.py`.

You can edit any of these by hand. Rerun `/setup <step>` to redo one with
an interview.
