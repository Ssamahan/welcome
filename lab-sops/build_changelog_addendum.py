#!/usr/bin/env python3
"""
Change-log addendum for the November 2026 equipment-maintenance block.
Same column shape as the 'Start here' sheet of 00 - Change log, coding and
ISO 15189 gaps.xlsx, so the rows paste straight in.
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

OUT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(OUT, "00 - Change log ADDENDUM - equipment maintenance block (Nov 2026).xlsx")

NAVY = "1F4E79"
GREY = "EDEDED"
THIN = Side(style="thin", color="A6A6A6")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = Workbook()
ws = wb.active
ws.title = "New documents"

ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 44
ws.column_dimensions["C"].width = 24
ws.column_dimensions["D"].width = 26
ws.column_dimensions["E"].width = 60
ws.column_dimensions["F"].width = 26
ws.column_dimensions["G"].width = 50

r = 1
ws.cell(row=r, column=2, value="RULI DISTRICT HOSPITAL \u2013 LABORATORY DEPARTMENT\nP.O. BOX 1285 KIGALI  \u2022  Tel: (+250) 0781 316 368  \u2022  ruli.hospital@moh.gov.rw  \u2022  rulihospital.rw")
ws.cell(row=r, column=2).font = Font(size=8.5, color="595959")
ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True)
ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
ws.row_dimensions[r].height = 26
r += 1
ws.cell(row=r, column=2, value="Change log addendum \u2013 equipment maintenance block, November 2026")
ws.cell(row=r, column=2).font = Font(bold=True, size=13, color=NAVY)
r += 1
ws.cell(row=r, column=2,
        value="Companion to 00 - Change log, coding and ISO 15189 gaps.xlsx. Prepared 14 "
              "November 2026.")
ws.cell(row=r, column=2).font = Font(italic=True, size=8.5, color="595959")
r += 2

intro = [
    "Seven SOPs and three forms were created on 14 November 2026 to close gaps in "
    "equipment maintenance. They are first issues: there is no previous version, so the "
    "\u2018Old number\u2019 column is empty and there is nothing to mark obsolete.",
    "The main change log is an Office file and could not be written to directly without "
    "risk of damaging the sheets it already holds (Changes in every SOP, Changes by SOP, "
    "To confirm, Coding rules, Coding crosswalk, ISO 15189 gaps, Sources). This sheet holds "
    "the rows in the same column order as its \u2018Start here\u2019 sheet so they can be "
    "typed or pasted in.",
]
for line in intro:
    ws.cell(row=r, column=2, value=line)
    ws.cell(row=r, column=2).font = Font(size=9.5)
    ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    ws.row_dimensions[r].height = 30
    r += 1

r += 1
HDR = ["N\u00b0", "Revised SOP", "Old number", "New number", "What is new",
       "Need your answer", "File"]
for i, h in enumerate(HDR, 2):
    c = ws.cell(row=r, column=i, value=h)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.font = Font(bold=True, size=9, color="FFFFFF")
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BOX
ws.row_dimensions[r].height = 26
r += 1

ROWS = [
    ("53", "Use, Care and Preventive Maintenance of the Microscope", "\u2014",
     "RliDHL-ADM-SOP-053-VERS-001",
     "New SOP. Daily care, objective and condenser cleaning, Koehler alignment, oil "
     "immersion discipline, bulb and fuse replacement, annual service. Closes a gap: the "
     "laboratory had RliDHL-PAR-SOP-017 on using a microscope, but nothing on maintaining "
     "one.",
     "\u2014",
     "RliDHL-ADM-SOP-053-VERS-001 - Use, Care and Preventive Maintenance of the "
     "Microscope.docx"),
    ("54", "Operation, Care and Preventive Maintenance of the Centrifuge", "\u2014",
     "RliDHL-ADM-SOP-054-VERS-001",
     "New SOP. Balancing, lid interlock, brush wear, speed and timer verification, spill "
     "and broken-tube decontamination, service interval.",
     "\u2014",
     "RliDHL-ADM-SOP-054-VERS-001 - Operation, Care and Preventive Maintenance of the "
     "Centrifuge.docx"),
    ("55", "Operation, Care and Preventive Maintenance of the Water Bath", "\u2014",
     "RliDHL-ADM-SOP-055-VERS-001",
     "New SOP. Daily water change, weekly disinfection, monthly temperature verification "
     "against a calibrated thermometer, fungal and algal control, drain-down procedure.",
     "\u2014",
     "RliDHL-ADM-SOP-055-VERS-001 - Operation, Care and Preventive Maintenance of the "
     "Water Bath.docx"),
    ("56", "Management and Maintenance of Non-Medical Laboratory Equipment", "\u2014",
     "RliDHL-ADM-SOP-056-VERS-001",
     "New SOP. Refrigerators and cold chain, freezer, water distiller and deioniser, air "
     "conditioning, UPS and power protection, fire extinguishers, eye wash and emergency "
     "shower. Includes the temperature-excursion procedure and the device register.",
     "Confirm the required range for the blood bank refrigerator: the SOP uses 2\u20136 "
     "\u00b0C, which is tighter than the 2\u20138 \u00b0C used for reagent fridges.",
     "RliDHL-ADM-SOP-056-VERS-001 - Management and Maintenance of Non-Medical Laboratory "
     "Equipment.docx"),
    ("57", "Maintenance of Laboratory ICT Equipment and the Laboratory Information System",
     "\u2014", "RliDHL-ADM-SOP-057-VERS-001",
     "New SOP. Workstations, server, printers, network, analyser interfaces, backup and "
     "restore with a monthly restore test, access control and password rules, downtime "
     "procedure, data destruction at disposal. Written against ISO 15189:2022 7.4.3 and "
     "8.4.",
     "\u2014",
     "RliDHL-ADM-SOP-057-VERS-001 - Maintenance of Laboratory ICT Equipment and the "
     "Laboratory Information System.docx"),
    ("58", "Use, Care and Preventive Maintenance of Hematology Analysers", "\u2014",
     "RliDHL-ADM-SOP-058-VERS-001",
     "New SOP, covering the three analysers in service in the Hematology section: Sysmex "
     "XN-330 (serial 17156, asset RULIDH/LAB/ME/0501), Sysmex XQ-320 (serial 12357, asset "
     "RULIDH/LAB/ME/0499) and the Alere Pima CD4 (serial PIMA-D-005378, asset "
     "RULIDH/LAB/ME/0485). Daily start-up, background count, IQC before patient samples, "
     "aspiration probe care, cleaning cycles, calibration and its verification, service "
     "and the fault escalation route. The Pima has its own start-up clause, 6.3.1, "
     "because it has no fluid system or background count, and its cartridge-lot and "
     "portable-use rules are stated separately. Instrument limits are deferred to each "
     "operator manual. Section 3.1 records the withdrawal of the KX-21N, XS-500i, Pochi "
     "and Humacount 5 and states that this SOP does not apply to them.",
     "The CD4 analyser was added to 058 at the Laboratory Manager's instruction of "
     "November 2026, since the Pima is held in the Hematology section. Confirm whether the "
     "CD4 bench SOP is to be merged into 058 or kept as a separate bench SOP; 058 "
     "currently cites it as a supporting document.",
     "RliDHL-ADM-SOP-058-VERS-001 - Use, Care and Preventive Maintenance of Hematology "
     "Analysers.docx"),
    ("59", "Use, Care and Preventive Maintenance of the GeneXpert Dx System", "\u2014",
     "RliDHL-ADM-SOP-059-VERS-001",
     "New SOP, written from Cepheid source documents: maintenance presentation 301-7990 "
     "Rev. C, maintenance log 302-8386 Rev. C and Operator Manual Chapter 9. Daily, "
     "weekly, monthly, quarterly and yearly tasks; cleaning agents and their dilutions; "
     "I-CORE, plunger and cartridge-bay cleaning; fan filters and prefilters; monthly "
     "optics cleaning for a high-dust site; module calibration at one year or 2,000 tests, "
     "whichever comes first; Xpert Check; the Cepheid support route.",
     "Confirm the number of modules and the installation date of the instrument, and "
     "whether an Xpert Check kit is on the annual order.",
     "RliDHL-ADM-SOP-059-VERS-001 - Use, Care and Preventive Maintenance of the GeneXpert "
     "Dx System.docx"),
]

for row in ROWS:
    for i, v in enumerate(row, 2):
        c = ws.cell(row=r, column=i, value=v)
        c.font = Font(size=8.5, bold=(i == 2))
        c.alignment = Alignment(wrap_text=True, vertical="top",
                               horizontal="center" if i == 2 else "left")
        c.border = BOX
    ws.row_dimensions[r].height = 66
    r += 1

# forms block
r += 1
ws.cell(row=r, column=2, value="Forms issued with these SOPs")
ws.cell(row=r, column=2).font = Font(bold=True, size=11, color=NAVY)
r += 1
HDR2 = ["N\u00b0", "Form", "Supports", "Format", "What it records", "Frequency", "File"]
for i, h in enumerate(HDR2, 2):
    c = ws.cell(row=r, column=i, value=h)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.font = Font(bold=True, size=9, color="FFFFFF")
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BOX
ws.row_dimensions[r].height = 26
r += 1

FORMS = [
    ("F01", "RliDHL-ADM-SOP-056-F01", "056",
     "Excel, device register plus twelve monthly sheets, printable A4 landscape",
     "Temperature of every refrigerator, freezer, cold box and room, twice daily for "
     "fridges and daily for rooms, with a device register carrying each required range.",
     "Twice daily / daily",
     "Form RliDHL-ADM-SOP-056-F01 - Temperature monitoring fridges freezers and rooms.xlsx"),
    ("F01", "RliDHL-ADM-SOP-058-F01", "058",
     "Excel, twelve monthly sheets plus a year-long CD4 register, printable A4 landscape",
     "Start-up, background count, IQC outcome, probe inspection, shutdown and operator "
     "initials for each Sysmex analyser, one row per task and one column per day; the Pima "
     "CD4 has its own register carrying date, site, cartridge lot, control outcome and "
     "number of patient runs, because it is portable and run on request rather than daily.",
     "Daily",
     "Form RliDHL-ADM-SOP-058-F01 - Hematology analyser daily maintenance log.xlsx"),
    ("F01", "RliDHL-ADM-SOP-059-F01", "059",
     "Excel, twelve monthly sheets plus a permanent module calibration register",
     "The Cepheid task list \u2013 daily, weekly, monthly, quarterly and yearly \u2013 with "
     "a two-letter initials row, plus module calibration date, kit lot and tests since "
     "calibration.",
     "Daily to annual",
     "Form RliDHL-ADM-SOP-059-F01 - GeneXpert maintenance log.xlsx"),
]
for row in FORMS:
    for i, v in enumerate(row, 2):
        c = ws.cell(row=r, column=i, value=v)
        c.font = Font(size=8.5, bold=(i == 3))
        c.alignment = Alignment(wrap_text=True, vertical="top",
                               horizontal="center" if i == 2 else "left")
        c.border = BOX
    ws.row_dimensions[r].height = 58
    r += 1

# closing notes
r += 1
NOTES = [
    ("Coding", "053 to 059 continue the three-digit ADM series in which the biomedical "
               "equipment SOP sits as ADM-008. The management series runs 1 to 52. 053 "
               "onwards was confirmed free against the Master List, the 50-series folder "
               "and the SOP review register before the first file was written. The next "
               "free number is 060."),
    ("Not in the review register", "These seven SOPs are not entered in 00 - SOP review "
                                   "register (due to 31 Mar 2027).xlsx. Their review date "
                                   "is 14 November 2028, which is outside that register's "
                                   "window, and adding them would make its summary counts "
                                   "wrong. Enter them in the register that opens the 2028 "
                                   "review cycle, or track them on this addendum until "
                                   "then."),
    ("Status", "All seven SOPs and all three forms are VERS-001 first issues, effective "
               "14/11/2026, review 14/11/2028. None is in force until the Laboratory "
               "Manager has prepared it, the Laboratory Quality Manager (Jean Paul "
               "NSENGIYUMVA) has reviewed it, and the Director General has approved it by "
               "signing the cover block and the signature page. If signature happens "
               "later, change the effective date in the document, the file name and this "
               "addendum to the date of authorisation."),
    ("Sources and links", "Section 10 of every SOP now carries a numbered reference "
                          "list with a live link wherever a public source exists: ISO 15189:2022 "
                          "(iso.org/standard/76677), WHO Laboratory quality management system "
                          "handbook, WHO Laboratory biosafety manual 4th ed., WHO malaria "
                          "microscopy QA manual, WHO consolidated HIV guidelines, Rwanda Law "
                          "No. 058/2021, ISO/IEC 27001:2022, IEC 61010-2-020:2026, CLSI C24 and "
                          "QMS01, the Cepheid 301-7990 maintenance presentation and the GLI "
                          "Xpert training package. Manufacturer manuals that ship with the "
                          "instrument carry no link and are cited as supplied with it. Two "
                          "references were corrected at the same time: CLSI GP41 was mis-cited "
                          "as a quality-management document when it is Collection of Diagnostic "
                          "Venous Blood Specimens, and replaced by CLSI QMS01; and IEC "
                          "61010-2-020 was cited in its 2016 third edition, which was "
                          "superseded by the fourth edition on 2 September 2026."),
    ("Where the documents sit", "All of them, with the Master List insert and the "
                                "approval tracker, are in 4. Reception > Administration > "
                                "6. Equipment, Stock and Suppliers."),
]
for name, text in NOTES:
    c = ws.cell(row=r, column=2, value=name)
    c.font = Font(bold=True, size=9)
    c.alignment = Alignment(vertical="top")
    c2 = ws.cell(row=r, column=3, value=text)
    c2.font = Font(size=9)
    c2.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=7)
    ws.row_dimensions[r].height = 34
    r += 1

ws.sheet_view.showGridLines = False

wb.save(PATH)
print("written:", PATH)
