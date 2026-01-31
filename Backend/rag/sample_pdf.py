import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def make_pdf(path="Backend/data/knowledge.pdf"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)

    lines = [
        "SECTION 1: VISA & LEGAL STATUS (SEVIS COMPLIANCE)",
        "- Full-time Enrollment: Undergraduate students must take 12+ credits per semester.",
        "- Online Class Limit: Only 1 online course (max 3 credits) counts toward the 12-credit minimum.",
        "- Travel Endorsement: You must get a 'Travel Signature' on your I-20 before leaving the US.",
        "- Signature Validity: Signatures for current students are valid for 12 months.",
        "- Address Changes: You MUST update your local US address in the portal within 10 days of moving.",
        "",
        "SECTION 2: EMPLOYMENT & WORK PERMITS",
        "- On-Campus Work: Limited to 20 hours per week during active semesters.",
        "- Break Periods: During Winter/Summer breaks, you may work up to 40 hours per week on campus.",
        "- CPT (Curricular Practical Training): For internships related to your major. Apply after 2 semesters.",
        "- OPT (Optional Practical Training): 12 months of post-grad work. Apply 90 days before graduation.",
        "- SSN: Social Security Numbers are only issued if you have a valid job offer letter.",
        "",
        "SECTION 3: HOUSING, TRANSPORT, & HEALTH",
        "- Health Waiver: The deadline to opt-out of university insurance is September 15th.",
        "- Night Owl Shuttle: A free safety shuttle running from 8:00 PM to 3:00 AM daily.",
        "- Student ID Perks: Your ID provides 50% off monthly local city bus passes.",
        "- Dorm Leases: The 'Global House' is the only dorm offering 12-month (year-round) leases.",
        "",
        "SECTION 4: EMERGENCY CONTACTS & LOCATIONS",
        "- International Student Office (ISO): Located in Student Union, Room 402.",
        "- Campus Police (Emergency): 555-0199",
        "- ISO Walk-in Hours: Monday to Friday, 10:00 AM - 3:00 PM.",
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()


if __name__ == "__main__":
    make_pdf()