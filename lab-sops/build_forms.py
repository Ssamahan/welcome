#!/usr/bin/env python3
"""
Builds the three tracking forms:
  1. Daily PM log for the hematology analysers \u2013 monthly sheets for the two
     Sysmex instruments, a year-long register for the portable Alere Pima CD4
  2. Daily PM log for the GeneXpert Dx System, following the Cepheid log (302-8386 Rev. C)
  3. Temperature monitoring for refrigerators, freezer, cold box and rooms
One worksheet per month, printable landscape on A4.
"""
import os, calendar
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.dirname(os.path.abspath(__file__))

NAVY = "1F4E79"
GREY = "EDEDED"
YELLOW = "FFF2CC"
GREEN = "E2EFDA"
RED = "FCE4E4"
THIN = Side(style="thin", color="A6A6A6")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

MONTHS = [(m, calendar.month_name[m]) for m in range(1, 13)]
YEAR = 2026


def head(ws, title, subtitle, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value="RULI DISTRICT HOSPITAL \u2013 LABORATORY DEPARTMENT")
    c.font = Font(bold=True, size=9, color="595959")
    c.alignment = CEN

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c = ws.cell(row=2, column=1, value=title)
    c.font = Font(bold=True, size=14, color=NAVY)
    c.alignment = CEN
    ws.row_dimensions[2].height = 22

    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncols)
    c = ws.cell(row=3, column=1, value=subtitle)
    c.font = Font(italic=True, size=8.5, color="595959")
    c.alignment = CEN


def id_block(ws, row, fields, ncols):
    """fields: list of (label, value, span). Lays identifying fields across the page."""
    col = 1
    for label, value, span in fields:
        lc = ws.cell(row=row, column=col, value=label)
        lc.font = Font(bold=True, size=8.5)
        lc.fill = PatternFill("solid", fgColor=GREY)
        lc.border = BOX
        lc.alignment = LEFT
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col)
        v_col = col + 1
        if span > 1:
            ws.merge_cells(start_row=row, start_column=v_col,
                           end_row=row, end_column=v_col + span - 1)
        for k in range(v_col, v_col + span):
            ws.cell(row=row, column=k).border = BOX
        vc = ws.cell(row=row, column=v_col, value=value)
        vc.font = Font(size=8.5)
        vc.alignment = LEFT
        col = v_col + span
    return col


def setup_print(ws, ncols):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = ws.page_margins.right = 0.3
    ws.page_margins.top = ws.page_margins.bottom = 0.4


def style_header(ws, row, ncols, height=30):
    for i in range(1, ncols + 1):
        c = ws.cell(row=row, column=i)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.font = Font(bold=True, size=8, color="FFFFFF")
        c.alignment = CEN
        c.border = BOX
    ws.row_dimensions[row].height = height


# =====================================================================
# 1. HEMATOLOGY ANALYSER DAILY PM LOG
# =====================================================================
def hematology_log():
    wb = Workbook()
    wb.remove(wb.active)

    for mnum, mname in MONTHS:
        ws = wb.create_sheet(mname[:3])
        ndays = calendar.monthrange(YEAR, mnum)[1]
        # cols: task, target, then days, then done count
        first_day = 3
        last_day = first_day + ndays - 1
        ncols = last_day + 1
        head(ws, "HEMATOLOGY ANALYSER \u2013 DAILY MAINTENANCE AND START-UP LOG",
             f"{mname} {YEAR}  \u2022  RliDHL-ADM-SOP-058  \u2022  one row per task, "
             f"initial and tick the box each day", ncols)

        id_block(ws, 4, [
            ("Analyser", "\u25a1 Sysmex XN-330   \u25a1 Sysmex XQ-320", 1),
            ("Serial no.", "17156 / 12357", 1),
            ("Asset no.", "ME/0501 / ME/0499", 1),
            ("Location", "Hematology Room", 1),
        ], ncols)
        id_block(ws, 5, [
            ("Diluent lot / exp", "", 1),
            ("Lyse lot / exp", "", 1),
            ("Cleaner lot / exp", "", 1),
            ("Control lot / exp", "", 1),
        ], ncols)

        # day header
        hr = 7
        ws.cell(row=hr, column=1, value="Task")
        ws.cell(row=hr, column=2, value="Acceptance / target")
        for d in range(ndays):
            ws.cell(row=hr, column=first_day + d, value=d + 1)
        ws.cell(row=hr, column=ncols, value="Days\nlogged")
        style_header(ws, hr, ncols, height=26)

        TASKS = [
            ("1", "Warm-up completed as manual directs", "Per manual", "tick"),
            ("2", "Background / blank count run", "0 or below manual limit", "value"),
            ("3", "Reagents present, in date, adequate", "All OK", "tick"),
            ("4", "Waste container below maximum", "Below max line", "tick"),
            ("5", "IQC normal level within 2 SD", "2 SD", "tick"),
            ("6", "IQC abnormal level within 2 SD", "2 SD", "tick"),
            ("7", "Aspiration probe inspected / wiped", "No residue", "tick"),
            ("8", "Shutdown / standby cycle at end of shift", "Done", "tick"),
            ("9", "Exterior cleaned", "No soil", "tick"),
            ("", "Instrument temperature (\u00b0C)", "Per manual", "value"),
            ("", "Operator initials", "", "init"),
        ]
        r = hr + 1
        for num, task, target, kind in TASKS:
            ws.cell(row=r, column=1, value=f"{num}. {task}" if num else task)
            ws.cell(row=r, column=2, value=target)
            for d in range(first_day, last_day + 1):
                c = ws.cell(row=r, column=d)
                if kind == "value":
                    c.fill = PatternFill("solid", fgColor=YELLOW)
                elif kind == "init":
                    c.fill = PatternFill("solid", fgColor=YELLOW)
            r += 1
        last_task = r - 1

        for row in ws.iter_rows(min_row=hr + 1, max_row=last_task,
                                min_col=1, max_col=ncols):
            for c in row:
                c.border = BOX
                c.alignment = CEN if c.column >= first_day else LEFT
                if c.column == 1:
                    c.font = Font(size=7.5)
                elif c.column == 2:
                    c.font = Font(size=6.5, italic=True)
                else:
                    c.font = Font(size=7)
            ws.row_dimensions[row[0].row].height = 20

        # comments / faults block
        rc = last_task + 2
        ws.cell(row=rc, column=1, value="Comments, faults and corrective action:").font = Font(bold=True, size=8.5)
        for rr in range(rc + 1, rc + 4):
            ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=ncols)
            for k in range(1, ncols + 1):
                ws.cell(row=rr, column=k).border = BOX
            ws.row_dimensions[rr].height = 16

        rs = rc + 5
        ws.cell(row=rs, column=1, value="Reviewed by (section head):").font = Font(bold=True, size=8.5)
        ws.cell(row=rs, column=2, value="Name / signature / date").font = Font(size=8)
        ws.merge_cells(start_row=rs, start_column=2, end_row=rs, end_column=8)
        ws.cell(row=rs, column=2).border = BOX

        # widths
        ws.column_dimensions["A"].width = 42
        ws.column_dimensions["B"].width = 16
        for d in range(first_day, last_day + 1):
            ws.column_dimensions[get_column_letter(d)].width = 2.6
        ws.column_dimensions[get_column_letter(ncols)].width = 7

        ws.freeze_panes = ws.cell(row=hr + 1, column=first_day)
        setup_print(ws, ncols)

    # ---- Pima CD4 register: one year-long sheet, not twelve monthly ones,
    #      because the instrument is run when a CD4 is requested rather than daily.
    ws = wb.create_sheet("Pima CD4 register")
    PCOLS = ["Date", "Site", "Cartridge lot / expiry", "Control result",
             "In / out 2 SD", "Instrument check", "Temp \u00b0C",
             "Patient runs", "Initials", "Comments"]
    ncols = len(PCOLS)

    head(ws, "ALERE PIMA CD4 ANALYSER \u2013 DAILY CHECK AND RUN REGISTER",
         f"RliDHL-ADM-SOP-058  \u2022  one line per day the instrument is used, "
         f"whole year on one sheet  \u2022  {YEAR}", ncols)

    id_block(ws, 5, [
        ("Analyser", "Alere Pima CD4", 1),
        ("Serial no.", "PIMA-D-005378", 1),
        ("Asset no.", "RULIDH/LAB/ME/0485", 1),
        ("Location", "Hematology Room", 1),
    ], ncols)
    id_block(ws, 6, [
        ("Stored at", "Hematology Room", 1),
        ("Used at", "Hematology Room / clinic / health centre \u2013 write the site", 3),
    ], ncols)

    hr = 8
    for i, h in enumerate(PCOLS, 1):
        ws.cell(row=hr, column=i, value=h)
    style_header(ws, hr, ncols, height=34)

    r = hr + 1
    for _ in range(60):
        for k in range(1, ncols + 1):
            c = ws.cell(row=r, column=k)
            c.border = BOX
            c.font = Font(size=8)
            c.alignment = CEN if k in (1, 5, 7, 8, 9) else LEFT
            if k in (4, 6):
                pass
        r += 1
    last = r - 1

    # control failure / abstention block
    rc = last + 2
    ws.cell(row=rc, column=1, value="Runs rejected, aborted or repeated, with the "
                                    "reason and the action taken:").font = Font(bold=True, size=8.5)
    for rr in range(rc + 1, rc + 5):
        ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=ncols)
        for k in range(1, ncols + 1):
            ws.cell(row=rr, column=k).border = BOX
        ws.row_dimensions[rr].height = 16

    rs = rc + 6
    ws.cell(row=rs, column=1, value="Reviewed by (section head):").font = Font(bold=True, size=8.5)
    ws.cell(row=rs, column=2, value="Name / signature / date").font = Font(size=8)
    ws.merge_cells(start_row=rs, start_column=2, end_row=rs, end_column=6)
    ws.cell(row=rs, column=2).border = BOX

    widths = [10, 14, 20, 16, 12, 14, 8, 10, 9, 34]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    setup_print(ws, ncols)

    # ---- instructions sheet
    ws = wb.create_sheet("How to use", 0)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 100
    lines = [
        ("t", "Hematology analyser \u2013 daily maintenance and start-up log"),
        ("n", "RliDHL-ADM-SOP-058 \u2022 Ruli District Hospital Laboratory \u2022 forms "
              "prepared 14 November 2026"),
        ("b", ""),
        ("h", "What this form is for"),
        ("p", "One sheet per month. It records the start-up checks, the background count, "
              "the internal quality control outcome and the daily care of the analyser, "
              "so that any result produced on a given day can be shown to have come from "
              "an instrument that had passed its checks."),
        ("b", ""),
        ("h", "How to fill it in"),
        ("p", "1.  There are three analysers. The Sysmex XN-330 (serial 17156, asset "
              "RULIDH/LAB/ME/0501) and the Sysmex XQ-320 (serial 12357, asset "
              "RULIDH/LAB/ME/0499) are recorded on the monthly sheets. The Alere Pima CD4 "
              "analyser (serial PIMA-D-005378, asset RULIDH/LAB/ME/0485) is recorded on "
              "the \u2018Pima CD4 register\u2019 sheet, because it is run when a CD4 is "
              "requested rather than every working day. They are not interchangeable "
              "records: tick the box at the head of the monthly sheet for the Sysmex "
              "instrument the sheet belongs to, and keep one set of sheets per instrument. "
              "If the reagent or control lot changes during the month, write the new lot "
              "and the date of change in the comments box."),
        ("p", "1a. The Pima register carries one line for each day the instrument is used. "
              "Write the site, because the instrument is portable and a control run in the "
              "laboratory does not cover a run performed at a clinic or health centre. "
              "Write the number of patient runs, not the results themselves \u2013 those "
              "belong in the CD4 register of results."),
        ("p", "2.  Each working day, tick the box for every task performed."),
        ("p", "3.  In the shaded yellow cells, write the actual value: the background "
              "count, the instrument temperature and the initials of the person who "
              "performed the checks."),
        ("p", "4.  If any check fails, do not release patient results. Write what happened "
              "and what was done in the comments box, and inform the section head."),
        ("p", "5.  The section head signs the bottom of the sheet at the end of the month."),
        ("p", "6.  Print one sheet per month and keep it at the bench. A completed "
              "monthly sheet is filed in 6. Equipment, Stock and Suppliers > 7. Preventive "
              "maintenance and temperature logs and kept for five years."),
        ("b", ""),
        ("h", "Do not release results when"),
        ("p", "\u2022  the background count is above the limit printed in the operator "
              "manual for that parameter"),
        ("p", "\u2022  a control result is outside its assigned mean \u00b1 2 standard "
              "deviations and the repeat has not resolved it"),
        ("p", "\u2022  there is a clot, a short sample or a repeated aspiration error"),
        ("p", "\u2022  the analyser has an unresolved pressure, fluidic or temperature "
              "error"),
        ("b", ""),
        ("h", "Only these three analysers are in service"),
        ("p", "The KX-21N, XS-500i, Pochi and Humacount 5 have been decommissioned. Do not "
              "open a sheet for them and do not record maintenance against them. If an "
              "analyser is withdrawn, close its sheet and mark the instrument out of "
              "service on the inventory."),
        ("b", ""),
        ("h", "Calibration is not recorded on this form"),
        ("p", "Calibration and verification are recorded on a separate calibration record, "
              "because they happen a few times a year rather than daily. Note the "
              "calibration date in the comments box when it changes."),
    ]
    r = 1
    for kind, txt in lines:
        c = ws.cell(row=r, column=2, value=txt)
        if kind == "t":
            c.font = Font(bold=True, size=13, color=NAVY)
        elif kind == "h":
            c.font = Font(bold=True, size=10, color=NAVY)
        elif kind == "n":
            c.font = Font(italic=True, size=8.5, color="595959")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        else:
            c.font = Font(size=9.5)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1

    wb.save(os.path.join(OUT, "Form RliDHL-ADM-SOP-058-F01 - Hematology analyser daily maintenance log.xlsx"))


# =====================================================================
# 2. GENEXPERT DAILY PM LOG (Cepheid model)
# =====================================================================
def genexpert_log():
    wb = Workbook()
    wb.remove(wb.active)

    for mnum, mname in MONTHS:
        ws = wb.create_sheet(mname[:3])
        ndays = calendar.monthrange(YEAR, mnum)[1]
        first_day = 3
        last_day = first_day + ndays - 1
        ncols = last_day + 1
        head(ws, "GENEXPERT Dx SYSTEM \u2013 MAINTENANCE LOG",
             f"{mname} {YEAR}  \u2022  RliDHL-ADM-SOP-059  \u2022  modelled on Cepheid "
             f"document 302-8386 Rev. C", ncols)

        id_block(ws, 4, [
            ("Institution", "Ruli District Hospital Laboratory", 2),
            ("GeneXpert serial no.", "", 1),
        ], ncols)
        id_block(ws, 5, [
            ("Installation date", "", 1),
            ("Last calibration check date", "", 1),
            ("Number of modules", "", 1),
        ], ncols)

        hr = 7
        ws.cell(row=hr, column=1, value="Frequency")
        ws.cell(row=hr, column=2, value="Maintenance task")
        for d in range(ndays):
            ws.cell(row=hr, column=first_day + d, value=d + 1)
        style_header(ws, hr, ncols, height=26)

        GROUPS = [
            ("Daily", GREEN, [
                "Clean work area",
                "Discard used cartridges",
                "Close all module doors",
                "Dust cover fitted when not in use",
            ]),
            ("Weekly", YELLOW, [
                "Clean fan prefilter",
                "Power down instrument and computer, then restart",
            ]),
            ("Monthly", "DDEBF7", [
                "Clean I-CORE with I-CORE brush",
                "Clean plunger rods (software: Plunger Maintenance)",
                "Clean cartridge bay interior, all modules",
                "Clean instrument surfaces",
                "Clean module PCR tube slots",
                "Clean fan filters",
                "Archive and purge tests",
                "Back up database",
            ]),
            ("Quarterly", RED, [
                "Replace fan filters and prefilters",
                "Review system log report",
                "Confirm no module near calibration limit",
            ]),
            ("Yearly", "E4DFEC", [
                "Annual instrument maintenance with Xpert Check",
                "Calibrate each module (or at 2,000 tests)",
            ]),
        ]
        r = hr + 1
        for freq, color, tasks in GROUPS:
            start = r
            for t in tasks:
                ws.cell(row=r, column=2, value=t)
                for d in range(first_day, last_day + 1):
                    ws.cell(row=r, column=d)
                r += 1
            # merged frequency label
            ws.merge_cells(start_row=start, start_column=1, end_row=r - 1, end_column=1)
            c = ws.cell(row=start, column=1, value=freq)
            c.font = Font(bold=True, size=8)
            c.alignment = CEN
            c.fill = PatternFill("solid", fgColor=color)

        # initials row
        ws.cell(row=r, column=1, value="")
        ws.cell(row=r, column=2, value="Technician initials (two letters)")
        for d in range(first_day, last_day + 1):
            c = ws.cell(row=r, column=d)
            c.fill = PatternFill("solid", fgColor=YELLOW)
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=GREY)
        last_row = r

        for row in ws.iter_rows(min_row=hr + 1, max_row=last_row,
                                min_col=1, max_col=ncols):
            for c in row:
                c.border = BOX
                if c.column >= first_day:
                    c.alignment = CEN
                    c.font = Font(size=7)
            ws.row_dimensions[row[0].row].height = 18
        ws.row_dimensions[last_row].height = 22
        ws.cell(row=last_row, column=2).font = Font(bold=True, size=7.5)
        ws.cell(row=last_row, column=2).alignment = LEFT

        # module notes
        rn = last_row + 2
        ws.cell(row=rn, column=1, value="Module calibration status and notes").font = Font(bold=True, size=8.5)
        for rr in range(rn + 1, rn + 4):
            ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=ncols)
            for k in range(1, ncols + 1):
                ws.cell(row=rr, column=k).border = BOX
            ws.row_dimensions[rr].height = 16

        rc = rn + 5
        ws.cell(row=rc, column=1, value="Comments, errors and corrective action:").font = Font(bold=True, size=8.5)
        for rr in range(rc + 1, rc + 4):
            ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=ncols)
            for k in range(1, ncols + 1):
                ws.cell(row=rr, column=k).border = BOX
            ws.row_dimensions[rr].height = 16

        rs = rc + 5
        ws.cell(row=rs, column=1, value="Reviewed by (molecular section head):").font = Font(bold=True, size=8.5)
        ws.merge_cells(start_row=rs, start_column=2, end_row=rs, end_column=8)
        ws.cell(row=rs, column=2, value="Name / signature / date").font = Font(size=8)
        ws.cell(row=rs, column=2).border = BOX

        ws.column_dimensions["A"].width = 10
        ws.column_dimensions["B"].width = 38
        for d in range(first_day, last_day + 1):
            ws.column_dimensions[get_column_letter(d)].width = 2.6

        ws.freeze_panes = ws.cell(row=hr + 1, column=first_day)
        setup_print(ws, ncols)

    # ---- module calibration register (annual, permanent)
    ws = wb.create_sheet("Module calibration")
    head(ws, "GENEXPERT MODULE CALIBRATION REGISTER",
         "One row per module. A module may be used for patient testing only while its "
         "calibration is current.", 10)
    hr = 4
    cols = ["Module no.", "Module serial no.", "Installation date",
            "Last calibration date", "Kit lot", "Kit expiry",
            "Tests since calibration", "Calibration due (date or 2,000 tests)",
            "Status", "Certificate filed"]
    for i, c in enumerate(cols, 1):
        ws.cell(row=hr, column=i, value=c)
    style_header(ws, hr, 10, height=40)

    dv = DataValidation(type="list",
                        formula1='"In use,Due soon,Overdue,Out of service"',
                        allow_blank=True)
    ws.add_data_validation(dv)

    for r in range(hr + 1, hr + 17):
        ws.cell(row=r, column=1, value=r - hr)
        for c in range(1, 11):
            ws.cell(row=r, column=c).border = BOX
            ws.cell(row=r, column=c).alignment = CEN
            ws.cell(row=r, column=c).font = Font(size=9)
        ws.row_dimensions[r].height = 20
    dv.add(f"I{hr+1}:I{hr+16}")

    widths = [9, 18, 14, 16, 12, 12, 16, 26, 14, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    note = hr + 18
    ws.cell(row=note, column=1,
            value="Calibration interval: once a year, or after 2,000 tests on that "
                  "module, whichever comes first. Record the earlier of the two dates in "
                  "column H. A module whose calibration has expired is marked Overdue "
                  "and is not used for patient testing.").font = Font(italic=True, size=8.5)
    ws.merge_cells(start_row=note, start_column=1, end_row=note, end_column=10)
    ws.cell(row=note, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[note].height = 30
    setup_print(ws, 10)

    # ---- instructions
    ws = wb.create_sheet("How to use", 0)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 100
    lines = [
        ("t", "GeneXpert Dx System \u2013 maintenance log"),
        ("n", "RliDHL-ADM-SOP-059 \u2022 modelled on the Cepheid GeneXpert System "
              "Maintenance Log, document 302-8386 Rev. C \u2022 prepared 14 November 2026"),
        ("b", ""),
        ("h", "Structure"),
        ("p", "There is one sheet per month, plus a permanent module calibration register "
              "and a separate quarterly and yearly record. The task list follows Cepheid's "
              "own maintenance log so that a Cepheid engineer, an assessor or a "
              "supervisor can compare the two directly."),
        ("b", ""),
        ("h", "How to fill it in"),
        ("p", "1.  Complete the header once per month: institution, instrument serial "
              "number, installation date, date of the last calibration check and the "
              "number of modules."),
        ("p", "2.  Each day, tick the box under the date for every task performed, and "
              "write your two-letter initials in the bottom row."),
        ("p", "3.  Daily tasks are performed every testing day. Weekly tasks once a week. "
              "Monthly tasks once a month. Quarterly and yearly tasks when they fall due, "
              "which is why they appear only in the quarters and months in which they "
              "occur."),
        ("p", "4.  Record every error, failed run and corrective action in the comments "
              "box, with the module number."),
        ("p", "5.  The molecular section head reviews and signs each month."),
        ("b", ""),
        ("h", "The one rule that matters most"),
        ("p", "A module is calibrated once a year or after 2,000 tests on that module, "
              "whichever comes first. A module used outside its calibration produces "
              "results that cannot be defended in an assessment or a court, and may void "
              "the Cepheid warranty. Check the calibration register before the first run "
              "of every day."),
        ("b", ""),
        ("h", "Materials"),
        ("p", "\u2022  1:10 dilution of household bleach, about 0.5% available chlorine, "
              "prepared fresh and used within one day"),
        ("p", "\u2022  70% ethanol or 70% isopropyl alcohol"),
        ("p", "\u2022  lint-free wipes and non-cotton swabs"),
        ("p", "\u2022  mild detergent and clean water for the fan filter"),
        ("p", "\u2022  I-CORE cleaning brush and the Cepheid fan filters"),
        ("p", "\u2022  disposable gloves and eye protection"),
        ("b", ""),
        ("h", "Do not"),
        ("p", "\u2022  touch the slit at the back of the cartridge bay into which the "
              "reaction tube is inserted \u2013 Cepheid warns of this explicitly"),
        ("p", "\u2022  use a stronger chlorine solution than 1:10; it corrodes the "
              "instrument and clouds the optics"),
        ("p", "\u2022  use 100% ethanol"),
        ("p", "\u2022  use cotton swabs; they shed fibres onto the optics"),
        ("p", "\u2022  refit a fan filter before it is completely dry"),
        ("p", "\u2022  leave a used cartridge in a module"),
        ("b", ""),
        ("h", "High-dust environments"),
        ("p", "Cepheid states that where dust or air pollution is high, the optics are "
              "cleaned monthly rather than at the longer interval. This laboratory is in "
              "a dusty environment, so the monthly sheet includes the I-CORE optics "
              "cleaning. If the laboratory moves to a cleaner site, the frequency may be "
              "reviewed, but not before the change is recorded."),
        ("b", ""),
        ("h", "Retention"),
        ("p", "Completed monthly sheets and the calibration register are kept for five "
              "years, or for the life of the module plus five years in the case of the "
              "calibration register, in 6. Equipment, Stock and Suppliers > 7. Preventive "
              "maintenance and temperature logs."),
    ]
    r = 1
    for kind, txt in lines:
        c = ws.cell(row=r, column=2, value=txt)
        if kind == "t":
            c.font = Font(bold=True, size=13, color=NAVY)
        elif kind == "h":
            c.font = Font(bold=True, size=10, color=NAVY)
        elif kind == "n":
            c.font = Font(italic=True, size=8.5, color="595959")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        else:
            c.font = Font(size=9.5)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1

    wb.save(os.path.join(OUT, "Form RliDHL-ADM-SOP-059-F01 - GeneXpert maintenance log.xlsx"))


# =====================================================================
# 3. TEMPERATURE MONITORING
# =====================================================================
def temperature_log():
    wb = Workbook()
    wb.remove(wb.active)

    # device register
    ws = wb.create_sheet("Device register")
    head(ws, "TEMPERATURE MONITORING \u2013 DEVICE REGISTER",
         "Register each refrigerator, freezer, cold box and air-conditioned room before logging "
         "temperatures for it.", 9)
    hr = 4
    cols = ["No.", "Device / room", "Location", "Asset no.",
            "Required range", "Thermometer or logger ID",
            "Logger calibrated (date)", "Responsible person", "Monitoring frequency"]
    for i, c in enumerate(cols, 1):
        ws.cell(row=hr, column=i, value=c)
    style_header(ws, hr, 9, height=40)

    EXAMPLES = [
        ("Refrigerator \u2013 BB R625 S", "Biochemistry Room",
         "RBC/RCBT.RW/GV/FR001/19", "2 \u00b0C to 8 \u00b0C", "", "", "", "Twice daily"),
        ("Refrigerator \u2013 0914327-03", "Biochemistry Room",
         "RULIDH/LAB/ME/0106", "2 \u00b0C to 8 \u00b0C", "", "", "", "Twice daily"),
        ("Refrigerator \u2013 FIOCCHETTI", "TB Preparation Room",
         "RULIDH/LAB/ME/0105", "2 \u00b0C to 8 \u00b0C", "", "", "", "Twice daily"),
        ("Freezer", "fill in \u2013 acquired 11/08/2026",
         "not yet on inventory", "-20 \u00b0C \u00b1 5 \u00b0C", "", "", "", "Twice daily"),
        ("Cold box \u2013 sample transport", "Reception", "", "2 \u00b0C to 8 \u00b0C",
         "", "", "", "At departure and arrival"),
        ("Room \u2013 Hematology", "Hematology Room", "", "18 \u00b0C to 25 \u00b0C",
         "", "", "", "Daily"),
        ("Room \u2013 Biochemistry", "Biochemistry Room", "", "18 \u00b0C to 25 \u00b0C",
         "", "", "", "Daily"),
        ("Room \u2013 TB testing", "TB Testing Room", "", "18 \u00b0C to 25 \u00b0C",
         "", "", "", "Daily"),
        ("Room \u2013 TB preparation", "TB Preparation Room", "",
         "18 \u00b0C to 25 \u00b0C", "", "", "", "Daily"),
    ]
    r = hr + 1
    for i, ex in enumerate(EXAMPLES, 1):
        ws.cell(row=r, column=1, value=i)
        for j, v in enumerate(ex, 2):
            ws.cell(row=r, column=j, value=v)
        r += 1
    for r2 in range(r, r + 8):
        ws.cell(row=r2, column=1, value=r2 - hr)
    for row in ws.iter_rows(min_row=hr + 1, max_row=r + 7, min_col=1, max_col=9):
        for c in row:
            c.border = BOX
            c.alignment = CEN if c.column == 1 else LEFT
            c.font = Font(size=9)
        ws.row_dimensions[row[0].row].height = 20

    widths = [6, 24, 20, 12, 22, 20, 18, 22, 18]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    note = r + 9
    ws.cell(row=note, column=1,
            value="Ranges: refrigerator 2\u20138 \u00b0C, freezer -20 \u00b0C \u00b1 5 "
                  "\u00b0C, cold box 2\u20138 \u00b0C in transit, rooms 18\u201325 "
                  "\u00b0C and below 70% relative humidity, per RliDHL-ADM-SOP-056. "
                  "The freezer was acquired on 11 August 2026 and is not yet on the "
                  "hospital equipment inventory; write its model, serial number and asset "
                  "code here as soon as they are assigned, and add it to the inventory at "
                  "the next revision.").font = Font(italic=True, size=8.5)
    ws.merge_cells(start_row=note, start_column=1, end_row=note, end_column=9)
    ws.cell(row=note, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[note].height = 30
    setup_print(ws, 9)

    # monthly sheets
    for mnum, mname in MONTHS:
        ws = wb.create_sheet(mname[:3])
        ndays = calendar.monthrange(YEAR, mnum)[1]
        ncols = 2 + ndays + 3
        head(ws, "TEMPERATURE MONITORING RECORD",
             f"{mname} {YEAR}  \u2022  refrigerators, freezer, cold box and rooms  \u2022  "
             f"RliDHL-ADM-SOP-056", ncols)

        id_block(ws, 4, [
            ("Month", f"{mname} {YEAR}", 2),
            ("Thermometer / logger ID", "", 2),
        ], ncols)

        hr = 6
        ws.cell(row=hr, column=1, value="Device / room")
        ws.cell(row=hr, column=2, value="Required range")
        for d in range(ndays):
            ws.cell(row=hr, column=3 + d, value=d + 1)
        ws.cell(row=hr, column=ncols - 2, value="Readings\nout of range")
        ws.cell(row=hr, column=ncols - 1, value="\\n")
        ws.cell(row=hr, column=ncols, value="\\n")
        style_header(ws, hr, ncols, height=30)

        DEVICES = [
            ("Refrigerator \u2013 BB R625 S", "2\u20138 \u00b0C"),
            ("Refrigerator \u2013 0914327-03", "2\u20138 \u00b0C"),
            ("Refrigerator \u2013 FIOCCHETTI", "2\u20138 \u00b0C"),
            ("Freezer", "-20 \u00b0C \u00b1 5"),
            ("Cold box \u2013 transport", "2\u20138 \u00b0C"),
            ("Room \u2013 Hematology", "18\u201325 \u00b0C"),
            ("Room \u2013 Biochemistry", "18\u201325 \u00b0C"),
            ("Room \u2013 TB testing", "18\u201325 \u00b0C"),
            ("Room \u2013 TB preparation", "18\u201325 \u00b0C"),
            ("", ""),
            ("", ""),
        ]
        r = hr + 1
        for name, rng in DEVICES:
            ws.cell(row=r, column=1, value=name)
            ws.cell(row=r, column=2, value=rng)
            for d in range(3, 3 + ndays):
                c = ws.cell(row=r, column=d)
                c.fill = PatternFill("solid", fgColor=YELLOW)
            r += 1
        # AM / PM split rows
        ws.cell(row=r, column=1, value="Comments")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=ncols)
        ws.cell(row=r, column=1).fill = PatternFill("solid", fgColor=GREY)
        ws.cell(row=r, column=1).font = Font(bold=True, size=8.5)
        ws.cell(row=r, column=3).border = BOX
        comments_row = r
        for rr in range(r + 1, r + 3):
            ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=ncols)
            for k in range(1, ncols + 1):
                ws.cell(row=rr, column=k).border = BOX
            ws.row_dimensions[rr].height = 16

        for row in ws.iter_rows(min_row=hr + 1, max_row=comments_row,
                                min_col=1, max_col=ncols):
            for c in row:
                c.border = BOX
                if c.column >= 3:
                    c.alignment = CEN
        for rr in range(hr + 1, comments_row):
            ws.row_dimensions[rr].height = 20
            ws.cell(row=rr, column=1).font = Font(size=8)
            ws.cell(row=rr, column=1).alignment = LEFT
            ws.cell(row=rr, column=2).font = Font(size=7, italic=True)
            ws.cell(row=rr, column=2).alignment = CEN

        # signature row
        rs = comments_row + 4
        labels = ["Recorded by (initials)", "Reviewed by (section head)", "Date"]
        spans = [(1, 2), (3, 5), (6, 7)]
        for (label, (a, b)) in zip(labels, spans):
            c = ws.cell(row=rs, column=a, value=label)
            c.font = Font(bold=True, size=8)
            c.fill = PatternFill("solid", fgColor=GREY)
            c.border = BOX
            if b > a:
                ws.merge_cells(start_row=rs, start_column=a, end_row=rs, end_column=b)
            for k in range(a, b + 1):
                ws.cell(row=rs, column=k).border = BOX
            ws.cell(row=rs, column=a).alignment = LEFT

        ws.column_dimensions["A"].width = 22
        ws.column_dimensions["B"].width = 14
        for d in range(3, 3 + ndays):
            ws.column_dimensions[get_column_letter(d)].width = 2.4
        for k in range(ncols - 2, ncols + 1):
            ws.column_dimensions[get_column_letter(k)].width = 7

        ws.freeze_panes = ws.cell(row=hr + 1, column=3)
        setup_print(ws, ncols)

    # 2-column AM/PM variant instructions
    ws = wb.create_sheet("How to use", 0)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 100
    lines = [
        ("t", "Temperature monitoring \u2013 refrigerators, freezer, cold box and rooms"),
        ("n", "RliDHL-ADM-SOP-056 \u2022 Ruli District Hospital Laboratory \u2022 forms "
              "prepared 14 November 2026"),
        ("b", ""),
        ("h", "Sheets in this workbook"),
        ("p", "Device register \u2013 fill this in once. It is pre-filled with every "
              "unit the laboratory actually holds: three refrigerators, the freezer, the "
              "sample-transport cold box and four rooms. Add a unit only when it exists "
              "and has been assigned a required range."),
        ("p", "Jan to Dec \u2013 one monitoring sheet per month."),
        ("b", ""),
        ("h", "How to record"),
        ("p", "1.  Write the temperature in the yellow box for the day, in \u00b0C, to "
              "one decimal place."),
        ("p", "2.  For devices read twice a day, write both readings in the same box, "
              "separated by a slash, for example 4.2/5.1 for morning and afternoon."),
        ("p", "3.  Write your initials in the comments row at the end of the week."),
        ("p", "4.  Circle or highlight any reading outside the required range and write "
              "the action taken in the comments box."),
        ("p", "5.  The section head signs at the bottom of the sheet each month."),
        ("b", ""),
        ("h", "A newly acquired unit must be verified before it holds anything"),
        ("p", "The freezer arrived on 11 August 2026 from a health centre. An instrument "
              "that has been moved is not the same instrument until it has been shown to "
              "hold temperature. Before it is trusted with specimens or reagents: let it "
              "run empty for 24 hours, then record the temperature at start and end of day "
              "for a full week with a calibrated thermometer or a logger, confirm it holds "
              "-20 \u00b0C \u00b1 5 \u00b0C across that week, and record the "
              "verification here and in the comments box of the first monthly sheet."),
        ("b", ""),
        ("h", "If a reading is out of range"),
        ("p", "Do not discard the contents on the basis of the reading alone. Move them "
              "to a verified backup unit or a cold box, record the duration and the "
              "extent of the excursion, assess each reagent and specimen against its "
              "storage specification, quarantine anything outside specification, and "
              "inform the Laboratory Quality Manager the same day. The full procedure is in "
              "RliDHL-ADM-SOP-056, section 6.2."),
        ("b", ""),
        ("h", "Rooms"),
        ("p", "Rooms are recorded because humidity and temperature control the growth of "
              "fungus on microscope optics and the stability of reagents. The range is "
              "18 to 25 \u00b0C and below 70% relative humidity. If the laboratory has a "
              "hygrometer, add the humidity reading to the comments box."),
        ("b", ""),
        ("h", "Minimum expectations"),
        ("p", "\u2022  Refrigerators and the freezer: twice every working day."),
        ("p", "\u2022  Rooms: once every working day."),
        ("p", "\u2022  Cold boxes: at departure and at arrival."),
        ("p", "\u2022  Data loggers: downloaded and filed at least monthly, in addition "
              "to the manual readings."),
        ("b", ""),
        ("h", "Retention"),
        ("p", "Five years, in 6. Equipment, Stock and Suppliers > 7. Preventive "
              "maintenance and temperature logs. The device register is permanent."),
    ]
    r = 1
    for kind, txt in lines:
        c = ws.cell(row=r, column=2, value=txt)
        if kind == "t":
            c.font = Font(bold=True, size=13, color=NAVY)
        elif kind == "h":
            c.font = Font(bold=True, size=10, color=NAVY)
        elif kind == "n":
            c.font = Font(italic=True, size=8.5, color="595959")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        else:
            c.font = Font(size=9.5)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1

    wb.save(os.path.join(OUT, "Form RliDHL-ADM-SOP-056-F01 - Temperature monitoring fridges freezers and rooms.xlsx"))


if __name__ == "__main__":
    hematology_log()
    genexpert_log()
    temperature_log()
    print("done")
