#!/usr/bin/env python3
"""
build_cv_review.py: renders the visual CV review page used by the screen
check (`/ats-check <slug>`, .claude/skills/ats-check).

Combines ats_check.py's flags with a line-level diff against cv/master.md
into inline highlights plus a diff panel, written as a standalone HTML file
you can open in any browser.

Usage (from the repo root):
    python3 scripts/build_cv_review.py --cv cv/<slug>.md \\
        --jd jds/<slug>.md --master cv/master.md --out /tmp/review.html \\
        [--title "Company, Role"]

Design: light/dark token pairs, IBM Plex Mono + IBM Plex Sans, severity
stripe + tint + tag label per flag category. Only the content (stats, chips,
cv_html, diff_html) changes per application.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ats_check import (  # noqa: E402
    build_report, strip_html_comments, strip_markdown as strip_md,
    WEAK_VERB_PHRASES, BUZZWORDS, PASSIVE_RE,
)

BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
HEADER_RE = re.compile(r"^(#{1,3})\s+(.*)$")

CAT_ORDER = ["weak-verb", "passive-voice", "buzzword"]
CAT_LABEL = {
    "weak-verb": "weak verb",
    "passive-voice": "passive voice",
    "buzzword": "buzzword",
}
# Quantified impact is deliberately NOT a per-bullet highlight; see
# ats_check.py's impact_stats(). On a narrative/leadership-heavy resume most
# legitimate bullets lack a literal number; tagging ~70% of the CV trains the
# reader to ignore the flag. It's surfaced as one aggregate stat tile instead
# (see build()).


def mark_phrase(text_html, plain_text, phrase, css_class):
    idx = plain_text.lower().find(phrase.lower())
    if idx == -1:
        return text_html, False
    before, matched, after = (
        text_html[:idx], text_html[idx:idx + len(phrase)], text_html[idx + len(phrase):]
    )
    return f'{before}<mark class="{css_class}">{matched}</mark>{after}', True


def render_bullet(raw_text, flags_by_bullet):
    plain = strip_md(raw_text)
    working = html.escape(plain)
    cats = {f["category"] for f in flags_by_bullet.get(plain, [])}

    low = plain.lower()
    for phrase in WEAK_VERB_PHRASES:
        if phrase in low:
            working, ok = mark_phrase(working, plain, phrase, "mk-weakverb")
            if ok:
                cats.add("weak-verb")
            break
    for term in BUZZWORDS:
        if term in low:
            working, ok = mark_phrase(working, plain, term, "mk-buzzword")
            if ok:
                cats.add("buzzword")
    m = PASSIVE_RE.search(plain)
    if m:
        working, ok = mark_phrase(working, plain, m.group(0), "mk-passive")
        if ok:
            cats.add("passive-voice")

    present = [c for c in CAT_ORDER if c in cats]
    stripe_class = f"li-{present[0]}" if present else ""
    tags = "".join(f'<span class="tag tag-{c}">{CAT_LABEL[c]}</span>' for c in present)
    return f'<li class="{stripe_class}">{working}{tags}</li>'


def render_cv_html(lines, flags_by_bullet):
    out, in_list = [], False
    for line in lines:
        if not line.strip():
            continue
        hm, bm = HEADER_RE.match(line), BULLET_RE.match(line)
        if hm:
            if in_list:
                out.append("</ul>")
                in_list = False
            level, text = len(hm.group(1)), strip_md(hm.group(2))
            tag = "cv-name" if level == 1 else "cv-section"
            wrapper = "h1" if level == 1 else "h3"
            out.append(f'<{wrapper} class="{tag}">{html.escape(text)}</{wrapper}>')
        elif bm:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(render_bullet(bm.group(1), flags_by_bullet))
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            s = line.strip()
            if s.startswith("**") and "·" in s:
                out.append(f'<p class="cv-companyline">{html.escape(strip_md(s))}</p>')
            elif s.startswith("**"):
                out.append(f'<p class="cv-role">{html.escape(strip_md(s))}</p>')
            elif s.startswith("*"):
                out.append(f'<p class="cv-subtitle">{html.escape(strip_md(s))}</p>')
            else:
                out.append(f'<p class="cv-body">{html.escape(s)}</p>')
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def diff_rows(master_lines, cv_lines, context=1):
    import difflib
    sm = difflib.SequenceMatcher(None, master_lines, cv_lines, autojunk=False)
    ops = sm.get_opcodes()
    rows, n = [], len(ops)
    for idx, (tag, i1, i2, j1, j2) in enumerate(ops):
        if tag == "equal":
            eq = master_lines[i1:i2]
            head = eq[:context] if idx > 0 else []
            tail = eq[-context:] if idx < n - 1 else []
            mid = len(eq) - len(head) - len(tail)
            if idx > 0:
                rows += [{"type": "equal", "text": t} for t in head]
            if mid > 0:
                rows.append({"type": "collapsed", "text": f"{mid} unchanged line(s)"})
            if idx < n - 1:
                rows += [{"type": "equal", "text": t} for t in tail]
        elif tag == "delete":
            rows += [{"type": "del", "text": t} for t in master_lines[i1:i2] if t.strip()]
        elif tag == "insert":
            rows += [{"type": "add", "text": t} for t in cv_lines[j1:j2] if t.strip()]
        elif tag == "replace":
            rows += [{"type": "del", "text": t} for t in master_lines[i1:i2] if t.strip()]
            rows += [{"type": "add", "text": t} for t in cv_lines[j1:j2] if t.strip()]
    clean = []
    for r in rows:
        if clean and clean[-1] == r:
            continue
        clean.append(r)
    return clean


def diff_row_html(row):
    t = row["type"]
    if t == "collapsed":
        return f'<div class="diff-collapsed">⋯ {html.escape(row["text"])} ⋯</div>'
    text = html.escape(row["text"]) if row["text"].strip() else "&nbsp;"
    cls = {"del": "diff-del", "add": "diff-add", "equal": "diff-equal"}[t]
    return f'<div class="diff-line {cls}">{text}</div>'


def build(cv_path: Path, jd_path: Path, master_path: Path, title: str) -> str:
    cv_text = strip_html_comments(cv_path.read_text(encoding="utf-8"))
    jd_text = jd_path.read_text(encoding="utf-8")
    master_text = strip_html_comments(master_path.read_text(encoding="utf-8"))

    report = build_report(cv_path.read_text(encoding="utf-8"), jd_text)
    flags_by_bullet = {}
    for f in report["flags"]:
        flags_by_bullet.setdefault(f["bullet"], []).append(f)

    cv_lines = [l for l in cv_text.split("\n") if not l.strip().startswith("*")]
    master_lines = master_text.split("\n")

    cv_html = render_cv_html(cv_lines, flags_by_bullet)
    diff_html = "\n".join(diff_row_html(r) for r in diff_rows(master_lines, cv_lines))
    missing_html = "".join(
        f'<span class="chip chip-keyword">{html.escape(k)}</span>'
        for k in report["keywords"]["missing_keywords"]
    )
    by_cat = {}
    for f in report["flags"]:
        by_cat[f["category"]] = by_cat.get(f["category"], 0) + 1

    kw, st = report["keywords"], report["structural"]

    def stat(label, value):
        return f'<div class="stat"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'

    im = report["impact"]
    stats_html = "".join([
        stat("Keyword overlap", f'{kw["overlap_pct"]}%'),
        stat("JD terms matched", f'{len(kw["matched_keywords"])}/{len(kw["matched_keywords"]) + len(kw["missing_keywords"])}'),
        stat("Quantified impact", f'{im["bullets_with_impact"]}/{im["countable_bullets"]} bullets'),
        stat("Length", f'{st["word_count"]}w · ~{st["est_page_count"]}p'),
        stat("Em dashes found", st["em_dash_count"]),
    ])

    legend_cats = [
        ("weak-verb", "Weak verb"),
        ("passive-voice", "Passive voice"), ("buzzword", "Buzzword"),
        ("keyword", "Missing JD keyword"),
    ]
    legend_html = "".join(
        f'<div class="legend-item"><span class="legend-swatch sw-{c}"></span>{label} '
        f'<span class="legend-count">{by_cat.get(c, "") if c != "keyword" else ""}</span></div>'
        for c, label in legend_cats
    )

    template = (Path(__file__).parent / "cv_review_template.html").read_text(encoding="utf-8")
    return template.format(
        title=html.escape(title),
        stats_html=stats_html,
        legend_html=legend_html,
        missing_html=missing_html,
        cv_html=cv_html,
        diff_html=diff_html,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cv", required=True, type=Path)
    ap.add_argument("--jd", required=True, type=Path)
    ap.add_argument("--master", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--title", default="CV Review")
    args = ap.parse_args()
    args.out.write_text(build(args.cv, args.jd, args.master, args.title), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
