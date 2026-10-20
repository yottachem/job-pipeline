# Step 4: Export format

**Writes:** `profile/export.md`
**Why it can't ship pre-filled:** a resume's look is personal, and the
template has no way to know yours. The shared exporter
(`scripts/export_docx.py`) produces a clean single-column, ATS-safe docx;
this step decides how it is styled and how output is checked.
**Reads first:** `cv/master.md`.

## Interview branches (in order)

1. **Reference document.** Do they have a current resume .docx whose look
   they want to keep? If yes, copy it to `profile/reference.docx`. Explain the
   limit: pandoc's reference document carries named styles (fonts, sizes,
   heading look), not per-paragraph layout. Everything else comes from the
   options below.
2. **Font and size.** Recommend the font from their current resume, or
   Calibri 11.
3. **Layout options.** Right-align dates and contact items (recommended),
   thin rule under the contact block, section headers as plain bold caps
   (recommended, most ATS-friendly) or styled headings.
4. **Length.** Target page count for a submitted resume. The master can run
   long; tailored versions should fit this.
5. **File names.** Pattern for exported files, for example
   `Lastname CV <Company>.docx`. Avoid "final" and version numbers in names
   recruiters see.
6. **PDF.** Do they submit PDF, docx, or both? PDF conversion needs Word or
   LibreOffice installed locally; check which is available.
7. **Test export.** Run the export on `cv/master.md` into `/tmp` (or the
   scratch location the user prefers), have the user open it, and adjust
   options until it looks right. Check the rendered page, not the XML:
   spacing and indentation bugs are only visible on the page.

## Output format

```markdown
# Export

## Command
python3 scripts/export_docx.py --md <input.md> --out "<name>.docx" \
    [--reference profile/reference.docx] --font "<font>" --size <pt> \
    [--no-right-align] [--no-rule] [--styled-headings]

## Choices
- Font: ...  ·  Size: ...
- Right-aligned dates/contact: yes/no  ·  Rule under contact: yes/no
- Headers: plain bold caps / styled
- Target length: <n> pages
- File name pattern: ...
- Submit as: docx / pdf / both
- PDF converter available: Word / LibreOffice / none

## Verification
- Open the rendered file and check page count, spacing, and that nothing
  ran off the page.
- Copy all text from the PDF and confirm it reads top to bottom in one
  order (name, contact, summary, experience, education). Columns or tables
  that read out of order are what break ATS parsers.
```

**Done when:** the user has opened a test export and approved its look.
