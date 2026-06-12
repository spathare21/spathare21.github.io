from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer


def add_section(story, title, title_style, body_style):
    story.append(Spacer(1, 6))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#1f2937")))
    story.append(Spacer(1, 4))


def add_bullets(story, items, body_style):
    for item in items:
        story.append(Paragraph(f"- {item}", body_style))
        story.append(Spacer(1, 2))


def build_resume(output_file: str):
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Sachin Pathare - Resume",
        author="Sachin Pathare",
    )

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=2,
    )
    role_style = ParagraphStyle(
        "RoleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=colors.HexColor("#111827"),
        spaceAfter=4,
    )
    contact_style = ParagraphStyle(
        "ContactStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=11.8,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=2,
    )
    section_title_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.6,
        leading=12,
        textColor=colors.HexColor("#111827"),
        spaceAfter=1,
        allCaps=True,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=12.4,
        textColor=colors.HexColor("#111827"),
    )
    role_header_style = ParagraphStyle(
        "RoleHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.8,
        leading=12,
        textColor=colors.HexColor("#111827"),
    )

    story = []

    story.append(Paragraph("Sachin Pathare", name_style))
    story.append(Paragraph("Staff Software Engineer (MTS 5) | Quality Engineering and Test Automation Leader", role_style))
    story.append(
        Paragraph(
            "Pune, India  |  sachinvpathare@gmail.com  |  linkedin.com/in/sachin-pathare-b76b8496  |  github.com/spathare21",
            contact_style,
        )
    )
    story.append(
        Paragraph(
            "12+ years of experience across SaaS, data security, cloud, fintech, and platform engineering.",
            contact_style,
        )
    )

    add_section(story, "Professional Summary", section_title_style, body_style)
    summary = [
        "Staff Software Engineer leading quality engineering strategy for enterprise SaaS products, with deep experience in UI, API, mobile, and performance automation.",
        "Built and scaled AI-assisted quality workflows for triage, test planning, and automation maintenance to improve engineering velocity and release confidence.",
        "Known for leading high-performing QA teams, improving standards, and reducing escaped defects through customer-scenario-driven testing.",
    ]
    add_bullets(story, summary, body_style)

    add_section(story, "Leadership Impact", section_title_style, body_style)
    leadership = [
        "Led and mentored a 7-8 member QA team across multiple squads, improving planning discipline and on-time quality delivery.",
        "Established higher quality standards using review checklists, reusable automation patterns, and stronger Definition-of-Done practices.",
        "Introduced monthly defect analysis for field and production issues; converted findings into preventive regression scenarios and framework updates.",
        "Drove cross-functional quality partnerships with Product Owners and engineering leads to close quality gaps early in the release cycle.",
    ]
    add_bullets(story, leadership, body_style)

    add_section(story, "Core Skills", section_title_style, body_style)
    skill_lines = [
        "Automation: Selenium WebDriver, Robot Framework, Cypress, Appium, Pytest, JUnit, TestNG, Cucumber/BDD",
        "Languages: Python, Java, JavaScript, SQL, Shell/Bash, Groovy",
        "AI and Productivity: LLM integrations, Cursor, Claude, GitHub Copilot, AI triage and test-plan generation",
        "DevOps and Platforms: Jenkins, GoCD, Docker, Kubernetes, Terraform, Maven, Gradle, Linux",
        "Performance and Security: Gatling, JMeter, load testing, stress testing, OWASP-focused validation",
    ]
    for line in skill_lines:
        story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 2))

    add_section(story, "Professional Experience", section_title_style, body_style)

    story.append(
        Paragraph(
            "Cohesity | Staff Software Engineer (MTS 5) | Hybrid, Pune | Jun 2023 - Present (Promoted from MTS 4 in Oct 2025)",
            role_header_style,
        )
    )
    story.append(Spacer(1, 2))
    cohesity_points = [
        "Architected AI-powered triage and test-plan generation workflows using LLM integrations, reducing manual triage effort by 60%+ across three product squads.",
        "Standardized practical usage of Cursor and Claude for automation scripting, test plan drafting, and triaging flaky automation failures.",
        "Addressed testing gaps by adding customer scenarios derived from field issues and production defects into release validation suites.",
        "Contributed to an automation execution dashboard showing run history, stability trends, and failure insights for release decisions.",
        "Contributed to MCP-based triage workflows that fetch automation history and trigger failure notifications using log scanning and email alerts.",
        "Owned end-to-end quality strategy for a data-protection SaaS platform spanning test plans, regression suites, and CI/CD-integrated frameworks.",
    ]
    add_bullets(story, cohesity_points, body_style)

    story.append(Spacer(1, 4))
    story.append(
        Paragraph("Druva Data Solutions Pvt Ltd | Senior SDET | Apr 2021 - Jun 2023", role_header_style)
    )
    story.append(Spacer(1, 2))
    add_bullets(
        story,
        [
            "Owned automation for Microsoft 365, Google Workspace, and Slack integrations using Robot Framework and Python.",
            "Defined test strategies and sprint-level test plans; collaborated on acceptance criteria, desk checks, and release demos.",
            "Improved automation coverage and reduced manual regression effort for cloud backup and recovery scenarios.",
        ],
        body_style,
    )

    story.append(Spacer(1, 4))
    story.append(Paragraph("Thoughtworks Technologies India Pvt Ltd | Quality Analyst | Jun 2019 - Mar 2021", role_header_style))
    story.append(Spacer(1, 2))
    add_bullets(
        story,
        [
            "Delivered BDD automation using Java, Serenity, JUnit, and Gradle for client programs.",
            "Implemented Gatling performance tests and identified API bottlenecks to improve response times.",
            "Promoted shift-left quality through story kickoffs, acceptance criteria reviews, and desk checks.",
        ],
        body_style,
    )

    story.append(Spacer(1, 4))
    story.append(Paragraph("Red Hat India Pvt Ltd | Quality Engineer | Nov 2016 - Jun 2019", role_header_style))
    story.append(Spacer(1, 2))
    add_bullets(
        story,
        [
            "Automated RHEL i18n test scenarios in Python and OpenQA for 20+ locales across major releases.",
            "Built Selenium + Java automation for web UI systems and validated APIs with RestAssured.",
            "Contributed to open-source code and test planning across product release cycles.",
        ],
        body_style,
    )

    story.append(Spacer(1, 4))
    story.append(Paragraph("Vertis Infotech | Software Engineer - Test | Oct 2015 - Nov 2016", role_header_style))
    story.append(Spacer(1, 2))
    add_bullets(
        story,
        [
            "Built an automation framework from scratch using Selenium, Java, and REST-Assured for UI and API testing.",
            "Developed mobile SDK automation on Android and iOS using Appium.",
        ],
        body_style,
    )

    story.append(Spacer(1, 4))
    story.append(Paragraph("PTC India | Software Engineer Intern | Jun 2014 - Jun 2015", role_header_style))
    story.append(Spacer(1, 2))
    add_bullets(
        story,
        [
            "Performed manual and automated validation for a PLM platform and supported regression cycles.",
        ],
        body_style,
    )

    add_section(story, "Education and Certifications", section_title_style, body_style)
    story.append(Paragraph("Bachelor of Engineering, Computer Engineering | University of Pune | 2010 - 2014", body_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Certifications: ISTQB, RHCSA, RHCE, Red Hat Certified in Containerized Application Development", body_style))

    doc.build(story)


if __name__ == "__main__":
    build_resume("assets/cv/sachin-pathare-cv.pdf")
    print("Generated assets/cv/sachin-pathare-cv.pdf")