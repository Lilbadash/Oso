"""Generate fillable PDF onboarding/monitoring contract forms.

Produces one PDF per apartment site:
  - 405 S Anaheim Blvd Apartments
  - 500 S Anaheim Blvd Apartments
"""

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfform
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

PAGE_W, PAGE_H = LETTER
MARGIN_L = 0.75 * inch
MARGIN_R = 0.75 * inch
MARGIN_T = 0.75 * inch
MARGIN_B = 0.75 * inch
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

LABEL_COLOR = HexColor("#1f2937")
SUB_COLOR = HexColor("#6b7280")
ACCENT = HexColor("#0f172a")
BORDER = HexColor("#cbd5e1")
BG = HexColor("#f8fafc")

styles = getSampleStyleSheet()

LABEL_STYLE = ParagraphStyle(
    "label",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=11,
    textColor=LABEL_COLOR,
)

SUB_STYLE = ParagraphStyle(
    "sub",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=9,
    textColor=SUB_COLOR,
)

BODY_STYLE = ParagraphStyle(
    "body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=11,
    textColor=LABEL_COLOR,
)

TERMS_BODY = ParagraphStyle(
    "terms",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=10,
    textColor=LABEL_COLOR,
    spaceAfter=4,
)

TERMS_HEADING = ParagraphStyle(
    "terms_heading",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=10,
    textColor=ACCENT,
    spaceBefore=4,
    spaceAfter=2,
)


SERVICES = [
    "Fire Alarm Monitoring & Cellular  $65 Monthly  Billed Quarterly ($195.00)",
    "LTE Cellular Phone Line Service / Month  Billed Quarterly  $39.95/mo ($119.85)",
    "Alarm.com Monitoring & Cellular Service  $39.95 Monthly  Billed Quarterly ($119.95)",
    "Alarm.com Pro Video  $15.95 Monthly  Billed Quarterly ($47.85)",
]


TERMS = [
    ("Contract Terms",
     "Terms of Agreement: This agreement is valid for 1 year from the contract date."),
    (None,
     "NOTE: Billing occurs on the 1st day of each month. The first monitoring invoice will be "
     "prorated to cover the activation month's balance and a full period as selected above. "
     "Monitoring charges are billed separately from equipment sales."),
    ("Services Contracted &amp; Provided",
     "RHR Systems Inc. (The Company) agrees to arrange alarm monitoring service for The Alarm "
     "Customer on behalf of RHR Systems Inc. (Install Co.). The Company's obligations are "
     "limited to monitoring alarm signals and transmitting notifications to appropriate "
     "authorities or contacts listed in the Monitoring Details provided by The Alarm Customer, "
     "unless reasonable cause suggests no emergency conditions (e.g., storms, power outages). "
     "The initial term starts on the operational service date and automatically renews unless "
     "canceled with at least 30 days' notice before renewal. The Company may adjust rates as "
     "requested by the Install Co. The Alarm Customer must inform insurers upon agreement "
     "termination. The Install Co. may enter premises to reprogram devices upon termination, "
     "possibly at billable rates."),
    ("Responsibilities of the Alarm Customer",
     "The Alarm Customer must not discriminate against The Company's personnel or engage in "
     "verbal abuse. The Company reserves the right to terminate the Agreement in such events."),
    ("Limitation of Liability",
     "The Company, Install Co., their agents, employees, and sub-contractors are not insurers "
     "and are exempt from liability for alarm system failure or delayed response to alarm "
     "signals. The system can fail beyond their control. The Alarm Customer's payment is for "
     "monitoring only, not protection or insurance. The Alarm Customer's remedies for any loss "
     "are personal resources or insurers. Failure of the system doesn't impose liability on The "
     "Company or Install Co. beyond returning the monitoring service fee, limited to $1,000.00 "
     "or the annual fee, whichever is lower."),
    ("The Company and Install Co. Liability",
     "Under no circumstances are The Company or Install Co. liable for lost profit, "
     "consequential damage, or claims from third parties. The Alarm Customer acknowledges this."),
    ("Exclusions From Liability",
     "The Company or Install Co. is not responsible for losses due to acts, misuse, "
     "environmental conditions, false alarm assessments, power failures, equipment tampering, "
     "or other causes beyond their control."),
    ("Indemnification",
     "The Alarm Customer agrees to indemnify and hold harmless The Company and Install Co. "
     "against any claims or demands."),
    ("Signals",
     "Passive alarms may generate up to 4 signals per month; signal logging systems up to 75 "
     "signals per month. Excessive signals may lead to additional charges per signal."),
    ("Change Authorization",
     "The Alarm Customer grants permission to the Install Co. to communicate changes to the "
     "account, including zone descriptions, call-out procedures, and monitoring service "
     "cancellations."),
    ("Binding Effect of Document",
     "This document, when signed and accepted, constitutes a binding contract for monitoring "
     "services."),
    ("Early Termination",
     "Early termination may result in an early contract termination fee calculated based on "
     "remaining unfulfilled months multiplied by the current monthly rate."),
    ("Suspension or Cancellation of Monitoring Services",
     "The Company may cancel monitoring service if its station is inoperable, or due to The "
     "Alarm Customer's actions, without liability except for a refund of fees paid "
     "post-cancellation."),
    ("Suspension or Cancellation by Police Agencies",
     "The Company will continue service even if police or authorities suspend response. The "
     "Company is not liable for delay or failure in response by authorities."),
    ("Suspension or Cancellation for Non-Payment",
     "Monitoring service may be suspended or canceled if payments are overdue or checks are "
     "not honored."),
    ("Collection Costs",
     "Default may lead to account sent for third-party collection, including collection costs."),
    ("Assignability of Agreement",
     "This agreement and The Company's monitoring service are not transferable without written "
     "consent. The Company can assign this agreement without Alarm Customer's consent."),
    ("Entire Agreement",
     "This agreement is the entire agreement between parties. No changes are valid unless in "
     "writing and signed by The Company and the Alarm Customer. No other representations or "
     "warranties exist. No one other than authorized Company representatives can alter these "
     "terms. These terms override any inconsistent terms in submitted documents."),
]


def draw_paragraph(c, text, style, x, y, width):
    """Draw a paragraph at (x, y top) and return its height."""
    p = Paragraph(text, style)
    w, h = p.wrap(width, 10000)
    p.drawOn(c, x, y - h)
    return h


def draw_header(c, site_name):
    """Draw the company header band and return the y cursor below it."""
    # Title bar
    c.setFillColor(white)
    c.setStrokeColor(BORDER)
    c.rect(MARGIN_L, PAGE_H - MARGIN_T - 0.85 * inch,
           CONTENT_W, 0.85 * inch, stroke=1, fill=1)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN_T - 0.32 * inch,
                        "Onboarding / Monitoring Contract")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN_T - 0.55 * inch,
                        "New Customer / New Site")
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(SUB_COLOR)
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN_T - 0.74 * inch,
                        f"Site: {site_name}")

    y = PAGE_H - MARGIN_T - 0.85 * inch - 0.18 * inch

    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(PAGE_W / 2, y, "RHR Systems Inc. dba Trend Systems Group")
    y -= 12
    c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_W / 2, y, "18952 MacArthur Blvd Suite 100, Irvine, California 92612")
    y -= 11
    c.drawCentredString(PAGE_W / 2, y, "Office: 714.842.0270   |   Email: reice@trendsystems.net")
    y -= 14

    c.setStrokeColor(BORDER)
    c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
    y -= 16
    return y


def draw_footer(c, site_name):
    c.setFillColor(SUB_COLOR)
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 0.5 * inch,
                        f"RHR Systems Inc. dba Trend Systems Group  |  {site_name}")
    c.drawRightString(PAGE_W - MARGIN_R, 0.5 * inch,
                      f"Page {c.getPageNumber()}")


def draw_section_title(c, title, y):
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN_L, y, title)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.75)
    c.line(MARGIN_L, y - 3, PAGE_W - MARGIN_R, y - 3)
    c.setLineWidth(1)
    return y - 16


def text_field(c, name, x, y, width, height, value="", maxlen=120, multiline=False):
    form = c.acroForm
    form.textfield(
        name=name,
        tooltip=name,
        x=x,
        y=y,
        width=width,
        height=height,
        borderColor=BORDER,
        fillColor=BG,
        textColor=black,
        forceBorder=True,
        value=value,
        maxlen=maxlen,
        fieldFlags="multiline" if multiline else "",
        fontSize=9,
    )


def checkbox(c, name, x, y, size=10, checked=False):
    c.acroForm.checkbox(
        name=name,
        tooltip=name,
        x=x,
        y=y,
        size=size,
        borderColor=BORDER,
        fillColor=BG,
        textColor=black,
        forceBorder=True,
        checked=checked,
    )


def labeled_field(c, label, name, y, width=CONTENT_W, sub=None, value="",
                  field_h=16, label_w=2.2 * inch):
    """Draw a label on the left and a single text field on the right."""
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L, y - 2, label)
    fx = MARGIN_L + label_w
    fw = width - label_w
    text_field(c, name, fx, y - field_h, fw, field_h, value=value)
    if sub:
        c.setFillColor(SUB_COLOR)
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(fx, y - field_h - 9, sub)
        return y - field_h - 14
    return y - field_h - 6


def name_pair_field(c, label, base_name, y, label_w=2.2 * inch):
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L, y - 2, label)
    fx = MARGIN_L + label_w
    fw = CONTENT_W - label_w
    half = (fw - 8) / 2
    text_field(c, f"{base_name}_first", fx, y - 16, half, 16)
    text_field(c, f"{base_name}_last", fx + half + 8, y - 16, half, 16)
    c.setFillColor(SUB_COLOR)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(fx, y - 25, "First Name")
    c.drawString(fx + half + 8, y - 25, "Last Name")
    return y - 30


def address_field(c, label, base_name, y, label_w=2.2 * inch, prefilled_street=None,
                  prefilled_city=None, prefilled_state=None, prefilled_zip=None):
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L, y - 2, label)
    fx = MARGIN_L + label_w
    fw = CONTENT_W - label_w

    text_field(c, f"{base_name}_street", fx, y - 16, fw, 16,
               value=prefilled_street or "")
    c.setFillColor(SUB_COLOR)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(fx, y - 25, "Street Address")

    text_field(c, f"{base_name}_city", fx, y - 41, fw, 16,
               value=prefilled_city or "")
    c.drawString(fx, y - 50, "City")

    half = (fw - 8) / 2
    text_field(c, f"{base_name}_state", fx, y - 66, half, 16,
               value=prefilled_state or "")
    text_field(c, f"{base_name}_zip", fx + half + 8, y - 66, half, 16,
               value=prefilled_zip or "")
    c.drawString(fx, y - 75, "State")
    c.drawString(fx + half + 8, y - 75, "Postal / Zip Code")

    return y - 84


def page1(c, site_name, site_street, site_city, site_state, site_zip, project_code):
    y = draw_header(c, site_name)

    # Services
    y = draw_section_title(c, "Our Services", y)
    for i, svc in enumerate(SERVICES):
        checkbox(c, f"service_{i}", MARGIN_L, y - 10, size=10,
                 checked=(i == 0))  # default to first one as in screenshot
        c.setFillColor(LABEL_COLOR)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN_L + 16, y - 8, svc)
        y -= 16
    y -= 6

    # Customer info
    y = draw_section_title(c, "Customer Information", y)
    y = name_pair_field(c, "Person Responsible *", "responsible_person", y)
    y = labeled_field(c, "Company / Entity *", "company_name", y)
    y = labeled_field(c, "Company & c/o Company *", "company_co", y,
                      sub="YOUR COMPANY NAME AND OTHER COMPANY: COMPANY 1 o/c COMPANY 2")
    y = address_field(c, "Address of Company / Entity *", "company_addr", y)

    y -= 4
    y = draw_section_title(c, "Site Being Monitored", y)
    y = address_field(c, "Site Address *", "site_addr", y,
                      prefilled_street=site_street,
                      prefilled_city=site_city,
                      prefilled_state=site_state,
                      prefilled_zip=site_zip)
    y = labeled_field(c, "Site Address Project Code *", "site_code", y,
                      sub="EXAMPLE: 162 W Standard Street code will be 162STA",
                      value=project_code)

    draw_footer(c, site_name)
    c.showPage()


def page2(c, site_name):
    y = draw_header(c, site_name)

    y = draw_section_title(c, "Accounts Payable", y)
    y = name_pair_field(c, "AP Name *", "ap_name", y)
    y = labeled_field(c, "AP Phone *", "ap_phone", y)
    y = labeled_field(c, "AP Email *", "ap_email", y)
    y = address_field(c, "AP Address *", "ap_addr", y)

    y -= 4
    y = draw_section_title(c, "Contacts For Monitoring", y)
    c.setFillColor(SUB_COLOR)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(MARGIN_L, y,
                 "Initial list of names and phone numbers we will call in case of emergency.")
    y -= 14

    for i in range(1, 4):
        required = " *" if i == 1 else ""
        y = name_pair_field(c, f"Contact {i} Name{required}", f"contact_{i}_name", y)
        y = labeled_field(c, f"Contact {i} Phone{required}", f"contact_{i}_phone", y)
        y -= 4

    draw_footer(c, site_name)
    c.showPage()


def page3(c, site_name, project_code, account_number):
    y = draw_header(c, site_name)

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_W / 2, y, "Monitoring Contract")
    y -= 18

    # Account number
    y = labeled_field(c, "Acct # *", "account_number", y,
                      sub="Format example: 1234TGIP",
                      value=account_number)

    # Terms
    y = draw_section_title(c, "Terms and Conditions *", y)

    for heading, body in TERMS:
        if heading:
            h = draw_paragraph(c, heading.upper(), TERMS_HEADING,
                               MARGIN_L, y, CONTENT_W)
            y -= h + 1
        h = draw_paragraph(c, body, TERMS_BODY, MARGIN_L, y, CONTENT_W)
        y -= h + 3

        if y < MARGIN_B + 1.6 * inch:
            draw_footer(c, site_name)
            c.showPage()
            y = draw_header(c, site_name)
            y = draw_section_title(c, "Terms and Conditions (continued)", y)

    y -= 6
    checkbox(c, "accept_terms", MARGIN_L, y - 12, size=12)
    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L + 18, y - 9, "I accept the Terms and Conditions.")
    y -= 26

    # Date and signature
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L, y - 2, "Date *")
    text_field(c, "signed_date", MARGIN_L + 0.5 * inch, y - 16,
               2.0 * inch, 16)
    c.setFillColor(SUB_COLOR)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(MARGIN_L + 0.5 * inch, y - 25, "dd-MMM-yyyy")
    y -= 32

    c.setFillColor(LABEL_COLOR)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN_L, y - 2, "Signature *")
    text_field(c, "signature", MARGIN_L + 0.7 * inch, y - 26,
               CONTENT_W - 0.7 * inch, 26)

    draw_footer(c, site_name)
    c.showPage()


def build_pdf(out_path, site_name, site_street, site_city, site_state,
              site_zip, project_code, account_number):
    c = canvas.Canvas(out_path, pagesize=LETTER)
    c.setTitle(f"Onboarding/Monitoring Contract - {site_name}")
    c.setAuthor("RHR Systems Inc. dba Trend Systems Group")
    c.setSubject("New Customer / New Site Monitoring Contract")

    page1(c, site_name, site_street, site_city, site_state, site_zip, project_code)
    page2(c, site_name)
    page3(c, site_name, project_code, account_number)

    c.save()


def main():
    sites = [
        {
            "filename": "405_S_Anaheim_Blvd_Monitoring_Contract.pdf",
            "name": "405 S Anaheim Blvd",
            "street": "405 S Anaheim Blvd",
            "city": "Anaheim",
            "state": "CA",
            "zip": "",
            "project_code": "405ANA",
            "account_number": "AY630006",
        },
        {
            "filename": "524_S_Anaheim_Blvd_Monitoring_Contract.pdf",
            "name": "524 S Anaheim Blvd",
            "street": "524 S Anaheim Blvd",
            "city": "Anaheim",
            "state": "CA",
            "zip": "",
            "project_code": "524ANA",
            "account_number": "AY630007",
        },
    ]

    for s in sites:
        build_pdf(
            s["filename"],
            s["name"],
            s["street"],
            s["city"],
            s["state"],
            s["zip"],
            s["project_code"],
            s["account_number"],
        )
        print(f"Wrote {s['filename']}")


if __name__ == "__main__":
    main()
