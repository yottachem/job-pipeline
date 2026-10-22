#!/usr/bin/env python3
"""
export_docx.py: render a CV or cover letter markdown file to a clean,
single-column, ATS-safe .docx.

Pipeline: strip comments and *Flag:* notes -> pandoc (optionally with your
reference .docx for styles) -> python-docx post-processing for the layout
details pandoc can't express:
  - tight spacing on every paragraph (pandoc's default 8pt space-after makes
    bullet lists look double-spaced)
  - " · " on contact and company/date lines becomes a tab to a right-aligned
    tab stop at the page's usable width, so the right item sits flush right
  - optional thin rule under the contact block
  - section headers as plain bold caps (or keep styled headings)
  - one font and size on every run
  - keep-with-next on headers and role lines so none strand at a page bottom

Requires: pandoc on PATH, python-docx (pip install -r requirements.txt).
Optional: --pdf converts with LibreOffice (soffice) when installed, else with
Microsoft Word on macOS (exported inside Word's sandbox container).

Usage (from the repo root):
    python3 scripts/export_docx.py --md cv/<slug>.md --out "Lastname CV Company.docx" \\
        [--reference profile/reference.docx] [--font Calibri] [--size 11] \\
        [--margin 0.75] [--no-right-align] [--no-rule] [--styled-headings] [--pdf]

Always open the result and check it on the page. Spacing and indentation
problems are invisible in the file structure.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    sys.exit("python-docx is required: pip install -r requirements.txt")

SENTINEL = "⇥"  # stands in for a tab through pandoc, which collapses literal tabs
HEADING_STYLES = {"Heading 1", "Heading 2", "Heading 3", "Title"}


def preprocess(md: str, right_align: bool) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    blocks = re.split(r"\n\s*\n", md)
    md = "\n\n".join(b for b in blocks if not b.strip().startswith("*Flag:"))

    out, in_header, seen_name = [], False, False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("# ") and not seen_name:
            seen_name, in_header = True, True
            out += [line, ""]
            continue
        if s.startswith("## "):
            in_header = False
        is_company = bool(re.match(r"^\*\*.+?\*\*\s*·\s*.+$", s))
        is_subtitle = bool(re.match(r"^\*[^*].*\*$", s))
        if right_align and ((in_header and s.count(" · ") == 1) or is_company):
            line = line.replace(" · ", SENTINEL, 1)
        out.append(line)
        # Separate lines pandoc would otherwise merge into one paragraph.
        if s and (in_header or is_company or is_subtitle):
            out.append("")
    return "\n".join(out).strip() + "\n"


def run_pandoc(md_text: str, out: Path, reference: Path | None):
    if not shutil.which("pandoc"):
        sys.exit("pandoc is required: https://pandoc.org/installing.html")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md_text)
        src = f.name
    cmd = ["pandoc", src, "-f", "markdown-smart", "-o", str(out)]
    if reference:
        cmd += ["--reference-doc", str(reference)]
    subprocess.run(cmd, check=True)


def set_run_font(run, font: str, size: Pt):
    run.font.name = font
    run.font.size = size
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), font)


def bottom_rule(paragraph):
    ppr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "4"), ("w:color", "000000")):
        bottom.set(qn(k), v)
    bdr.append(bottom)
    ppr.append(bdr)


def postprocess(path: Path, font: str, size_pt: float, rule: bool, styled: bool, margin: float | None):
    doc = Document(str(path))
    sec = doc.sections[0]
    # pandoc's built-in reference doc sets no page size; default to US Letter.
    if sec.page_width is None:
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        if margin is not None or getattr(sec, side) is None:
            setattr(sec, side, Inches(margin if margin is not None else 1.0))
    usable = sec.page_width - sec.left_margin - sec.right_margin
    size = Pt(size_pt)
    paras = doc.paragraphs

    last_contact = None
    seen_section = False
    role_header = False
    for p in paras:
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(0), 1.0
        style = p.style.name if p.style is not None else ""

        for run in p.runs:
            if SENTINEL in run.text:
                run.text = run.text.replace(SENTINEL, "\t")
                pf.tab_stops.add_tab_stop(usable, WD_TAB_ALIGNMENT.RIGHT)
            set_run_font(run, font, size)

        if style in ("Heading 1", "Title") and not seen_section:
            # Name line
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(size_pt + 5)
                run.font.color.rgb = RGBColor(0, 0, 0)
            pf.space_after = Pt(2)
            continue

        if style == "Heading 2":
            seen_section, role_header = True, False
            pf.space_before, pf.space_after = Pt(10), Pt(4)
            pf.keep_with_next = True
            if not styled:
                p.style = doc.styles["Normal"]
                text = p.text.upper()
                for run in p.runs[1:]:
                    run._element.getparent().remove(run._element)
                if p.runs:
                    p.runs[0].text = text
                    p.runs[0].bold = True
                    set_run_font(p.runs[0], font, size)
            continue

        if style == "Heading 3":
            role_header = True
            pf.space_before = Pt(8)
            pf.keep_with_next = True
            if not styled:
                p.style = doc.styles["Normal"]
                for run in p.runs:
                    run.bold = True
                    set_run_font(run, font, size)
            continue

        if not seen_section and p.text.strip():
            last_contact = p
        # Company/date and subtitle lines stay with the bullets below them.
        if role_header and p._p.pPr is not None and p._p.pPr.numPr is not None:
            role_header = False
        if role_header:
            pf.keep_with_next = True

        if not styled:
            for run in p.runs:
                run.font.color.rgb = RGBColor(0, 0, 0)

    if rule and last_contact is not None:
        last_contact.paragraph_format.space_after = Pt(4)
        bottom_rule(last_contact)

    doc.save(str(path))


def word_to_pdf(path: Path) -> bool:
    """macOS fallback: export through Microsoft Word over AppleScript.

    Word is sandboxed. Saving outside folders it has been granted raises a
    "Grant File Access" dialog and the AppleEvent times out, so the export
    runs inside Word's own container and the PDF is moved back afterward.
    """
    if sys.platform != "darwin" or not Path("/Applications/Microsoft Word.app").exists():
        return False
    box = Path.home() / "Library/Containers/com.microsoft.Word/Data/Documents/job-pipeline-export"
    box.mkdir(parents=True, exist_ok=True)
    src = box / path.name
    pdf = src.with_suffix(".pdf")
    shutil.copy(path, src)
    script = f"""
with timeout of 60 seconds
tell application "Microsoft Word"
    open POSIX file "{src}"
    delay 1
    save as document "{src.name}" file name "{pdf}" file format format PDF
    close document "{src.name}" saving no
end tell
end timeout
"""
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
        shutil.move(str(pdf), str(path.with_suffix(".pdf")))
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    finally:
        src.unlink(missing_ok=True)
    return True


def to_pdf(path: Path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir",
                        str(path.parent), str(path)], check=True, capture_output=True)
    elif not word_to_pdf(path):
        print("No LibreOffice or Microsoft Word found for --pdf. Export to PDF manually.", file=sys.stderr)
        return
    print(f"wrote {path.with_suffix('.pdf')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--md", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--reference", type=Path, help="your resume .docx; pandoc copies its styles")
    ap.add_argument("--font", default="Calibri")
    ap.add_argument("--size", type=float, default=11)
    ap.add_argument("--margin", type=float, help="page margins in inches (default: reference doc's, else 1.0)")
    ap.add_argument("--no-right-align", action="store_true")
    ap.add_argument("--no-rule", action="store_true")
    ap.add_argument("--styled-headings", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    args = ap.parse_args()

    md = preprocess(args.md.read_text(encoding="utf-8"), not args.no_right_align)
    if "\u2014" in md:
        print("Note: the source contains em dashes. Check profile/voice.md for your rule.", file=sys.stderr)
    if "<!-- claude-drafted -->" in args.md.read_text(encoding="utf-8"):
        print("Note: the source contains Claude-drafted lines you haven't approved.", file=sys.stderr)
    run_pandoc(md, args.out, args.reference)
    postprocess(args.out, args.font, args.size, not args.no_rule, args.styled_headings, args.margin)
    print(f"wrote {args.out}")
    if args.pdf:
        to_pdf(args.out)


if __name__ == "__main__":
    main()
