"""
BrandGuard AI — Executive Master Presentation & Project Dossier Generator
Builds a high-impact, landscape presentation PDF document using ReportLab.
Team Synapse: Aman Sharma & Janhavi Kanojia (Inkloom AI Hackathon)
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas that computes total page count dynamically
    and draws professional running headers and footers on every slide.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = self._pagesize  # 792 x 612 in landscape letter

        # Don't draw running header/footer on Slide 1 (Cover)
        if self._pageNumber > 1:
            # Top accent bar
            self.setFillColor(colors.HexColor('#0EA5E9'))
            self.rect(0, h - 4, w, 4, fill=True, stroke=False)

            # Running Top Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(36, h - 22, "BRANDGUARD AI  •  ENTERPRISE BRAND GOVERNANCE PLATFORM")
            self.setFont("Helvetica", 8)
            self.drawRightString(w - 36, h - 22, "INKLOOM AI HACKATHON • MASTER PROJECT DOSSIER")

            # Header thin line
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.6)
            self.line(36, h - 28, w - 36, h - 28)

            # Footer thin line
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.6)
            self.line(36, 32, w - 36, 32)

            # Running Bottom Footer
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#0EA5E9'))
            self.drawString(36, 20, "TEAM SYNAPSE:")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(110, 20, "Aman Sharma (Team Lead & Backend) & Janhavi Kanojia (Frontend & UI/UX)")

            page_str = f"Slide {self._pageNumber} of {page_count}"
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#475569'))
            self.drawRightString(w - 36, 20, page_str)

        self.restoreState()


def build_pdf(output_filename="BrandGuard_AI_Executive_Presentation.pdf"):
    # Landscape Letter: 792 pt wide by 612 pt high
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    C_NAVY = '#0F172A'
    C_SLATE = '#1E293B'
    C_BLUE = '#2563EB'
    C_CYAN = '#0EA5E9'
    C_TEXT = '#1E293B'
    C_MUTED = '#64748B'
    C_LIGHT_BG = '#F8FAFC'
    C_BORDER = '#E2E8F0'
    C_GREEN = '#10B981'
    C_AMBER = '#F59E0B'
    C_RED = '#EF4444'

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor('#94A3B8'),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=2
    )

    eyebrow_style = ParagraphStyle(
        'Eyebrow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor(C_BLUE),
        textTransform='uppercase',
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor(C_TEXT)
    )

    body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor(C_MUTED)
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=4
    )

    metric_big = ParagraphStyle(
        'MetricBig',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=26,
        textColor=colors.HexColor(C_BLUE)
    )

    metric_big_red = ParagraphStyle(
        'MetricBigRed',
        parent=metric_big,
        textColor=colors.HexColor(C_RED)
    )

    metric_big_green = ParagraphStyle(
        'MetricBigGreen',
        parent=metric_big,
        textColor=colors.HexColor(C_GREEN)
    )

    metric_big_amber = ParagraphStyle(
        'MetricBigAmber',
        parent=metric_big,
        textColor=colors.HexColor(C_AMBER)
    )

    story = []

    # =========================================================================
    # SLIDE 1: COVER SLIDE (EXECUTIVE NAVY HERO)
    # =========================================================================
    cover_data = [
        [
            Paragraph("<font color='#0EA5E9'><b>INKLOOM AI HACKATHON • ROUND 1 MASTER ARCHITECTURE PLAN</b></font>", eyebrow_style)
        ],
        [
            Paragraph("BrandGuard AI", title_style)
        ],
        [
            Paragraph("Pre-Publication Multi-Modal Brand Governance & Compliance Platform", subtitle_style)
        ],
        [
            Spacer(1, 10)
        ],
        [
            Table([
                [
                    Paragraph("<b>CORE VALUE PROPOSITION</b><br/><font color='#CBD5E1'>An advisory pre-publication stage-gate co-pilot that screens text copy, claims, and graphic banners against brand guidelines and FTC Section 5 rules, offering 1-click tone-preserving rewrites and cryptographic PDF audit certificates.</font>", ParagraphStyle('CoverCard1', parent=body_style, textColor=colors.HexColor('#FFFFFF'), fontSize=9.5, leading=14)),
                    Paragraph("<b>TEAM SYNAPSE LEADERSHIP</b><br/><font color='#38BDF8'><b>Aman Sharma</b></font> — Team Leader & Full-Stack / Backend Architect<br/><font color='#38BDF8'><b>Janhavi Kanojia</b></font> — Frontend & UI/UX Experience Lead<br/><font color='#94A3B8' size='8'>Built with Python 3.11 • Flask • Werkzeug • SQLite/Postgres • ReportLab • OpenCV</font>", ParagraphStyle('CoverCard2', parent=body_style, textColor=colors.HexColor('#FFFFFF'), fontSize=9.5, leading=14))
                ]
            ], colWidths=[380, 310], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 14),
            ])
        ],
        [
            Spacer(1, 16)
        ],
        [
            Paragraph("<font color='#64748B' size='8'>LIVE REPOSITORY: <b>https://github.com/CodingWithAman1/BrandGovernanceAI.git</b>  •  LIVE APPLICATION: <b>https://brandgovernanceai.onrender.com</b></font>", ParagraphStyle('CoverLinks', parent=body_style, textColor=colors.HexColor('#64748B'), alignment=1))
        ]
    ]

    t_cover = Table(cover_data, colWidths=[720])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('PADDING', (0,0), (-1,-1), 22),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 26),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: THE GOVERNANCE CRISIS & REGULATORY PRESSURES
    # =========================================================================
    story.append(Paragraph("THE MARKET CHALLENGE & LEGAL IMPERATIVES", eyebrow_style))
    story.append(Paragraph("The Content Governance Crisis: Empirical Evidence & Regulatory Crackdown", h1_style))
    story.append(Spacer(1, 10))

    crisis_metrics = [
        [
            Paragraph("85%", metric_big_red),
            Paragraph("3.2 Days", metric_big_amber),
            Paragraph("30%", metric_big),
            Paragraph("+33%", metric_big_green)
        ],
        [
            Paragraph("<b>Have Brand Guidelines</b><br/><font color='#64748B'>Organizations establish formal brand guidelines and style guides.</font>", body_style),
            Paragraph("<b>Average Review Latency</b><br/><font color='#64748B'>Legal and brand teams take over 72 hours per campaign asset approval.</font>", body_style),
            Paragraph("<b>Consistent Enforcement</b><br/><font color='#64748B'>Only 30% enforce guidelines consistently across all content channels.</font>", body_style),
            Paragraph("<b>Revenue Uplift</b><br/><font color='#64748B'>Consistent brand presentation across platforms yields up to 33% higher revenue.</font>", body_style)
        ]
    ]
    t_crisis = Table(crisis_metrics, colWidths=[175, 175, 175, 175])
    t_crisis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_crisis)
    story.append(Spacer(1, 14))

    legal_cards = [
        [
            Table([
                [Paragraph("<b>FTC Act Section 5 & Operation AI Comply</b>", card_title)],
                [Paragraph("Regulatory enforcement against unsubstantiated marketing claims, misleading AI capabilities, and unverified '#1' claims. Companies face massive financial penalties and consent decrees for false marketing superlatives.", body_muted)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)]),

            Table([
                [Paragraph("<b>SEC 'AI-Washing' Enforcement</b>", card_title)],
                [Paragraph("The SEC actively prosecutes organizations falsely overstating AI capabilities, autonomous reliability, and guaranteed ROI to prospective enterprise customers and public investors.", body_muted)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)]),

            Table([
                [Paragraph("<b>WCAG 2.1 AA & Accessibility Standards</b>", card_title)],
                [Paragraph("Legal requirements mandate minimum 4.5:1 luminance contrast ratios for standard text and 3:1 for graphical elements. Non-compliant marketing assets face civil accessibility litigation under ADA Title III.", body_muted)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)])
        ]
    ]
    t_legal = Table(legal_cards, colWidths=[240, 240, 240])
    t_legal.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_legal)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: THREE ISOLATED ROLE PORTALS & FIREBASE AUTHENTICATION
    # =========================================================================
    story.append(Paragraph("ROLE-BASED WORKSPACE ARCHITECTURE", eyebrow_style))
    story.append(Paragraph("Three Dedicated Portals with Strict Privilege Separation & Firebase Auth", h1_style))
    story.append(Spacer(1, 10))

    portal_table = [
        [
            Table([
                [Paragraph("<font color='#0EA5E9'><b>CLIENT / CREATOR PORTAL</b></font>", eyebrow_style)],
                [Paragraph("<b>Marketing & Agency Workspace</b>", card_title)],
                [Paragraph("<b>URL:</b> <font color='#0EA5E9'>/client/dashboard</font><br/><b>Primary Users:</b> Content Creators, Copywriters, Agencies<br/><b>Core Capabilities:</b><br/>• Pre-Publication Studio with live character counter<br/>• 3 instant test presets (Risky, Jargon, Compliant)<br/>• Real-time diagnostic scorecards with radial gauges<br/>• 1-Click tone-preserving rewrite acceptance<br/>• Side-by-side live diff preview and clean text export<br/>• Stage-gate routing and personal certificate archive", body_style)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_CYAN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)]),

            Table([
                [Paragraph("<font color='#F59E0B'><b>REVIEWER & LEGAL DESK</b></font>", eyebrow_style)],
                [Paragraph("<b>Governance & Stage-Gate Desk</b>", card_title)],
                [Paragraph("<b>URL:</b> <font color='#F59E0B'>/reviewer/dashboard</font><br/><b>Primary Users:</b> Brand Managers, Legal Counsel<br/><b>Core Capabilities:</b><br/>• Centralized Stage-Gate queue of pending releases<br/>• Deep diagnostic inspection with legal citation links<br/>• Side-by-side red/green diff review engine<br/>• Creator justification and override inspection<br/>• Threaded review comments and feedback logs<br/>• 1-Click Approve, Request Changes, or Reject<br/>• Automated PDF Certificate generation on approval", body_style)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_AMBER)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)]),

            Table([
                [Paragraph("<font color='#EF4444'><b>EXECUTIVE ADMIN CONTROL</b></font>", eyebrow_style)],
                [Paragraph("<b>Aman Sharma (Sole Administrator)</b>", card_title)],
                [Paragraph("<b>URL:</b> <font color='#EF4444'>/admin/dashboard</font><br/><b>Authorized User:</b> aman@synapse.ai (Strictly enforced)<br/><b>Core Capabilities:</b><br/>• System-wide telemetry & cross-department metrics<br/>• Dynamic Brand Rulebook CRUD editor (tone, claims, visual)<br/>• SQL Truth Bank manager with citation links<br/>• User management: promote/demote Reviewers & Clients<br/>• Tamper-evident immutable audit log viewer<br/>• Comprehensive Guideline Clarity & Friction Index", body_style)]
            ], colWidths=[225], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_RED)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 10)])
        ]
    ]
    t_portals = Table(portal_table, colWidths=[240, 240, 240])
    t_portals.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_portals)
    story.append(Spacer(1, 10))

    # Firebase Auth Callout Box
    fb_box = [
        [
            Paragraph("<b>FIREBASE AUTHENTICATION ARCHITECTURE (PROJECT: brandbuildai-2749e)</b><br/><font color='#64748B'>Seamless 1-Click Google Sign-In powered by the Firebase Web SDK. Authenticated tokens are synchronized via <b>/auth/api/firebase-sync</b> to provision user accounts and establish secure, role-restricted Flask-Login sessions with automated RBAC redirects.</font>", body_style)
        ]
    ]
    t_fb = Table(fb_box, colWidths=[720])
    t_fb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_fb)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: THE FOUR COMPLIANCE ENGINES
    # =========================================================================
    story.append(Paragraph("DETERMINISTIC COMPLIANCE ARCHITECTURE", eyebrow_style))
    story.append(Paragraph("The Four Multi-Modal Governance Engines: Zero-Hallucination Design", h1_style))
    story.append(Spacer(1, 10))

    engine_grid = [
        [
            Table([
                [Paragraph("<font color='#2563EB'><b>ENGINE 1: TONE CALIBRATOR</b></font>", eyebrow_style)],
                [Paragraph("<b>Voice Polarity & Robotic Jargon Filter</b>", card_title)],
                [Paragraph("• Evaluates draft text against 5 enterprise tone polarities.<br/>• Regex detection of robotic AI filler (<i>'delve into'</i>, <i>'rich tapestry'</i>, <i>'a testament to'</i>, <i>'game-changer'</i>).<br/>• Filters aggressive/condescending phrasing (<i>'crush competition'</i>, <i>'obviously'</i>).<br/>• Docks score proportionally (Critical: -15, Warning: -10, Suggestion: -5).<br/>• Generates tone-preserving 1-click suggested rewrites.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<font color='#EF4444'><b>ENGINE 2: TRUTH BANK CHECKER</b></font>", eyebrow_style)],
                [Paragraph("<b>FTC Section 5 Claims & Evidence Guardrails</b>", card_title)],
                [Paragraph("• Cross-references claims against the SQL <b>ApprovedFact</b> repository.<br/>• Flags unverified absolute claims (<i>'#1 in the world'</i>, <i>'world's fastest'</i>).<br/>• Catches illegal guarantees (<i>'100% risk-free'</i>, <i>'foolproof'</i>, <i>'never fails'</i>).<br/>• Docks score by -20 per FTC regulatory violation.<br/>• Requires verifiable empirical citations or independent market study links.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ],
        [
            Table([
                [Paragraph("<font color='#0EA5E9'><b>ENGINE 3: VISUAL INSPECTOR</b></font>", eyebrow_style)],
                [Paragraph("<b>OpenCV K-Means & WCAG 2.1 Contrast</b>", card_title)],
                [Paragraph("• OpenCV/PIL image processing with K-Means color quantization.<br/>• Validates uploaded banners against approved corporate design tokens.<br/>• Calculates WCAG 2.1 AA relative luminance contrast ratios:<br/>  <b>Ratio = (L1 + 0.05) / (L2 + 0.05)</b>, enforcing minimum 4.5:1 text threshold.<br/>• Optical Character Recognition (OCR) scans text embedded in banners.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<font color='#10B981'><b>ENGINE 4: CLARITY ENGINE</b></font>", eyebrow_style)],
                [Paragraph("<b>Guideline Friction Index & Feedback Loop</b>", card_title)],
                [Paragraph("• Tracks creator dispute rates, overrides, and 1-click acceptance ratios.<br/>• Generates the <b>Guideline Clarity Index</b> and Friction Heatmap.<br/>• Computes rule friction: <b>Friction = Disputed Overrides / Total Flags</b>.<br/>• Identifies ambiguous corporate rules causing repetitive creator mistakes.<br/>• Empowers leadership to fix outdated guidelines instead of blaming staff.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ]
    ]
    t_engines = Table(engine_grid, colWidths=[360, 360])
    t_engines.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8)
    ]))
    story.append(t_engines)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: END-TO-END WORKFLOW & CRYPTOGRAPHIC CERTIFICATION
    # =========================================================================
    story.append(Paragraph("HUMAN-IN-THE-LOOP (HITL) GOVERNANCE LIFECYCLE", eyebrow_style))
    story.append(Paragraph("The Five-Step Pre-Publication Stage-Gate & PDF Certification", h1_style))
    story.append(Spacer(1, 10))

    flow_steps = [
        [
            Table([
                [Paragraph("<b>STEP 1</b>", eyebrow_style)],
                [Paragraph("<b>Pre-Publish Studio</b>", card_title)],
                [Paragraph("Creator inputs campaign copy or graphic asset. Studio triggers Laser Scanner HUD modal before submission.", body_muted)]
            ], colWidths=[135], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>STEP 2</b>", eyebrow_style)],
                [Paragraph("<b>Diagnostic Scorecard</b>", card_title)],
                [Paragraph("Multi-engine evaluation runs in <150ms. Renders Health Score radial gauge and granular finding cards.", body_muted)]
            ], colWidths=[135], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>STEP 3</b>", eyebrow_style)],
                [Paragraph("<b>1-Click Remediation</b>", card_title)],
                [Paragraph("Creator accepts 1-click rewrites. Live diff updates with green pulse; compliance score recalculates dynamically.", body_muted)]
            ], colWidths=[135], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>STEP 4</b>", eyebrow_style)],
                [Paragraph("<b>Stage-Gate Queue</b>", card_title)],
                [Paragraph("Clean draft routes to Reviewer Desk. Manager and Legal Counsel inspect diffs, citations, and comment threads.", body_muted)]
            ], colWidths=[135], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<font color='#10B981'><b>STEP 5</b></font>", eyebrow_style)],
                [Paragraph("<b>PDF Certification</b>", card_title)],
                [Paragraph("Formal approval triggers SHA-256 content hashing and generates an immutable PDF Compliance Certificate.", body_muted)]
            ], colWidths=[135], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 3, colors.HexColor(C_GREEN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ]
    ]
    t_flow = Table(flow_steps, colWidths=[144, 144, 144, 144, 144])
    t_flow.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_flow)
    story.append(Spacer(1, 14))

    cert_info = [
        [
            Paragraph("<b>ANATOMY OF THE CRYPTOGRAPHIC PDF COMPLIANCE CERTIFICATE</b>", card_title)
        ],
        [
            Table([
                [
                    Paragraph("<b>• SHA-256 Digital Fingerprint:</b> Cryptographically seals the exact approved text so any post-approval tampering invalidates the certificate.<br/><b>• Complete Audit Trail:</b> Logs Submission ID, Approver ID, Formal Approver Name, Department, and UTC Timestamp.<br/><b>• Health Score Card:</b> Embeds final Overall Compliance, Tone Balance, Truth Verification, and Visual Contrast scores.", body_style),
                    Paragraph("<b>• Enterprise Due Diligence:</b> Serves as an immutable legal defense artifact for regulatory compliance audits (FTC, SEC, and EU AI Act).<br/><b>• Automated Generation:</b> Assembled on the fly via ReportLab using vector graphics, formal regulatory headings, and security seals.<br/><b>• Instant Client Access:</b> Downloadable directly from the Client Portal and Reviewer Desk.", body_style)
                ]
            ], colWidths=[350, 350], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 8),
            ])
        ]
    ]
    t_cert = Table(cert_info, colWidths=[720])
    t_cert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cert)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: OBSIDIAN CYBER UI & INTERACTIVE MICRO-INTERACTIONS
    # =========================================================================
    story.append(Paragraph("UI/UX DESIGN SYSTEM & LIVE MICRO-INTERACTIONS", eyebrow_style))
    story.append(Paragraph("Extraordinary Obsidian Cyberpunk Interface with Dual Cursor & Laser HUD", h1_style))
    story.append(Spacer(1, 10))

    ui_grid = [
        [
            Table([
                [Paragraph("<b>Interactive Dual Cyber Cursor</b>", card_title)],
                [Paragraph("• Inner luminous pointer dot (<b>#cursor-dot</b>) with instantaneous tracking.<br/>• Outer magnetic trailing glow ring (<b>#cursor-ring</b>) using 60 FPS Linear Interpolation (lerp) trailing physics.<br/>• Dynamic role-based color shifting (Cyan for Client, Amber for Reviewer, Crimson for Admin).<br/>• Magnetic hover scale on buttons, chips, and inputs with click shockwave ripple animation.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>Moving Background Aurora & Particles</b>", card_title)],
                [Paragraph("• Four ambient radial aurora orbs (Indigo, Cyan, Violet, Rose) drifting along smooth Lissajous curves.<br/>• HTML5 Canvas constellation particle engine generating 40+ drifting luminous nodes that connect with faint vector lines.<br/>• Cyber command grid overlay with radial vignette mask.<br/>• Auto-pauses on background tabs for zero battery drain.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ],
        [
            Table([
                [Paragraph("<b>Multi-Engine Laser Scanner HUD</b>", card_title)],
                [Paragraph("• Holographic modal overlay triggered upon clicking 'Run Pre-Publication Audit'.<br/>• Oscillating neon laser scanline traversing down the document.<br/>• Real-time digital progress gauge counting from 0% to 100%.<br/>• Live terminal status ticks verifying NLP features, Truth Bank claims, OpenCV contrast, and rewrite calibration.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>Side-by-Side Diff Engine & 1-Click Fixes</b>", card_title)],
                [Paragraph("• Live comparison between unvetted initial draft and active remediated copy.<br/>• 1-Click Accept Fix flashes updated text with emerald dark-mode glow.<br/>• Instant 'Copy Snippet' button for each individual recommendation.<br/>• 'Copy Clean Copy' and 'Export (.txt)' buttons for zero-friction copywriter workflow.<br/>• Glassmorphism toast notifications confirming all actions.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ]
    ]
    t_ui = Table(ui_grid, colWidths=[360, 360])
    t_ui.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8)
    ]))
    story.append(t_ui)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: TECHNICAL ARCHITECTURE & DATA SCHEMA
    # =========================================================================
    story.append(Paragraph("TECHNICAL SPECIFICATIONS & SCHEMA", eyebrow_style))
    story.append(Paragraph("Relational SQL Data Model, Flask Modular Architecture & RESTful API", h1_style))
    story.append(Spacer(1, 10))

    schema_data = [
        [
            Paragraph("<b>DATABASE MODEL</b>", eyebrow_style),
            Paragraph("<b>CORE ATTRIBUTES & RELATIONS</b>", eyebrow_style),
            Paragraph("<b>GOVERNANCE RESPONSIBILITY</b>", eyebrow_style)
        ],
        [
            Paragraph("<b>User</b>", body_style),
            Paragraph("id, name, email, role (CREATOR, REVIEWER, ADMIN), department, organization, firebase_uid, is_active", body_muted),
            Paragraph("Role-Based Access Control; strictly locks sole admin privilege to aman@synapse.ai.", body_muted)
        ],
        [
            Paragraph("<b>BrandGuideline</b>", body_style),
            Paragraph("id, rule_code, category (TONE, CLAIM, VISUAL), rule_title, severity, forbidden_patterns, citation_ref", body_muted),
            Paragraph("The corporate brand rulebook; drives deterministic regex and NLP evaluation.", body_muted)
        ],
        [
            Paragraph("<b>ApprovedFact</b>", body_style),
            Paragraph("id, topic, claim_statement, approved_source_link, evidence_excerpt, expiration_date, is_active", body_muted),
            Paragraph("The immutable SQL Truth Bank; grounds verified enterprise claims under FTC Section 5.", body_muted)
        ],
        [
            Paragraph("<b>Submission</b>", body_style),
            Paragraph("id, title, content_type, raw_content, original_content, creator_id, reviewer_id, status, compliance_scores", body_muted),
            Paragraph("The lifecycle tracking model spanning Draft, Scanned, Pending, Changes Requested, and Approved.", body_muted)
        ],
        [
            Paragraph("<b>EvaluationFlag</b>", body_style),
            Paragraph("id, submission_id, guideline_id, flag_type, flagged_snippet, explanation, suggested_fix, status, override_reason", body_muted),
            Paragraph("Granular violation items enabling 1-click remediation or formal creator justifications.", body_muted)
        ],
        [
            Paragraph("<b>ReviewLog</b>", body_style),
            Paragraph("id, submission_id, actor_id, action (SCAN, FIX_ACCEPTED, SUBMIT, APPROVED), comment, timestamp", body_muted),
            Paragraph("Immutable tamper-evident audit ledger capturing all human and system actions.", body_muted)
        ]
    ]
    t_schema = Table(schema_data, colWidths=[120, 340, 260])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 10))

    api_callout = [
        [
            Paragraph("<b>PROGRAMMATIC REST API ENDPOINTS</b><br/>"
                      "• <b>POST /api/v1/scan</b> — Payload: <i>{\"text\": \"...\"}</i> &rarr; Returns: overall score, tone score, claim score, and flag list.<br/>"
                      "• <b>GET /api/v1/guidelines</b> — Returns: active corporate rules, categories, severities, and source citations.<br/>"
                      "• <b>POST /auth/api/firebase-sync</b> — Payload: <i>{idToken, uid, email, portal}</i> &rarr; Syncs Firebase token and returns session cookie.", body_muted)
        ]
    ]
    t_api = Table(api_callout, colWidths=[720])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_api)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: TESTING, PRODUCTION DEPLOYMENT & SUMMARY
    # =========================================================================
    story.append(Paragraph("TESTING, DEPLOYMENT & ROADMAP", eyebrow_style))
    story.append(Paragraph("Comprehensive Verification, Cloud Deployment & Next Milestones", h1_style))
    story.append(Spacer(1, 10))

    summary_cards = [
        [
            Table([
                [Paragraph("<b>32/32 Automated Tests (100% Pass Across 3 Suites)</b>", card_title)],
                [Paragraph("• <b>test_complete_suite.py (12 Tests):</b> Tone Calibrator, Claims Checker, Visual Inspector, Clarity Engine, PDF Generator, Route Protection, Sole Admin Lock, Portal Isolation, and Full Lifecycle.<br/>• <b>test_portals_auth.py (10 Tests):</b> Firebase sync, dynamic navbars, role redirects, and RBAC enforcement.<br/>• <b>test_ai_features.py (10 Tests):</b> AI Co-Pilot, Deep Harmonize, FTC Safe Harbor, and Rule Synthesis.<br/>• All tests passing with 100% assertions satisfied.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_GREEN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>Production Cloud Deployment (Render)</b>", card_title)],
                [Paragraph("• <b>Render Cloud PaaS:</b> Connected directly to GitHub repository with automatic CI/CD on git push to <b>main</b>.<br/>• <b>Gunicorn WSGI:</b> Configured via <b>gunicorn.conf.py</b> and <b>Procfile</b> binding dynamically to <b>0.0.0.0:$PORT</b>.<br/>• <b>Zero-Downtime Healthcheck:</b> Dedicated <b>/healthz</b> route for Render load balancers.<br/>• <b>Live Repo:</b> github.com/CodingWithAman1/BrandGovernanceAI", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_BLUE)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ]
    ]
    t_summary = Table(summary_cards, colWidths=[360, 360])
    t_summary.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_summary)
    story.append(Spacer(1, 12))

    # Closing Team Box
    closing_box = [
        [
            Paragraph("<font color='#0EA5E9'><b>SUBMISSION FOR INKLOOM AI HACKATHON • ROUND 1 MASTER PLAN</b></font>", eyebrow_style)
        ],
        [
            Paragraph("<b>Team Synapse:</b> Aman Sharma & Janhavi Kanojia", card_title)
        ],
        [
            Paragraph("BrandGuard AI transitions enterprise brand governance from a reactive, bureaucratic bottleneck into an intelligent, real-time advisory co-pilot. By unifying linguistic polarity checks, FTC claim verification, accessibility inspections, and cryptographic certification into three dedicated role portals, BrandGuard AI ensures that every piece of published content is verifiable, compliant, and on-brand.", body_style)
        ],
        [
            Spacer(1, 4)
        ],
        [
            Table([
                [
                    Paragraph("<b>Live GitHub Repository:</b><br/><font color='#2563EB'>https://github.com/CodingWithAman1/BrandGovernanceAI.git</font>", body_muted),
                    Paragraph("<b>Live Cloud Application:</b><br/><font color='#2563EB'>https://brandgovernanceai.onrender.com</font>", body_muted)
                ]
            ], colWidths=[350, 350], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('PADDING', (0,0), (-1,-1), 8),
            ])
        ]
    ]
    t_closing = Table(closing_box, colWidths=[720])
    t_closing.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_closing)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated executive presentation PDF: {output_filename}")


if __name__ == '__main__':
    build_pdf()
