from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)
from reportlab.lib import colors

from django.http import FileResponse

from ..models import Application
from school.models import SchoolSettings


def generate_admission_letter(application):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    # ==========================================
    # COLORS
    # ==========================================

    RED = colors.HexColor("#c62828")
    LIGHT_GREEN = colors.HexColor("#66bb6a")
    DARK_TEXT = colors.HexColor("#222222")
    GREY_TEXT = colors.HexColor("#666666")
    LIGHT_GREY = colors.HexColor("#f5f5f5")

    # ==========================================
    # STYLES
    # ==========================================

    school_style = ParagraphStyle(
        "SchoolName",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=RED,
        spaceAfter=4,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=8.5,
        leading=12,
        textColor=GREY_TEXT,
    )

    title_style = ParagraphStyle(
        "LetterTitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=RED,
        spaceBefore=8,
        spaceAfter=12,
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        fontName="Helvetica",
        fontSize=10.5,
        leading=17,
        textColor=DARK_TEXT,
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=8,
        leading=11,
        textColor=GREY_TEXT,
    )

    greeting_style = ParagraphStyle(
        "Greeting",
        parent=normal_style,
        fontName="Helvetica-Bold",
        spaceAfter=5,
    )

    # ==========================================
    # STORY
    # ==========================================

    story = []

    # ==========================================
    # SCHOOL SETTINGS
    # ==========================================

    school = SchoolSettings.objects.first()

    if school:
        school_name = school.school_name or "Paraclete Classical International School"
        address = school.address or ""
        phone = school.phone or ""
        email = school.email or ""
    else:
        school_name = "Paraclete Classical International School"
        address = ""
        phone = ""
        email = ""

    # ==========================================
    # SCHOOL LOGO
    # USE THE SAME LOGO AS NAVBAR
    # ==========================================

    if school and school.logo:

        try:

            logo = Image(
                school.logo.path,
                width=28 * mm,
                height=28 * mm,
            )

            logo.hAlign = "CENTER"

            story.append(logo)
            story.append(Spacer(1, 4))

        except Exception:
            pass

    # ==========================================
    # SCHOOL NAME
    # ==========================================

    story.append(
        Paragraph(
            school_name,
            school_style,
        )
    )

    # ==========================================
    # CONTACT INFORMATION
    # ==========================================

    contact_information = []

    if address:
        contact_information.append(address)

    if phone:
        contact_information.append(
            f"Tel: {phone}"
        )

    if email:
        contact_information.append(
            f"Email: {email}"
        )

    if contact_information:

        story.append(
            Paragraph(
                " | ".join(contact_information),
                contact_style,
            )
        )

    story.append(Spacer(1, 7))

    # ==========================================
    # LETTERHEAD LINE
    # ==========================================

    story.append(
        HRFlowable(
            width="100%",
            thickness=2,
            color=RED,
            spaceBefore=2,
            spaceAfter=2,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=LIGHT_GREEN,
            spaceBefore=1,
            spaceAfter=10,
        )
    )

    # ==========================================
    # TITLE
    # ==========================================

    story.append(
        Paragraph(
            "OFFICIAL ADMISSION LETTER",
            title_style,
        )
    )

    # ==========================================
    # APPLICATION INFORMATION
    # ==========================================

    application_data = [

        [
            Paragraph("<b>Application Number</b>", normal_style),
            Paragraph(
                application.application_number,
                normal_style,
            ),
        ],

        [
            Paragraph("<b>Student Name</b>", normal_style),
            Paragraph(
                f"{application.first_name} "
                f"{application.last_name}",
                normal_style,
            ),
        ],

        [
            Paragraph("<b>Class</b>", normal_style),
            Paragraph(
                application.class_applying_for,
                normal_style,
            ),
        ],

        [
            Paragraph("<b>Parent / Guardian</b>", normal_style),
            Paragraph(
                application.parent_name,
                normal_style,
            ),
        ],

        [
            Paragraph("<b>Date</b>", normal_style),
            Paragraph(
                application.created_at.strftime(
                    "%d %B %Y"
                ),
                normal_style,
            ),
        ],
    ]

    table = Table(
        application_data,
        colWidths=[
            55 * mm,
            105 * mm,
        ],
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                LIGHT_GREY,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#cccccc"),
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

        ])
    )

    story.append(table)

    story.append(Spacer(1, 18))

    # ==========================================
    # GREETING
    # ==========================================

    story.append(
        Paragraph(
            f"Dear {application.parent_name},",
            greeting_style,
        )
    )

    story.append(Spacer(1, 6))

    # ==========================================
    # FIRST PARAGRAPH
    # ==========================================

    story.append(
        Paragraph(
            f"We are pleased to inform you that "
            f"<b>{application.first_name} "
            f"{application.last_name}</b> has been "
            f"officially offered admission to "
            f"<b>{application.class_applying_for}</b> "
            f"at <b>{school_name}</b>.",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    # ==========================================
    # SECOND PARAGRAPH
    # ==========================================

    story.append(
        Paragraph(
            "We congratulate you on this achievement "
            "and look forward to welcoming the student "
            "to our school community. We are confident "
            "that the student will benefit from the "
            "academic, moral, and personal development "
            "opportunities provided by our school.",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    # ==========================================
    # REPORTING INSTRUCTIONS
    # ==========================================

    story.append(
        Paragraph(
            "<b>Reporting Instructions</b>",
            normal_style,
        )
    )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "Please present this admission letter when "
            "reporting to the school. You should also "
            "bring all required original academic and "
            "personal documents as requested by the "
            "school administration.",
            normal_style,
        )
    )

    story.append(Spacer(1, 10))

    # ==========================================
    # IMPORTANT NOTICE
    # ==========================================

    notice_data = [[
        Paragraph(
            "<b>IMPORTANT:</b> This admission letter is "
            "officially issued after approval of the "
            "application and confirmation of the "
            "required admission payment.",
            normal_style,
        )
    ]]

    notice_table = Table(
        notice_data,
        colWidths=[160 * mm],
    )

    notice_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#f0f8f0"),
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                LIGHT_GREEN,
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),

        ])
    )

    story.append(notice_table)

    story.append(Spacer(1, 35))

    # ==========================================
    # SIGNATURE AREA
    # ==========================================

    signature_data = [[
        Paragraph(
            "______________________________",
            normal_style,
        ),

        Paragraph(
            "______________________________",
            normal_style,
        ),
    ], [
        Paragraph(
            "<b>Headteacher / Principal</b>",
            normal_style,
        ),

        Paragraph(
            "<b>Official School Stamp</b>",
            normal_style,
        ),
    ]]

    signature_table = Table(
        signature_data,
        colWidths=[
            78 * mm,
            78 * mm,
        ],
    )

    signature_table.setStyle(
        TableStyle([

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "LEFT",
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                0,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),

        ])
    )

    story.append(signature_table)

    story.append(Spacer(1, 20))

    # ==========================================
    # FOOTER
    # ==========================================

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=LIGHT_GREEN,
            spaceBefore=5,
            spaceAfter=5,
        )
    )

    story.append(
        Paragraph(
            "This is an official computer-generated "
            "admission letter. Please retain a copy "
            "for your records.",
            small_style,
        )
    )

    # ==========================================
    # BUILD PDF
    # ==========================================

    document.build(story)

    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=(
            f"{application.application_number}"
            "_admission_letter.pdf"
        ),
        content_type="application/pdf",
    )