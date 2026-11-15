#!/usr/bin/env python3
"""
Builds the approval and issue tracker for the seven new equipment-maintenance SOPs.
These are first issues, so what the laboratory needs is a signature route, not a
review-due entry (they are not due until 14 November 2028).
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(OUT, "00 - New SOP approvals - equipment maintenance block (Nov 2026).xlsx")

HDR_FILL = PatternFill("solid", fgColor="1F4E79")
HDR_FONT = Font(bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(bold=True, size=13, color="1F4E79")
NOTE_FONT = Font(italic=True, size=9, color="595959")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()

# ---------------------------------------------------------------- README
ws = wb.active
ws.title = "How to use this file"
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 112

rows = [
    ("t", "New equipment-maintenance SOPs \u2013 approval and issue tracker"),
    ("n", "Prepared 14 November 2026 for the Laboratory Manager, Ruli District Hospital."),
    ("b", ""),
    ("h", "What this file is for"),
    ("p", "Seven SOPs were written in November 2026 to close gaps found during the "
          "reorganisation of the SOP collection. They are first issues and they are not "
          "yet signed. This file is the record of who approved them and the route to "
          "signature. It is not a review register: the review date is 14 November 2028, "
          "which is outside the 31 March 2027 window used by the SOP review register."),
    ("b", ""),
    ("h", "What has to happen before the SOPs can be used"),
    ("p", "1.  The Laboratory Manager reads each SOP and prepares it, signing the cover "
          "block and the signature page."),
    ("p", "2.  The Laboratory Quality Manager reviews it and signs as reviewer."),
    ("p", "3.  The Director General approves it, signing the cover block and the "
          "signature page. Under ISO 15189:2022 the approval of a controlled laboratory "
          "document rests with the head of the institution."),
    ("p", "4.  The signed scans are uploaded next to the Word files in "
          "4. Reception > Administration > 6. Equipment, Stock and Suppliers."),
    ("p", "5.  The SOP is entered in the Master List with its code, title, effective "
          "date and review date, in the crosscutting section."),
    ("p", "6.  Bench staff sign the signature page to record that they have read and "
          "understood it."),
    ("b", ""),
    ("h", "Important"),
    ("p", "The dates already printed in each document (effective 14/11/2026, review "
          "14/11/2028) are proposed dates. If the signing route takes a different amount "
          "of time, the effective date must be changed to the date of authorisation "
          "before the SOP is used, and the file renamed with the corrected date where the "
          "name carries one."),
    ("b", ""),
    ("h", "Numbering"),
    ("p", "The codes are RliDHL-ADM-SOP-053 to 059, version 001. The existing "
          "management SOP series runs 1 to 52, and the 2026 biomedical equipment SOP is "
          "ADM-008. 053 onwards is a free block: nothing in the Master List, in the "
          "50-series folder or in the SOP review register uses these numbers. Check the "
          "Master List again before issuing 060."),
    ("b", ""),
    ("h", "The seven documents"),
    ("p", "053  Use, Care and Preventive Maintenance of the Microscope"),
    ("p", "054  Operation, Care and Preventive Maintenance of the Centrifuge"),
    ("p", "055  Operation, Care and Preventive Maintenance of the Water Bath"),
    ("p", "056  Management and Maintenance of Non-Medical Laboratory Equipment"),
    ("p", "057  Maintenance of Laboratory ICT Equipment and the Laboratory "
          "Information System"),
    ("p", "058  Use, Care and Preventive Maintenance of Hematology Analysers"),
    ("p", "059  Use, Care and Preventive Maintenance of the GeneXpert Dx System"),
    ("b", ""),
    ("h", "The three forms"),
    ("p", "058-F01  Hematology analyser daily maintenance and start-up log, one sheet "
          "per month, one row per daily task"),
    ("p", "059-F01  GeneXpert Dx System maintenance log, modelled on the Cepheid form "
          "302-8386 Rev. C, with a permanent module calibration register"),
    ("p", "056-F01  Temperature monitoring for fridges, freezers, cold boxes and "
          "rooms, with a device register"),
    ("p", "Each form is issued as an Excel workbook with twelve monthly sheets, so the "
          "bench can either print a sheet or type into it. The forms are listed on the "
          "Forms issued sheet of this file and are recorded in the Master List against "
          "their parent SOP."),
    ("b", ""),
    ("n", "Sheets in this file: Approval tracker (the main sheet), and Content map "
          "(what each SOP covers, so a reviewer can find a section quickly)."),
]
r = 1
for kind, text in rows:
    c = ws.cell(row=r, column=2, value=text)
    if kind == "t":
        c.font = TITLE_FONT
    elif kind == "h":
        c.font = Font(bold=True, size=10, color="1F4E79")
    elif kind == "n":
        c.font = NOTE_FONT
        c.alignment = Alignment(wrap_text=True, vertical="top")
    else:
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.font = Font(size=10)
    r += 1

# ---------------------------------------------------------------- TRACKER
ws = wb.create_sheet("Approval tracker")
ws["A1"] = "RULI DISTRICT HOSPITAL \u2013 LABORATORY DEPARTMENT\nP.O. BOX 1285 KIGALI  \u2022  Tel: (+250) 0781 316 368  \u2022  ruli.hospital@moh.gov.rw  \u2022  rulihospital.rw"
ws["A1"].font = Font(size=8.5, color="595959")
ws["A1"].alignment = Alignment(horizontal="center", wrap_text=True)
ws.row_dimensions[1].height = 26
ws.merge_cells("A1:K1")
ws["A2"] = "Approval and issue tracker \u2013 new equipment-maintenance SOPs (November 2026)"
ws["A2"].font = TITLE_FONT
ws.merge_cells("A2:K2")

ws["A3"] = ("Fill the shaded columns as each step is completed. A SOP is not in force "
            "until the prepared-by, reviewed-by and approved-by signatures and dates are "
            "entered and the signed scan is filed.")
ws["A3"].font = NOTE_FONT
ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A3:K3")
ws.row_dimensions[3].height = 28

headers = [
    "SOP code", "Title", "Version", "Proposed effective\ndate",
    "Review due", "Prepared by\nLaboratory Manager\n(name / date)",
    "Reviewed by\nLaboratory Quality Manager\n(name / date)",
    "Approved by\nDirector General\n(name / date)",
    "Signed scan\nfiled?", "Master List\nupdated?", "Status",
]
HR = 4
for i, h in enumerate(headers, 1):
    c = ws.cell(row=HR, column=i, value=h)
    c.fill = HDR_FILL
    c.font = HDR_FONT
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = BORDER
ws.row_dimensions[HR].height = 38

SOPs = [
    ("RliDHL-ADM-SOP-053-VERS-001",
     "Use, Care and Preventive Maintenance of the Microscope"),
    ("RliDHL-ADM-SOP-054-VERS-001",
     "Operation, Care and Preventive Maintenance of the Centrifuge"),
    ("RliDHL-ADM-SOP-055-VERS-001",
     "Operation, Care and Preventive Maintenance of the Water Bath"),
    ("RliDHL-ADM-SOP-056-VERS-001",
     "Management and Maintenance of Non-Medical Laboratory Equipment"),
    ("RliDHL-ADM-SOP-057-VERS-001",
     "Maintenance of Laboratory ICT Equipment and the Laboratory Information System"),
    ("RliDHL-ADM-SOP-058-VERS-001",
     "Use, Care and Preventive Maintenance of Hematology Analysers"),
    ("RliDHL-ADM-SOP-059-VERS-001",
     "Use, Care and Preventive Maintenance of the GeneXpert Dx System"),
]

r = HR + 1
for code, title in SOPs:
    vals = [code, title, "001", "14/11/2026", "14/11/2028",
            "Kelvin SAMAHANI", "Jean Paul NSENGIYUMVA", "Dr. D\u00e9ogratias KANEZA",
            "No", "No", "Awaiting approval"]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.border = BORDER
        c.alignment = WRAP
        c.font = Font(size=9)
        if i in (6, 7, 8, 9, 10, 11):
            c.fill = PatternFill("solid", fgColor="FFF2CC")
    ws.row_dimensions[r].height = 40
    r += 1

dv = DataValidation(type="list", formula1='"Awaiting approval,Prepared - awaiting Quality Manager review,Reviewed - awaiting DG approval,Approved - in force,Superseded,Withdrawn"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"K{HR+1}:K{r-1}")

dv2 = DataValidation(type="list", formula1='"Yes,No,Not applicable"', allow_blank=True)
ws.add_data_validation(dv2)
dv2.add(f"I{HR+1}:J{r-1}")

widths = [27, 46, 9, 14, 12, 22, 20, 22, 11, 12, 24]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = f"C{HR+1}"

nr = r + 1
ws.cell(row=nr, column=1,
        value="Rows are pre-filled with the code, title and proposed dates. Enter the "
              "signature dates and change the status as each step completes.").font = NOTE_FONT
ws.merge_cells(f"A{nr}:K{nr}")

# ---------------------------------------------------------------- CONTENT MAP
ws2 = wb.create_sheet("Content map")
ws2["A1"] = "What each SOP covers, by section"
ws2["A1"].font = TITLE_FONT
ws2.merge_cells("A1:D1")
ws2["A2"] = ("Use this to find the section that answers a question, or to see at a "
             "glance whether a topic is already covered before writing a new document.")
ws2["A2"].font = NOTE_FONT
ws2.merge_cells("A2:D2")
ws2["A2"].alignment = Alignment(wrap_text=True, vertical="top")

h2 = ["SOP", "Topic already covered", "Where", "Notes"]
for i, h in enumerate(h2, 1):
    c = ws2.cell(row=4, column=i, value=h)
    c.fill = HDR_FILL
    c.font = HDR_FONT
    c.border = BORDER
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

content = [
    ("053 Microscope", "Daily, weekly and monthly care of the microscope", "6.3 \u2013 6.5",
     "Dust cover is the single most effective action in this climate"),
    ("053 Microscope", "Setting up Koehler illumination", "6.6",
     "Step-by-step; repeated after a lamp change or service"),
    ("053 Microscope", "Oil immersion technique", "6.7",
     "Oil is wiped off immediately, never left to harden"),
    ("053 Microscope", "Annual preventive maintenance and acceptance criteria", "6.8",
     "Eight-point checklist the service provider must report on"),
    ("053 Microscope", "Faults and when to take it out of service", "6.9",
     "Includes fungal growth \u2013 stop using, do not clean"),
    ("053 Microscope", "Humidity and storage", "6.10",
     "Ties to relative humidity below 70%"),
    ("054 Centrifuge", "Balancing a load", "6.3",
     "Every run, every speed, no exceptions"),
    ("054 Centrifuge", "RCF versus rpm and the conversion formula", "6.4",
     "RCF is set directly wherever the instrument allows"),
    ("054 Centrifuge", "Broken tube and spill inside the bowl", "6.6",
     "30-minute wait before opening if infectious"),
    ("054 Centrifuge", "Speed and timer verification limits", "6.8",
     "\u00b1 10% speed, \u00b1 5% timer, every 6 months and after repair"),
    ("054 Centrifuge", "Rotor life record and retirement", "6.9",
     "Rotors have a finite life in hours or years"),
    ("055 Water bath", "Water quality and filling", "6.1",
     "Distilled water only; tap water scales the heater"),
    ("055 Water bath", "Daily temperature check and acceptance limits", "6.2 and 6.4",
     "\u00b1 1.0 \u00b0C at 37 \u00b0C and at 56 \u00b0C"),
    ("055 Water bath", "Weekly drain, clean and disinfect", "6.3",
     "Biofilm appears within two weeks if neglected"),
    ("055 Water bath", "Electrical safety", "6.5",
     "RCD, dry control housing, cord inspection"),
    ("056 Non-medical", "Full list of what counts as non-medical equipment", "3",
     "Six classes: cold storage, water, air, power, environment, safety"),
    ("056 Non-medical", "Refrigerator and cold chain temperature ranges", "6.2",
     "Reagent 2\u20138 \u00b0C, blood bank 2\u20136 \u00b0C, freezer -20 \u00b0C"),
    ("056 Non-medical", "Action on a temperature excursion", "6.2",
     "Do not discard on the reading alone; assess then decide"),
    ("056 Non-medical", "Water distiller and deioniser maintenance", "6.3",
     "Includes conductivity acceptance limit"),
    ("056 Non-medical", "Air conditioning and humidity control", "6.4",
     "18\u201325 \u00b0C and below 70% RH \u2013 protects the microscopes"),
    ("056 Non-medical", "UPS testing and battery replacement", "6.5",
     "Monthly simulated mains failure, batteries every 3\u20135 years"),
    ("056 Non-medical", "Fire extinguishers, eye wash, emergency shower", "6.6",
     "Monthly and weekly checks with records"),
    ("057 ICT", "ICT register contents", "6.1",
     "Includes OS version so out-of-support builds are visible"),
    ("057 ICT", "Access control and confidentiality rules", "6.2",
     "Named accounts, least privilege, quarterly account review"),
    ("057 ICT", "Routine maintenance schedule", "6.3",
     "Daily to annual, in one table"),
    ("057 ICT", "Backup frequency, retention and location", "6.4",
     "Off-site copy of each weekly full backup"),
    ("057 ICT", "Restore test", "6.3 and 6.4",
     "Monthly; a backup that has never been restored is not evidence"),
    ("057 ICT", "Downtime procedure", "6.5",
     "Paper register, entry on restoration, second-person check"),
    ("057 ICT", "Change control for LIS and interfaces", "6.6",
     "Written approval before the change, validation after"),
    ("057 ICT", "Data destruction before disposal", "6.8",
     "Witnessed, recorded, storage wiped or destroyed"),
    ("057 ICT", "Fault escalation table", "6.9",
     "First action and escalation route for eight common faults"),
]

r = 5
for row in content:
    for i, v in enumerate(row, 1):
        c = ws2.cell(row=r, column=i, value=v)
        c.border = BORDER
        c.alignment = WRAP
        c.font = Font(size=9)
    r += 1

for i, w in enumerate([20, 52, 16, 46], 1):
    ws2.column_dimensions[get_column_letter(i)].width = w
ws2.freeze_panes = "A5"

# ---------------------------------------------------------------- FORMS ISSUED
ws3 = wb.create_sheet("Forms issued")
ws3["A1"] = "Forms issued under these SOPs"
ws3["A1"].font = TITLE_FONT
ws3.merge_cells("A1:F1")
ws3["A2"] = ("Each form is a controlled document in its own right. When a form is revised, "
             "the old version is withdrawn and the new one issued with a new form number.")
ws3["A2"].font = NOTE_FONT
ws3["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws3.merge_cells("A2:F2")

fh = ["Form number", "Title", "Supports SOP", "Frequency", "Format", "Status"]
for i, h in enumerate(fh, 1):
    c = ws3.cell(row=4, column=i, value=h)
    c.fill = HDR_FILL
    c.font = HDR_FONT
    c.border = BORDER
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")

forms = [
    ("RliDHL-ADM-SOP-058-F01", "Hematology analyser daily maintenance and start-up log",
     "058", "Daily", "Excel, 12 monthly sheets", "Issued 14/11/2026"),
    ("RliDHL-ADM-SOP-059-F01", "GeneXpert Dx System maintenance log, with module calibration register",
     "059", "Daily to annual", "Excel, 12 monthly sheets plus register", "Issued 14/11/2026"),
    ("RliDHL-ADM-SOP-056-F01", "Temperature monitoring: fridges, freezers, cold boxes and rooms",
     "056", "Twice daily / daily", "Excel, device register plus 12 monthly sheets", "Issued 14/11/2026"),
    ("RliDHL-ADM-SOP-053-F01", "Not yet created", "053", "Daily / weekly / monthly",
     "Proposed", "Pending"),
    ("RliDHL-ADM-SOP-054-F01", "Not yet created", "054", "Daily / weekly / monthly",
     "Proposed", "Pending"),
]

r = 5
for f in forms:
    for i, v in enumerate(f, 1):
        c = ws3.cell(row=r, column=i, value=v)
        c.border = BORDER
        c.alignment = WRAP
        c.font = Font(size=9)
    ws3.row_dimensions[r].height = 30
    r += 1

for i, w in enumerate([26, 52, 12, 20, 32, 18], 1):
    ws3.column_dimensions[get_column_letter(i)].width = w
ws3.freeze_panes = "A5"

wb.save(PATH)
print("written:", PATH)
