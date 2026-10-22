#!/usr/bin/env python3
"""
check_setup.py: setup status, command gates, and master CV format check.

Stdlib only. Every pipeline skill runs this first (CLAUDE.md ground rule 3).

Usage (from the repo root):
    python3 scripts/check_setup.py                 # status of /start and setup steps 0-6
    python3 scripts/check_setup.py --for score     # exit 1 if score's steps are pending
    python3 scripts/check_setup.py --cv cv/master.md   # format + content check

A profile file counts as set up once its first-line
"<!-- SETUP-STUB ... -->" marker is gone (/setup removes it on approval).
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from ats_check import (  # noqa: E402
    check_bullets, find_bullets, impact_stats, check_structure, strip_html_comments,
)

STUB = "<!-- SETUP-STUB"
ANCHOR_PENDING = "<!-- ANCHOR-PENDING"
DRAFTED = "<!-- claude-drafted -->"

STEPS = [
    (0, "Master CV", "cv/master.md", "/cv-master"),
    (1, "Profile", "profile/profile.md", "/setup 1"),
    (2, "Rubric", "profile/rubric.md", "/setup 2"),
    (3, "Voice", "profile/voice.md", "/setup 3"),
    (4, "Export format", "profile/export.md", "/setup 4"),
    (5, "Tracking and privacy", "profile/tracking.md", "/setup 5"),
    (6, "Score anchor", "profile/rubric.md", "runs at the end of the first /score"),
]

# command -> (required steps, recommended steps)
GATES = {
    "score": ({0, 1, 2}, set()),
    "ats-check": ({0, 1, 2}, set()),
    "tailor": ({0, 1, 2}, {4}),
    "cover-letter": ({0, 1, 2, 3}, {4}),
    "release": ({0, 1, 2, 5}, {4}),
    "log": ({5}, set()),
    "calibrate": ({5}, set()),
    "dashboard": ({5}, set()),
}


# --- master CV format ---------------------------------------------------------

def validate_cv(text: str) -> list[str]:
    """Return format errors that would break the scripts. Empty list = valid."""
    errors = []
    if "FICTIONAL EXAMPLE" in text:
        errors.append("This is still the fictional sample CV (examples/sample-master.md). "
                      "Replace it with your own: /cv-master.")
    body = strip_html_comments(text)
    lines = body.splitlines()

    name_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if name_idx is None:
        return ["No '# Your Name' heading found."]

    first_section = next(
        (i for i, l in enumerate(lines) if l.startswith("## ") and i > name_idx), len(lines)
    )
    contact = [l.strip() for l in lines[name_idx + 1:first_section] if l.strip()]
    if len(contact) != 2:
        errors.append(f"Expected exactly 2 contact lines under the name, found {len(contact)}.")
    for c in contact:
        if c.count(" · ") != 1:
            errors.append(f"Contact line needs exactly one ' · ' separator: {c!r}")

    sections = {}
    for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", body, re.M | re.S):
        sections[m.group(1).strip().lower()] = m.group(2)
    for req in ("summary", "professional experience", "education"):
        if req not in sections:
            errors.append(f"Missing required section: '## {req.title()}'.")

    if "summary" in sections and not sections["summary"].strip():
        errors.append("Summary section is empty.")

    if "professional experience" in sections:
        roles = re.split(r"^### ", sections["professional experience"], flags=re.M)[1:]
        if not roles:
            errors.append("Professional Experience has no '### Role Title' entries.")
        for rb in roles:
            rlines = [l.strip() for l in rb.splitlines()]
            title = rlines[0] if rlines else "?"
            rest = [l for l in rlines[1:] if l]
            if not rest or not re.match(r"^\*\*.+?\*\*\s*·\s*.+$", rest[0]):
                errors.append(f"Role '{title}': first line must be '**Company** · dates'.")
            if not any(l.startswith("- ") for l in rest):
                errors.append(f"Role '{title}': no bullets ('- ...').")

    if "education" in sections and not re.search(r"^- ", sections["education"], re.M):
        errors.append("Education has no entries ('- **Degree, Field** · School, Year').")

    return errors


def drafted_lines(text: str) -> list[int]:
    return [i + 1 for i, l in enumerate(text.splitlines()) if DRAFTED in l]


def cv_report(path: Path) -> int:
    if not path.exists():
        print(f"{path} does not exist. Run /cv-master to create it.")
        return 1
    text = path.read_text(encoding="utf-8")
    errors = validate_cv(text)
    print(f"## Master CV check: {path}\n")
    if errors:
        print("**Format: FAIL**")
        for e in errors:
            print(f"- {e}")
    else:
        print("**Format: pass**")

    clean = strip_html_comments(text)
    bullets = find_bullets(clean)
    flags = check_bullets(bullets)
    im = impact_stats(bullets)
    st = check_structure(clean)
    print(f"\n**Content flags:** {len(flags) or 'none'}")
    for f in flags:
        print(f"- [{f['category']}] {f['detail']}: \"{f['bullet'][:90]}\"")
    print(f"\n**Quantified impact:** {im['bullets_with_impact']}/{im['countable_bullets']} "
          f"accomplishment bullets contain a digit, % or $ (aggregate signal only).")
    print(f"**Length:** {st['word_count']} words (~{st['est_page_count']} pages). "
          f"A master CV can run long; tailored versions select from it.")
    if st["em_dash_count"]:
        print(f"**Em dashes:** {st['em_dash_count']} line(s). Check profile/voice.md for your rule.")

    drafted = drafted_lines(text)
    if drafted:
        print(f"\n**Claude-drafted lines: {len(drafted)}** (lines {', '.join(map(str, drafted))}).")
        print("Your master CV is strongly encouraged to be in your own words. Rewrite these,")
        print("or delete the marker yourself once you've read the line and stand behind it.")
    return 1 if errors else 0


# --- setup status -------------------------------------------------------------

def step_done(n: int) -> bool:
    _, _, rel, _ = STEPS[n]
    p = ROOT / rel
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    if n == 0:
        return not validate_cv(text)
    if n == 6:
        return step_done(2) and ANCHOR_PENDING not in text
    return not text.lstrip().startswith(STUB)


def start_done() -> bool:
    p = ROOT / "profile/user.md"
    return p.exists() and not p.read_text(encoding="utf-8").lstrip().startswith(STUB)


def status() -> dict:
    return {n: step_done(n) for n, *_ in STEPS}


def print_status(done: dict):
    print("| Step | Name | Status | Run |")
    print("|------|------|--------|-----|")
    print(f"| Start | Experience check | {'done' if start_done() else 'pending'} | {'' if start_done() else '/start'} |")
    for n, name, _, how in STEPS:
        print(f"| {n} | {name} | {'done' if done[n] else 'pending'} | {'' if done[n] else how} |")
    master = ROOT / "cv/master.md"
    if master.exists():
        if (d := drafted_lines(master.read_text(encoding="utf-8"))):
            print(f"\nNote: cv/master.md has {len(d)} Claude-drafted line(s). "
                  f"Run `python3 scripts/check_setup.py --cv cv/master.md` for details.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--for", dest="command", choices=sorted(GATES), help="check the gate for one command")
    ap.add_argument("--cv", type=Path, help="validate a master CV file's format and content")
    args = ap.parse_args()

    if args.cv:
        sys.exit(cv_report(args.cv))

    done = status()
    if not args.command:
        print_status(done)
        return

    required, recommended = GATES[args.command]
    missing = sorted(n for n in required if not done[n])
    soft = sorted(n for n in recommended if not done[n])
    if not start_done():
        print(f"/{args.command} is blocked. Run /start first: one question about your experience")
        print("with AI tools, so the rest of the steps are explained at the right level.")
        sys.exit(1)
    if missing:
        print(f"/{args.command} is blocked. Pending setup:")
        for n in missing:
            print(f"- Step {n} ({STEPS[n][1]}): run {STEPS[n][3]}")
        if 0 in missing:
            print("Start with /cv-master. Your master CV is strongly encouraged to be written by you.")
        sys.exit(1)
    print(f"/{args.command}: setup OK.")
    for n in soft:
        print(f"- Recommended first: step {n} ({STEPS[n][1]}), {STEPS[n][3]}")
    if args.command == "score" and not done[6]:
        print("- Anchor pending: finish this /score with setup step 6 (.claude/skills/setup/steps/6-anchor.md).")


if __name__ == "__main__":
    main()
