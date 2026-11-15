#!/usr/bin/env python3
"""
Master List insert sheet for SOP 053-059 and the three new forms.
Laid out with the same columns as MASTER LIST.docx so the rows can be
pasted straight into the CROSSCUTTING section.
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(OUT, "MASTER LIST insert - SOP 053 to 059 and Forms F01 (Nov 2026).docx")

NAVY = RGBColor(0x1F, 0x4E, 0x79)
GREY = RGBColor(0x59, 0x59, 0x59)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def cell_text(cell, text, bold=False, size=8, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Times New Roman"
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)


def para(doc, text, size=10, bold=False, italic=False, space_before=0,
         space_after=4, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.name = "Times New Roman"
    if color:
        r.font.color.rgb = color
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    return p


doc = Document()

# landscape A4
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
sec.left_margin = sec.right_margin = Cm(1.4)
sec.top_margin = sec.bottom_margin = Cm(1.4)

style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(10)

# ---- header: crest left, Ruli logo right
ASSETS = os.path.join(OUT, "assets")
_logo = doc.add_table(rows=1, cols=2)
_logo.alignment = WD_TABLE_ALIGNMENT.CENTER
_logo.autofit = False
_lw = Cm(12.4)
_logo.columns[0].width = _lw
_logo.columns[1].width = _lw
for _i in (0, 1):
    _logo.cell(0, _i).width = _lw
_p = _logo.cell(0, 0).paragraphs[0]
_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
_p.paragraph_format.space_after = Pt(0)
_p.add_run().add_picture(os.path.join(ASSETS, "rwanda-crest.jpeg"), height=Cm(2.0))
_p = _logo.cell(0, 1).paragraphs[0]
_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
_p.paragraph_format.space_after = Pt(0)
_p.add_run().add_picture(os.path.join(ASSETS, "ruli-hospital.png"), height=Cm(1.88))
_bd = OxmlElement("w:tblBorders")
for _e in ("top", "left", "bottom", "right", "insideH", "insideV"):
    _x = OxmlElement(f"w:{_e}")
    _x.set(qn("w:val"), "none")
    _x.set(qn("w:sz"), "0")
    _bd.append(_x)
_tp = _logo._tbl.tblPr
_lk = _tp.find(qn("w:tblLook"))
if _lk is not None:
    _lk.addprevious(_bd)
else:
    _tp.append(_bd)

para(doc, "REPUBLIC OF RWANDA \u2022 MINISTRY OF HEALTH \u2022 GAKENKE DISTRICT",
     size=8, bold=True, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
para(doc, "RULI DISTRICT HOSPITAL \u2013 LABORATORY DEPARTMENT",
     size=10, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "MASTER LIST \u2013 INSERT SHEET",
     size=15, bold=True, color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "New documents issued 14 November 2026: SOP 053 to 059 and Forms F01",
     size=9.5, italic=True, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

# ---- what this sheet is
para(doc, "What this sheet is", size=11, bold=True, color=NAVY, space_before=4, space_after=3)
para(doc,
     "Seven new standard operating procedures and three new forms were issued on "
     "14 November 2026. The Master List does not yet carry them. This sheet gives the rows "
     "in the same column order as the Master List, so they can be typed or pasted into the "
     "crosscutting section in one action, and carries the same signature block so the "
     "addition is authorised at the same time as the SOPs themselves.",
     space_after=8)

# ---- crosscutting table
para(doc, "A.  CROSSCUTTING STANDARD OPERATING PROCEDURES \u2013 equipment maintenance block",
     size=11, bold=True, color=NAVY, space_before=6, space_after=4)

HDR = ["N\u00b0", "Document Code", "Document Title", "Effective date",
       "Review date", "Locations"]

ROWS = [
    ("53", "RliDHL-ADM-SOP-053-VERS-001",
     "Use, Care and Preventive Maintenance of the Microscope", "14/11/2026",
     "14/11/2028", "RliDHL Office; all bench rooms"),
    ("54", "RliDHL-ADM-SOP-054-VERS-001",
     "Operation, Care and Preventive Maintenance of the Centrifuge", "14/11/2026",
     "14/11/2028", "RliDHL Office; Hematology, Biochemistry, Blood bank"),
    ("55", "RliDHL-ADM-SOP-055-VERS-001",
     "Operation, Care and Preventive Maintenance of the Water Bath", "14/11/2026",
     "14/11/2028", "RliDHL Office; Serology, Blood bank"),
    ("56", "RliDHL-ADM-SOP-056-VERS-001",
     "Management and Maintenance of Non-Medical Laboratory Equipment", "14/11/2026",
     "14/11/2028", "RliDHL Office; all rooms"),
    ("57", "RliDHL-ADM-SOP-057-VERS-001",
     "Maintenance of Laboratory ICT Equipment and the Laboratory Information System",
     "14/11/2026", "14/11/2028", "RliDHL Office; all rooms"),
    ("58", "RliDHL-ADM-SOP-058-VERS-001",
     "Use, Care and Preventive Maintenance of Hematology Analysers", "14/11/2026",
     "14/11/2028", "RliDHL Office; Hematology bench, CD4 bench"),
    ("59", "RliDHL-ADM-SOP-059-VERS-001",
     "Use, Care and Preventive Maintenance of the GeneXpert Dx System", "14/11/2026",
     "14/11/2028", "RliDHL Office; TB room, Molecular"),
]

t = doc.add_table(rows=1, cols=len(HDR))
t.style = "Table Grid"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, h in enumerate(HDR):
    c = t.rows[0].cells[i]
    cell_text(c, h, bold=True, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade(c, "D9E2F3")
for row in ROWS:
    cells = t.add_row().cells
    for i, v in enumerate(row):
        cell_text(cells[i], v, size=8,
                  align=WD_ALIGN_PARAGRAPH.CENTER if i in (0, 3, 4) else WD_ALIGN_PARAGRAPH.LEFT)

widths = [Cm(1.0), Cm(5.6), Cm(9.4), Cm(2.4), Cm(2.4), Cm(6.0)]
for r in t.rows:
    for i, w in enumerate(widths):
        r.cells[i].width = w

# ---- forms table
para(doc, "B.  FORMS \u2013 recorded against the SOP that controls them",
     size=11, bold=True, color=NAVY, space_before=12, space_after=4)

HDR2 = ["Form number", "Form title", "Parent SOP", "Frequency", "Effective date", "Locations"]
ROWS2 = [
    ("RliDHL-ADM-SOP-056-F01",
     "Temperature monitoring: fridges, freezers, cold boxes and rooms",
     "056", "Twice daily / daily", "14/11/2026", "RliDHL Office; all rooms"),
    ("RliDHL-ADM-SOP-058-F01",
     "Hematology analyser daily maintenance and start-up log",
     "058", "Daily", "14/11/2026", "RliDHL Office; Hematology bench"),
    ("RliDHL-ADM-SOP-059-F01",
     "GeneXpert Dx System maintenance log, with module calibration register",
     "059", "Daily to annual", "14/11/2026", "RliDHL Office; TB room"),
]
t2 = doc.add_table(rows=1, cols=len(HDR2))
t2.style = "Table Grid"
for i, h in enumerate(HDR2):
    c = t2.rows[0].cells[i]
    cell_text(c, h, bold=True, size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade(c, "D9E2F3")
for row in ROWS2:
    cells = t2.add_row().cells
    for i, v in enumerate(row):
        cell_text(cells[i], v, size=8,
                  align=WD_ALIGN_PARAGRAPH.CENTER if i in (2, 3, 4) else WD_ALIGN_PARAGRAPH.LEFT)

widths2 = [Cm(4.6), Cm(10.0), Cm(1.8), Cm(3.0), Cm(2.4), Cm(4.8)]
for r in t2.rows:
    for i, w in enumerate(widths2):
        r.cells[i].width = w

# ---- notes
para(doc, "C.  Why each document exists", size=11, bold=True, color=NAVY,
     space_before=12, space_after=4)
NOTES = [
    ("053 Microscope",
     "The laboratory had a bench SOP for using a microscope (RliDHL-PAR-SOP-017) but no "
     "document covering its daily care, the cleaning of the objectives and condenser, the "
     "Koehler alignment, the oil-immersion discipline or the annual service. A microscope "
     "that is not cleaned correctly gives the wrong answer on a malaria slide."),
    ("054 Centrifuge",
     "Balancing, lid interlock, brush wear, speed verification and the log of tubes broken "
     "inside the bowl were all undocumented. A centrifuge that is out of balance or has a "
     "worn brush changes the separation and therefore the result."),
    ("055 Water bath",
     "Used for serology inactivation and for warming reagents. The water is a bacterial "
     "reservoir and the thermometer drifts. Daily water change, weekly disinfection and "
     "monthly temperature verification are now written down."),
    ("056 Non-medical equipment",
     "Refrigerators, freezer, water distiller, air conditioning, UPS, fire extinguishers and "
     "the eye wash. These are the equipment that everything else depends on, and none of "
     "them had a maintenance SOP."),
    ("057 ICT and LIS",
     "Workstations, server, printers, network, analyser interfaces, backup and restore, "
     "access control, the downtime procedure and the destruction of data at disposal. "
     "ISO 15189:2022 clauses 7.4.3 and 8.4 require the information system to be maintained "
     "and protected; it had no procedure."),
    ("058 Hematology analysers",
     "The laboratory runs three analysers in this section: the Sysmex XN-330 (serial "
     "17156) and XQ-320 (serial 12357), both supplied in 2025, and the Alere Pima CD4 "
     "(serial PIMA-D-005378, 2018). Each had a bench SOP for running "
     "samples but none for the daily start-up, the background count, the care of the "
     "aspiration probe, the calibration interval or the service record. Written to cover "
     "all three, with each instrument's own limits left to its operator manual and its "
     "serial and asset code printed in the scope so a record traces to one physical "
     "instrument. The Pima has its own start-up clause (6.3.1) because it has no fluid "
     "system or background count, and is recorded on a separate register page of the "
     "form because it is portable."),
    ("059 GeneXpert Dx System",
     "Written from the Cepheid documents themselves \u2013 the maintenance presentation "
     "301-7990 Rev. C, the maintenance log 302-8386 Rev. C and Chapter 9 of the Operator "
     "Manual \u2013 not from general practice. The module calibration rule (one year or "
     "2,000 tests, whichever comes first) and the monthly optics cleaning for a dusty site "
     "are the two points that matter most for a laboratory in this setting."),
]
for name, text in NOTES:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(name + ".  ")
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.name = "Times New Roman"
    r2 = p.add_run(text)
    r2.font.size = Pt(9.5)
    r2.font.name = "Times New Roman"

# ---- status
para(doc, "D.  Status", size=11, bold=True, color=NAVY, space_before=12, space_after=4)
para(doc,
     "All seven SOPs and all three forms are VERS-001 first issues. The effective date of "
     "14/11/2026 is the proposed date. None of them is in force until the Head of "
     "Laboratory Manager has prepared it, the Laboratory Quality Manager has reviewed it, and the Director "
     "General has approved it by signing the cover block and the signature page. Under "
     "ISO 15189:2022 the approval of a controlled laboratory document rests with the head "
     "of the institution. If signature happens on a later date, the effective date in this "
     "Master List insert, in the SOP cover block and in the file name must be changed to "
     "the date of authorisation. The approval route is tracked in \u201c00 - New SOP "
     "approvals - equipment maintenance block (Nov 2026).xlsx\u201d, in the same folder.",
     space_after=10)

# ---- signature block
para(doc, "E.  Authorisation of this addition to the Master List",
     size=11, bold=True, color=NAVY, space_before=8, space_after=6)

sig = doc.add_table(rows=2, cols=4)
sig.style = "Table Grid"
heads = ["Role", "Name", "Signature", "Date"]
for i, h in enumerate(heads):
    c = sig.rows[0].cells[i]
    cell_text(c, h, bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade(c, "D9E2F3")
roles = ["Prepared by \u2013 Laboratory Manager",
         "Reviewed by \u2013 Laboratory Quality Manager",
         "Approved by \u2013 Director General", ""]
# rebuild with 3 data rows
sig2 = doc.add_table(rows=4, cols=4)
sig2.style = "Table Grid"
for i, h in enumerate(heads):
    c = sig2.rows[0].cells[i]
    cell_text(c, h, bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    shade(c, "D9E2F3")
for r, role in zip(range(1, 4), roles[:3]):
    cell_text(sig2.rows[r].cells[0], role, size=9)
    for i in (1, 2, 3):
        cell_text(sig2.rows[r].cells[i], "", size=9)
    sig2.rows[r].height = Cm(1.0)
for r in sig2.rows:
    for i, w in enumerate([Cm(8.0), Cm(6.0), Cm(6.0), Cm(4.0)]):
        r.cells[i].width = w

# remove the stray two-row table
sig._element.getparent().remove(sig._element)

# ---- footer note
para(doc, "Ruli District Hospital \u2013 Laboratory Department  \u2022  Master List insert  "
          "\u2022  prepared 14 November 2026", size=8, italic=True, color=GREY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14)

doc.save(PATH)
print("written:", PATH)
