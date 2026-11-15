#!/usr/bin/env python3
"""
Adds the instrument-specific maintenance SOPs:
  ADM-058  Hematology analysers (Sysmex XN-330, Sysmex XQ-320 and the Alere Pima
           CD4 analyser, the three in service)
  ADM-059  GeneXpert Dx System, written from Cepheid source material
Reuses the layout helpers in build_sops.py.
"""
import os
from build_sops import base_doc, H, P, B, NUM, TBL, tail

OUT = os.path.dirname(os.path.abspath(__file__))


def hematology():
    code = "058"
    title = "Use, Care and Preventive Maintenance of Hematology Analysers"
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "The full blood count is the most frequently requested examination in this "
        "laboratory and it is produced almost entirely by automated analysers. The "
        "analyser aspirates a small volume of anticoagulated blood, dilutes it, lyses "
        "part of it and counts and sizes cells by impedance and, in the five-part "
        "instruments, by fluorescence flow cytometry. Every result the department issues "
        "rests on the assumption that the fluidic system is clean, the reagents are "
        "correct and in date, the background count is acceptable, and the instrument has "
        "passed its quality control that day.",
    )
    P(
        doc,
        "None of those assumptions is visible in the result. A partially blocked "
        "aspiration probe produces a plausible but falsely low platelet count. A "
        "deteriorated lyse reagent inflates the lymphocyte percentage. A background count "
        "that has drifted upward adds phantom cells to every sample counted after it. "
        "Because the failure is silent, the maintenance described in this SOP is not "
        "housekeeping: it is the control that makes the numbers trustworthy.",
    )
    P(
        doc,
        "The laboratory operates three analysers in this section: the Sysmex XN-330, the "
        "Sysmex XQ-320 and the Alere Pima CD4 analyser. They are not the same instrument. "
        "The XN-330 is the larger of the two Sysmex instruments and produces a full "
        "differential; the XQ-320 is a compact analyser used for the routine workload and "
        "as the backup when the XN-330 is down; the Pima is a single-purpose, "
        "battery-capable instrument that counts CD4 cells from a finger-prick or venous "
        "sample and is used to stage and monitor HIV infection. This SOP sets one "
        "maintenance discipline that applies to all three, and states separately where a "
        "limit or an interval differs between them, so that the standard does not depend "
        "on which instrument a sample happens to reach.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "To define the daily, weekly, monthly and periodic maintenance of the hematology "
        "analysers, the acceptance criteria for background counts and quality control, "
        "the action to take when those criteria are not met, and the records that show "
        "the instrument was fit for patient testing on the day it was used.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to every automated analyser held in the Hematology section, "
        "including the CD4 analyser, and to any such analyser used at a linked site under "
        "this laboratory's supervision. That includes the Pima when it is carried to a "
        "clinic or health centre for the day, in which case the same start-up, control and "
        "recording requirements apply at the site of use.",
    )
    TBL(
        doc,
        ["Analyser", "Serial no.", "Asset code", "Location", "Provision year", "Role"],
        [
            ("Sysmex XN-330", "17156", "RULIDH/LAB/ME/0501", "Hematology Room",
             "2025", "Main haematology analyser"),
            ("Sysmex XQ-320", "12357", "RULIDH/LAB/ME/0499", "Hematology Room",
             "2025", "Routine workload and backup"),
            ("Alere Pima CD4", "PIMA-D-005378", "RULIDH/LAB/ME/0485", "Hematology Room",
             "2018", "CD4 count"),
        ],
        widths=[2.8, 2.4, 3.4, 2.6, 1.6, 3.8],
    )
    P(
        doc,
        "All three are held on the hospital equipment inventory under the asset code "
        "shown. The serial number and the asset code in this table are what must be "
        "written at the head of every maintenance log sheet, so that a record can be "
        "traced to one physical instrument and not merely to \u201cthe Sysmex\u201d or "
        "\u201cthe Pima\u201d.",
    )
    P(
        doc,
        "The parameters, the measuring principle and the maintenance tasks are not "
        "identical between the three instruments. The two Sysmex analysers aspirate "
        "anticoagulated whole blood, dilute and lyse it, and count cells by impedance "
        "and fluorescence flow cytometry. The Pima works differently: it takes a "
        "capillary or venous sample into its own cartridge, the cartridge is the reaction "
        "chamber, and the instrument reports an absolute CD4 count and percentage. It has "
        "no reagents to lot-track in the way the Sysmex instruments do, and its "
        "consumable is the cartridge itself. Confirm the parameters each reports, and its "
        "own limits for background, carryover and precision, against the operator manual "
        "held beside it. Do not carry a limit from one instrument to another.",
    )
    P(
        doc,
        "This SOP does not replace the bench SOP for the full blood count, which defines "
        "specimen acceptance, the reporting of results and the reference intervals. It "
        "also does not replace the manufacturer's manual. Where the manual requires a "
        "task more often, or an additional task, the manual prevails and this SOP is "
        "amended at the next review.",
    )
    H(doc, "3.1  Analysers withdrawn from service")
    P(
        doc,
        "Four analysers that this laboratory once used have been decommissioned: the "
        "Sysmex KX-21N (serial B9854, asset RULIDH/LAB/ME/0087), the Sysmex XS-500i "
        "(serial 11491, asset RULIDH/LAB/ME/0108), the Pochi and the Humacount 5. They "
        "appear on the hospital inventory as physically absent and disposed of, or were "
        "never held on it.",
    )
    P(
        doc,
        "This SOP therefore does not apply to them, and no maintenance is performed on "
        "them. Their legacy bench SOPs are retained in the Hematology folder for "
        "historical reference only and are marked superseded; they must not be used to "
        "run a sample. If any of these instruments is reintroduced, it must be added to "
        "the table in section 3, commissioned and verified against its own manual, and "
        "this SOP amended before it is used for patient testing.",
    )
    P(
        doc,
        "The same rule applies in reverse: when the XN-330 or the XQ-320 is withdrawn, "
        "the maintenance log is closed, the instrument is marked out of service on the "
        "inventory, and this SOP is amended at the next review so that the record does "
        "not describe an instrument the laboratory no longer has.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("Background count",
             "The particle count produced when the instrument aspirates diluent or "
             "cleaning solution instead of blood. It proves the fluidic path is clean."),
            ("Blank / rinse",
             "The cycle that washes the aspirator and the counting chamber between "
             "samples."),
            ("Carryover",
             "Contamination of a sample by the previous sample, measured by running a "
             "diluent blank immediately after a high-value sample."),
            ("IQC",
             "Internal quality control: stabilised control material of known value run "
             "each day before patient samples."),
            ("eQC / EQA",
             "External quality assessment: the national or regional proficiency scheme."),
            ("Clog",
             "A partial or complete obstruction of the aspiration probe, the counting "
             "aperture or the tubing."),
            ("Waste",
             "The diluted, lysed waste blood leaving the instrument, which is "
             "biohazardous and contains cyanide-free but still irritant reagents."),
            ("CD4 count",
             "The absolute number of CD4 T-lymphocytes per microlitre of blood, "
             "reported with the CD4 percentage of lymphocytes. It is the laboratory "
             "measure used to stage HIV infection and to decide when to start or "
             "change antiretroviral treatment."),
            ("Cartridge",
             "The single-use Pima test cartridge. It contains the reagents and the "
             "flow path, so it is the Pima's consumable in place of the diluent, lyse "
             "and cleaner used on the Sysmex instruments."),
            ("PM", "Preventive maintenance."),
            ("BMeT",
             "Biomedical Equipment Technician. The hospital's biomedical engineering "
             "post, held by Pacifique ISHIMWE at Ruli District Hospital. The BMeT holds "
             "the equipment inventory, the service records and the service contracts, and "
             "performs the maintenance within the hospital's competence. The BMeT does "
             "not review laboratory documents; that is the role of the Laboratory Quality "
             "Manager."),
            ("ADF", "Assay definition file. Not used in hematology; listed for "
                    "completeness of the equipment vocabulary."),
        ],
        widths=[4.4, 12.2],
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
             "Prepares and signs this SOP, and reviews it before it goes for approval. Is "
             "accountable for it and for the resources it requires. Authorises the "
             "withdrawal of an analyser from service and the purchase of reagents and "
             "service."),
            ("Laboratory Quality Manager",
             "Reviews this SOP when it is prepared and after every amendment, and "
             "maintains the controlled document system, the review register and the "
             "change log. Reviews QC trends monthly and investigates any period in which "
             "a failed QC was followed by released results."),
            ("Section head, Hematology",
             "Reviews the daily maintenance log and the QC record every working day "
             "before results are released. Authorises a repeat run after a QC failure."),
            ("Bench technologist",
             "Performs and records the daily and weekly tasks. Runs and interprets the "
             "background count and the IQC. Reports faults immediately."),
            ("BMeT (Biomedical Equipment Technician)",
             "Holds the analyser inventory, the service record and the contract with the "
             "supplier. Performs the electrical safety checks and the tasks within the "
             "hospital's competence, and witnesses the annual service."),
            ("Supplier service engineer",
             "Performs the scheduled and corrective service visits and issues a signed "
             "service report."),
        ],
        widths=[4.6, 12.0],
    )
    P(
        doc,
        "Only staff trained on the specific analyser and competence-assessed on it may "
        "perform the daily start-up, the quality control run or any maintenance task that "
        "requires the instrument to be placed in a service mode.",
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Environment, siting and power", 2)
    B(
        doc,
        [
            "Site the analyser on a stable bench free of vibration, away from direct "
            "sunlight and away from the sink, the water bath and the centrifuge.",
            "Maintain the room within the range stated in the operator manual, typically "
            "15 \u00b0C to 30 \u00b0C, and keep relative humidity below 70%.",
            "Allow the clearance around the instrument that the manual specifies for "
            "ventilation and for opening the covers.",
            "Connect through a voltage stabiliser or an uninterruptible power supply. "
            "Hematology analysers are sensitive to voltage dips, and a dip during a run "
            "loses the sample and can corrupt the stored data.",
            "Keep the instrument out of the direct line of an air conditioner vent, which "
            "causes dust to settle into the aspiration area.",
        ]
    )

    H(doc, "6.2 Reagents, controls and consumables", 2)
    B(
        doc,
        [
            "Store diluent, lyse, cleaner and sheath fluid within the temperature range on "
            "the label, and never allow a reagent pack to freeze.",
            "Record the lot number and the expiry date of each reagent and control when it "
            "is opened, and again when it is replaced.",
            "Do not use a reagent beyond its expiry date or beyond its stated in-use "
            "stability after opening. An expired lyse reagent gives falsely high "
            "lymphocyte percentages that look entirely plausible.",
            "Allow refrigerated reagents and controls to reach room temperature and mix "
            "them gently before use, as the package insert requires.",
            "Verify each new lot of control against its assigned values before the lot is "
            "put into routine use, and record the verification.",
            "Keep the waste container below the maximum level marked on it, and treat the "
            "contents as infectious waste.",
            "For the Pima, check the cartridge lot number and expiry date on the foil "
            "pouch before use, and store cartridges at the temperature the package insert "
            "states. A cartridge that has been frozen, or left in the sun, is discarded "
            "and not run, because the resulting count cannot be distinguished from a true "
            "low CD4.",
            "Record the cartridge lot in use on the working sheet and on the daily log, so "
            "that a run of implausible CD4 results can be traced to a lot.",
        ]
    )

    H(doc, "6.3 Daily start-up, before the first patient sample", 2)
    NUM(
        doc,
        [
            "Check that the reagents are present, in date and at a sufficient level, and "
            "that the waste container has capacity.",
            "Switch on the analyser and allow the warm-up period stated in the manual.",
            "Run the background or blank count, or the automatic start-up cycle, as the "
            "manual directs.",
            "Confirm that the background count is zero or below the limit printed in the "
            "operator manual for each parameter reported. Record the result.",
            "Run the internal quality control at the levels the bench SOP specifies, "
            "normally a normal level and at least one abnormal level.",
            "Confirm that every control result lies within its assigned mean \u00b1 2 "
            "standard deviations, and apply the control rules in 6.6.",
            "Record on the daily maintenance log: date, reagent lots, background result, "
            "QC outcome, instrument temperature where displayed, and initials.",
            "Only then begin patient testing.",
        ]
    )
    P(
        doc,
        "The first six steps above are written for the Sysmex analysers, which have a "
        "fluid system to prime and a background count to run. The Pima has neither. Its "
        "start-up is shorter and is set out separately so that no step in the list above "
        "is ticked for it that the instrument cannot actually perform.",
    )
    H(doc, "6.3.1 Daily start-up of the Alere Pima CD4 analyser", 3)
    NUM(
        doc,
        [
            "Confirm the Pima is charged, or connected to mains power through its "
            "supply, and that the battery holds enough charge to complete the planned "
            "runs. A run interrupted by a flat battery wastes the cartridge and the "
            "sample.",
            "Check the instrument temperature and that it has had time to equilibrate to "
            "the room, particularly if it has been carried between rooms or used "
            "outside.",
            "Run the electronic or manufacturer-supplied check the manual requires, at "
            "the interval it states, and record the outcome.",
            "Run a CD4 control, at the level the bench SOP specifies, before the first "
            "patient sample of the day. The Pima is a single-analyte instrument, so the "
            "control is the whole of its daily quality evidence and is not optional.",
            "Confirm the control lies within its assigned mean \u00b1 2 standard "
            "deviations, and apply the rules in 6.6.",
            "Record on the daily log: date, cartridge lot, control lot and outcome, "
            "instrument check result, temperature if displayed, and initials.",
            "Only then begin patient testing.",
        ]
    )
    P(
        doc,
        "The Pima is portable and may be used in the clinic or at a health centre. When "
        "it is moved, repeat the temperature equilibration and the control run at the new "
        "site before testing, and record the site on the log. A control run in the "
        "laboratory does not cover a run performed elsewhere.",
    )

    H(doc, "6.4 Daily, during and at the end of the shift", 2)
    B(
        doc,
        [
            "Inspect the aspiration probe for blood residue and wipe it with a lint-free "
            "tissue moistened with the cleaner recommended by the manufacturer.",
            "Watch the first few aspirations of the shift for a short sample, a clot or an "
            "aspiration error. A clot in the probe is the most common cause of a falsely "
            "low platelet count.",
            "Do not leave the instrument standing with blood in the line. Run the shutdown "
            "or standby cycle at the end of the shift as the manual directs.",
            "Empty or check the waste container, and never let it reach the overflow "
            "level.",
            "Wipe the exterior with a cloth moistened with a mild detergent or 70% "
            "ethanol. Never spray liquid onto the instrument.",
            "Switch off, or leave in standby, exactly as the manual states. Some models "
            "must remain powered for the reagent to stay cool.",
        ]
    )
    P(
        doc,
        "A significant change in ambient temperature or humidity triggers a repeat of the "
        "background count and the QC before further patient samples are run.",
    )

    H(doc, "6.5 Weekly and monthly maintenance", 2)
    TBL(
        doc,
        ["Frequency", "Task", "Acceptance"],
        [
            ("Weekly", "Clean the aspiration probe and the wash block with the recommended "
                       "cleaner, following the manual's procedure",
             "No visible residue; background within limit after cleaning"),
            ("Weekly", "Wash or replace the peristaltic pump tube where the model has one",
             "No deformation, no leak, smooth aspiration"),
            ("Weekly", "Clean the sample rotor and the tube holder",
             "Free of dried blood"),
            ("Weekly", "Check tubing and connections for leaks, air bubbles and crimping",
             "No leak, no trapped air"),
            ("Weekly", "Confirm printer paper, labels and barcode reader operation",
             "Readable output; barcode read at first attempt"),
            ("Monthly", "Run the extended cleaning or descaling cycle specified by the "
                        "manufacturer", "Background within limit afterwards"),
            ("Monthly (Pima)", "Clean the exterior and the cartridge port with the "
                               "solution the manual names; inspect the port for dried "
                               "blood or dust and remove it",
             "Port clean; cartridge seats without resistance"),
            ("Monthly (Pima)", "Check the instrument check or the reference check the "
                               "manual specifies, and the battery condition",
             "Passes; battery completes a working day"),
            ("Monthly", "Inspect the apertures and the flow cell according to the manual, "
                        "and clean only as the manual permits",
             "No clot, no debris"),
            ("Monthly", "Review QC charts for bias and trend over the month",
             "No shift or trend; documented review"),
            ("Monthly", "Check the date and time on the instrument against the laboratory "
                        "clock", "Within one minute"),
            ("Monthly", "Review the maintenance log and the fault log for gaps",
             "No missing day"),
        ],
        widths=[2.8, 8.6, 5.2],
    )
    P(
        doc,
        "Tasks that require the instrument to be opened, the aperture to be removed or a "
        "service mode to be entered are performed only by staff trained for that task or "
        "by the supplier's engineer. Where a decision is in doubt, call the engineer.",
    )

    H(doc, "6.6 Quality control rules and the action to take", 2)
    P(
        doc,
        "Internal quality control is the daily proof that the analyser is measuring "
        "correctly. It is run before patient samples and it is recorded whether it passes "
        "or fails.",
    )
    NUM(
        doc,
        [
            "A control result outside the mean \u00b1 2 standard deviations is repeated "
            "once with a fresh aliquot of the same control.",
            "If the repeat is also outside, a second, different level of control is run. "
            "Two levels outside 2 SD, or any single result outside 3 SD, is a rejection: "
            "patient results are not released from that instrument until the cause is "
            "found.",
            "A trend, a shift or a rising coefficient of variation across several days is "
            "treated as a failure even when each individual point is inside 2 SD.",
            "Check in this order: control storage and handling, control expiry, reagent "
            "lot and expiry, background count, a clot or partial blockage, and finally "
            "calibration.",
            "Recalibrate only when the manual permits it and only with the specified "
            "calibrator. Record the calibration, the values before and after, and the "
            "person who performed it.",
            "If the failure is not resolved by these steps, take the analyser out of "
            "service, label it, and call the supplier. Patient samples are run on the "
            "backup analyser.",
            "Any patient result already released from a period later found to be affected "
            "is reviewed, and the clinician is informed in line with the laboratory's "
            "nonconforming work procedure.",
        ]
    )

    H(doc, "6.7 Calibration and verification", 2)
    B(
        doc,
        [
            "Calibration is performed with the manufacturer's calibrator and at the "
            "interval the manufacturer states, after replacement of a counting aperture, "
            "a flow cell or a significant component, and whenever QC indicates a bias that "
            "cannot be explained by reagent or control.",
            "Verification, as distinct from calibration, is performed after any service "
            "visit, after a move of the instrument, and at the annual PM, by running three "
            "levels of control and comparing the results with assigned values.",
            "The record states the calibrator lot, the expiry, the values entered, the "
            "coefficients applied, and the acceptance decision.",
        ]
    )

    H(doc, "6.8 Scheduled service and annual preventive maintenance", 2)
    TBL(
        doc,
        ["Item", "What the supplier checks"],
        [
            ("Fluidic system", "Tubing, pumps, valves, seals, waste path"),
            ("Counting apertures and flow cell", "Condition, cleanliness, replacement if "
                                                 "worn"),
            ("Aspiration and sampling", "Probe alignment, sample volume accuracy, carryover"),
            ("Optics and detectors", "Alignment, signal gain, cleanliness"),
            ("Mechanics", "Sample rotor, racks, barcode reader, door sensors"),
            ("Electrical safety", "Earth continuity, insulation, cord and plug"),
            ("Software", "Version, database integrity, backup of patient data and settings"),
            ("Performance verification", "Background, carryover, reproducibility, "
                                         "calibration verification"),
        ],
        widths=[4.8, 11.8],
    )
    P(
        doc,
        "The Pima is serviced on the same schedule but against a shorter list. Its "
        "scheduled visit covers the optical and electronic system, the cartridge port and "
        "its seals, the battery and charging circuit, the enclosure and its earth "
        "continuity, and a verification run against control material. It has no counting "
        "aperture, no peristaltic pump and no reagent line, so those items on the table "
        "above do not apply to it.",
    )
    P(
        doc,
        "The service report is signed by the engineer and by the Laboratory Manager, filed "
        "with the equipment records, and the next service date is entered on the PM "
        "schedule in the format of the laboratory PM planner.",
    )

    H(doc, "6.9 Faults and withdrawal from service", 2)
    TBL(
        doc,
        ["Symptom", "Probable cause", "Action"],
        [
            ("Aspiration error or short sample", "Clot in the probe, low sample volume, "
                                                 "worn pump tube",
             "Clean the probe, check the tube, rerun; service if persistent"),
            ("Platelet count unexpectedly low", "Clot, partial blockage, sample "
                                                "aggregation",
             "Repeat on a fresh tube; check the probe; inspect the film"),
            ("Background count above limit", "Contaminated diluent or chamber, dirty "
                                             "aperture",
             "Run the cleaning cycle; replace diluent; service if unresolved"),
            ("QC drift or rising CV", "Reagent deterioration, worn aperture, calibration "
                                      "drift",
             "Follow the sequence in 6.6; recalibrate or call service"),
            ("Pressure or fluidic error", "Leak, blocked waste, pump failure",
             "Out of service"),
            ("Barcode not read", "Dirty window, label quality, misalignment",
             "Clean the window; check the label; service if persistent"),
            ("Analyser will not power up", "Power, fuse, stabiliser",
             "Check power; out of service"),
            ("Pima cartridge rejected at insertion", "Cartridge not at room "
                                                     "temperature, dirty cartridge "
                                                     "port, expired lot",
             "Equilibrate the cartridge, clean the port, check the lot; discard if expired"),
            ("Pima run aborted part-way", "Low battery, instrument moved, cartridge "
                                          "dislodged",
             "Repeat on a new cartridge once the cause is corrected; record the abort"),
            ("Implausible CD4 count (very low or very high)", "Clot or short sample, "
                                                             "cartridge lot fault, "
                                                             "control failure",
             "Repeat on a fresh sample; if it recurs across samples, quarantine the "
             "cartridge lot and run the control again"),
        ],
        widths=[5.0, 5.4, 6.2],
    )

    H(doc, "6.10 Data and results integrity", 2)
    B(
        doc,
        [
            "Patient results are held on the analyser's work list and released only after "
            "the QC for that day has passed.",
            "Results transmitted to the laboratory information system are checked against "
            "the work list before release, and any result flagged by the analyser is "
            "reviewed, not simply accepted.",
            "The analyser's internal database is backed up at the interval the manual "
            "specifies, and before any service visit.",
            "The instrument date and time are correct, because they are attached to every "
            "result and to the audit trail.",
        ]
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Days with a completed and signed daily maintenance log", "100%"),
            ("Days with IQC run before the first patient sample", "100%"),
            ("Patient results released after a failed QC without corrective action", "0"),
            ("Scheduled PM completed within the month due", "100%"),
            ("Analyser downtime exceeding one working day", "0"),
            ("Repeat runs caused by a specimen or instrument fault", "Monitored and trended"),
            ("Calibration records available for every calibration performed", "100%"),
            ("CD4 control run before the first patient sample (Pima)", "100%"),
            ("CD4 runs rejected for an expired or unrecorded cartridge lot", "0"),
            ("Turnaround for a CD4 result requested at the clinic", "Same working day"),
        ],
        widths=[11.4, 5.2],
    )

    tail(
        doc,
        [
            ("Daily maintenance log, analyser (monthly sheet)", "5 years",
             "6. Equipment > 7. PM and temperature logs"),
            ("IQC record and Levey-Jennings charts", "5 years", "Hematology folder"),
            ("Reagent and control lot record", "5 years", "Hematology folder"),
            ("CD4 cartridge lot and run record, including site of testing", "5 years",
             "Hematology folder"),
            ("Calibration and verification record", "5 years", "Equipment records"),
            ("Service report, signed", "Life of instrument + 5 years",
             "Equipment records"),
            ("Fault and downtime log", "5 years", "Equipment records"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "RliDHL-ADM-SOP-056 \u2013 Management and Maintenance of Non-Medical "
            "Laboratory Equipment (power protection)",
            "RliDHL-ADM-SOP-058 daily maintenance log form and the scheduled PM record",
            "Bench SOP for the full blood count and for each analyser model in use, "
            "including the CD4 bench SOP",
            "HIV testing and treatment monitoring algorithm of the Rwanda Ministry of "
            "Health, for the clinical use of the CD4 result",
        ],
        [
            ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: International Organization for Standardization; 2022, clauses 6.4 (equipment), 6.4.4 (preventive maintenance), 7.3.2 (verification) and 7.3.7 (quality control).",
             "https://www.iso.org/standard/76677.html"),
            "ISO 15189:2022, clause 7.3.6 on documentation of examination procedures.",
            ("Clinical and Laboratory Standards Institute. C24, Statistical Quality Control for Quantitative Measurement Procedures: Principles and Definitions. 4th edition. Wayne, PA: CLSI; 2016.",
             "https://clsi.org/shop/standards/c24/"),
            ("Clinical and Laboratory Standards Institute. QMS01, A Quality Management System Model for Laboratory Services. 6th edition. Wayne, PA: CLSI; 2026.",
             "https://clsi.org/shop/standards/qms01/"),
            ("World Health Organization. Laboratory quality management system: handbook. Geneva: WHO; 2011, on the management of equipment records.",
             "https://www.who.int/publications/i/item/9789241548274"),
            ("World Health Organization. Consolidated guidelines on HIV prevention, testing, treatment, service delivery and monitoring: recommendations for a public health approach. Geneva: WHO; 2021, for the CD4 thresholds that trigger clinical action.",
             "https://www.who.int/publications/i/item/9789240031593"),
            ("Rwanda Ministry of Health. National guidelines for prevention and management of HIV. Kigali: Ministry of Health; 2020, for the national algorithm that sets when a CD4 count is requested.",
             "https://www.prepwatch.org/wp-content/uploads/2022/08/Rwanda-National-HIV-Guidelines-for-Prevention-Management-of-HIV-2020.pdf"),
            "Manufacturer's operator and service manuals for each analyser model in use (Sysmex XN-330, Sysmex XQ-320, Alere Pima CD4), supplied with the instrument and held beside it; no public link, because the manual is model- and serial-specific.",
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


def genexpert():
    code = "059"
    title = ("Use, Care and Preventive Maintenance of the GeneXpert Dx System")
    doc = base_doc(code, title)

    H(doc, "1. Introduction")
    P(
        doc,
        "The GeneXpert Dx System performs the laboratory's molecular testing for "
        "tuberculosis and rifampicin resistance, HIV viral load, HIV early infant "
        "diagnosis, and hepatitis B and C viral load. Each module is an independent "
        "instrument containing a syringe, a thermal unit and a fluorescent detection "
        "system, and each module is calibrated individually.",
    )
    P(
        doc,
        "The maintenance regime is set by Cepheid and differs in one important respect "
        "from most laboratory equipment: the annual requirement is a calibration of every "
        "module, not merely a cleaning. Cepheid calibrates each module once a year or "
        "after 2,000 tests on that module, whichever comes first, and a module that has "
        "passed its calibration date must not be used for patient testing. The remaining "
        "tasks are cleaning and disinfection, which keep the optical detection system and "
        "the plunger mechanism free of bleach residue, dust and dried blood.",
    )
    P(
        doc,
        "The laboratory additionally operates in a dusty environment, and Cepheid states "
        "that in areas of high dust or air pollution the optics should be cleaned "
        "monthly rather than at the longer interval. That condition applies here and is "
        "written into this SOP.",
    )

    H(doc, "2. Purpose")
    P(
        doc,
        "To define the daily, weekly, monthly, quarterly, annual and as-needed "
        "maintenance of the GeneXpert system exactly as Cepheid specifies it, together "
        "with the module calibration requirement, the acceptance criteria and the records "
        "that demonstrate that only calibrated modules were used for patient testing.",
    )

    H(doc, "3. Scope")
    P(
        doc,
        "This SOP applies to the GeneXpert Dx System in the molecular area of the "
        "laboratory, including its controlling computer, the GeneXpert Dx software, all "
        "installed modules, and the dust cover and cleaning accessories.",
    )
    P(
        doc,
        "It covers the instrument only. The procedures for each assay, the cartridge "
        "handling, the specimen preparation and the interpretation of results are defined "
        "in the assay-specific SOPs, which are listed in section 9.",
    )
    P(
        doc,
        "The manufacturer's Operator Manual, Chapter 9, Service and Maintenance, is the "
        "authoritative source. This SOP reproduces its requirements in the laboratory's "
        "format and adds the laboratory's responsibilities, records and acceptance "
        "criteria. Where this SOP and the current Cepheid documentation differ, the "
        "Cepheid documentation prevails and this SOP is amended.",
    )

    H(doc, "4. Definitions and Abbreviations")
    TBL(
        doc,
        ["Term", "Definition"],
        [
            ("Module",
             "One independent testing position within the instrument. A four-module "
             "instrument runs four tests at once. Each module is calibrated separately."),
            ("Cartridge",
             "The single-use test device containing the reaction tubes and the reagents "
             "for one sample."),
            ("I-CORE",
             "The optical module inside the instrument that reads the fluorescence signal. "
             "It is cleaned with the I-CORE cleaning brush."),
            ("Plunger rod",
             "The spring-loaded rod that drives the syringe in the cartridge. It is "
             "cleaned from the Maintenance menu."),
            ("Xpert Check",
             "The Cepheid calibration kit used to verify and recalibrate modules. One kit "
             "covers four modules."),
            ("ADF",
             "Assay definition file: the software definition of an assay, updated when "
             "Cepheid releases a new version or after a software upgrade."),
            ("Archive and purge",
             "Exporting completed test records to storage and removing them from the "
             "active database to keep the system responsive."),
            ("Dust cover",
             "The fabric cover supplied with the instrument, which is the first defence "
             "against dust entering the optics."),
            ("PPE", "Personal protective equipment."),
        ],
        widths=[4.2, 12.4],
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
             "Is accountable for this SOP and for the resources it requires. Ensures the "
             "annual calibration kits are budgeted and procured. Authorises withdrawal of "
             "a module from use, and countersigns the SOP for approval by the Director "
             "General."),
            ("Molecular section head",
             "Holds the module calibration register and confirms before each run that "
             "every module in use is within its calibration date."),
            ("Laboratory Quality Manager",
             "Reviews the maintenance log and the calibration register monthly. "
             "Investigates any period in which a module was used out of calibration."),
            ("Bench technologist",
             "Performs and records the daily, weekly and monthly tasks. Reports errors and "
             "module failures immediately."),
            ("Cepheid authorised service provider, or the laboratory technologist "
             "designated in writing for this task",
             "Performs the annual calibration and any repair, and issues the calibration "
             "certificate."),
        ],
        widths=[5.6, 11.0],
    )
    P(
        doc,
        "Only staff trained by Cepheid or by an authorised service provider, and "
        "competence-assessed, may perform the plunger maintenance, the fan filter "
        "replacement, the I-CORE cleaning or the annual calibration.",
    )

    H(doc, "6. Procedure")

    H(doc, "6.1 Materials kept at the instrument", 2)
    P(
        doc,
        "These are the materials Cepheid specifies. Substituting another disinfectant, in "
        "particular a stronger chlorine solution, damages the plastic and the optics.",
    )
    TBL(
        doc,
        ["Material", "Specification", "Note"],
        [
            ("Chlorine solution",
             "1:10 dilution of household bleach, giving about 0.5% available chlorine",
             "Prepared fresh and used within 1 day of preparation. Discard unused "
             "solution."),
            ("Ethanol",
             "70% ethanol, or 70% isopropyl alcohol", "Never use 100% ethanol."),
            ("Wipes and swabs",
             "Lint-free wipes, non-cotton swabs",
             "Cotton swabs shed fibres onto the optics."),
            ("Detergent", "Mild detergent and clean water",
             "For the fan filter only."),
            ("Brushes", "I-CORE cleaning brush and the brushes supplied with the system",
             "Per Cepheid supply."),
            ("PPE", "Disposable gloves and eye protection",
             "Required for every disinfection task."),
            ("Fan filters", "Replacement filters and prefilters from Cepheid",
             "Kept as a stock item; do not substitute."),
        ],
        widths=[3.8, 7.4, 5.4],
    )

    H(doc, "6.2 Siting and environment", 2)
    B(
        doc,
        [
            "Leave at least 10 cm clear on all sides of the instrument. Cepheid states "
            "this explicitly because the fan draws air through the filters.",
            "Keep the instrument out of direct sunlight and away from a window, a sink or "
            "an air conditioner vent.",
            "Maintain the room at the temperature stated in the Operator Manual and keep "
            "relative humidity below the stated maximum.",
            "Connect the instrument and the computer through an uninterruptible power "
            "supply. A power interruption during a run loses the cartridge and can leave "
            "the module in an error state.",
            "Keep the dust cover on whenever the instrument is not in use. In this "
            "environment it is the single most useful maintenance action available.",
            "Do not place cartridges, manuals or boxes on top of the instrument or against "
            "its ventilation grilles.",
        ]
    )

    H(doc, "6.3 Daily maintenance", 2)
    P(
        doc,
        "Performed at the end of each testing day, or at the start of the shift before "
        "testing resumes, and recorded on the daily maintenance log.",
    )
    NUM(
        doc,
        [
            "Remove every used cartridge from its module and discard it into the "
            "infectious waste container. Do not leave a cartridge in a module.",
            "Close all module doors. A door left open admits dust and the system will not "
            "pass its self-check.",
            "Clean and disinfect the work area around the instrument, following the "
            "laboratory's bench decontamination procedure.",
            "Confirm that there is 10 cm of clearance on every side of the instrument.",
            "Place the dust cover over the instrument whenever it is not in use.",
            "Record the date, the tasks performed and the initials on the daily "
            "maintenance log.",
        ]
    )

    H(doc, "6.4 Weekly maintenance", 2)
    NUM(
        doc,
        [
            "Disinfect the interior of the cartridge bay of every module, using the "
            "disinfection procedure in 6.7. Open each module door, clean the interior of "
            "the bay, the inside of the door and the top lip of the door, and close the "
            "door.",
            "Do not touch the narrow slit at the back of the cartridge bay into which the "
            "cartridge reaction tube is inserted. Cepheid warns of this explicitly and "
            "damage to that slit takes the module out of service.",
            "Restart the instrument and the computer in the correct order: close the "
            "software, power down the computer, power down the instrument, wait two "
            "minutes, power up the instrument, then the computer, then launch the "
            "software.",
            "Clean the fan prefilter, where the model has one, by washing it in water and "
            "detergent and drying it completely between two paper towels before "
            "replacing it.",
            "Record the tasks and the initials on the log.",
        ]
    )
    P(
        doc,
        "The restart is required because the software accumulates memory over a week of "
        "continuous operation. It is not required on days when the instrument and computer "
        "are already powered down at the end of each day, but the log must then record "
        "that fact.",
    )

    H(doc, "6.5 Monthly maintenance", 2)
    P(
        doc,
        "Each task below is recorded separately. The plunger cleaning is performed through "
        "the software and must not be done by hand.",
    )
    TBL(
        doc,
        ["Task", "Method", "Acceptance"],
        [
            ("Clean the plunger rods",
             "In the software, Maintenance then Plunger Maintenance, select the module or "
             "Clean All, follow the dialog. The plungers lower automatically. Clean each "
             "rod with bleach solution, wait 2 minutes, then with 70% ethanol. Then select "
             "Move Up All and Close.",
             "No visible residue on the rod; plungers return without error"),
            ("Clean the instrument surfaces",
             "Shut down the system. Wipe all outside surfaces and the bench around the "
             "instrument with a lint-free wipe moistened with 70% ethanol. One wipe for "
             "the instrument, a fresh one for the bench.",
             "No visible soil; no liquid entering any opening"),
            ("Clean the fan filter",
             "Unplug the instrument. Remove the rear panel screws with a cross-head "
             "screwdriver, remove the grey foam filter, wash in water and detergent, dry "
             "completely, replace, refit the panel.",
             "Filter completely dry before refitting; no dust on the filter face"),
            ("Clean the module tube slots",
             "Clean the slots with a swab moistened with 70% ethanol, as the manual "
             "directs.", "No debris in the slot"),
            ("Archive and purge tests",
             "Archive completed tests to the external device, then purge them from the "
             "active database, following the manual.",
             "Database responsive; archive file readable"),
            ("Back up the database",
             "Copy the database to the approved external device and record the file name "
             "and location.", "Backup file opens and contains the month's runs"),
        ],
        widths=[4.0, 8.2, 4.4],
    )
    P(
        doc,
        "Because this laboratory is in a dusty environment, the optics are cleaned "
        "monthly rather than at the longer interval Cepheid allows for clean sites. The "
        "I-CORE is cleaned with the I-CORE cleaning brush as part of the monthly optics "
        "task, and the date is recorded.",
    )

    H(doc, "6.6 Quarterly and annual maintenance", 2)
    TBL(
        doc,
        ["Frequency", "Task", "Who performs it"],
        [
            ("Quarterly",
             "Replace the fan filters and prefilters, review the error and system logs, "
             "and confirm that no module is approaching its calibration limit",
             "Trained laboratory technologist"),
            ("Annually, or after 2,000 tests on a module, whichever comes first",
             "Calibrate every module with the Xpert Check kit. One kit covers four "
             "modules. Record the calibration date for each module separately.",
             "Cepheid authorised service provider, or a trained laboratory technologist "
             "where the laboratory is authorised to perform it"),
            ("Annually",
             "Full preventive maintenance by the service provider, including I-CORE "
             "condition, syringe and plunger mechanism, door sensors, fans and "
             "electrical safety",
             "Service provider"),
            ("As needed",
             "Update the assay definition file after a software upgrade; print the system "
             "log report; clean the I-CORE; re-run a module that has failed",
             "Trained laboratory technologist"),
            ("After any repair or module replacement",
             "Calibrate the replacement module before it is used for patient testing",
             "Service provider"),
        ],
        widths=[4.4, 7.8, 4.4],
    )

    H(doc, "6.7 Disinfection procedure", 2)
    P(
        doc,
        "This is the Cepheid procedure for the work area, the cartridge bay, the plunger "
        "rods and the instrument surfaces. The two-step sequence is essential: the "
        "chlorine kills, and the ethanol removes the chlorine residue, which would "
        "otherwise corrode the metal parts and cloud the optics.",
    )
    NUM(
        doc,
        [
            "Put on gloves and eye protection.",
            "Dampen a lint-free wipe or a non-cotton swab with the 1:10 bleach solution, "
            "prepared the same day.",
            "Wipe the surface or element to be cleaned.",
            "Discard the used wipe.",
            "Wait at least 2 minutes for the contact time Cepheid specifies. Where the "
            "laboratory's infection prevention and control policy requires a longer "
            "contact time, follow the longer time.",
            "Dampen a new wipe with 70% ethanol.",
            "Wipe the same surface or element.",
            "Discard the wipe, and repeat the ethanol step once more.",
            "Discard the wipes as infectious waste, and allow the surfaces to dry "
            "completely before closing the module door or powering up.",
        ]
    )
    P(
        doc,
        "After a spill inside a module, the cartridge bay is cleaned by this procedure "
        "before any further cartridge is loaded, and the event is recorded.",
    )

    H(doc, "6.8 Module calibration register", 2)
    P(
        doc,
        "A module used out of calibration produces results that cannot be defended and, "
        "where the instrument is still under warranty, may void it. The laboratory "
        "therefore keeps a register with one row per module:",
    )
    TBL(
        doc,
        ["Column", "Content"],
        [
            ("Module number", "The module position, 1 to 16"),
            ("Serial number", "The module serial number from the software"),
            ("Installation date", "Date the module entered service"),
            ("Date of last calibration", "From the calibration certificate"),
            ("Calibration kit lot and expiry", "From the Xpert Check kit"),
            ("Tests run since calibration", "Cumulative count from the software"),
            ("Calibration due", "The earlier of one year after the last calibration or "
                                "2,000 tests on that module"),
            ("Status", "In use, due, overdue, out of service"),
        ],
        widths=[5.2, 11.4],
    )
    P(
        doc,
        "The section head checks the register before the first run of each day. A module "
        "whose calibration has expired is disabled in the software or clearly marked and "
        "is not used for patient testing.",
    )

    H(doc, "6.9 Faults and error codes", 2)
    TBL(
        doc,
        ["Symptom or error", "Likely cause", "Action"],
        [
            ("Module will not initialise or a module error appears at start-up",
             "Door sensor, plunger obstruction, communication fault",
             "Restart per 6.4. If the error persists, take the module out of service and "
             "call the provider"),
            ("Cartridge error during a run", "Cartridge not seated, wrong cartridge, "
                                              "damaged reaction tube",
             "Discard the cartridge, inspect the bay, repeat with a new cartridge"),
            ("Repeated cartridge errors on one module", "Plunger or tube slot "
                                                        "contaminated",
             "Clean per 6.5 and repeat"),
            ("Fluorescence or signal error", "Dirty optics, I-CORE contamination",
             "Clean the I-CORE; if unresolved, service"),
            ("Pressure or fluidic error", "Syringe or plunger fault",
             "Out of service; service call"),
            ("Software slow, database large", "Tests not archived and purged",
             "Archive and purge per 6.5"),
            ("Computer will not communicate with the instrument",
             "Cable, USB port, power state", "Power down in the specified order and "
                                             "restart"),
            ("Module calibration overdue", "Calibration not performed",
             "Module withdrawn from use until calibrated"),
        ],
        widths=[5.2, 4.6, 6.8],
    )
    P(
        doc,
        "Before telephoning Cepheid or the authorised service provider, have ready the "
        "instrument serial number, the module number, the error code, a description of "
        "what happened, and the archived run if one exists. Cepheid Technical Support "
        "asks for these four items.",
    )

    H(doc, "6.10 Waste and biosafety", 2)
    B(
        doc,
        [
            "Used cartridges are contaminated with amplified nucleic acid and with "
            "specimen. They are discarded into the infectious waste stream and never into "
            "general waste.",
            "Do not open a used cartridge.",
            "Perform cartridge removal and disinfection with gloves. Add eye protection "
            "when there is any risk of splash.",
            "Work with the module door closed and the instrument running normally; do not "
            "lean into an open module while a run is in progress.",
            "In the event of a spill inside the instrument, follow 6.7 and record the "
            "incident.",
        ]
    )

    H(doc, "6.11 Software and assay definition files", 2)
    B(
        doc,
        [
            "The GeneXpert Dx software version in use is recorded on the instrument "
            "record.",
            "When Cepheid releases a software update, the assay definition files are "
            "re-imported after the update, and the import is recorded with the date and "
            "the file version.",
            "A software change is not made in the middle of a run, and the module "
            "calibration status is checked after any software update.",
            "The computer is dedicated to the instrument. No other software, and no "
            "personal use, is permitted on it.",
        ]
    )

    H(doc, "7. Monitoring and Quality Indicators")
    TBL(
        doc,
        ["Indicator", "Target"],
        [
            ("Days with a completed daily maintenance log", "100%"),
            ("Weekly, monthly and quarterly tasks completed in the period due", "100%"),
            ("Modules used for patient testing with a current calibration", "100%"),
            ("Modules out of calibration in use at any time", "0"),
            ("Module downtime exceeding seven days", "0"),
            ("Failed runs attributable to instrument maintenance", "Monitored and trended"),
            ("Calibration certificates filed for every module", "100%"),
        ],
        widths=[11.6, 5.0],
    )

    tail(
        doc,
        [
            ("GeneXpert daily maintenance log (monthly sheet)", "5 years",
             "6. Equipment > 7. PM and temperature logs"),
            ("Module calibration register", "Life of module + 5 years",
             "Molecular section"),
            ("Calibration certificates, one per module per year", "Life of module + 5 "
                                                                  "years",
             "Equipment records"),
            ("Service and repair reports", "Life of instrument + 5 years",
             "Equipment records"),
            ("Database backup records", "2 years", "Molecular section"),
            ("Error and downtime log", "5 years", "Equipment records"),
        ],
        [
            "17. Use and Maintenance of Biomedical Equipment (RliDHL-ADM-SOP-008-VERS-005)",
            "RliDHL-ADM-SOP-056 \u2013 Management and Maintenance of Non-Medical "
            "Laboratory Equipment (power protection)",
            "RliDHL-MYC-SOP-002 \u2013 TB Bacilloscopy using Auramine",
            "RliDHL-MOL-SOP-002 \u2013 HIV Early Infant Diagnosis using GeneXpert",
            "RliDHL-MOL-SOP-003 \u2013 Hepatitis B Virus Viral Load using GeneXpert",
            "RliDHL-MOL-SOP-004 \u2013 Hepatitis C Virus Viral Load using GeneXpert",
            "Tuberculosis testing in stool using Xpert Ultra (TB folder)",
            "Sample processing using GeneXpert (TB folder)",
        ],
        [
            ("Cepheid. GeneXpert\u00ae Maintenance: GeneXpert Dx System, document 301-7990 Rev. C. August 2021.",
             "https://www.cepheid.com/content/dam/www-cepheid-com/documents/documents/Cepheid-GeneXpertDx-Maintenenace%20presentation-Global-301-7990-Rev.C-English%20.pdf"),
            ("Global Laboratory Initiative. Training package on Xpert MTB/RIF, Module 10, Maintenance, adapted from Cepheid.",
             "https://www.stoptb.org/who-we-are/stop-tb-working-groups/global-laboratory-initiative-gli/training-packages/xpert-mtbrif"),
            "Cepheid. GeneXpert\u00ae System Maintenance Log, document 302-8386 Rev. C. Supplied with the instrument.",
            "Cepheid. GeneXpert\u00ae Dx System Operator Manual, Chapter 9, Service and Maintenance. Supplied with the instrument; the copy held in the laboratory is the authoritative version.",
            "Cepheid. Xpert\u00ae MTB/RIF and Xpert\u00ae MTB/RIF Ultra assay package inserts, for the handling requirements that affect instrument use.",
            ("ISO 15189:2022, Medical laboratories \u2014 Requirements for quality and competence. 4th edition. Geneva: ISO; 2022, clauses 6.4 (equipment), 6.4.4 (preventive maintenance), 7.3.2 (verification) and 7.6 (control of data and information).",
             "https://www.iso.org/standard/76677.html"),
        ],
    )
    doc.save(os.path.join(OUT, f"RliDHL-ADM-SOP-{code}-VERS-001 - {title}.docx"))


if __name__ == "__main__":
    hematology()
    genexpert()
    print("done")
