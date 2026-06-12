"""
Resume — Sachin Pathare
Design: Clean two-column, senior professional grade
Colour philosophy: near-zero colour — dark sidebar / white main / grey typography only
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether,
    PageTemplate, Paragraph, Spacer, Table, TableStyle, Flowable,
)

# ── Page geometry ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4          # 595.28 × 841.89 pt
SB_W   = 70 * mm             # sidebar width
TOP_H  =  5 * mm             # top header band
BOT_H  = 10 * mm             # bottom margin
SB_PL  = 10 * mm             # sidebar left pad  — increased breathing room
SB_PR  =  7 * mm             # sidebar right pad
SB_IW  = SB_W - SB_PL - SB_PR          # ~53 mm inner
MN_PL  =  8 * mm
MN_PR  = 10 * mm
MN_FX  = SB_W + MN_PL
MN_FW  = PAGE_W - SB_W - MN_PL - MN_PR

# ── Colour palette — near-zero colour ─────────────────────────────────────────
# Sidebar
SB_BG    = colors.HexColor("#1E293B")   # dark slate (no pure black = friendlier)
SB_BAND  = colors.HexColor("#162130")   # slightly darker for top band
SB_DIV   = colors.HexColor("#2D4055")   # subtle divider inside sidebar
SB_WHITE = colors.HexColor("#F8FAFC")   # primary sidebar text (near-white)
SB_LIGHT = colors.HexColor("#CBD5E1")   # secondary sidebar text (slate-300)
SB_MUT   = colors.HexColor("#94A3B8")   # muted labels (slate-400)

# Main
M_BLACK  = colors.HexColor("#0F172A")   # headings / name / companies
M_BODY   = colors.HexColor("#374151")   # body text / bullets
M_MUT    = colors.HexColor("#6B7280")   # dates / tagline / tags
M_RULE   = colors.HexColor("#E2E8F0")   # hairline dividers
M_SECBG  = colors.HexColor("#F8FAFC")   # section header background (barely-there)
M_SECDIV = colors.HexColor("#CBD5E1")   # section header bottom border


# ── Canvas helpers ─────────────────────────────────────────────────────────────
def _wrap(text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        probe = (cur + " " + w).strip()
        if stringWidth(probe, font, size) <= max_w:
            cur = probe
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def ctext(c, text, x, y, font, size, color, max_w=None, lh=None, align="left"):
    """Draw text (wrapping + explicit \\n). Returns y after last line."""
    lh = lh or size * 1.42
    c.setFont(font, size)
    c.setFillColor(color)
    segments = text.split("\n")
    all_lines = []
    for seg in segments:
        all_lines.extend(_wrap(seg, font, size, max_w) if max_w else [seg])
    for ln in all_lines:
        w = stringWidth(ln, font, size)
        dx = {"center": -w / 2, "right": -w}.get(align, 0)
        c.drawString(x + dx, y, ln)
        y -= lh
    return y


# ── Sidebar painter (canvas callback — runs every page) ───────────────────────
def paint_sidebar(canvas, doc):
    canvas.saveState()
    c = canvas

    # ── Full sidebar background ──────────────────────────────────────────────
    c.setFillColor(SB_BG)
    c.rect(0, 0, SB_W, PAGE_H, fill=1, stroke=0)

    # ── Narrow top band (full width) — dark accent, NOT bright blue ──────────
    c.setFillColor(SB_BAND)
    c.rect(0, PAGE_H - TOP_H, PAGE_W, TOP_H, fill=1, stroke=0)

    # ── Thin right edge of sidebar (1 pt, slightly lighter than bg) ──────────
    c.setStrokeColor(SB_DIV)
    c.setLineWidth(1)
    c.line(SB_W, 0, SB_W, PAGE_H)

    # ── Page number in MAIN area (bottom right of each page) ─────────────────
    c.setFont("Helvetica", 7.5)
    c.setFillColor(M_MUT)
    c.drawRightString(PAGE_W - MN_PR, 6 * mm, f"Page {doc.page}")

    # ── Sidebar content: page 1 only ─────────────────────────────────────────
    if doc.page != 1:
        canvas.restoreState()
        return

    x  = SB_PL
    iw = SB_IW
    cx = SB_W / 2
    y  = PAGE_H - TOP_H - 6 * mm

    # ── SECTION HELPER ───────────────────────────────────────────────────────
    def sb_section(label):
        nonlocal y
        y -= 1.5 * mm
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(SB_WHITE)
        c.drawString(x, y, label)
        y -= 3.5 * mm
        # thin full-width rule in muted colour
        c.setStrokeColor(SB_DIV)
        c.setLineWidth(0.6)
        c.line(x, y, x + iw, y)
        y -= 3.5 * mm

    # ── DIVIDER HELPER ───────────────────────────────────────────────────────
    def sb_div():
        nonlocal y
        y -= 2 * mm
        c.setStrokeColor(SB_DIV)
        c.setLineWidth(0.5)
        c.line(x, y, x + iw, y)
        y -= 3 * mm

    # ── PHOTO ────────────────────────────────────────────────────────────────
    r = 11 * mm
    c.saveState()
    p = c.beginPath()
    p.circle(cx, y - r, r)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader("assets/images/avatar.jpg"),
                cx - r, y - r * 2, width=r * 2, height=r * 2, mask="auto")
    c.restoreState()
    c.setStrokeColor(SB_WHITE)
    c.setLineWidth(1.5)
    c.circle(cx, y - r, r, fill=0, stroke=1)
    y -= r * 2 + 6 * mm        # photo → name: 6 mm gap

    # ── NAME ─────────────────────────────────────────────────────────────────
    y = ctext(c, "Sachin Pathare", cx, y, "Helvetica-Bold", 14.5, SB_WHITE,
              align="center")
    y -= 0.5 * mm              # name → role: tight

    # ── ROLE ─────────────────────────────────────────────────────────────────
    y = ctext(c, "Staff SDET  (MTS 5)", cx, y, "Helvetica-Bold", 8.5, SB_LIGHT,
              align="center")
    y -= 0.8 * mm              # role → tagline: tight

    # ── TAGLINE ──────────────────────────────────────────────────────────────
    y = ctext(c, "12+ Years  |  Quality Engineering", cx, y,
              "Helvetica", 7.5, SB_MUT, align="center")
    y -= 2 * mm

    sb_div()

    # ── CONTACT ──────────────────────────────────────────────────────────────
    sb_section("CONTACT")
    contacts = [
        ("Email",    "sachinvpathare@gmail.com"),
        ("LinkedIn", "sachin-pathare-b76b8496"),
        ("GitHub",   "github.com/spathare21"),
        ("Website",  "spathare21.github.io"),
        ("Location", "Pune, India"),
    ]
    for lbl, val in contacts:
        # label — capture return so y moves past the label bottom
        y = ctext(c, lbl.upper(), x, y, "Helvetica-Bold", 6.8, SB_MUT)
        y -= 0.8 * mm          # small gap: label bottom → value top
        # value — slightly indented, bright white
        y = ctext(c, val, x + 2, y, "Helvetica", 8.2, SB_LIGHT, iw - 2, 3.3 * mm)
        y -= 3 * mm            # gap between contact items
    y -= 1 * mm

    sb_div()

    # ── TECHNICAL SKILLS ─────────────────────────────────────────────────────
    sb_section("TECHNICAL SKILLS")
    skills = [
        ("Automation",
         "Selenium, Robot FW, Cypress, Appium\nPytest, JUnit, TestNG, Cucumber/BDD"),
        ("Languages",
         "Python, Java, JavaScript, SQL\nShell/Bash, Groovy"),
        ("AI & LLM",
         "LLM Integration, Cursor, Claude\nCopilot, Prompt Engineering"),
        ("DevOps & CI/CD",
         "Jenkins, GoCD, Docker, Kubernetes\nTerraform, Git, Maven, AWS"),
        ("Performance & Security",
         "Gatling, JMeter, Load/Stress Testing\nOWASP Validation"),
    ]
    for idx, (cat, vals) in enumerate(skills):
        # subtle separator before every category except the first
        if idx > 0:
            y -= 1 * mm
            c.setStrokeColor(SB_DIV)
            c.setLineWidth(0.4)
            c.line(x, y, x + iw, y)
            y -= 2.5 * mm      # clear gap after separator
        y = ctext(c, cat, x, y, "Helvetica-Bold", 8.5, SB_WHITE)
        y -= 0.8 * mm          # gap: category label bottom → values
        y = ctext(c, vals, x, y, "Helvetica", 7.8, SB_LIGHT, iw, 3.2 * mm)
        y -= 1 * mm
    y -= 1.5 * mm

    sb_div()

    # ── EDUCATION ────────────────────────────────────────────────────────────
    sb_section("EDUCATION")
    edu = [
        ("MCA — Master of Comp. Applications",
         "D.Y. Patil Institute, Pune",
         "Savitribai Phule Pune University",
         "2012 – 2015"),
        ("B.Sc. — Computer Science",
         "MIT College of Engineering, Pune",
         "Pune University",
         "2008 – 2011"),
    ]
    for deg, school, board, years in edu:
        y = ctext(c, deg,    x, y, "Helvetica-Bold", 8.2, SB_WHITE, iw, 3.3 * mm)
        y -= 0.5 * mm
        y = ctext(c, school, x, y, "Helvetica",      7.8, SB_LIGHT, iw, 3.2 * mm)
        y = ctext(c, board,  x, y, "Helvetica",      7.2, SB_MUT,   iw, 3 * mm)
        y = ctext(c, years,  x, y, "Helvetica-Bold", 8,   SB_WHITE)
        y -= 5.5 * mm

    sb_div()

    # ── CERTIFICATIONS ───────────────────────────────────────────────────────
    sb_section("CERTIFICATIONS")
    certs = [
        "ISTQB — Foundation Level",
        "RHCSA & RHCE — Red Hat",
        "Red Hat: Containerised App Dev",
    ]
    for cert in certs:
        # small dash bullet drawn as a rect
        c.setFillColor(SB_MUT)
        c.rect(x, y + 3, 6, 1, fill=1, stroke=0)
        y = ctext(c, cert, x + 9, y, "Helvetica", 8.2, SB_LIGHT, iw - 9, 3.3 * mm)
        y -= 3 * mm

    canvas.restoreState()


# ── Main column flowables ──────────────────────────────────────────────────────
class SectionHeader(Flowable):
    """Bold heading + thin bottom rule — no distracting background colour."""
    def __init__(self, text, iw):
        super().__init__()
        self._text = text
        self._iw   = iw
        self.height = 18
        self.width  = iw

    def wrap(self, aw, ah):
        return self._iw, self.height

    def draw(self):
        # Very subtle off-white background strip — barely visible
        self.canv.setFillColor(M_SECBG)
        self.canv.rect(0, 0, self._iw, self.height, fill=1, stroke=0)
        # Thin dark left accent bar (2.5 pt)
        self.canv.setFillColor(M_BLACK)
        self.canv.rect(0, 0, 2.5, self.height, fill=1, stroke=0)
        # Section label
        self.canv.setFont("Helvetica-Bold", 9.5)
        self.canv.setFillColor(M_BLACK)
        self.canv.drawString(9, 5, self._text)
        # Bottom hairline
        self.canv.setStrokeColor(M_SECDIV)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self._iw, 0)


class ThinRule(Flowable):
    def __init__(self, w, color=M_RULE, t=0.5):
        super().__init__()
        self.width = w; self.color = color; self.t = t
        self.height = t + 1.5

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.t)
        self.canv.line(0, 0, self.width, 0)


# ── Paragraph styles ──────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    def S(name, **kw):
        return ParagraphStyle(name, parent=kw.pop("parent", base["Normal"]), **kw)
    return {
        "name":    S("Nm",  fontName="Helvetica-Bold",    fontSize=26,  leading=30, textColor=M_BLACK),
        "role":    S("Rl",  fontName="Helvetica-Bold",    fontSize=11,  leading=15, textColor=M_BLACK),
        "tagline": S("Tl",  fontName="Helvetica",         fontSize=8.5, leading=12, textColor=M_MUT),
        "summary": S("Su",  fontName="Helvetica",         fontSize=8.8, leading=13.5, textColor=M_BODY),
        "co":      S("Co",  fontName="Helvetica-Bold",    fontSize=9,   leading=12, textColor=M_BLACK),
        "period":  S("Pe",  fontName="Helvetica",         fontSize=8.5, leading=11, textColor=M_MUT),
        "jobrole": S("Jr",  fontName="Helvetica-Bold",    fontSize=10,  leading=13, textColor=M_BLACK),
        "promo":   S("Pr",  fontName="Helvetica-Oblique", fontSize=7.5, leading=10, textColor=M_MUT),
        "bullet":  S("Bu",  fontName="Helvetica",         fontSize=8.5, leading=12.5, textColor=M_BODY,
                     leftIndent=11, firstLineIndent=-9),
        "tags":    S("Ta",  fontName="Helvetica",         fontSize=7,   leading=10, textColor=M_MUT),
    }


# ── Experience entry builder ───────────────────────────────────────────────────
def job_block(job, st, iw):
    items = []
    loc = f"  ·  {job['loc']}" if job.get("loc") else ""

    # Company + period row
    pw = 34 * mm
    cw = iw - pw
    hdr = Table(
        [[Paragraph(f"{job['company']}{loc}", st["co"]),
          Paragraph(job["period"], st["period"])]],
        colWidths=[cw, pw],
    )
    hdr.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "BOTTOM"),
        ("ALIGN",         (1, 0), (1, 0),   "RIGHT"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    items.append(hdr)
    items.append(Spacer(1, 1.2 * mm))
    items.append(Paragraph(job["role"], st["jobrole"]))

    if job.get("promo"):
        items.append(Spacer(1, 0.8 * mm))
        items.append(Paragraph(f"Promoted:  {job['promo']}", st["promo"]))

    items.append(Spacer(1, 2.5 * mm))
    items.append(ThinRule(iw, M_RULE, 0.5))
    items.append(Spacer(1, 2.5 * mm))

    for pt in job["points"]:
        items.append(Paragraph(f"–  {pt}", st["bullet"]))
        items.append(Spacer(1, 1.5 * mm))

    if job.get("tags"):
        items.append(Spacer(1, 1.5 * mm))
        items.append(Paragraph("  /  ".join(job["tags"]), st["tags"]))

    return KeepTogether(items)


# ── Resume data ───────────────────────────────────────────────────────────────
SUMMARY = (
    "Staff SDET with <b>12+ years</b> building enterprise-grade quality at scale across SaaS, "
    "data security, cloud, fintech, and platform domains. Led <b>7–8 member QA teams</b> across "
    "multiple squads, established AI-powered triage and test-plan workflows cutting manual effort "
    "by <b>60%+</b>, and consistently delivered measurable improvements to release quality and "
    "engineering standards. Treats automation code as production-quality deliverable."
)

JOBS = [
    {
        "role":    "Staff SDET (MTS 5)",
        "promo":   "MTS 4 (Jun 2023)  >>  MTS 5 (Oct 2025)",
        "company": "Cohesity",
        "loc":     "Hybrid, Pune",
        "period":  "Jun 2023 – Present",
        "tags":    ["AI Automation", "Team Leadership", "CI/CD", "Data Security SaaS"],
        "points": [
            "Led and mentored a <b>7–8 member QA team</b> across 3 product squads, improving planning discipline, Definition-of-Done alignment, and on-time quality delivery.",
            "Architected an <b>AI-powered test triage system and automated test-plan generator</b> using LLM integrations, reducing manual triage effort by <b>60%+</b> and accelerating release cycles.",
            "Standardised practical use of <b>Cursor and Claude</b> for automation scripting, test-plan drafting, and flaky-failure triage — establishing org-wide AI usage standards for QA.",
            "Contributed <b>MCP-based triage workflows</b>: fetching automation history, scanning logs, and delivering actionable failure notifications via email alerts.",
            "Built an automation <b>execution dashboard</b> surfacing run history, stability trends, and failure insights to improve release confidence across all squads.",
            "Established monthly <b>defect pattern analysis</b> to convert field/production issues into preventive regression scenarios and framework improvements.",
            "Owned end-to-end quality strategy for a data-protection SaaS platform: test plans, automation frameworks, regression suites, and CI/CD-integrated pipelines.",
        ],
    },
    {
        "role":    "Senior SDET",
        "promo":   None,
        "company": "Druva Data Solutions Pvt Ltd",
        "loc":     "",
        "period":  "Apr 2021 – Jun 2023",
        "tags":    ["Robot Framework", "Python", "M365", "Google Workspace"],
        "points": [
            "Owned end-to-end automation for <b>Microsoft 365, Google Workspace, and Slack</b> integrations using Robot Framework and Python — covering cloud backup and recovery scenarios.",
            "Defined sprint-level test strategies; collaborated with POs and engineers on acceptance criteria, desk checks, and release demos.",
            "Improved automation coverage and significantly reduced manual regression effort across integration releases.",
        ],
    },
    {
        "role":    "Quality Analyst",
        "promo":   None,
        "company": "Thoughtworks Technologies India Pvt Ltd",
        "loc":     "",
        "period":  "Jun 2019 – Mar 2021",
        "tags":    ["BDD", "Java", "Serenity", "Gatling", "Shift-Left"],
        "points": [
            "Delivered <b>BDD automation</b> (Java, Serenity, JUnit, Gradle) for McKinsey &amp; GPN client programs; championed shift-left quality through story kickoffs, acceptance criteria, and desk checks.",
            "Implemented <b>Gatling performance test suite</b>; identified API bottlenecks that drove measurable improvements in system response times.",
            "Contributed to unit and integration testing alongside developers, treating quality as a shared team responsibility.",
        ],
    },
    {
        "role":    "Quality Engineer",
        "promo":   "Associate QE (Nov 2016)  >>  Quality Engineer (Nov 2017)",
        "company": "Red Hat India Pvt Ltd",
        "loc":     "",
        "period":  "Nov 2016 – Jun 2019",
        "tags":    ["Python", "Selenium", "OpenQA", "i18n/L10n", "Open Source"],
        "points": [
            "Automated <b>RHEL i18n test scenarios</b> in Python and OpenQA, validating 20+ locales across major Red Hat product releases.",
            "Built Selenium + Java automation for Zanata, Transtats, and Satellite web UIs; validated REST APIs with RestAssured.",
            "Contributed open-source code to Transtats and Zanata projects; maintained test plans across product release cycles.",
        ],
    },
    {
        "role":    "Software Engineer – Test",
        "promo":   None,
        "company": "Vertis Infotech",
        "loc":     "",
        "period":  "Oct 2015 – Nov 2016",
        "tags":    ["Selenium", "Java", "REST-Assured", "Appium", "Fintech"],
        "points": [
            "Designed and built a <b>Selenium + Java + REST-Assured automation framework from scratch</b> for a fintech/payments product — covering end-to-end UI flows, API contract validation, and payment transaction scenarios.",
            "Developed <b>mobile SDK test automation</b> for Android and iOS using Appium, validating cross-platform SDK behaviour across multiple device configurations.",
            "Executed structured test cases for payment flows, session handling, and error boundary scenarios; actively managed defects through the full lifecycle in JIRA.",
            "Participated in sprint ceremonies, release readiness reviews, and exploratory testing sessions to ensure quality across agile delivery cycles.",
        ],
    },
    {
        "role":    "Software Engineer – Intern",
        "promo":   None,
        "company": "PTC India",
        "loc":     "",
        "period":  "Jun 2014 – Jun 2015",
        "tags":    ["PLM", "Manual Testing", "Test Design", "QA Fundamentals"],
        "points": [
            "Performed manual and automated validation for a <b>PLM (Product Lifecycle Management)</b> platform; planned and executed regression test cycles covering key product workflows.",
            "Authored test cases, test plans, and defect reports using standardised QA documentation practices, ensuring traceability from requirements to test coverage.",
            "Collaborated with senior QA engineers and developers to translate product requirements into structured test scenarios and identify edge cases.",
            "Gained foundational experience in software QA processes, defect lifecycle management, test design techniques, and agile team participation.",
        ],
    },
]


# ── Main story ────────────────────────────────────────────────────────────────
def build_story(st, iw):
    s = []

    # Name
    s.append(Paragraph("Sachin Pathare", st["name"]))
    s.append(Spacer(1, 2 * mm))
    # Role — same dark colour as name, slightly smaller
    s.append(Paragraph("Staff SDET (MTS 5)", st["role"]))
    s.append(Spacer(1, 1.5 * mm))
    # Tagline — muted, one line
    s.append(Paragraph("Quality Engineering  ·  AI Test Automation  ·  Pune, India", st["tagline"]))
    s.append(Spacer(1, 3 * mm))
    # Clean thin rule — dark grey, NOT bright blue
    s.append(ThinRule(iw, M_BLACK, 1))
    s.append(Spacer(1, 5 * mm))

    # Summary
    s.append(SectionHeader("PROFESSIONAL SUMMARY", iw))
    s.append(Spacer(1, 3 * mm))
    s.append(Paragraph(SUMMARY, st["summary"]))
    s.append(Spacer(1, 6 * mm))

    # Experience
    s.append(SectionHeader("PROFESSIONAL EXPERIENCE", iw))
    s.append(Spacer(1, 4 * mm))

    for i, job in enumerate(JOBS):
        s.append(job_block(job, st, iw))
        if i < len(JOBS) - 1:
            s.append(Spacer(1, 4.5 * mm))

    return s


# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_resume(output_file: str):
    st = make_styles()
    doc = BaseDocTemplate(
        output_file,
        pagesize=A4,
        title="Sachin Pathare — Resume",
        author="Sachin Pathare",
    )
    frame = Frame(
        x1=MN_FX, y1=BOT_H,
        width=MN_FW, height=PAGE_H - TOP_H - BOT_H,
        id="main", showBoundary=0,
        leftPadding=0, rightPadding=0,
        topPadding=5 * mm, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="R", frames=[frame], onPage=paint_sidebar)])
    doc.build(build_story(st, MN_FW))
    print(f"✓  {output_file}")


if __name__ == "__main__":
    build_resume("assets/cv/sachin-pathare-cv.pdf")
