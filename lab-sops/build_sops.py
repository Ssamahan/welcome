#!/usr/bin/env python3
"""
Generates the missing Ruli District Hospital laboratory SOPs on the
management (crosscutting) layout defined in
"01 - Standard SOP layout mapped to ISO 15189-2022.docx".
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.dirname(os.path.abspath(__file__))
EFF = "14 / 11 / 2026"
REV = "14 / 11 / 2028"
PREP = "Kelvin SAMAHANI"
PREP_T = "Head of Laboratory"
REV_BY = "Pacifique ISHIMWE"
REV_BY_T = "BMeT"
AUTH = "Dr. D\u00e9ogratias KANEZA"
AUTH_T = "Director General"


def shade(cell, hexcolor="D9D9D9"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def base_doc(code, title, version="001"):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.line_spacing = 1.08

    for s in doc.sections:
        s.top_margin = Cm(1.9)
        s.bottom_margin = Cm(1.9)
        s.left_margin = Cm(2.0)
        s.right_margin = Cm(2.0)

    # ---- cover block ----
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("REPUBLIC OF RWANDA \u2013 MINISTRY OF HEALTH")
    r.bold = True
    r.font.size = Pt(10)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("RULI DISTRICT HOSPITAL \u2013 LABORATORY DEPARTMENT")
    r.bold = True
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run(title.upper())
    r.bold = True
    r.font.size = Pt(15)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("STANDARD OPERATING PROCEDURE")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    t = doc.add_table(rows=7, cols=2)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    rows = [
        ("SOP Number", f"RliDHL-ADM-SOP-{code}-VERS-{version}"),
        ("Version", version),
        ("Effective date", EFF),
        ("Next review date", REV),
        ("Prepared by", f"{PREP} \u2013 {PREP_T}"),
        ("Reviewed by", f"{REV_BY} \u2013 {REV_BY_T}"),
        ("Approved by", f"{AUTH} \u2013 {AUTH_T}"),
    ]
    for i, (k, v) in enumerate(rows):
        t.cell(i, 0).text = ""
        t.cell(i, 1).text = ""
        c0 = t.cell(i, 0).paragraphs[0].add_run(k)
        c0.bold = True
        t.cell(i, 1).paragraphs[0].add_run(v)
        shade(t.cell(i, 0), "EDEDED")
    t.columns[0].width = Cm(4.4)
    t.columns[1].width = Cm(12.2)
    for row in t.rows:
        row.cells[0].width = Cm(4.4)
        row.cells[1].width = Cm(12.2)

    doc.add_paragraph()

    # ---- review history ----
    h = doc.add_paragraph()
    r = h.add_run("Review History")
    r.bold = True
    r.font.size = Pt(11)
    t2 = doc.add_table(rows=2, cols=4)
    t2.style = "Table Grid"
    hdr = ["Prepared / Reviewed by", "Version", "Date", "Description of change"]
    for i, x in enumerate(hdr):
        c = t2.cell(0, i)
        c.text = ""
        run = c.paragraphs[0].add_run(x)
        run.bold = True
        shade(c)
    vals = [PREP, version, EFF, "First issue. New document."]
    for i, x in enumerate(vals):
        t2.cell(1, i).text = x

    # ---- controlled copies / supersedes ----
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Controlled copies. ").bold = True
    p.add_run(
        "The master copy of this SOP is held electronically in the laboratory "
        "Google Drive, folder SOPs by Room > 4. Reception > Administration > "
        "6. Equipment, Stock and Suppliers. One printed, signed copy is held by the "
        "Laboratory Manager. Printed copies taken to a bench are uncontrolled unless "
        "stamped and signed."
    )
    p = doc.add_paragraph()
    p.add_run("Supersedes. ").bold = True
    p.add_run("No previous version. This is the first issue of this SOP.")

    # footer
    for s in doc.sections:
        fp = s.footer.paragraphs[0]
        fp.text = f"RliDHL-ADM-SOP-{code}-VERS-{version} \u2013 {title}"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in fp.runs:
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_page_break()
    return doc


def H(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12) if level == 1 else Pt(10.5)
    return p


def P(doc, text, bold_lead=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_lead:
        p.add_run(bold_lead).bold = True
    p.add_run(text)
    return p


def B(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(it)


def NUM(doc, items):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(f"{i}.  ")
        p.add_run(it)


def _render_refs(doc, references):
    """Accepts a list of plain strings or of (text, url) tuples."""
    norm = []
    for r in references:
        if isinstance(r, (tuple, list)):
            norm.append((r[0], r[1] if len(r) > 1 else None))
        else:
            norm.append((r, None))
    REF(doc, norm)


def add_hyperlink(paragraph, url, text, size=Pt(9.5)):
    """Insert a real clickable hyperlink run into a paragraph."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size.pt * 2)))
    rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def REF(doc, entries):
    """Numbered reference list. Each entry: (text, url or None).
    A URL is rendered as a live clickable link after the citation."""
    for i, (text, url) in enumerate(entries, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(f"{i}.  ").font.size = Pt(9.5)
        r = p.add_run(text + ("  " if url else ""))
        r.font.size = Pt(9.5)
        if url:
            add_hyperlink(p, url, url)


def TBL(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, x in enumerate(headers):
        c = t.cell(0, i)
        c.text = ""
        run = c.paragraphs[0].add_run(x)
        run.bold = True
        run.font.size = Pt(9.5)
        shade(c)
    for row in rows:
        cells = t.add_row().cells
        for i, x in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(x))
            run.font.size = Pt(9.5)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


def tail(doc, records, supporting, references):
    H(doc, "8. Records")
    P(
        doc,
        "The following records are produced by this procedure. Each is retained in the "
        "laboratory for the period shown, in the folder named in column three.",
    )
    TBL(
        doc,
        ["Record", "Retention", "Where kept"],
        records,
        widths=[8.0, 3.2, 5.4],
    )

    H(doc, "9. Supporting Documents")
    B(doc, supporting)

    H(doc, "10. References")
    _render_refs(doc, references)

    H(doc, "11. Signature Page")
    P(
        doc,
        "This SOP is prepared by the Head of Laboratory, reviewed for technical accuracy "
        "by the hospital BMeT, and approved and signed by the Director General. It takes "
        "effect on the date of that approval. The signature block below records the "
        "approval; the staff list records that each member of staff has read and "
        "understood the SOP and will work to it.",
    )
    TBL(
        doc,
        ["Approval", "Name", "Job title", "Signature", "Date"],
        [
            ("Prepared by", PREP, PREP_T, "", ""),
            ("Reviewed by", REV_BY, REV_BY_T, "", ""),
            ("Approved by", AUTH, AUTH_T, "", ""),
        ],
        widths=[2.8, 4.0, 3.6, 3.4, 2.8],
    )
    P(
        doc,
        "I have read and understood this version of the SOP and I will work to it. "
        "Signed staff are authorised to carry out the procedure described.",
    )
    TBL(
        doc,
        ["Name", "Job title", "Signature", "Date"],
        [("", "", "", "") for _ in range(8)],
        widths=[5.0, 4.6, 4.0, 3.0],
    )

    H(doc, "12. Amendment Page")
    P(
        doc,
        "Handwritten amendments are authorised by the Director General, on the written "
        "recommendation of the Head of Laboratory, before the next revision. Each "
        "amendment must be initialled and dated. The amendment is incorporated at the "
        "next revision and this page is cleared.",
    )
    TBL(
        doc,
        ["Section", "Amendment made", "Authorised by", "Date"],
        [("", "", "", "") for _ in range(6)],
        widths=[2.6, 7.4, 4.0, 2.6],
    )


# =====================================================================
# 1. MICROSCOPE
# =====================================================================
def microscope():
    code, title = "053", "Use, Care and Preventive Maintenance of the Microscope"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "Microscopy is the primary diagnostic method for malaria and other blood "
        "parasites, stool and urine parasites, tuberculosis by Ziehl-Neelsen and by "
        "auramine fluorescence, Gram staining, and the microscopic differential of the "
        "full blood count. In every one of these examinations the result depends on the "
        "optical and mechanical condition of the instrument itself. A microscope with "
        "dirty optics, a misaligned condenser or a loose coarse focus produces either "
        "false negative results, because parasites are missed, or false positive "
        "results, because dust and fungus are read as organisms.",
    )
    P(
        doc,
        "Ruli District Hospital is in a humid highland climate. Humidity is the single "
        "most important cause of microscope deterioration here: fungal filaments grow "
        "across lens coatings within weeks in an uncapped instrument and etch the glass "
        "permanently. Fungal damage cannot be repaired by cleaning and requires "
        "replacement of the lens. Prevention, which costs nothing, is therefore the "
        "central concern of this SOP.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "This SOP defines how every microscope in the laboratory is used, cleaned, "
        "maintained and serviced, how faults are recognised and reported, and what "
        "records are kept. It exists so that the same standard of optical performance "
        "is available at every bench, and so that a reader of any microscopy result can "
        "be confident that the instrument that produced it was fit for purpose.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to every binocular compound light microscope in the "
        "laboratory, including those with a fluorescence attachment, in the "
        "Parasitology, TB, Bacteriology and Hematology sections, and to any microscope "
        "used at a linked health centre under this laboratory's supervision.",
    )
    P(
        doc,
        "It covers the instrument itself: siting, use, cleaning, preventive "
        "maintenance, servicing, fault handling and disposal. It does not describe how "
        "to perform any particular examination. Those procedures are documented in the "
        "bench SOPs of each section and are listed in section 9.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("Koehler illumination",
             "The correct alignment of light source, condenser and objective so that the "
             "field is evenly illuminated and the specimen is seen with maximum contrast "
             "and resolution."),
            ("Condenser",
             "The lens system below the stage that focuses light onto the specimen."),
            ("Iris diaphragm",
             "The adjustable aperture in the condenser that controls the cone of light and "
             "so the contrast."),
            ("Numerical aperture (NA)",
             "The light-gathering capacity of an objective, engraved on its barrel. "
             "Resolution depends on it."),
            ("Oil immersion objective",
             "A 100x objective designed to be used with immersion oil between the lens and "
             "the slide, to raise the NA above 1.0."),
            ("Parfocal",
             "The property of objectives that keeps the specimen approximately in focus "
             "when the objective is changed."),
            ("Fungal etching",
             "Permanent damage to a lens coating caused by fungal growth. Irreparable."),
            ("PM", "Preventive maintenance."),
        ],
        widths=[4.6, 12.0],
    )

    H(doc, "5. Responsibilities and Authorisation")
    TBL(
        doc,
        ["Role", "Responsibility"],
        [
            ("Director General",
             "Approves this SOP and signs the cover block and the signature page. Under "
             "ISO 15189:2022 the approval of a controlled laboratory document rests with "
             "the head of the institution, not with the laboratory."),
            ("Laboratory Manager",
             "Is accountable for this SOP and for the resources it requires. Authorises "
             "the purchase of replacement instruments and lenses. Signs service reports "
             "and countersigns the SOP for approval by the Director General."),
            ("Laboratory Quality Officer",
             "Maintains the PM schedule for every microscope, verifies that PM has been "
             "done on time, and reviews PM records monthly."),
            ("Bench staff (all sections)",
             "Perform the daily and weekly care described in this SOP. Report any optical "
             "or mechanical fault immediately. Do not dismantle the instrument."),
            ("BMeT (Biomedical Equipment Technician)",
             "Holds the microscope inventory, the PM log and the service records, and the "
             "service contract. Performs the tasks the service provider is not contracted "
             "for, and witnesses the annual PM."),
            ("BMeT, or the contracted service provider",
             "Performs the annual preventive maintenance and any repair. Issues a signed "
             "service report for each visit."),
        ],
        widths=[5.4, 11.2],
    )
    P(
        doc,
        "Only staff who have been trained on this SOP and whose competence has been "
        "assessed may set up Koehler illumination, change a lamp or clean an objective. "
        "Disassembly of the head, the condenser mount or the focus block is done only by "
        "the service provider.",
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Inventory and identification", 2)
    P(
        doc,
        "Every microscope carries a laboratory asset number on a label fixed to its "
        "base, and that number appears in the laboratory equipment inventory. The asset "
        "number is the key that links the instrument to its PM log and its service "
        "history. A microscope without an asset number is added to the inventory before "
        "it is used for patient testing.",
    )

    H(doc, "6.2 Siting", 2)
    B(
        doc,
        [
            "Place on a rigid bench that does not carry a centrifuge or a vortex mixer. "
            "Vibration loosens the focus mechanism and blurs the image.",
            "Keep out of direct sunlight. Sunlight heats the instrument and bleaches "
            "stained slides during reading.",
            "Keep away from the water bath, the sink and the autoclave. Steam is the "
            "second cause of fungal growth after humidity itself.",
            "Keep at least 30 cm from a wall or shelf so the head can be tilted and the "
            "lamp ventilated.",
            "Keep the dust cover on whenever the microscope is not in use. This is the "
            "single most effective maintenance action in this laboratory.",
        ]
    )

    H(doc, "6.3 Daily use and care (every shift)", 2)
    P(doc, "Before the first use of the shift:", bold_lead="")
    NUM(
        doc,
        [
            "Check that the dust cover has been in place and that the instrument is dry.",
            "Inspect the stage, the objectives and the eyepieces for dust and for "
            "fingerprints.",
            "Switch on and confirm even illumination across the field. A dark or uneven "
            "field is a fault, not a setting to be worked around.",
            "Confirm that the mechanical stage moves freely in both axes and that the "
            "coarse and fine focus turn without stiffness or slip.",
        ]
    )
    P(doc, "After the last use of the shift:", bold_lead="")
    NUM(
        doc,
        [
            "Remove the slide. Lower the stage fully and turn the nosepiece to the "
            "lowest-power objective.",
            "Wipe any immersion oil from the 100x objective and from the stage with lens "
            "tissue, then with a tissue lightly moistened with 70% ethanol. Oil left to "
            "dry hardens into a film that destroys contrast.",
            "Dim the lamp to minimum, then switch off. Do not leave the lamp at full "
            "brightness with the instrument covered; the trapped heat damages coatings.",
            "Replace the dust cover.",
        ]
    )

    H(doc, "6.4 Weekly care", 2)
    B(
        doc,
        [
            "Clean the eyepiece lenses on both the upper and the lower surface with lens "
            "tissue and a breath of condensation. Do not use paper towel or clothing.",
            "Clean the condenser top lens, which collects dust and oil from below.",
            "Clean the stage surface and the slide clips with 70% ethanol.",
            "Check that the condenser centring screws and the iris lever move freely.",
            "Inspect each objective against a light for dust between the lenses or a "
            "white haze on the coating. Record the finding on the PM log.",
        ]
    )

    H(doc, "6.5 Monthly care", 2)
    NUM(
        doc,
        [
            "Set up Koehler illumination as described in 6.6 and record that it was done.",
            "Inspect all objectives and eyepieces with a torch held at an angle. Any "
            "cobweb-like or powdery white growth is fungus. Stop using that objective, "
            "label it, and report it the same day. Do not attempt to clean it.",
            "Check the lamp housing for dust and clean the ventilation grilles.",
            "Check the power cord and the plug for cracks and for exposed conductor. A "
            "damaged cord takes the instrument out of service.",
            "Replace the desiccant sachet in the storage cabinet, or dry the existing one "
            "as instructed by the manufacturer, once a month.",
        ]
    )

    H(doc, "6.6 Setting up Koehler illumination", 2)
    P(
        doc,
        "Koehler illumination is set up at the start of each session by a trained member "
        "of staff, after a lamp change, and after any service visit.",
    )
    NUM(
        doc,
        [
            "Switch on the lamp and set it to about two thirds brightness. Place a "
            "stained slide on the stage and focus on the specimen with the 10x objective.",
            "Close the field diaphragm, the ring at the base of the condenser, until its "
            "image appears as a dark-edged polygon in the field of view.",
            "Turn the condenser focus knob until the edges of that polygon are sharp.",
            "Centre the polygon with the two centring screws on the condenser, until it "
            "is concentric with the field of view.",
            "Open the field diaphragm until its edges just leave the field of view.",
            "Remove one eyepiece and look down the tube. Close the iris diaphragm until "
            "it occupies about three quarters of the bright circle, then open it slightly "
            "so that it just clears the objective. Replace the eyepiece.",
            "Record the date and the initials on the PM log.",
        ]
    )

    H(doc, "6.7 Oil immersion technique", 2)
    B(
        doc,
        [
            "Use only the immersion oil supplied for the instrument. Do not substitute "
            "cedar oil or a general-purpose oil.",
            "Place a single drop on the coverslip, not on the objective. Lower the "
            "objective by watching from the side, never through the eyepiece.",
            "Use the 100x objective only with oil. Using it dry scratches the front lens "
            "and gives a blurred, low-contrast image that is easily misread.",
            "After use, wipe the oil off immediately with dry lens tissue, then with "
            "tissue moistened with 70% ethanol. Never let oil remain on the lens.",
            "Never use xylene routinely on cemented lenses. Use it only when the service "
            "provider directs it, and never on the eyepieces.",
        ]
    )

    H(doc, "6.8 Annual preventive maintenance", 2)
    P(
        doc,
        "Once every twelve months the service provider performs and documents the "
        "following. The BMeT checks that each item appears in the report.",
    )
    TBL(
        doc,
        ["Item", "What is checked", "Acceptance"],
        [
            ("Optics", "All lenses inspected with a torch; fungus and delamination "
                       "assessed", "No fungus, no delamination, no scratches"),
            ("Mechanical stage", "Free movement, no backlash, graduations legible",
             "Smooth in both axes"),
            ("Focus", "Coarse and fine focus; specimen does not drift",
             "No drift over 5 minutes"),
            ("Condenser", "Centring, iris and field diaphragm operation",
             "Full range of movement"),
            ("Illumination", "Lamp condition, brightness control, evenness",
             "Even field at all powers"),
            ("Fluorescence attachment", "Filter cubes, barrier filter, lamp hours",
             "Per manufacturer"),
            ("Electrical safety", "Earth continuity, insulation, cord and plug",
             "Earth bond under 0.1 ohm; no damage"),
            ("Cleanliness", "Interior dust and fungal spores removed",
             "No visible growth"),
        ],
        widths=[3.6, 7.6, 5.4],
    )
    P(
        doc,
        "The service report is signed by the service provider and by the Laboratory "
        "Manager, filed with the equipment records, and the PM date is entered on the PM "
        "log and in the equipment inventory.",
    )

    H(doc, "6.9 Faults and when to stop using the microscope", 2)
    P(
        doc,
        "A microscope with any of the faults below is taken out of service immediately, "
        "labelled OUT OF SERVICE with the date and the fault, and reported to the "
        "Quality Officer. Results already produced on it in that shift are reviewed to "
        "decide whether they are affected.",
    )
    TBL(
        doc,
        ["Symptom", "Usual cause", "Action"],
        [
            ("Field is dark or uneven", "Lamp failed, iris closed, condenser "
                                        "misaligned", "Check iris and condenser; change "
                                                      "lamp if failed"),
            ("Image blurred at all powers", "Dirty eyepiece or objective; oil on a dry "
                                            "lens", "Clean optics; dry the lens"),
            ("Image sharp at one power only", "Objective damaged or dry; parfocal "
                                              "drift", "Report for service"),
            ("Specimen drifts out of focus", "Stage or focus mechanism worn",
             "Out of service; service visit"),
            ("Black specks that move when the eyepiece is rotated",
             "Dirt in the eyepiece", "Clean the eyepiece"),
            ("Black specks that stay still", "Dirt on the objective or the slide",
             "Clean the objective; use a new slide"),
            ("White powdery or cobweb growth", "Fungus", "Out of service; do not clean; "
                                                         "report"),
            ("Burning smell or warm plug", "Electrical fault", "Switch off at the wall; "
                                                               "out of service"),
        ],
        widths=[5.4, 5.4, 5.8],
    )

    H(doc, "6.10 Storage and humidity control", 2)
    B(
        doc,
        [
            "Keep the dust cover on at all times when not in use.",
            "Where a microscope is stored in a cabinet, keep a desiccant sachet in the "
            "cabinet and renew or dry it monthly.",
            "Do not store a microscope in a room where the relative humidity regularly "
            "exceeds 70%. Where no air conditioning exists, use a sealed cabinet with "
            "desiccant.",
            "Never store a microscope with the lamp lit or warm.",
        ]
    )

    H(doc, "6.11 Moving a microscope", 2)
    P(
        doc,
        "Carry a microscope with two hands, one under the base and one on the arm, with "
        "the head locked and the stage lowered. Never carry it by the eyepiece tube, the "
        "stage or the power cord. Before any move, remove the eyepieces and pack the "
        "objectives only if the manufacturer's instructions say so.",
    )

    H(doc, "7. Monitoring and Quality Indicators")
    P(
        doc,
        "The Quality Officer reviews the following indicators every quarter and reports "
        "them at the management review.",
    )
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Microscopes with PM completed within the 12-month interval", "100%"),
            ("Microscopes out of service for more than 14 days", "0"),
            ("Microscopes found with fungal growth at inspection", "0"),
            ("PM records signed and filed within one week of the service", "100%"),
        ],
        widths=[11.0, 5.6],
    )

    tail(
        doc,
        [
            ("Microscope Preventive maintenance log 24 (daily/weekly/monthly entries)",
             "5 years", "6. Equipment > 7. PM and temperature logs"),
            ("Koehler illumination set-up record", "5 years", "As above"),
            ("Annual service report, signed", "Life of instrument + 5 years",
             "Equipment records"),
            ("Microscope fault and repair log", "5 years", "Equipment records"),
            ("Microscope inventory / asset register", "Permanent", "Equipment records"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "RliDHL-PAR-SOP-017 \u2013 Use of a Microscope (bench procedure, parasitology)",
            "Bench SOPs for malaria Giemsa, TB ZN and auramine microscopy, Gram staining",
            "Laboratory equipment inventory",
        ],
        [
        ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022.",
         "https://www.iso.org/standard/76677.html"),
        "ISO 15189:2022, clauses 6.4 (equipment), 6.4.4 (preventive maintenance) and 6.4.5 (malfunction reporting).",
        ("World Health Organization. Malaria microscopy quality assurance manual, version 2. Geneva: WHO; 2016.",
         "https://iris.who.int/handle/10665/204266"),
        "Manufacturer's operating manual for the microscope models in use at this laboratory: Olympus CX21FS1, Olympus CX21LEDFS1 and Zeiss Primo Star, held beside each instrument.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


# =====================================================================
# 2. CENTRIFUGE
# =====================================================================
def centrifuge():
    code, title = "054", "Operation, Care and Preventive Maintenance of the Centrifuge"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "The centrifuge separates serum or plasma from cells, deposits urinary sediment, "
        "packs red cells for the cross-match, and prepares specimens for a large "
        "proportion of the examinations in this laboratory. Two things about it matter "
        "clinically. The first is that the relative centrifugal force applied determines "
        "whether the separation is correct: too low a force leaves cells in the "
        "supernatant and invalidates a chemistry or serology result; too high a force "
        "haemolyses the sample. The second is that a centrifuge is the most dangerous "
        "routine instrument in the laboratory. A rotor loaded out of balance releases "
        "enough energy to break the drive shaft, pierce the bowl and throw fragments "
        "across the room, and it aerosolises whatever infectious material the tubes "
        "contained.",
    )
    P(
        doc,
        "Both risks are controlled by ordinary discipline: setting the instrument in "
        "relative centrifugal force rather than in revolutions per minute, balancing the "
        "load every single time, and keeping the rotor, buckets and lid interlock in "
        "verified condition.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "This SOP defines how centrifuges are selected, loaded, run, cleaned, verified "
        "and serviced, the acceptance limits for speed and time, the action to take after "
        "a tube breakage, and the records that demonstrate the instrument was in a "
        "verified state whenever patient specimens were processed.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to every centrifuge in the laboratory: bench-top "
        "general-purpose centrifuges, micro-haematocrit centrifuges, and any "
        "cytocentrifuge or blood-bank centrifuge in use. It applies to all staff who "
        "operate a centrifuge, including staff in the TB, hematology, biochemistry and "
        "blood transfusion areas.",
    )
    P(
        doc,
        "It does not describe the centrifugation conditions for a particular test. Those "
        "are stated in each bench SOP and must be followed exactly, in relative "
        "centrifugal force and in time.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("RCF (relative centrifugal force)",
             "The force applied to the specimen, expressed as a multiple of gravity "
             "(x g). It is the parameter that determines separation and it depends on "
             "both speed and radius."),
            ("rpm",
             "Revolutions per minute. The speed of the rotor. On its own it does not "
             "define the force, because two centrifuges of different radius run at the "
             "same rpm apply different forces."),
            ("Rotor",
             "The rotating assembly that carries the buckets or tubes. Fixed-angle or "
             "swing-out."),
            ("Bucket / trunnion",
             "The swinging carrier that holds the tube in a swing-out rotor."),
            ("Balancing",
             "Loading tubes of equal mass in positions diametrically opposite each other "
             "so that the centre of gravity stays on the axis of rotation."),
            ("Lid interlock",
             "The safety device that prevents the lid opening while the rotor turns and "
             "prevents starting with the lid open."),
            ("Aerosol",
             "Fine airborne droplets released when a tube breaks or a lid is opened too "
             "soon after a run with infectious material."),
            ("PM", "Preventive maintenance."),
        ],
        widths=[4.6, 12.0],
    )

    H(doc, "5. Responsibilities and Authorisation")
    TBL(
        doc,
        ["Role", "Responsibility"],
        [
            ("Director General",
             "Approves this SOP and signs the cover block and the signature page. Under "
             "ISO 15189:2022 the approval of a controlled laboratory document rests with "
             "the head of the institution, not with the laboratory."),
            ("Laboratory Manager",
             "Is accountable for this SOP and for the resources it requires. Authorises "
             "purchase and withdrawal from service. Signs service and verification "
             "reports, and countersigns the SOP for approval by the Director General."),
            ("Laboratory Quality Officer",
             "Maintains the verification schedule, reviews verification and PM records "
             "monthly, and investigates any out-of-limit verification."),
            ("Bench staff",
             "Balance every load, run the instrument as instructed, clean after use, and "
             "report faults and breakages immediately."),
            ("BMeT (Biomedical Equipment Technician)",
             "Holds the centrifuge inventory, the rotor life record, the verification log "
             "and the service records."),
            ("BMeT, or the service provider",
             "Performs the speed and timer verification, the annual PM, and all repairs. "
             "Issues a signed report."),
        ],
        widths=[5.4, 11.2],
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Inventory, siting and identification", 2)
    B(
        doc,
        [
            "Every centrifuge carries an asset number that links it to the equipment "
            "inventory, its verification log and its service history.",
            "Place on a level, rigid bench that is not shared with a balance. Vibration "
            "disturbs weighing and unbalances nothing so much as a moving bench.",
            "Leave at least 10 cm clear around the ventilation grilles and never cover "
            "the instrument while it runs.",
            "Keep the instrument at least one metre from the microscope bench.",
            "Plug into a socket protected by a residual current device. Do not use an "
            "extension lead.",
        ]
    )

    H(doc, "6.2 Checks before every run", 2)
    NUM(
        doc,
        [
            "Confirm the lid is closed and the interlock engages. The instrument must not "
            "start with the lid open.",
            "Inspect the rotor and the buckets for cracks, corrosion, scoring and "
            "discolouration. A cracked bucket is replaced, never used.",
            "Confirm that the buckets swing freely on their trunnions and that the rotor "
            "is seated fully on the drive shaft.",
            "Check that tubes are the correct type for the rotor, are undamaged, and are "
            "not filled above the manufacturer's maximum.",
            "Check that the tubes are dry on the outside. A wet tube slips and a "
            "disinfectant film is slippery.",
        ]
    )

    H(doc, "6.3 Loading and balancing", 2)
    P(
        doc,
        "This is the step that prevents accidents. It is not optional and it does not "
        "depend on the speed being used.",
    )
    NUM(
        doc,
        [
            "Always load an even number of tubes.",
            "Place tubes diametrically opposite each other, in positions that are "
            "symmetrical about the centre of the rotor.",
            "Balance each pair to within 0.1 g on the laboratory balance where a balance "
            "is available, or by matching to the eye against a spare tube filled with "
            "water to the same level.",
            "Where a single specimen must be run, prepare a balance tube of the same "
            "type, filled with water to the same mass, and place it opposite.",
            "Never run a single tube alone, and never leave empty bucket positions "
            "unmatched in a swing-out rotor.",
            "Close and lock the lid before starting.",
        ]
    )

    H(doc, "6.4 Setting the run", 2)
    P(
        doc,
        "Set the centrifuge in relative centrifugal force (x g), not in revolutions per "
        "minute, wherever the instrument allows it. The bench SOP for each examination "
        "states the force and the time. Where an instrument can only be set in rpm, the "
        "rpm equivalent for that rotor is calculated and displayed on a card fixed to the "
        "instrument, and it is recalculated whenever the rotor changes.",
    )
    P(
        doc,
        "The relation between the two is:",
        bold_lead="",
    )
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("RCF (x g)  =  1.118 \u00d7 10\u207b\u2075  \u00d7  r  \u00d7  (rpm)\u00b2")
    r.bold = True
    r.font.size = Pt(11)
    P(
        doc,
        "where r is the radius in centimetres, measured from the centre of rotation to "
        "the bottom of the tube in the loaded position. Because r differs between "
        "rotors and between bucket types, an rpm figure is never transferred from one "
        "centrifuge to another.",
    )

    H(doc, "6.5 During and after the run", 2)
    B(
        doc,
        [
            "Never open the lid while the rotor is turning, and never try to slow the "
            "rotor by hand.",
            "Stay within sight or hearing of the instrument until it has stopped. Stop "
            "the run at once if there is loud vibration, a scraping noise, or movement of "
            "the instrument on the bench.",
            "After the rotor has come to a complete stop, wait a further five minutes "
            "before opening the lid if the load contained infectious material, to allow "
            "any aerosol to settle.",
            "Open the lid slowly and inspect the tubes for breakage before removing them.",
            "Remove tubes promptly. Do not leave specimens in a stopped centrifuge.",
        ]
    )

    H(doc, "6.6 Broken tube or spill", 2)
    NUM(
        doc,
        [
            "Do not open the lid for 30 minutes if the load contained infectious "
            "material. Display a warning notice on the instrument.",
            "Put on gloves, a gown, eye protection and a mask.",
            "Open the lid slowly and remove the rotor or buckets to a tray. Do not pour "
            "liquid out of the bowl.",
            "Remove glass or plastic fragments with forceps, never with the hands.",
            "Flood the bowl and the buckets with 1% hypochlorite and leave for 30 "
            "minutes, then wipe with absorbent paper.",
            "Clean the rotor, buckets and seals with 70% ethanol, and dry fully before "
            "reassembly.",
            "Discard materials as infectious waste. Record the incident on the fault and "
            "incident log.",
            "Have the rotor inspected by the service provider before it returns to use.",
        ]
    )

    H(doc, "6.7 Routine cleaning", 2)
    TBL(
        doc,
        ["Frequency", "Task"],
        [
            ("After each use", "Wipe the bowl, the rotor and the lid seal with 70% "
                               "ethanol if any spill is visible. Dry."),
            ("Daily", "Wipe the exterior with a damp cloth and a mild detergent. Clean "
                      "the control panel with a dry cloth only."),
            ("Weekly", "Remove the rotor, clean behind it, clean the drive shaft and the "
                       "bowl with 70% ethanol, and inspect the rotor and buckets for "
                       "corrosion."),
            ("Monthly", "Inspect the rotor for cracks with a bright light and a "
                        "magnifier. Record the inspection. Check the lid interlock by "
                        "trying to open the lid during a low-speed run."),
        ],
        widths=[3.4, 13.2],
    )
    P(
        doc,
        "Do not use hypochlorite on aluminium rotors, because it corrodes them. Use 70% "
        "ethanol or the disinfectant specified by the manufacturer.",
    )

    H(doc, "6.8 Speed and timer verification", 2)
    P(
        doc,
        "The speed and the timer of every centrifuge are verified every six months and "
        "after any repair that touches the drive, the control board or the rotor.",
    )
    TBL(
        doc,
        ["Parameter", "Method", "Acceptance limit"],
        [
            ("Speed", "Hand-held tachometer or the manufacturer's calibration mode, at "
                      "three points across the working range", "Within \u00b1 10% of the "
                                                                   "set value"),
            ("Timer", "Stopwatch, at 5 minutes and at 15 minutes",
             "Within \u00b1 5% of the set time"),
            ("Lid interlock", "Attempt to open the lid during rotation",
             "Lid remains locked; rotor stops when opened"),
            ("Emergency stop / brake", "Operate the stop control at mid speed",
             "Rotor decelerates smoothly"),
        ],
        widths=[3.6, 8.2, 4.8],
    )
    P(
        doc,
        "A centrifuge that fails verification is labelled OUT OF SERVICE and is not used "
        "for patient specimens until it has been adjusted and re-verified. Verification "
        "results are recorded in the centrifuge verification log, dated and signed by the "
        "person who performed them and by the Quality Officer.",
    )

    H(doc, "6.9 Annual preventive maintenance", 2)
    P(
        doc,
        "The service provider performs the following once a year and documents it in a "
        "signed report.",
    )
    TBL(
        doc,
        ["Item", "What is checked"],
        [
            ("Rotor and buckets", "Cracks, corrosion, elongation of tube holes, "
                                  "trunnion wear; rotor life hours against the "
                                  "manufacturer's limit"),
            ("Drive", "Bearings, brushes where fitted, motor mounts, noise and vibration"),
            ("Lid and interlock", "Latch, hinge, interlock switch, gas strut"),
            ("Electrical safety", "Earth continuity, insulation resistance, cord, plug, "
                                  "fuse rating"),
            ("Controls", "Speed, timer, brake, imbalance detector"),
            ("Calibration", "Speed and timer re-verified after service"),
        ],
        widths=[4.6, 12.0],
    )
    P(
        doc,
        "Rotors have a finite life expressed in hours of use or in years. The equipment "
        "BMeT keeps a rotor life record for each rotor: the date it entered service, "
        "the manufacturer's stated life, and the cumulative hours of use. A rotor that "
        "reaches its stated life, or that is dropped or shows a crack, is retired from "
        "service and destroyed, not stored.",
    )

    H(doc, "6.10 Faults and withdrawal from service", 2)
    TBL(
        doc,
        ["Symptom", "Probable cause", "Action"],
        [
            ("Loud vibration or walking on the bench", "Load out of balance",
             "Stop; rebalance; check rotor seating"),
            ("Scraping or grinding noise", "Bearing or rotor contact",
             "Out of service; service visit"),
            ("Will not start", "Lid interlock, fuse, power",
             "Check interlock and power; out of service if not resolved"),
            ("Rotor stops slowly or will not stop", "Brake fault",
             "Out of service"),
            ("Speed drifts or exceeds setting", "Control fault",
             "Out of service; re-verify after repair"),
            ("Rotor corroded, cracked or scored", "Chemical attack or fatigue",
             "Retire the rotor; do not use"),
        ],
        widths=[5.4, 5.0, 6.2],
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Centrifuges with speed and timer verification within the 6-month interval",
             "100%"),
            ("Tube breakages per quarter", "0"),
            ("Centrifuges out of service more than 7 days", "0"),
            ("Rotor inspections recorded monthly", "100%"),
            ("Out-of-limit verifications not followed by corrective action", "0"),
        ],
        widths=[11.6, 5.0],
    )

    tail(
        doc,
        [
            ("Centrifuge Preventive maintenance / cleaning log",
             "5 years", "6. Equipment > 7. PM and temperature logs"),
            ("Speed and timer verification log", "5 years", "Equipment records"),
            ("Rotor life record", "Life of rotor + 5 years", "Equipment records"),
            ("Fault, repair and breakage log", "5 years", "Equipment records"),
            ("Annual service report, signed", "Life of instrument + 5 years",
             "Equipment records"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "Bench SOPs for each examination, which state the required RCF and time",
            "Laboratory equipment inventory",
        ],
        [
        ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022.",
         "https://www.iso.org/standard/76677.html"),
        "ISO 15189:2022, clause 6.3.3 on decontamination and 7.8 on reports of adverse incidents.",
        ("IEC 61010-2-020:2026, Safety requirements for electrical equipment for measurement, control and laboratory use \u2013 Part 2-020: Particular requirements for laboratory centrifuges. Edition 4.0. Geneva: International Electrotechnical Commission; 2026. Published on 2 September 2026; it cancels the 2016 third edition that earlier drafts of this SOP cited.",
         "https://webstore.iec.ch/en/publication/90934"),
        "Manufacturer's operating and service manual for each centrifuge model in use: centrifuge 1207 and HUMAX 4K.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


# =====================================================================
# 3. WATER BATH
# =====================================================================
def waterbath():
    code, title = "055", "Operation, Care and Preventive Maintenance of the Water Bath"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "The laboratory water bath is used to bring reagents and specimens to a defined "
        "temperature: for the inactivation of serum before serology, for warming "
        "reagents used in the cross-match, and for melting and holding media and stains. "
        "In each of these uses the result depends on the water being at the temperature "
        "stated, and on the water itself being clean.",
    )
    P(
        doc,
        "A water bath is also one of the most heavily contaminated items in a clinical "
        "laboratory. Water at 37 \u00b0C to 56 \u00b0C with traces of protein is an "
        "efficient incubator for Gram-negative bacteria and for biofilm, which then "
        "contaminates every tube and reagent that enters it. Scum floating on the surface "
        "and a film on the inner wall are the visible signs; they appear within two weeks "
        "of neglect in this climate. The bath is also a combination of mains electricity "
        "and standing water, which makes electrical safety part of its maintenance.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "This SOP defines how the water bath is filled, used, checked for temperature, "
        "cleaned and disinfected, verified and serviced, and the records that show it was "
        "at the correct temperature and in a clean condition whenever it was used for "
        "patient specimens.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to every thermostatically controlled water bath, water bath "
        "with a shaking platform, and circulating bath in the laboratory, and to any "
        "bead bath or dry block heater used in place of a water bath.",
    )
    P(
        doc,
        "It does not describe the incubation conditions for a particular examination. "
        "Those are stated in each bench SOP.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("Set point", "The temperature to which the bath is adjusted."),
            ("Working temperature", "The actual temperature of the water, measured with a "
                                    "calibrated thermometer."),
            ("Verification", "Confirmation, against a calibrated reference thermometer, "
                             "that the working temperature is within the acceptance "
                             "limit of the set point."),
            ("Biofilm", "A layer of micro-organisms attached to the inner surfaces of the "
                        "bath, resistant to simple rinsing."),
            ("Calibrated reference thermometer",
             "A thermometer with a current certificate traceable to a national standard."),
            ("PM", "Preventive maintenance."),
        ],
        widths=[5.2, 11.4],
    )

    H(doc, "5. Responsibilities and Authorisation")
    TBL(
        doc,
        ["Role", "Responsibility"],
        [
            ("Director General",
             "Approves this SOP and signs the cover block and the signature page. Under "
             "ISO 15189:2022 the approval of a controlled laboratory document rests with "
             "the head of the institution, not with the laboratory."),
            ("Laboratory Manager",
             "Is accountable for this SOP and for the resources it requires. Authorises "
             "withdrawal from service, and countersigns the SOP for approval by the "
             "Director General."),
            ("Laboratory Quality Officer",
             "Holds the calibration certificate for the reference thermometer, reviews "
             "the temperature log monthly, and investigates excursions."),
            ("Bench staff", "Check and record the temperature each working day, maintain "
                            "the water level, and clean as scheduled."),
            ("BMeT (Biomedical Equipment Technician)",
             "Holds the inventory, the temperature log and the service records."),
            ("BMeT, or the service provider",
             "Performs the annual PM, the electrical safety test and any repair. The "
             "BMeT performs the electrical safety test where the hospital holds the "
             "test instrument, and witnesses the rest."),
        ],
        widths=[5.4, 11.2],
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Filling and water quality", 2)
    B(
        doc,
        [
            "Fill with distilled or deionised water, never with tap water. Tap water "
            "deposits calcium scale on the heater and on the tubes.",
            "Fill to the level marked by the manufacturer, normally 2 to 3 cm below the "
            "rim. Never operate below the minimum level; the heater will burn out.",
            "Do not overfill. Water that reaches the rim spills into the control housing.",
            "Add the biocide recommended by the manufacturer at the stated "
            "concentration, where one is recommended.",
        ]
    )

    H(doc, "6.2 Daily checks", 2)
    NUM(
        doc,
        [
            "Check the water level and top up with distilled water if needed.",
            "Check the set point on the display against the temperature required by the "
            "bench SOP in use.",
            "Measure the working temperature with the calibrated reference thermometer, "
            "held in the water for at least two minutes and not touching the heater, the "
            "wall or a tube.",
            "Record the reading, the time, the set point and the initials on the "
            "temperature log.",
            "Check that the water is clear and free of scum, particles and odour. If it "
            "is not, drain and clean before use.",
        ]
    )
    P(
        doc,
        "A reading outside the acceptance limit takes the bath out of service. Specimens "
        "or reagents already processed in it during that shift are reviewed by the "
        "section head against the bench SOP and the incident log entry is made.",
    )

    H(doc, "6.3 Weekly cleaning and disinfection", 2)
    P(
        doc,
        "The bath is drained, cleaned and refilled once a week on a fixed day, and "
        "immediately after any spill of specimen or reagent.",
    )
    NUM(
        doc,
        [
            "Switch off and unplug the bath. Allow it to cool below 40 \u00b0C.",
            "Drain the water through the tap or by tipping, into the sink with running "
            "water.",
            "Clean the inner walls, the floor of the tank and the heater guard with a soft "
            "cloth and a mild detergent. Do not use an abrasive pad on the stainless "
            "steel.",
            "Rinse thoroughly with distilled water until no detergent remains.",
            "Disinfect with 70% ethanol or with the agent recommended by the "
            "manufacturer, and rinse again with distilled water.",
            "Refill with fresh distilled water to the correct level, add biocide if used, "
            "and switch on.",
            "Allow the bath to reach the set point, verify the temperature and record it "
            "before use.",
        ]
    )

    H(doc, "6.4 Temperature verification", 2)
    P(
        doc,
        "The temperature is verified with the calibrated reference thermometer monthly, "
        "after any repair or adjustment, and after the bath has been moved.",
    )
    TBL(
        doc,
        ["Set point", "Acceptance limit", "Frequency"],
        [
            ("37 \u00b0C", "\u00b1 1.0 \u00b0C", "Daily check; monthly full verification"),
            ("56 \u00b0C (inactivation)", "\u00b1 1.0 \u00b0C",
             "Daily check; monthly full verification"),
            ("100 \u00b0C (boiling)", "Boiling observed", "Each use"),
        ],
        widths=[4.4, 5.4, 6.8],
    )
    P(
        doc,
        "The reference thermometer certificate is renewed every two years by a provider "
        "traceable to a national standard, and the certificate is filed with the "
        "equipment records. A reference thermometer without a current certificate is not "
        "used to verify a bath.",
    )

    H(doc, "6.5 Electrical safety", 2)
    B(
        doc,
        [
            "Plug into a socket protected by a residual current device.",
            "Never operate the bath with wet hands or with water on the control panel.",
            "Keep the control housing and the ventilation slots dry. Wipe the exterior "
            "with a cloth that is damp, not wet.",
            "Inspect the cord and plug weekly for cracks; a damaged cord takes the bath "
            "out of service.",
            "Earth continuity and insulation resistance are checked at the annual PM.",
        ]
    )

    H(doc, "6.6 Annual preventive maintenance", 2)
    TBL(
        doc,
        ["Item", "What is checked"],
        [
            ("Heater and thermostat", "Response, overshoot, stability over one hour"),
            ("Temperature calibration", "Adjusted to the reference thermometer where "
                                        "adjustable, then re-verified"),
            ("Seals and gaskets", "Perished rubber, leaks at the tap and the heater gland"),
            ("Electrical safety", "Earth continuity, insulation resistance, cord and plug"),
            ("Tank", "Scale, corrosion, pitting"),
            ("Lid and cover", "Fit, condensation control"),
        ],
        widths=[4.6, 12.0],
    )

    H(doc, "6.7 Faults", 2)
    TBL(
        doc,
        ["Symptom", "Probable cause", "Action"],
        [
            ("Will not heat", "Heater or thermostat failed, fuse, low water cut-out",
             "Out of service; service visit"),
            ("Overheats or boils", "Thermostat failed closed",
             "Unplug immediately; out of service"),
            ("Temperature unstable", "Low water, scale on the heater, faulty sensor",
             "Refill; descale; service if persistent"),
            ("Scum, film or smell", "Biofilm",
             "Drain, clean and disinfect; increase cleaning frequency"),
            ("Leak from the tank or tap", "Perished seal or cracked weld",
             "Out of service; service visit"),
            ("Trips the residual current device", "Electrical fault",
             "Unplug; out of service; report"),
        ],
        widths=[5.2, 5.4, 6.0],
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Daily temperature records present and within limits", "100%"),
            ("Monthly verifications completed", "100%"),
            ("Baths found with visible biofilm at cleaning", "0"),
            ("Temperature excursions without an incident entry", "0"),
            ("Reference thermometer certificate current", "100%"),
        ],
        widths=[11.6, 5.0],
    )

    tail(
        doc,
        [
            ("Water bath temperature log", "5 years",
             "6. Equipment > 7. PM and temperature logs"),
            ("Weekly cleaning and disinfection record", "5 years", "As above"),
            ("Monthly temperature verification record", "5 years", "Equipment records"),
            ("Reference thermometer calibration certificate", "Current + 5 years",
             "Equipment records"),
            ("Annual service report, signed", "Life of instrument + 5 years",
             "Equipment records"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "Bench SOPs that specify the temperature for each procedure",
            "Laboratory equipment inventory",
        ],
        [
        ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022.",
         "https://www.iso.org/standard/76677.html"),
        "ISO 15189:2022, clause 7.3.2 on verification of measuring equipment.",
        ("World Health Organization. Laboratory biosafety manual, 4th edition. Geneva: WHO; 2020.",
         "https://www.who.int/publications/i/item/9789240011311"),
        "Manufacturer's operating manual for the water bath models in use: Memmert and HumAqua 5.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


# =====================================================================
# 4. NON-MEDICAL EQUIPMENT
# =====================================================================
def nonmedical():
    code, title = "056", "Management and Maintenance of Non-Medical Laboratory Equipment"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "Not every instrument in this laboratory examines a specimen, but almost every "
        "examination depends on one that does not. A refrigerator that drifts above 8 "
        "\u00b0C spoils reagents and invalidates every result produced with them. A "
        "water distiller with a spent cartridge delivers water that deposits ions into "
        "every reagent. An air conditioner that stops in a humid season creates the "
        "conditions in which fungus destroys microscope lenses. A failed uninterruptible "
        "power supply takes the analysers down in the middle of a run and can corrupt the "
        "data they hold.",
    )
    P(
        doc,
        "These items are called non-medical equipment here because they do not perform an "
        "examination. In practice they carry more risk per unit than the analysers, "
        "because they are bought, installed and then forgotten. This SOP gives them the "
        "same scheduled attention as the medical devices, and puts them on one inventory "
        "so that none of them is out of sight.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "To define the non-medical equipment of the laboratory, allocate responsibility "
        "for each item, set the monitoring and preventive maintenance schedule for each "
        "class of equipment, and define what happens when one of them fails or drifts out "
        "of specification.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to the following classes of equipment, whether owned, donated "
        "or provided under a maintenance contract:",
    )
    TBL(
        doc,
        ["Class", "Items included"],
        [
            ("Cold storage", "Laboratory refrigerators, blood bank refrigerator, freezers "
                             "at -20 \u00b0C, cold boxes and vaccine carriers, temperature "
                             "monitoring devices and data loggers"),
            ("Water systems", "Water distiller, deioniser, reverse osmosis unit, water "
                              "storage reservoir, filters"),
            ("Air and ventilation", "Air conditioners, extractor fans, fume extraction, "
                                    "biological safety cabinet exhaust ducting"),
            ("Power", "Uninterruptible power supplies, voltage stabilisers, surge "
                      "protection, generator interface and changeover"),
            ("Laboratory environment", "Lighting, benches and fume hoods where no "
                                       "examination is performed, sinks, eye wash "
                                       "station, emergency shower"),
            ("Safety installations", "Fire extinguishers, first aid kits, spill kits, "
                                     "emergency lighting"),
        ],
        widths=[4.4, 12.2],
    )
    P(
        doc,
        "Medical devices are outside the scope of this SOP and are covered by RliDHL-ADM-"
        "SOP-008. Furniture, vehicles and buildings are covered by the hospital's "
        "estates department and are listed here only where the laboratory depends on them "
        "for a controlled condition.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("Cold chain", "The uninterrupted sequence of controlled low temperatures "
                           "from storage to use."),
            ("Excursion", "A measured temperature outside the defined range for the item "
                          "stored."),
            ("Data logger", "A device that records temperature at intervals and can "
                            "export the record."),
            ("UPS", "Uninterruptible power supply: a battery unit that maintains power to "
                    "connected equipment for a short period during a mains failure."),
            ("Voltage stabiliser", "A device that holds the output voltage constant when "
                                   "the input varies."),
            ("RCD", "Residual current device: a switch that trips on earth leakage "
                    "current."),
            ("Conductivity / resistivity", "A measure of the ionic content of purified "
                                           "water. Resistivity falls as ions increase."),
            ("PM", "Preventive maintenance."),
        ],
        widths=[5.2, 11.4],
    )

    H(doc, "5. Responsibilities and Authorisation")
    TBL(
        doc,
        ["Role", "Responsibility"],
        [
            ("Director General",
             "Approves this SOP and signs the cover block and the signature page. Under "
             "ISO 15189:2022 the approval of a controlled laboratory document rests with "
             "the head of the institution, not with the laboratory."),
            ("Laboratory Manager",
             "Is accountable for this SOP and for the resources it requires. Authorises "
             "purchase, replacement and disposal. Signs service contracts and service "
             "reports, and countersigns the SOP for approval by the Director General."),
            ("Laboratory Quality Officer",
             "Owns the non-medical equipment register, sets the maintenance calendar, and "
             "reviews logs monthly."),
            ("BMeT (Biomedical Equipment Technician)",
             "Holds the register, the maintenance log, the temperature and water quality "
             "records, and schedules the contracted services."),
            ("Bench staff",
             "Record refrigerator temperatures twice daily, record water quality daily, "
             "and report any failure at once."),
            ("Hospital estates and maintenance department",
             "Carries out building, air conditioning, plumbing and electrical work under "
             "the service agreement."),
            ("Contracted service provider",
             "Performs scheduled servicing of refrigerators, air conditioners, distillers "
             "and UPS units, and issues a signed report."),
        ],
        widths=[5.4, 11.2],
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Register", 2)
    P(
        doc,
        "Every item in section 3 is entered in the non-medical equipment register with: "
        "asset number, description, manufacturer and model, serial number, date of "
        "purchase or donation, location by room, the person responsible, the maintenance "
        "provider, and the maintenance interval. The register is reviewed at least "
        "annually and whenever an item is added or removed.",
    )
    P(
        doc,
        "Each item carries an asset label. Items that cannot be labelled, such as a "
        "distiller installed in a fixed plumbing line, are identified by the register "
        "entry and a label on the adjacent wall.",
    )

    H(doc, "6.2 Cold storage and cold chain", 2)
    P(
        doc,
        "Temperature ranges are defined for each storage unit according to what it holds:",
    )
    TBL(
        doc,
        ["Storage", "Range", "Monitoring"],
        [
            ("Reagent refrigerator", "2 \u00b0C to 8 \u00b0C", "Twice daily, manual log, "
                                                              "plus data logger"),
            ("Blood bank refrigerator", "2 \u00b0C to 6 \u00b0C",
             "Twice daily, manual log, plus data logger"),
            ("Freezer", "-20 \u00b0C \u00b1 5 \u00b0C",
             "Twice daily, manual log. The unit in use was acquired on 11 August 2026"),
            ("Cold box in transit", "2 \u00b0C to 8 \u00b0C",
             "On departure and on arrival, with a temperature indicator"),
        ],
        widths=[4.6, 4.4, 7.6],
    )
    H(doc, "6.2.1  Bringing a newly acquired unit into service")
    P(
        doc,
        "Equipment that has been moved from another site is not a working cold store until "
        "it has been shown to hold temperature at this site. This applies to every "
        "refrigerator or freezer acquired second-hand or transferred from a health centre, "
        "and it is not satisfied by switching the unit on and reading the display once.",
    )
    NUM(
        doc,
        [
            "Inspect the unit before it is loaded: door seal intact, interior clean and "
            "free of mould, no corrosion on the evaporator, plug and cable undamaged, "
            "compressor running without abnormal noise.",
            "Record the make, model, serial number and, once the biomedical department has "
            "issued one, the hospital asset code. Until an asset code exists, write "
            "\u201cnot yet assigned\u201d and the date of acquisition, and add the unit to "
            "the hospital equipment inventory at the next revision.",
            "Run the unit empty for 24 hours.",
            "Verify the temperature for a full week against a calibrated thermometer or a "
            "data logger, not against the display alone: record the reading at the start "
            "and at the end of each working day for seven consecutive days and confirm it "
            "stays within the range for that class of unit.",
            "Confirm that the door alarm, if fitted, operates, and that the unit recovers "
            "its temperature within 30 minutes of the door being closed after a loading.",
            "Only then load specimens or reagents, and record the verification on the "
            "maintenance record before the first load.",
        ],
    )
    P(
        doc,
        "A unit that fails the week of verification is not used, and the fault is reported "
        "to the biomedical department in the same way as any other equipment fault.",
    )

    P(doc, "Routine monitoring:", bold_lead="")
    B(
        doc,
        [
            "Read the thermometer or logger display at the start and at the end of each "
            "working day and record the reading, the time and the initials.",
            "Do not open the door to read a thermometer; read the external display where "
            "one is fitted.",
            "Keep the unit at least two thirds full and never block the internal fan.",
            "Place no specimen or reagent against the walls or the evaporator plate.",
            "Check that the door seal closes fully and that the alarm is armed.",
        ]
    )
    P(doc, "Action on an excursion:", bold_lead="")
    NUM(
        doc,
        [
            "Move the contents to a verified backup unit or a cold box with a "
            "temperature indicator.",
            "Do not discard anything on the basis of the reading alone. Record the "
            "duration and the extent of the excursion.",
            "Assess the affected reagents and specimens against the manufacturer's "
            "storage specification and the bench SOP. Reagents outside specification are "
            "quarantined, labelled, and referred to the section head for a decision.",
            "Report to the Quality Officer the same day and enter the event in the "
            "incident log.",
            "Do not return the unit to service until the fault is corrected and the "
            "temperature has been verified stable over 24 hours.",
        ]
    )
    P(
        doc,
        "Data loggers are downloaded at least monthly. The downloaded file is retained as "
        "a record. Loggers are replaced or recalibrated annually as the manufacturer "
        "specifies.",
    )

    H(doc, "6.3 Water systems", 2)
    P(
        doc,
        "Purified water is a reagent in this laboratory and is treated as one.",
    )
    TBL(
        doc,
        ["Task", "Frequency", "Acceptance"],
        [
            ("Check conductivity or resistivity of the output", "Daily",
             "Per manufacturer; typically resistivity \u2265 1 M\u03a9\u00b7cm at 25 "
             "\u00b0C for deionised water"),
            ("Check the reservoir level and for visible growth", "Daily",
             "Clear, colourless, no odour"),
            ("Drain and clean the reservoir", "Weekly", "No visible biofilm"),
            ("Replace the pre-filter and carbon cartridge", "Per manufacturer, typically "
                                                           "every 3 to 6 months",
             "Per specification"),
            ("Descale the distiller with citric acid", "Quarterly or when scale is "
                                                       "visible", "No scale on the "
                                                                  "heater or walls"),
            ("Replace the deioniser resin", "When resistivity falls below the limit",
             "Restores resistivity above the limit"),
            ("Microbial check of the reservoir", "Annually", "No significant growth"),
        ],
        widths=[6.2, 4.8, 5.6],
    )
    P(
        doc,
        "Water that fails the conductivity limit is not used for reagent preparation or "
        "for the water bath. The failure, the action taken and the date of restoration "
        "are recorded.",
    )

    H(doc, "6.4 Air conditioning and ventilation", 2)
    B(
        doc,
        [
            "Clean the air conditioner filters monthly and record the cleaning.",
            "Have the units serviced every six months, including gas pressure, drainage "
            "and coil cleaning.",
            "Maintain the laboratory between 18 \u00b0C and 25 \u00b0C and below 70% "
            "relative humidity recorded daily where a hygrometer is installed. This is "
            "the condition that protects the microscopes from fungal growth.",
            "Keep extractor fans running whenever staining, fixation or volatile reagents "
            "are in use.",
            "Do not block return air grilles with stores or boxes.",
        ]
    )

    H(doc, "6.5 Power protection", 2)
    B(
        doc,
        [
            "Every analyser, the LIS server and the refrigerators are connected through a "
            "UPS or a stabiliser of adequate rating.",
            "Test each UPS monthly by simulating a mains failure and confirming that the "
            "connected load remains powered. Record the test.",
            "Record the battery replacement date on the unit. Replace batteries at the "
            "manufacturer's interval, typically every three to five years, or sooner if "
            "the runtime falls below the stated minimum.",
            "Do not connect non-essential loads to the UPS outlets.",
            "Have the hospital generator changeover tested by the estates department and "
            "keep the test record.",
        ]
    )

    H(doc, "6.6 Safety installations", 2)
    B(
        doc,
        [
            "Check fire extinguishers monthly for the pressure gauge in the green zone, "
            "the seal and the tag. Have them serviced annually by a licensed provider.",
            "Check the eye wash station weekly by running it for three minutes, and flush "
            "the emergency shower monthly. Record both.",
            "Restock the spill kits after every use and check them quarterly.",
            "Test emergency lighting quarterly.",
        ]
    )

    H(doc, "6.7 Annual preventive maintenance summary", 2)
    TBL(
        doc,
        ["Equipment", "Frequency", "Provider"],
        [
            ("Refrigerators and freezers", "Annual service plus 6-monthly seal and alarm "
                                           "check", "Contracted provider"),
            ("Air conditioning", "6-monthly", "Hospital estates / provider"),
            ("Water distiller and deioniser", "Cartridge changes per manufacturer, annual "
                                              "service", "Provider / in-house"),
            ("UPS", "Monthly test, battery per interval, annual service", "In-house / "
                                                                        "provider"),
            ("Electrical installation, RCD", "Annual test", "Hospital electrician"),
            ("Fire extinguishers", "Annual", "Licensed provider"),
            ("Data loggers", "Annual calibration", "Provider"),
        ],
        widths=[6.0, 5.4, 5.2],
    )

    H(doc, "6.8 Failure and downtime", 2)
    P(
        doc,
        "When a non-medical item fails, the bench reports it to the BMeT the same day. "
        "The BMeT records it, arranges repair, and informs the Laboratory "
        "Manager where the failure compromises a service. Where the failure affects "
        "patient testing, the contingency arrangements in RliDHL-ADM-SOP-047 apply.",
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Refrigerator temperature records complete for both daily readings", "100%"),
            ("Temperature excursions without an incident entry", "0"),
            ("Water quality checks recorded daily", "100%"),
            ("Scheduled maintenances completed on time", "100%"),
            ("Non-medical items on the register that are unlabelled", "0"),
            ("Eye wash and shower checks recorded monthly", "100%"),
        ],
        widths=[11.6, 5.0],
    )

    tail(
        doc,
        [
            ("Non-medical equipment register", "Permanent", "Equipment records"),
            ("Refrigerator and freezer temperature logs", "5 years",
             "6. Equipment > 7. PM and temperature logs"),
            ("Data logger downloads", "5 years", "Equipment records"),
            ("Water quality (conductivity) log", "5 years", "Equipment records"),
            ("Maintenance and service reports", "Life of item + 5 years",
             "Equipment records"),
            ("UPS test and battery replacement record", "5 years", "Equipment records"),
            ("Fire extinguisher, eye wash and emergency lighting checks", "5 years",
             "Health and safety file"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "RliDHL-ADM-SOP-047 \u2013 Laboratory Contingency Plan",
            "RliDHL-ADM-SOP-004 \u2013 Laboratory Temperature Control",
            "RliDHL-ADM-SOP-034 \u2013 Laboratory Waste Management",
            "RliDHL-ADM-SOP-057 \u2013 Maintenance of ICT Equipment",
        ],
        [
        ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022.",
         "https://www.iso.org/standard/76677.html"),
        "ISO 15189:2022, clause 6.4.4 on preventive maintenance.",
        ("World Health Organization. Laboratory biosafety manual, 4th edition. Geneva: WHO; 2020.",
         "https://www.who.int/publications/i/item/9789240011311"),
        "Manufacturer's manuals for each item on the register.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


# =====================================================================
# 5. ICT EQUIPMENT
# =====================================================================
def ict():
    code, title = "057", "Maintenance of Laboratory ICT Equipment and the Laboratory Information System"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "The laboratory depends on information technology at every step of the "
        "examination process. Specimens are registered on the laboratory information "
        "system, work lists are printed from it, analysers transmit results to it, and "
        "reports are released through it. The equipment that carries this traffic, being "
        "computers, printers, scanners, network switches and the server, sits in a room "
        "full of dust, humidity and the occasional spill, and is usually the last "
        "equipment in the laboratory to receive scheduled attention.",
    )
    P(
        doc,
        "Two distinct risks are managed here. The first is downtime: a failed workstation "
        "or printer stops the release of results, and a failed server stops the "
        "laboratory. The second is loss or disclosure of data. A laboratory holds "
        "identifiable patient results; a lost hard disk, a shared password or an "
        "unprotected backup is a breach of confidentiality as well as a clinical risk. "
        "Both risks are addressed by the same discipline of registration, backup, access "
        "control and planned maintenance.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "To define the ICT equipment of the laboratory, the routine maintenance and "
        "monitoring performed on it, the backup regime, the access control rules, the "
        "procedure when the system is unavailable, and the records kept.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to all laboratory ICT equipment and to the laboratory "
        "information system as used in this laboratory, whether hosted locally or "
        "centrally by the hospital:",
    )
    TBL(
        doc,
        ["Class", "Items included"],
        [
            ("Workstations", "Desktop computers, laptops, thin clients at every bench, "
                             "reception and the office"),
            ("Server and storage", "Laboratory server, network attached storage, external "
                                   "hard disks used for backup"),
            ("Peripherals", "Label and barcode printers, report printers, barcode "
                            "scanners, monitors, keyboards and mice"),
            ("Network", "Switches, routers, wireless access points, cabling and patch "
                        "panels within the laboratory"),
            ("Interfaces", "Analyser to LIS connections, including serial, network and "
                           "middleware links"),
            ("Power for ICT", "UPS and stabilisers dedicated to the server and the "
                              "workstations"),
            ("Portable media", "Encrypted USB drives and any removable storage approved "
                               "for laboratory use"),
        ],
        widths=[4.4, 12.2],
    )
    P(
        doc,
        "Hospital-wide network, email and the hospital information system are administered "
        "by the hospital IT Officer and are outside the scope of this SOP, except "
        "where the laboratory depends on them for results and where the laboratory must "
        "report a fault.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("LIS", "Laboratory information system."),
            ("HIS", "Hospital information system."),
            ("Backup", "A copy of data held separately from the original so that it can be "
                       "restored after loss."),
            ("Restore test", "A planned exercise in which data are recovered from a backup "
                             "to prove that the backup is usable."),
            ("Downtime", "Any period in which the LIS or a critical workstation is not "
                         "available for use."),
            ("RTO", "Recovery time objective: the maximum acceptable time to restore a "
                    "service."),
            ("Least privilege", "The principle that each user is given only the access "
                                "needed to do their work."),
            ("Patching", "Applying manufacturer updates to operating systems and "
                         "software."),
            ("Change control", "The documented approval of a change to a system before it "
                               "is made."),
        ],
        widths=[4.6, 12.0],
    )

    H(doc, "5. Responsibilities and Authorisation")
    TBL(
        doc,
        ["Role", "Responsibility"],
        [
            ("Director General",
             "Approves this SOP and signs the cover block and the signature page. Under "
             "ISO 15189:2022 the approval of a controlled laboratory document rests with "
             "the head of the institution, not with the laboratory."),
            ("Laboratory Manager",
             "Is accountable for this SOP and for the access rights of staff. Authorises "
             "changes to the LIS configuration in writing, and countersigns the SOP for "
             "approval by the Director General."),
            ("Laboratory Quality Officer",
             "Reviews the backup log, the downtime log and the ICT maintenance log "
             "monthly. Investigates any data loss or confidentiality incident."),
            ("ICT Officer",
             "A named member of laboratory staff who carries out the routine tasks in this "
             "SOP, keeps the ICT register, and is the single point of contact with the "
             "IT Officer and the LIS vendor."),
            ("IT Officer (hospital IT)",
             "Administers the network, the server where it is centralised, and hospital "
             "email. Responds to laboratory fault reports."),
            ("LIS vendor",
             "Provides the application support, upgrades and interface maintenance under "
             "contract."),
            ("All staff",
             "Use only their own account, lock the screen when leaving, never share "
             "passwords, and report faults and suspected breaches at once."),
        ],
        widths=[5.0, 11.6],
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 ICT register", 2)
    P(
        doc,
        "Every item in section 3 is entered in the laboratory ICT register with: asset "
        "number, description, manufacturer and model, serial number or service tag, "
        "operating system and version, location, the member of staff who uses it, the "
        "warranty end date, and the support provider. The register is updated whenever an "
        "item is added, moved, re-installed or disposed of.",
    )
    P(
        doc,
        "Antivirus software, the operating system build and the LIS client version are "
        "recorded for each workstation so that a version falling out of support is "
        "visible before it becomes a problem.",
    )

    H(doc, "6.2 Access control and confidentiality", 2)
    NUM(
        doc,
        [
            "Every user has a unique named account. Shared accounts and shared passwords "
            "are not permitted.",
            "Access rights are granted on the principle of least privilege: a bench "
            "technologist does not hold administrator rights, and reception staff see "
            "registration data but not result entry.",
            "Passwords meet the hospital policy length and complexity, are not written on "
            "paper at the bench, and are changed when there is any reason to believe they "
            "are known to another person.",
            "Accounts of staff who leave, or who move to another department, are disabled "
            "on the last working day. The ICT Officer checks the user list against "
            "the staff list every quarter and reports discrepancies to the Laboratory "
            "Manager.",
            "Screens lock automatically after a period set by policy, not longer than ten "
            "minutes, and staff lock the screen manually when leaving the bench.",
            "The audit trail of the LIS is enabled and is not edited or deleted by "
            "laboratory staff.",
            "Patient data are not copied to personal devices, personal email or "
            "unencrypted removable media.",
        ]
    )

    H(doc, "6.3 Routine maintenance schedule", 2)
    TBL(
        doc,
        ["Frequency", "Task"],
        [
            ("Daily", "Confirm that the LIS is available and that results are "
                      "transmitting from each analyser interface. Confirm that the "
                      "scheduled backup ran and record the result. Check printers for "
                      "paper and toner. Check that antivirus definitions are current."),
            ("Weekly", "Check free disk space on the server and on workstations. Clean "
                       "dust from keyboard, screen bezel and the ventilation grilles of "
                       "desktop units. Check for any pending operating system or "
                       "application update and log it for the change window."),
            ("Monthly", "Apply approved updates in the agreed change window, outside "
                        "working hours. Test each UPS serving ICT by simulating a mains "
                        "failure. Check the server room or cabinet for heat, dust and "
                        "unauthorised items. Review the user account list."),
            ("Monthly", "Perform a restore test: recover a defined set of data from the "
                        "most recent backup to a temporary location and confirm that it "
                        "opens and is complete."),
            ("Quarterly", "Review the ICT register against the physical equipment. Check "
                          "cabling and labelling. Review the downtime and incident logs "
                          "with the Quality Officer."),
            ("Annually", "Full hardware inventory audit. Review and renew the vendor "
                         "support contract. Test the disaster recovery plan, including "
                         "running the laboratory on the manual system for a defined "
                         "period."),
        ],
        widths=[3.0, 13.6],
    )
    P(
        doc,
        "Cleaning of ICT equipment uses a dry or lightly dampened lint-free cloth on the "
        "exterior only. No liquid is sprayed onto a keyboard, a screen or a printer. The "
        "inside of a computer, the server and the printer mechanisms are cleaned only by "
        "the support provider.",
    )

    H(doc, "6.4 Backup", 2)
    P(
        doc,
        "The loss of the LIS database is the single most serious ICT event that can occur "
        "in this laboratory. The backup regime is therefore defined and tested, not "
        "assumed.",
    )
    TBL(
        doc,
        ["Backup", "Frequency", "Retention", "Location"],
        [
            ("Database incremental", "Daily, automated", "30 days", "Server or NAS"),
            ("Database full", "Weekly", "12 weeks", "NAS plus an off-site copy"),
            ("Interface and configuration files", "After any change", "Current plus one "
                                                                     "previous",
             "Server"),
            ("Workstation documents and templates", "Weekly", "8 weeks", "NAS"),
        ],
        widths=[5.4, 3.8, 3.4, 4.0],
    )
    B(
        doc,
        [
            "The backup job is monitored. A failed backup is investigated the same day and "
            "recorded in the backup log.",
            "At least one copy of each weekly full backup is held physically away from the "
            "laboratory, so that a fire or theft in the laboratory does not destroy both "
            "the system and its backup.",
            "Backup media are encrypted where they leave the laboratory. A lost "
            "unencrypted backup is treated as a confidentiality incident.",
            "Backups are restored, not merely created. The monthly restore test is the "
            "only evidence that the backup is usable, and it is recorded.",
        ]
    )

    H(doc, "6.5 Downtime procedure", 2)
    P(
        doc,
        "When the LIS is unavailable, the laboratory continues to receive and test "
        "specimens using the manual system, and the following steps apply:",
    )
    NUM(
        doc,
        [
            "The ICT Officer declares downtime, informs the Laboratory Manager and "
            "records the start time in the downtime log.",
            "Specimens are registered on the paper downtime register, which is kept at "
            "reception and is pre-printed with the same fields as the LIS.",
            "Results are recorded on the bench worksheet and reported to the clinician by "
            "the route defined in the contingency plan, marked as reported during "
            "downtime.",
            "The cause and the expected duration are communicated to clinical staff so "
            "that urgent testing can be prioritised.",
            "On restoration, the ICT Officer confirms that the system and the "
            "analyser interfaces are working, then supervises the entry of the downtime "
            "records into the LIS.",
            "The entries are checked by a second person against the paper record, and the "
            "check is signed.",
            "The downtime log is closed with the restoration time and the number of "
            "specimens affected, and the event is reviewed with the Quality Officer.",
        ]
    )
    P(
        doc,
        "The manual system is exercised at least annually during the disaster recovery "
        "test, so that staff are familiar with it before it is needed.",
    )

    H(doc, "6.6 Changes, updates and new equipment", 2)
    B(
        doc,
        [
            "Any change to the LIS configuration, an interface, a report template or a "
            "workstation that affects result handling is requested in writing and "
            "approved by the Laboratory Manager before it is made. The change is recorded "
            "with the date, the person who made it and how it was verified.",
            "Operating system and application updates are applied in a defined change "
            "window, after a backup, and the LIS and each interface are tested afterwards.",
            "New analyser interfaces are validated by running patient and control samples "
            "in parallel with the existing route before the interface is used for "
            "reporting. The validation is recorded.",
            "Software is installed only from the vendor or an approved source. Unlicensed "
            "software is not installed on laboratory computers.",
        ]
    )

    H(doc, "6.7 Portable media and cybersecurity", 2)
    B(
        doc,
        [
            "Only laboratory-issued, encrypted USB drives are used, and only for the "
            "purpose for which they were issued.",
            "Every removable medium is scanned before use. Autorun is disabled on all "
            "laboratory computers.",
            "Staff do not open attachments or links from unknown senders on a laboratory "
            "computer, and do not connect a personal device to the laboratory network.",
            "Suspected malware, a ransomware message or any unexplained change to files is "
            "reported immediately. The affected equipment is disconnected from the network "
            "and left powered on for investigation.",
            "Antivirus is installed on every workstation and server, definitions update "
            "automatically, and a full scan runs weekly.",
        ]
    )

    H(doc, "6.8 Disposal and decommissioning", 2)
    P(
        doc,
        "Before any computer, server, hard disk, printer with internal storage or "
        "removable medium leaves the laboratory, its storage is destroyed or securely "
        "wiped so that no patient data can be recovered. The destruction is witnessed and "
        "recorded in the ICT disposal record, which states the asset number, the method "
        "used and the two people present. Equipment is not sold, donated or handed to "
        "another department with its storage intact.",
    )

    H(doc, "6.9 Faults and escalation", 2)
    TBL(
        doc,
        ["Fault", "First action", "Escalation"],
        [
            ("Workstation will not start", "Check power, UPS, monitor cable",
             "ICT Officer; spare workstation"),
            ("Cannot log in", "Check account status with the ICT Officer",
             "IT Officer"),
            ("Printer will not print", "Check paper, toner, queue, cable",
             "ICT Officer; call the provider"),
            ("Analyser results not reaching the LIS", "Check the interface cable and the "
                                                       "middleware service",
             "LIS vendor"),
            ("LIS slow or unresponsive", "Note the time and the number of users",
             "IT Officer and vendor"),
            ("Server down", "Declare downtime per 6.5", "IT Officer and "
                                                         "vendor immediately"),
            ("Suspected data breach or lost device", "Do not delete anything; secure the "
                                                     "area",
             "Laboratory Manager and Quality Officer immediately"),
        ],
        widths=[5.2, 5.6, 5.8],
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Scheduled backups completed", "\u2265 99%"),
            ("Monthly restore tests performed and successful", "100%"),
            ("Downtime events without a downtime log entry", "0"),
            ("LIS downtime exceeding 4 hours in a month", "0"),
            ("User accounts not matching the current staff list", "0"),
            ("Confidentiality incidents", "0"),
            ("ICT items on the register that are missing at audit", "0"),
        ],
        widths=[11.6, 5.0],
    )

    tail(
        doc,
        [
            ("Laboratory ICT register", "Permanent", "ICT file"),
            ("Backup log", "2 years", "ICT file"),
            ("Restore test record", "2 years", "ICT file"),
            ("Downtime log and downtime register sheets", "5 years", "ICT file and "
                                                                    "reception"),
            ("Change record for LIS and interfaces", "5 years", "ICT file"),
            ("User account review", "5 years", "ICT file"),
            ("ICT maintenance and service records", "Life of item + 5 years", "ICT file"),
            ("ICT disposal and data destruction record", "Permanent", "ICT file"),
            ("Confidentiality incident reports", "5 years", "Quality file"),
        ],
        [
            "RliDHL-ADM-SOP-042 \u2013 Laboratory Information System",
            "RliDHL-ADM-SOP-047 \u2013 Laboratory Contingency Plan",
            "RliDHL-ADM-SOP-008 \u2013 Use and Maintenance of Biomedical Equipment",
            "RliDHL-ADM-SOP-056 \u2013 Management and Maintenance of Non-Medical "
            "Laboratory Equipment",
            "RliDHL-ADM-SOP-019 \u2013 Document and Record Control",
        ],
        [
        ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022.",
         "https://www.iso.org/standard/76677.html"),
        "ISO 15189:2022, clause 7.6 (control of data and information management) and clause 7.6.6 on contingency and downtime.",
        "ISO 15189:2022, clauses 6.4 (equipment) and 8.4 (control of records).",
        ("ISO/IEC 27001:2022, Information security, cybersecurity and privacy protection \u2014 Information security management systems \u2014 Requirements. Geneva: ISO/IEC; 2022, with Amendment 1:2024, where the hospital operates a certified system.",
         "https://www.iso.org/standard/27001"),
        ("Republic of Rwanda. Law No. 058/2021 of 13/10/2021 relating to the protection of personal data and privacy. Official Gazette n\u00b0 Special of 15/10/2021.",
         "https://cyber.gov.rw/fileadmin/user_upload/NCSA/Documents/Laws/OG_Special_of_15.10.2021_Amakuru_bwite.pdf"),
        "Manufacturer and vendor documentation for the LIS and the analyser interfaces in use.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


if __name__ == "__main__":
    microscope()
    centrifuge()
    waterbath()
    nonmedical()
    ict()
    print("done")
