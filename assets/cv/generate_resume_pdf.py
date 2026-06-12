import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROFILE = {
    "name": "Sachin Pathare",
    "headline": "Staff SDET (MTS 5) | Quality Engineering and Test Automation",
    "location": "Pune, India",
    "email": "sachinvpathare@gmail.com",
    "linkedin": "linkedin.com/in/sachin-pathare-b76b8496",
    "github": "github.com/spathare21",
    "overview": "12+ years of experience across SaaS, data security, cloud, fintech, and platform engineering. Strong focus on automation quality, release reliability, and scalable testing practices.",
}

SUMMARY_POINTS = [
    "Staff SDET (MTS 5) owning quality engineering strategy for enterprise SaaS products, with deep experience in UI, API, mobile, and performance automation.",
    "Built and scaled AI-assisted workflows for triage, test planning, and automation maintenance to improve engineering velocity and release confidence.",
    "Managing a 7-8 member QA team across multiple squads with focus on predictable delivery, quality standards, and reduced escaped defects.",
]

TEAM_IMPACT_POINTS = [
    "Managing and mentoring a 7-8 member QA team across squads to improve planning discipline and on-time quality delivery.",
    "Established quality standards with review checklists, reusable automation patterns, and stronger Definition-of-Done alignment.",
    "Addressed testing gaps using customer scenarios based on field and production issues.",
    "Institutionalized monthly defect analysis and converted findings into preventive regression scenarios and framework updates.",
]

SKILL_LINES = [
    "Automation: Selenium WebDriver, Robot Framework, Cypress, Appium, Pytest, JUnit, TestNG, Cucumber/BDD",
    "Languages: Python, Java, JavaScript, SQL, Shell/Bash, Groovy",
    "AI Workflows: LLM integrations, Cursor, Claude, GitHub Copilot, AI triage, AI test-plan generation",
    "DevOps and Platforms: Jenkins, GoCD, Docker, Kubernetes, Terraform, Maven, Gradle, Linux",
    "Performance and Security: Gatling, JMeter, load testing, stress testing, OWASP-focused validation",
]

EXPERIENCE = [
    {
        "role": "Cohesity | Staff SDET (MTS 5)",
        "time": "Hybrid, Pune | Oct 2025 - Present",
        "points": [
            "Built AI-powered triage and test-plan workflows using LLM integrations, reducing manual triage effort by 60%+ across three product squads.",
            "Standardized practical use of Cursor and Claude for automation scripting, test plan drafting, and triaging flaky automation failures.",
            "Contributed to automation execution dashboards showing run history, stability trends, and failure insights for release decisions.",
            "Contributed to MCP-based triage workflows to fetch automation history and notify failures using log scanning with email alerts.",
            "Owned quality strategy for a data-protection SaaS platform spanning test plans, regression suites, and CI/CD-integrated frameworks.",
        ],
    },
    {
        "role": "Cohesity | Senior SDET (MTS 4)",
        "time": "Hybrid, Pune | Jun 2023 - Sep 2025",
        "points": [
            "Built and scaled regression automation suites across multiple squads to improve release readiness.",
            "Partnered with product and engineering teams to strengthen acceptance criteria, risk-based coverage, and release sign-off quality.",
            "Introduced customer-scenario validation and defect pattern analysis to reduce escaped defects in subsequent releases.",
        ],
    },
    {
        "role": "Druva Data Solutions Pvt Ltd | Senior SDET",
        "time": "Apr 2021 - Jun 2023",
        "points": [
            "Owned automation for Microsoft 365, Google Workspace, and Slack integrations using Robot Framework and Python.",
            "Defined sprint-level test strategies and collaborated on acceptance criteria, desk checks, and release demos.",
            "Improved automation coverage and reduced manual regression effort for cloud backup and recovery scenarios.",
        ],
    },
    {
        "role": "Thoughtworks Technologies India Pvt Ltd | Quality Analyst",
        "time": "Jun 2019 - Mar 2021",
        "points": [
            "Delivered BDD automation using Java, Serenity, JUnit, and Gradle for client programs.",
            "Implemented Gatling performance tests and identified API bottlenecks to improve response times.",
            "Advanced shift-left quality through story kickoffs, acceptance criteria reviews, and desk checks.",
        ],
    },
    {
        "role": "Red Hat India Pvt Ltd | Quality Engineer",
        "time": "Nov 2016 - Jun 2019",
        "points": [
            "Automated RHEL i18n test scenarios in Python and OpenQA for 20+ locales across major releases.",
            "Built Selenium + Java automation for web UI systems and validated APIs with RestAssured.",
            "Contributed to open-source code and release test planning across product cycles.",
        ],
    },
    {
        "role": "Vertis Infotech | Software Engineer - Test",
        "time": "Oct 2015 - Nov 2016",
        "points": [
            "Built an automation framework from scratch using Selenium, Java, and REST-Assured for UI and API testing.",
            "Developed mobile SDK automation on Android and iOS using Appium.",
        ],
    },
    {
        "role": "PTC India | Software Engineer Intern",
        "time": "Jun 2014 - Jun 2015",
        "points": [
            "Performed manual and automated validation for a PLM platform and supported regression cycles.",
        ],
    },
]

EDUCATION = "Bachelor of Engineering, Computer Engineering | University of Pune | 2010 - 2014"
CERTIFICATIONS = "ISTQB, RHCSA, RHCE, Red Hat Certified in Containerized Application Development"


def section_block(story, title, style):
    story.append(Spacer(1, 5))
    story.append(Paragraph(title, style))
    story.append(Spacer(1, 3))


def bullet_items(story, items, style):
    for item in items:
        story.append(Paragraph(f"&bull; {item}", style))
        story.append(Spacer(1, 1.5))


def add_role(story, role, time, role_style, time_style, bullet_style, points):
    table = Table([[Paragraph(role, role_style), Paragraph(time, time_style)]], colWidths=[118 * mm, 60 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 2))
    bullet_items(story, points, bullet_style)
    story.append(Spacer(1, 2))


def build_premium(output_file: str):
    accent = colors.HexColor("#0B6E5E")
    text = colors.HexColor("#111827")
    muted = colors.HexColor("#374151")

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(2)
        canvas.line(doc.leftMargin, A4[1] - 16 * mm, A4[0] - doc.rightMargin, A4[1] - 16 * mm)
        canvas.setStrokeColor(colors.HexColor("#D1D5DB"))
        canvas.setLineWidth(0.6)
        canvas.line(doc.leftMargin, 15 * mm, A4[0] - doc.rightMargin, 15 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawRightString(A4[0] - doc.rightMargin, 10.5 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="Sachin Pathare - Premium Resume",
        author=PROFILE["name"],
    )

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle("Name", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=21, leading=24, textColor=text)
    head_style = ParagraphStyle("Head", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.8, leading=13, textColor=accent)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=11, textColor=muted)
    section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.white, backColor=accent, leftIndent=4, rightIndent=4)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.2, textColor=text)
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontName="Helvetica", fontSize=9.2, leading=12, textColor=text, leftIndent=8)
    role_style = ParagraphStyle("Role", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.8, leading=12, textColor=text)
    time_style = ParagraphStyle("Time", parent=styles["Normal"], fontName="Helvetica", fontSize=8.8, leading=11, textColor=muted)

    story = []
    header = Table(
        [[
            [Paragraph(PROFILE["name"], name_style), Paragraph(PROFILE["headline"], head_style)],
            [
                Paragraph(PROFILE["location"], contact_style),
                Paragraph(PROFILE["email"], contact_style),
                Paragraph(PROFILE["linkedin"], contact_style),
                Paragraph(PROFILE["github"], contact_style),
            ],
        ]],
        colWidths=[116 * mm, 62 * mm],
    )
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    story.append(header)
    story.append(Spacer(1, 4))
    story.append(Paragraph(PROFILE["overview"], body_style))

    section_block(story, "PROFESSIONAL SUMMARY", section_style)
    bullet_items(story, SUMMARY_POINTS, bullet_style)

    section_block(story, "TEAM MANAGEMENT AND QUALITY IMPACT", section_style)
    bullet_items(story, TEAM_IMPACT_POINTS, bullet_style)

    section_block(story, "CORE SKILLS", section_style)
    for skill in SKILL_LINES:
        story.append(Paragraph(skill, body_style))
        story.append(Spacer(1, 1.5))

    section_block(story, "PROFESSIONAL EXPERIENCE", section_style)
    for item in EXPERIENCE:
        add_role(story, item["role"], item["time"], role_style, time_style, bullet_style, item["points"])

    section_block(story, "EDUCATION AND CERTIFICATIONS", section_style)
    story.append(Paragraph(EDUCATION, body_style))
    story.append(Spacer(1, 1.5))
    story.append(Paragraph(f"Certifications: {CERTIFICATIONS}", body_style))

    doc.build(story, onFirstPage=frame, onLaterPages=frame)


def build_ats(output_file: str):
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Sachin Pathare - ATS Resume",
        author=PROFILE["name"],
    )

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle("ATSName", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=21)
    role_style = ParagraphStyle("ATSRole", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13)
    section_style = ParagraphStyle("ATSSection", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=12)
    body_style = ParagraphStyle("ATSBody", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.4)
    bullet_style = ParagraphStyle("ATSBullet", parent=styles["Normal"], fontName="Helvetica", fontSize=9.3, leading=12, leftIndent=10)
    role_hdr_style = ParagraphStyle("ATSRoleHdr", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.7, leading=12)
    time_style = ParagraphStyle("ATSTime", parent=styles["Normal"], fontName="Helvetica", fontSize=9.1, leading=11)

    story = []
    story.append(Paragraph(PROFILE["name"], name_style))
    story.append(Paragraph(PROFILE["headline"], role_style))
    story.append(Paragraph(f"{PROFILE['location']} | {PROFILE['email']} | {PROFILE['linkedin']} | {PROFILE['github']}", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(PROFILE["overview"], body_style))

    story.append(Spacer(1, 5))
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
    bullet_items(story, SUMMARY_POINTS, bullet_style)

    story.append(Spacer(1, 5))
    story.append(Paragraph("TEAM MANAGEMENT AND QUALITY IMPACT", section_style))
    bullet_items(story, TEAM_IMPACT_POINTS, bullet_style)

    story.append(Spacer(1, 5))
    story.append(Paragraph("CORE SKILLS", section_style))
    for skill in SKILL_LINES:
        story.append(Paragraph(skill, body_style))
        story.append(Spacer(1, 1.2))

    story.append(Spacer(1, 5))
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
    for item in EXPERIENCE:
        story.append(Paragraph(item["role"], role_hdr_style))
        story.append(Paragraph(item["time"], time_style))
        bullet_items(story, item["points"], bullet_style)

    story.append(Spacer(1, 5))
    story.append(Paragraph("EDUCATION AND CERTIFICATIONS", section_style))
    story.append(Paragraph(EDUCATION, body_style))
    story.append(Spacer(1, 1.2))
    story.append(Paragraph(f"Certifications: {CERTIFICATIONS}", body_style))

    doc.build(story)


if __name__ == "__main__":
    premium = "assets/cv/sachin-pathare-cv-premium.pdf"
    ats = "assets/cv/sachin-pathare-cv-ats.pdf"
    default = "assets/cv/sachin-pathare-cv.pdf"

    build_premium(premium)
    build_ats(ats)
    shutil.copyfile(premium, default)

    print(f"Generated {premium}")
    print(f"Generated {ats}")
    print(f"Updated {default} (premium default)")
