#!/usr/bin/env python3
"""
build_dashboard.py: render applications.csv into a standalone HTML dashboard.

Stdlib only. Writes dashboard/index.html, which opens in any browser. Run by
/dashboard, and at the end of every /release and /log.

Usage (from the repo root):
    python3 scripts/build_dashboard.py [--csv applications.csv] [--out dashboard/index.html]

Screen = reached_screen is "yes", or the outcome is recruiter_screen or later.
Resolved = has an outcome other than blank. not_applied rows are excluded from
every count.
"""

import argparse
import csv
import html
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREEN_OR_LATER = {"recruiter_screen", "hm_interview", "onsite", "offer"}
BANDS = [(0, 39), (40, 59), (60, 79), (80, 100)]
SMALL_N = 15


def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("slug") or "").strip()]
    return [r for r in rows if (r.get("outcome") or "").strip() != "not_applied"]


def screened(r: dict) -> bool:
    return (r.get("reached_screen") or "").strip().lower() == "yes" or \
        (r.get("outcome") or "").strip() in SCREEN_OR_LATER


def resolved(r: dict) -> bool:
    return bool((r.get("outcome") or "").strip())


def score(r: dict):
    try:
        return int(float(r.get("fit_score") or ""))
    except ValueError:
        return None


def group_rates(rows, key_fn, order=None):
    groups = {}
    for r in rows:
        k = key_fn(r)
        if k is None:
            continue
        g = groups.setdefault(k, [0, 0])
        g[1] += 1
        g[0] += screened(r)
    keys = order if order else sorted(groups, key=lambda k: -groups[k][1])
    return [(k, *groups.get(k, [0, 0])) for k in keys]


def band_of(r):
    s = score(r)
    if s is None:
        return None
    return next(f"{lo}-{hi}" for lo, hi in BANDS if lo <= s <= hi)


def bars(title, desc, data):
    if not any(n for _, _, n in data):
        return f'<section class="panel"><h2>{title}</h2><p class="desc">No resolved applications yet.</p></section>'
    rows = []
    for label, hit, n in data:
        pct = round(100 * hit / n) if n else 0
        tip = f"{label}: {hit} of {n} reached a screen ({pct}%)" if n else f"{label}: none"
        rows.append(
            f'<div class="bar-row" tabindex="0" title="{html.escape(tip)}">'
            f'<span class="bar-label">{html.escape(str(label))}</span>'
            f'<span class="bar-track"><span class="bar" style="width:{max(pct, 0)}%"></span></span>'
            f'<span class="bar-value">{f"{hit}/{n} · {pct}%" if n else "none"}</span></div>'
        )
    return (f'<section class="panel"><h2>{title}</h2><p class="desc">{desc}</p>'
            f'<div class="bars">{"".join(rows)}</div></section>')


def build(rows: list[dict]) -> str:
    res = [r for r in rows if resolved(r)]
    n_screen = sum(screened(r) for r in res)
    rate = round(100 * n_screen / len(res)) if res else 0
    pending = len(rows) - len(res)

    note = (f'<p class="note">Only {len(res)} resolved application(s). Rates below are not meaningful '
            f'until about {SMALL_N}; run /calibrate then.</p>') if len(res) < SMALL_N else ""

    tiles = "".join(
        f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{k}</div></div>'
        for k, v in [("Applications", len(rows)), ("Pending", pending), ("Resolved", len(res)),
                     ("Reached a screen", n_screen), ("Screen rate", f"{rate}%")]
    )

    by_band = bars("Screen rate by fit score",
                   "Does a higher fit score convert more often? If the bars are flat, the score "
                   "is measuring fit, not your odds. Use it to pick targets, not to predict.",
                   group_rates(res, band_of, [f"{lo}-{hi}" for lo, hi in BANDS]))
    by_source = bars("Screen rate by source",
                     "How the application went in. Often a stronger signal than fit.",
                     group_rates(res, lambda r: (r.get("source") or "").strip() or "unknown"))
    by_type = bars("Screen rate by fit type", "Core roles vs. pivots into an adjacent field.",
                   group_rates(res, lambda r: (r.get("fit_type") or "").strip() or None))

    body_rows = []
    for r in sorted(rows, key=lambda r: r.get("date_applied") or "", reverse=True):
        s = score(r)
        body_rows.append(
            "<tr>" + "".join(f"<td>{html.escape(v)}</td>" for v in [
                r.get("company", ""), r.get("role", ""), r.get("date_applied", "") or "not yet",
                r.get("source", ""), r.get("fit_type", ""),
            ]) + f'<td class="num">{"" if s is None else s}</td>'
            + f'<td>{html.escape(r.get("outcome", "") or "pending")}</td>'
            + f'<td>{"yes" if screened(r) else ""}</td></tr>'
        )
    table = ('<section class="panel"><h2>All applications</h2><div class="table-scroll"><table>'
             '<thead><tr><th>Company</th><th>Role</th><th>Applied</th><th>Source</th><th>Fit type</th>'
             '<th class="num">Fit</th><th>Outcome</th><th>Screen</th></tr></thead><tbody>'
             + ("".join(body_rows) or '<tr><td colspan="8">No applications yet. Run /score to add one.</td></tr>')
             + "</tbody></table></div></section>")

    return TEMPLATE.format(asof=date.today().isoformat(), tiles=tiles, note=note,
                           by_band=by_band, by_source=by_source, by_type=by_type, table=table)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Job Pipeline</title>
<style>
  :root {{
    --bg: #f4f4f2; --surface: #fcfcfb; --ink: #0b0b0b; --muted: #52514e;
    --border: #dcdbd6; --track: #ecebe7; --series: #2a78d6;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #111110; --surface: #1a1a19; --ink: #ffffff; --muted: #c3c2b7;
      --border: #33332f; --track: #262624; --series: #3987e5;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #111110; --surface: #1a1a19; --ink: #ffffff; --muted: #c3c2b7;
    --border: #33332f; --track: #262624; --series: #3987e5;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink);
    font: 15px/1.5 -apple-system, "Segoe UI", system-ui, sans-serif; padding: 32px 16px 64px; }}
  .wrap {{ max-width: 960px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }}
  h1 {{ font-size: 24px; margin: 0; }}
  .asof {{ color: var(--muted); font-size: 13px; margin: 2px 0 0; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1px;
    background: var(--border); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }}
  .stat {{ background: var(--surface); padding: 14px 16px; }}
  .stat-value {{ font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; }}
  .stat-label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }}
  .note {{ margin: 0; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px;
    background: var(--surface); color: var(--muted); font-size: 13.5px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
  .panel {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; min-width: 0; }}
  h2 {{ font-size: 16px; margin: 0 0 4px; }}
  .desc {{ color: var(--muted); font-size: 13px; margin: 0 0 14px; }}
  .bars {{ display: flex; flex-direction: column; gap: 10px; }}
  .bar-row {{ display: grid; grid-template-columns: 72px 1fr auto; align-items: center; gap: 10px;
    font-size: 13px; border-radius: 4px; outline-offset: 2px; }}
  .bar-row:hover .bar, .bar-row:focus .bar {{ filter: brightness(1.12); }}
  .bar-label {{ color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .bar-track {{ height: 14px; background: var(--track); border-radius: 0 4px 4px 0; }}
  .bar {{ display: block; height: 100%; background: var(--series); border-radius: 0 4px 4px 0; }}
  .bar-value {{ font-variant-numeric: tabular-nums; min-width: 72px; text-align: right; }}
  .table-scroll {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
  th, td {{ text-align: left; padding: 7px 8px; border-bottom: 1px solid var(--border); white-space: nowrap; }}
  th {{ color: var(--muted); font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: .03em; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  footer {{ color: var(--muted); font-size: 12px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
  <header><h1>Job Pipeline</h1><p class="asof">As of {asof}. Fit scores measure fit with the job as written, not odds of a screen.</p></header>
  <div class="stats">{tiles}</div>
  {note}
  <div class="grid">{by_band}{by_source}{by_type}</div>
  {table}
  <footer>Generated by scripts/build_dashboard.py from applications.csv</footer>
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=ROOT / "applications.csv")
    ap.add_argument("--out", type=Path, default=ROOT / "dashboard/index.html")
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build(load(args.csv)), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
