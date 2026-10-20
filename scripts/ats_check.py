#!/usr/bin/env python3
"""
ats_check.py: deterministic ATS/content checklist for a CV against a JD.

No LLM calls, no external dependencies (stdlib only). This is the mechanical
half of the screen check (`/ats-check <slug>`, .claude/skills/ats-check): it
flags what's cheap to check by rule, and leaves judgment calls (does this
bullet actually address the JD's real ask?) to Claude reading the output
alongside the JD.

Usage (from the repo root):
    python3 scripts/ats_check.py --cv cv/master.md --jd jds/<slug>.md [--json out.json]

Output:
    - Human-readable checklist on stdout (goes into the analysis's
      "## ATS & Content Check" section, see templates/analysis.md).
    - Optional structured JSON (--json), consumed by build_cv_review.py.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# --- tokenization -----------------------------------------------------------

STOPWORDS = {
    "a", "about", "across", "after", "all", "an", "and", "any", "are", "as",
    "at", "be", "been", "being", "but", "by", "can", "did", "do", "does",
    "each", "for", "from", "had", "has", "have", "how", "if", "in", "into",
    "is", "it", "its", "may", "more", "most", "must", "of", "on", "or",
    "other", "our", "over", "own", "per", "should", "so", "some", "such",
    "than", "that", "the", "their", "them", "then", "there", "these",
    "they", "this", "through", "to", "under", "up", "us", "use", "using",
    "was", "we", "were", "what", "when", "where", "which", "while", "who",
    "will", "with", "within", "would", "you", "your", "years",
    "year", "including", "role", "team", "work", "working",
    "experience", "ability", "skills", "job", "candidate", "position",
}

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#/.\-]{1,}")


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def significant_counts(text: str) -> Counter:
    return Counter(w for w in tokenize(text) if w not in STOPWORDS and len(w) >= 3)


# --- content-quality checks --------------------------------------------------

WEAK_VERB_PHRASES = [
    "responsible for", "helped", "helped with", "worked on", "assisted",
    "assisted with", "involved in", "duties included", "in charge of",
    "participated in", "tasked with", "helped to",
]

BUZZWORDS = [
    "synergy", "synergies", "results-driven", "results driven",
    "team player", "hard worker", "go-getter", "detail-oriented",
    "detail oriented", "self-starter", "think outside the box",
    "fast-paced environment", "wear many hats", "dynamic", "passionate",
    "thought leader", "value-add", "circle back", "low-hanging fruit",
]

PASSIVE_RE = re.compile(
    r"\b(was|were|is|are|be|been|being)\s+\w+ed\b", re.IGNORECASE
)
IMPACT_RE = re.compile(r"[0-9%$]")

BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
HEADER_RE = re.compile(r"^#{1,3}\s+(.*)$")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b")

EXPECTED_SECTIONS = ["summary", "professional experience", "education"]


def strip_markdown(line: str) -> str:
    return re.sub(r"[*_`]", "", line).strip()


HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text: str) -> str:
    # Drafts routinely carry a leading <!-- ... --> block (export notes,
    # revision flags) that would otherwise push real content out of any
    # "first N lines" window (e.g. the contact-info check) or get scanned
    # as if it were CV content.
    return HTML_COMMENT_RE.sub("", text)


SKILLS_SECTION_RE = re.compile(r"\bskills?\b", re.IGNORECASE)


def find_bullets(cv_text: str) -> list[tuple[str, str]]:
    """Returns (bullet_text, current_section_header) pairs; section context
    matters for at least one check (a skills list isn't held to the same
    "quantified impact" bar as an accomplishment bullet)."""
    bullets = []
    section = ""
    for line in cv_text.splitlines():
        hm = HEADER_RE.match(line)
        if hm:
            section = strip_markdown(hm.group(1))
            continue
        m = BULLET_RE.match(line)
        if m:
            bullets.append((strip_markdown(m.group(1)), section))
    return bullets


def check_bullets(bullets: list[tuple[str, str]]) -> list[dict]:
    """Per-bullet flags worth calling out individually, rare enough that a
    reader can act on each one. Quantified-impact is deliberately NOT one of
    these (see impact_stats): on a narrative/leadership-heavy resume most
    legitimate bullets lack a literal number, so flagging every one
    individually just trains the reader to ignore the flag."""
    flags = []
    for b, _section in bullets:
        low = b.lower()
        for phrase in WEAK_VERB_PHRASES:
            if phrase in low:
                flags.append({"category": "weak-verb", "bullet": b, "detail": f'contains "{phrase}"'})
                break
        if PASSIVE_RE.search(b):
            flags.append({"category": "passive-voice", "bullet": b, "detail": "passive construction detected"})
        for term in BUZZWORDS:
            if term in low:
                flags.append({"category": "buzzword", "bullet": b, "detail": f'contains "{term}"'})
    return flags


def impact_stats(bullets: list[tuple[str, str]]) -> dict:
    """Aggregate only. Skills-list bullets (under a header matching /skills?/)
    are excluded; they enumerate tools/domains, not accomplishments."""
    countable = [b for b, section in bullets if not SKILLS_SECTION_RE.search(section)]
    with_impact = [b for b in countable if IMPACT_RE.search(b)]
    return {
        "countable_bullets": len(countable),
        "bullets_with_impact": len(with_impact),
    }


def check_structure(cv_text: str) -> dict:
    headers = [strip_markdown(m.group(1)).lower() for line in cv_text.splitlines()
               if (m := HEADER_RE.match(line))]
    missing = [s for s in EXPECTED_SECTIONS if not any(s in h for h in headers)]
    head = "\n".join(cv_text.splitlines()[:10])
    word_count = len(tokenize(cv_text))
    em_dash_lines = [l for l in cv_text.splitlines() if "\u2014" in l]
    return {
        "sections_found": headers,
        "sections_missing": missing,
        "email_present": bool(EMAIL_RE.search(head)),
        "phone_present": bool(PHONE_RE.search(head)),
        "word_count": word_count,
        "est_page_count": round(word_count / 550, 2),
        # Many readers treat em dashes as a sign of AI-written text. Reported,
        # not judged: profile/voice.md says whether the user allows them.
        "em_dash_count": len(em_dash_lines),
        "em_dash_examples": em_dash_lines[:5],
    }


# --- keyword overlap ----------------------------------------------------------

def keyword_overlap(cv_text: str, jd_text: str) -> dict:
    jd_counts = significant_counts(jd_text)
    cv_counts = significant_counts(cv_text)
    jd_terms = set(jd_counts)
    cv_terms = set(cv_counts)

    matched = sorted(jd_terms & cv_terms)
    missing_important = sorted(
        (t for t in jd_terms - cv_terms if jd_counts[t] >= 2),
        key=lambda t: -jd_counts[t],
    )
    overlap_pct = round(100 * len(matched) / len(jd_terms), 1) if jd_terms else 0.0

    return {
        "overlap_pct": overlap_pct,
        "matched_keywords": matched,
        "missing_keywords": missing_important,
    }


# --- reporting ----------------------------------------------------------------

def build_report(cv_text: str, jd_text: str) -> dict:
    cv_text = strip_html_comments(cv_text)
    jd_text = strip_html_comments(jd_text)
    bullets = find_bullets(cv_text)
    return {
        "keywords": keyword_overlap(cv_text, jd_text),
        "flags": check_bullets(bullets),
        "impact": impact_stats(bullets),
        "structural": check_structure(cv_text),
    }


def render_human_readable(report: dict) -> str:
    kw = report["keywords"]
    st = report["structural"]
    im = report["impact"]
    flags = report["flags"]
    by_cat = Counter(f["category"] for f in flags)

    lines = []
    lines.append("## ATS & Content Check")
    lines.append("")
    lines.append(f"**Keyword overlap: {kw['overlap_pct']}%** "
                  f"({len(kw['matched_keywords'])} matched / {len(kw['matched_keywords']) + len(kw['missing_keywords'])} significant JD terms)")
    if kw["missing_keywords"]:
        lines.append(f"- Missing (appear ≥2× in JD, absent from CV): {', '.join(kw['missing_keywords'][:20])}")
    lines.append("  <!-- unigram frequency match, no POS tagging; expect some generic-word noise")
    lines.append("       (e.g. \"plan\", \"teams\"); treat as a candidate list to review, not a verdict -->")
    lines.append("")
    lines.append(f"**Quantified impact: {im['bullets_with_impact']}/{im['countable_bullets']}** "
                  f"accomplishment bullets contain a digit/%/$ (skills-list bullets excluded from this "
                  f"count). Aggregate signal only, not a per-bullet callout; a narrative/leadership-heavy "
                  f"resume legitimately has bullets whose value isn't a number.")
    lines.append("")
    lines.append("**Content flags:** " + (
        ", ".join(f"{n} {cat}" for cat, n in by_cat.most_common()) if flags else "none"
    ))
    for f in flags:
        lines.append(f"- [{f['category']}] {f['detail']}: \"{f['bullet'][:90]}\"")
    lines.append("")
    lines.append("**Structure:**")
    lines.append(f"- Sections found: {', '.join(st['sections_found']) or 'none detected'}")
    if st["sections_missing"]:
        lines.append(f"- Sections missing: {', '.join(st['sections_missing'])}")
    lines.append(f"- Contact info: email {'present' if st['email_present'] else 'MISSING'}, "
                  f"phone {'present' if st['phone_present'] else 'MISSING'}")
    lines.append(f"- Length: {st['word_count']} words (~{st['est_page_count']} pages est.)")
    if st["em_dash_count"]:
        lines.append(f"- Em dash found on {st['em_dash_count']} line(s). Many readers treat these as "
                      f"a sign of AI-written text; check profile/voice.md for your rule:")
        for ex in st["em_dash_examples"]:
            lines.append(f"  - \"{ex.strip()[:90]}\"")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cv", required=True, type=Path)
    ap.add_argument("--jd", required=True, type=Path)
    ap.add_argument("--json", type=Path, help="also write structured JSON here")
    args = ap.parse_args()

    cv_text = args.cv.read_text(encoding="utf-8")
    jd_text = args.jd.read_text(encoding="utf-8")

    report = build_report(cv_text, jd_text)
    print(render_human_readable(report))

    if args.json:
        args.json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\n[wrote structured report to {args.json}]", file=sys.stderr)


if __name__ == "__main__":
    main()
