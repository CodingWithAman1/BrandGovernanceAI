#!/usr/bin/env python3
"""
BrandGuard AI — Executive Master Presentation & Project Dossier Generator
========================================================================
Inkloom AI Hackathon (Grand Finale Deliverable)
Team Synapse: Aman Sharma & Janhavi Kanojia

Builds an executive-level, landscape presentation PDF document using ReportLab.
Styled in the Obsidian Cyberpunk aesthetic with high contrast, structured layout,
and two-pass running headers and footers with total slide counts ("Slide X of Y").

Slides:
  Slide 1: Executive Cover Slide (Obsidian Navy Hero & Grand Finale Metadata)
  Slide 2: The Multi-Jurisdiction Regulatory Crisis (FTC, SEC, EU AI Act, CMA)
  Slide 3: Three Isolated Portals, 1-Click Persona Switcher & Sole Admin Access
  Slide 4: Deterministic Core Engines + Google Gemini 3 Flash Hybrid Co-Pilot
  Slide 5: Stage-Gate Clearance, Public Certificate Verifier & SHA-256 PDF
  Slide 6: Cyberpunk Obsidian Interface, 0ms Hardware Cursor & 3D WebGL Core
  Slide 7: Enterprise Architecture: Competitor Battlecards, Brand DNA & CI/CD Gate
  Slide 8: 24-Test Automated Verification, Render Cloud Deployment & Product Roadmap
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
            self.drawString(36, h - 22, "BRANDGUARD AI  •  PRE-PUBLICATION BRAND GOVERNANCE PLATFORM")
            self.setFont("Helvetica", 8)
            self.drawRightString(w - 36, h - 22, "INKLOOM AI HACKATHON • GRAND FINALE MASTER DOSSIER")

            # Header thin line
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.6)
            self.line(36, h - 28, w - 36, h - 28)

            # Footer thin line
            self.line(36, 28, w - 36, 28)

            # Running Bottom Footer
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#0F172A'))
            self.drawString(36, 16, "TEAM SYNAPSE:")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(108, 16, "Aman Sharma (Sole Admin & Backend Lead)  •  Janhavi Kanojia (Frontend & UI/UX)")

            # Dynamic Page Count "Slide X of Y"
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#2563EB'))
            page_str = f"Slide {self._pageNumber} of {page_count}"
            self.drawRightString(w - 36, 16, page_str)

        self.restoreState()


def build_pdf(output_filename="BrandGuard_AI_Executive_Presentation.pdf"):
    # Target size: 792 x 612 (Letter Landscape)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    C_NAVY = '#0F172A'       # Slate 900
    C_BLUE = '#2563EB'       # Blue 600
    C_CYAN = '#0EA5E9'       # Sky 500
    C_TEXT = '#1E293B'       # Slate 800
    C_MUTED = '#64748B'      # Slate 500
    C_LIGHT_BG = '#F8FAFC'   # Slate 50
    C_BORDER = '#E2E8F0'     # Slate 200
    C_GREEN = '#10B981'      # Emerald 500
    C_AMBER = '#F59E0B'      # Amber 500
    C_RED = '#EF4444'        # Red 500

    # Custom Typography Styles
    eyebrow_style = ParagraphStyle(
        'CoverEyebrow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor(C_BLUE),
        spaceAfter=3,
        textTransform='uppercase'
    )

    h1_style = ParagraphStyle(
        'SlideH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor(C_TEXT)
    )

    body_muted = ParagraphStyle(
        'SlideBodyMuted',
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
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=3
    )

    story = []

    # =========================================================================
    # SLIDE 1: COVER SLIDE (EXECUTIVE NAVY HERO)
    # =========================================================================
    cover_data = [
        [
            Paragraph("<font color='#38BDF8'><b>INKLOOM AI HACKATHON • GRAND FINALE CHAMPIONSHIP</b></font>", eyebrow_style)
        ],
        [
            Paragraph("<font color='#FFFFFF'><b>BRANDGUARD AI</b></font>", ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=colors.white))
        ],
        [
            Paragraph("<font color='#94A3B8'>Autonomous Pre-Publication Brand Governance, Multi-Jurisdiction Regulatory Enforcement &amp; Cryptographic Stage-Gate Clearance</font>", ParagraphStyle('CSub', fontName='Helvetica', fontSize=12.5, leading=17, textColor=colors.HexColor('#94A3B8')))
        ],
        [
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0EA5E9'), spaceBefore=8, spaceAfter=14)
        ],
        [
            Paragraph("<font color='#E2E8F0'><b>Team Synapse:</b> Aman Sharma (Sole Administrator &amp; Backend Lead) • Janhavi Kanojia (Frontend &amp; UI/UX Developer)<br/>"
                      "<b>Production Deployment:</b> <font color='#38BDF8'>https://brandgovernanceai.onrender.com</font> &bull; <b>GitHub:</b> github.com/CodingWithAman1/BrandGovernanceAI<br/>"
                      "<b>Core Architecture:</b> Dual Deterministic-Neural Hybrid (5 Tone Polarity Spectrums, SQL Truth Bank, Pillow K-Means WCAG 2.1 AA, Google Gemini 3 Flash)</font>", ParagraphStyle('CBody', fontName='Helvetica', fontSize=9, leading=14, textColor=colors.HexColor('#E2E8F0')))
        ],
        [
            Spacer(1, 12)
        ],
        [
            Table([
                [
                    Paragraph("<b>VERIFICATION MATRIX</b><br/><font color='#FFFFFF'>24 / 24 Automated Tests (100% Pass)</font>", ParagraphStyle('CM1', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#38BDF8'))),
                    Paragraph("<b>SOLE ADMIN LOCK</b><br/><font color='#FFFFFF'>aman@synapse.ai (Sole Administrator)</font>", ParagraphStyle('CM2', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#38BDF8'))),
                    Paragraph("<b>PUBLIC AUDIT LEDGER</b><br/><font color='#FFFFFF'>SHA-256 Zero-Login Verifier (/verify)</font>", ParagraphStyle('CM3', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#38BDF8'))),
                    Paragraph("<b>CI/CD INTEGRATIONS</b><br/><font color='#FFFFFF'>GitHub Actions Gate (/api/v1/gate/check)</font>", ParagraphStyle('CM4', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#38BDF8'))),
                ]
            ], colWidths=[170, 180, 175, 175], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
                ('PADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ])
        ]
    ]

    t_cover = Table(cover_data, colWidths=[720])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_NAVY)),
        ('PADDING', (0,0), (-1,-1), 22),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0EA5E9')),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: THE GOVERNANCE CRISIS & REGULATORY PRESSURES
    # =========================================================================
    story.append(Paragraph("THE PROBLEM STATEMENT & MARKET OPPORTUNITY", eyebrow_style))
    story.append(Paragraph("High-Velocity Generative Content vs. Strict Regulatory Compliance", h1_style))
    story.append(Spacer(1, 8))

    problem_cards = [
        [
            Table([
                [Paragraph("<b>1. FTC Section 5 & AI Comply</b>", card_title)],
                [Paragraph("• FTC 15 U.S.C. § 45 strictly prohibits deceptive marketing.<br/>• <i>Operation AI Comply</i> penalizes ungrounded '#1' claims and unverified speed superlatives.<br/>• <b>Penalty:</b> Up to $51,744/day per violation and civil consent decrees.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_RED)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>2. SEC AI-Washing Rule</b>", card_title)],
                [Paragraph("• SEC Rule 10b-5 targets deceptive forward-looking AI statements.<br/>• Companies claiming 'autonomous intelligence' or '100% zero risk' face securities enforcement.<br/>• <b>Penalty:</b> Executive bans, shareholder lawsuits, and mandatory fraud disclosures.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_AMBER)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ],
        [
            Table([
                [Paragraph("<b>3. EU AI Act Art. 50/52 Mandates</b>", card_title)],
                [Paragraph("• Mandates transparent synthetic content watermarking and disclosure.<br/>• Requires auditable human oversight (HITL) for high-impact promotional copy.<br/>• <b>Penalty:</b> Fines up to €35M or 7% of annual worldwide revenue.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_BLUE)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>4. ADA Title III & WCAG 2.1 AA Contrast</b>", card_title)],
                [Paragraph("• Federal courts require digital marketing to satisfy WCAG 2.1 contrast (4.5:1 ratio).<br/>• Over 4,000 accessibility lawsuits filed in 2023 targeting low-contrast banners.<br/>• <b>Penalty:</b> Statutory attorney fees, mandatory settlement decrees, and injunctions.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_CYAN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ]
    ]
    t_prob = Table(problem_cards, colWidths=[360, 360])
    t_prob.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8)
    ]))
    story.append(t_prob)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: THREE ISOLATED ROLE PORTALS & FIREBASE AUTHENTICATION
    # =========================================================================
    story.append(Paragraph("ROLE-BASED GOVERNANCE ARCHITECTURE", eyebrow_style))
    story.append(Paragraph("Three Mathematically Isolated Portals with Strict Sole Admin Lock", h1_style))
    story.append(Spacer(1, 8))

    portal_cards = [
        [
            Table([
                [Paragraph("<b>1. Client / Creator Workspace</b>", card_title)],
                [Paragraph("<b>Role:</b> CREATOR &bull; <code>/portal/client</code><br/>• Pre-Publish Compliance Studio with multi-modal scanning.<br/>• 1-Click suggested fixes with live score recalculation.<br/>• AI Deep Semantic Harmonization via Google Gemini 3 Flash.<br/>• Business exception rationale submission.<br/>• Personal submission tracking &amp; active certificates.", body_muted)]
            ], colWidths=[226], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_CYAN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>2. Reviewer Desk &amp; Legal Queue</b>", card_title)],
                [Paragraph("<b>Role:</b> REVIEWER / MANAGER &bull; <code>/portal/reviewer</code><br/>• Centralized Stage-Gate review queue with SLA timers.<br/>• Side-by-side red/green diff inspector with inline flag fixes.<br/>• Full visibility into author exception rationales &amp; citations.<br/>• 1-Click Stage-Gate clearance (Approve, Request Changes, Reject).<br/>• Automatic cryptographic SHA-256 PDF certificate compilation.", body_muted)]
            ], colWidths=[226], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_AMBER)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)]),

            Table([
                [Paragraph("<b>3. Executive Admin Command Plane</b>", card_title)],
                [Paragraph("<b>Role:</b> ADMIN &bull; Strictly locked to <b>Aman Sharma</b>.<br/>• Brand Rulebook CRUD with regex and severity controls.<br/>• SQL Truth Bank registry with evidence citations.<br/>• AI Ambiguity Resolver with creator dispute telemetry.<br/>• Clarity Index Analytics with Brand Drift Time-Travel.<br/>• Enterprise user activation/deactivation controls.", body_muted)]
            ], colWidths=[226], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_RED)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 9)])
        ]
    ]
    t_port = Table(portal_cards, colWidths=[240, 240, 240])
    t_port.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_port)
    story.append(Spacer(1, 10))

    switcher_box = [
        [
            Paragraph("<b>EVALUATOR &amp; JUDGE DEMO MODE: 1-CLICK PERSONA SWITCHER IN NAVBAR</b><br/>"
                      "To provide an effortless evaluation experience for hackathon judges, BrandGuard AI embeds an agile Persona Quick-Switcher directly into the header. Evaluators can switch seamlessly between Priya (Client Creator), Elena (Legal Reviewer), Marcus (Brand Director), and Aman Sharma (Sole Administrator) with full session re-authentication in 0.04s.", body_muted)
        ]
    ]
    t_sw = Table(switcher_box, colWidths=[720])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sw)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: THE FOUR COMPLIANCE ENGINES + GEMINI CO-PILOT
    # =========================================================================
    story.append(Paragraph("THE DETERMINISTIC & NEURAL ENGINE ARCHITECTURE", eyebrow_style))
    story.append(Paragraph("Four Deterministic Compliance Engines Combined with Google Gemini 3 Flash", h1_style))
    story.append(Spacer(1, 8))

    engine_cards = [
        [
            Table([
                [Paragraph("<b>Engine 1: Tone Calibrator</b>", card_title)],
                [Paragraph("• 5 Voice Polarity Vectors &amp; lexical filters.<br/>• Scans for 12 robotic AI filler clichés (<i>delve into</i>, <i>rich tapestry</i>, <i>game-changer</i>).<br/>• Flags combative attacks &amp; ungrounded superlatives.<br/>• Calculates Flesch Reading Ease and Formality Index.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Engine 2: SQL Truth Bank Fact-Checker</b>", card_title)],
                [Paragraph("• Cross-references claims against the <code>ApprovedFact</code> repository.<br/>• Flags unverified superlatives (<i>#1 in the world</i>, <i>100% risk-free</i>).<br/>• Docks -20 points per ungrounded regulatory claim.<br/>• Enforces FTC Act Section 5 substantiation standards.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ],
        [
            Table([
                [Paragraph("<b>Engine 3: Pillow K-Means WCAG Inspector</b>", card_title)],
                [Paragraph("• Extracts dominant palette colors using K-Means clustering.<br/>• Enforces WCAG 2.1 AA luminance formula: <code>Cr = (L1 + 0.05) / (L2 + 0.05)</code>.<br/>• Strict 4.5:1 minimum contrast threshold for text copy.<br/>• Prevents ADA Title III digital accessibility lawsuits.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Engine 4: Google Gemini 3 Flash Co-Pilot</b>", card_title)],
                [Paragraph("• Resilient multi-model cascade (<code>gemini-3.1-flash-lite</code> &rarr; <code>gemini-flash-lite-latest</code> &rarr; Local NLP).<br/>• Powers Deep Semantic Harmonization &amp; Safe Harbor Disclaimers.<br/>• Interactive slide-out governance chat drawer with live telemetry.<br/>• Closed-loop validator prevents generative AI hallucinations.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ]
    ]
    t_eng = Table(engine_cards, colWidths=[360, 360])
    t_eng.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8)
    ]))
    story.append(t_eng)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: WORKFLOW, PUBLIC VERIFIER & CRYPTOGRAPHIC CERTIFICATION
    # =========================================================================
    story.append(Paragraph("STAGE-GATE CLEARANCE & CRYPTOGRAPHIC LEDGER", eyebrow_style))
    story.append(Paragraph("Human-in-the-Loop Workflow, Public Verifier (/verify) & SHA-256 PDF", h1_style))
    story.append(Spacer(1, 8))

    workflow_flow = [
        [
            Table([
                [Paragraph("<b>Step 1: Multi-Modal Ingest</b>", card_title)],
                [Paragraph("Creator drafts marketing text or uploads banner creatives; Laser Scanner HUD executes 4-phase audit.", body_muted)]
            ], colWidths=[130], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 7)]),

            Table([
                [Paragraph("<b>Step 2: 1-Click Fix &amp; AI</b>", card_title)],
                [Paragraph("Accepts one-click suggested fixes or executes AI Deep Harmonization via Gemini 3 Flash.", body_muted)]
            ], colWidths=[130], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 7)]),

            Table([
                [Paragraph("<b>Step 3: Stage-Gate Queue</b>", card_title)],
                [Paragraph("Routes to Reviewer Desk; legal counsel reviews side-by-side red/green diffs and exception notes.", body_muted)]
            ], colWidths=[130], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 7)]),

            Table([
                [Paragraph("<b>Step 4: Formal Clearance</b>", card_title)],
                [Paragraph("Authorized reviewer executes 1-click Approval; locks copy text, approver email, and UTC timestamp.", body_muted)]
            ], colWidths=[130], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 7)]),

            Table([
                [Paragraph("<b>Step 5: Public Verifier</b>", card_title)],
                [Paragraph("ReportLab compiles tamper-evident PDF; registers SHA-256 digest on public <code>/verify</code> ledger.", body_muted)]
            ], colWidths=[130], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)), ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_GREEN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 7)])
        ]
    ]
    t_flow = Table(workflow_flow, colWidths=[144, 144, 144, 144, 144])
    t_flow.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_flow)
    story.append(Spacer(1, 10))

    cert_box = [
        [
            Paragraph("<b>PUBLIC CRYPTOGRAPHIC VERIFIER &amp; SHA-256 AUDIT LEDGER (/verify &amp; /verify/&lt;cert_hash&gt;)</b><br/>"
                      "• <b>Zero-Login External Verification:</b> Regulatory bodies (FTC/SEC/CMA) and enterprise customers can look up any certificate hash or scan a QR code to verify authenticity without requiring internal system access.<br/>"
                      "• <b>Tamper-Evident Digest Seal:</b> Evaluates <code>hashlib.sha256(raw_content)</code>. Modifying even a single character in approved marketing copy immediately fails verification, eliminating post-publication tampering.<br/>"
                      "• <b>Official PDF Compliance Certificates:</b> Generates downloadable PDF certificates embedding approver signature (Aman Sharma), multi-modal compliance sub-scores, and embeddable live HTML/Markdown badges.", body_muted)
        ]
    ]
    t_cert = Table(cert_box, colWidths=[720])
    t_cert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_GREEN)),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cert)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: OBSIDIAN CYBER UI & 0MS HARDWARE CURSOR
    # =========================================================================
    story.append(Paragraph("UI/UX DESIGN SYSTEM & LIVE MICRO-INTERACTIONS", eyebrow_style))
    story.append(Paragraph("Extraordinary Obsidian Cyberpunk Interface with 0ms Cursor & 3D WebGL", h1_style))
    story.append(Spacer(1, 8))

    ui_grid = [
        [
            Table([
                [Paragraph("<b>Hardware-Accelerated Cyber Cursor</b>", card_title)],
                [Paragraph("• Zero-lag <code>pointermove</code> listener with 0ms placement.<br/>• GPU-accelerated <code>translate3d</code> avoiding layout thrashing.<br/>• Dynamic role-based colors (Cyan Client, Amber Reviewer, Crimson Admin).<br/>• Strict <code>cursor: text !important</code> auto-fallback for form inputs.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Three.js 3D WebGL Holographic Core</b>", card_title)],
                [Paragraph("• Local offline-ready Three.js 3D Holographic Governance Core.<br/>• Single WebGL context architecture with RAF rendering loop.<br/>• IntersectionObserver pauses rendering when canvas leaves viewport.<br/>• Real-time 3D card parallax tilt with 60 FPS damping physics.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ],
        [
            Table([
                [Paragraph("<b>Multi-Engine Laser Scanner HUD</b>", card_title)],
                [Paragraph("• Full-screen holographic modal overlay on audit submission.<br/>• Oscillating neon laser scanline traversing down the document.<br/>• Real-time digital progress gauge counting from 0% to 100%.<br/>• Live terminal status ticks verifying NLP features, Truth Bank, and WCAG.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Omnichannel Live Social Previews</b>", card_title)],
                [Paragraph("• Pixel-accurate live preview mockups for LinkedIn, Twitter/X, and Google SERP.<br/>• Real-time synchronization with active Studio text input.<br/>• Visualizes social card clipping, metadata contrast, and search snippet boundaries.<br/>• 1-Click copy formatted clean copy into clipboard.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
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
    # SLIDE 7: ENTERPRISE ARCHITECTURE: BATTLECARDS, BRAND DNA & CI/CD
    # =========================================================================
    story.append(Paragraph("ROUND 3 ENTERPRISE EXPANSION", eyebrow_style))
    story.append(Paragraph("Competitor Battlecard Studio, Brand Voice DNA & CI/CD Stage-Gate", h1_style))
    story.append(Spacer(1, 8))

    ent_grid = [
        [
            Table([
                [Paragraph("<b>Competitor Battlecard Studio (/scanner/competitor-studio)</b>", card_title)],
                [Paragraph("• Crawls competitor URLs or analyzes pasted ad copy.<br/>• Flags unverified superlatives and AI-washing claims under FTC Section 5.<br/>• Cross-references assertions against the SQL Truth Bank.<br/>• Automatically synthesizes 3-pillar battlecards via Google Gemini 3 Flash:<br/>  1) AE Customer Call Pitch, 2) LinkedIn Hook, 3) Executive PR Positioning.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_BLUE)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Brand Voice DNA Profiler (/brand-dna)</b>", card_title)],
                [Paragraph("• Ingests corporate brand manifestos and founder style guides.<br/>• Extracts quantifiable 5-axis voice polarities (Authority, Warmth, Innovation, Plainspokenness, Technical Depth).<br/>• Synthesizes high-resonance power lexicons and banned synthetic clichés.<br/>• 1-Click commit of generated governance rules into the active rulebook.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_CYAN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ],
        [
            Table([
                [Paragraph("<b>Enterprise CI/CD Quality Gate (/api/v1/gate/check)</b>", card_title)],
                [Paragraph("• Copyable GitHub Actions workflow (<code>brandguard-gate.yml</code>).<br/>• Programmatic REST API endpoint evaluates marketing copy in CI pipelines.<br/>• Returns HTTP 422 to automatically block pull requests with scores &lt; 85.<br/>• Live API test playground in <code>/integrations</code> with cURL, Python, and Node.js.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_GREEN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Audit Vault &amp; Brand Drift Time-Travel</b>", card_title)],
                [Paragraph("• Dedicated Regulatory Audit Vault at <code>/analytics/audit-vault-export</code>.<br/>• Exports signed JSON compliance dossiers with cryptographic seals.<br/>• Time-travel telemetry tracks brand drift across campaign versions.<br/>• Webhook dispatch formats for Slack and Microsoft Teams incident alerts.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_AMBER)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ]
    ]
    t_ent = Table(ent_grid, colWidths=[360, 360])
    t_ent.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8)
    ]))
    story.append(t_ent)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: TESTING, DEPLOYMENT & ROADMAP
    # =========================================================================
    story.append(Paragraph("VERIFICATION, DEPLOYMENT & ROADMAP", eyebrow_style))
    story.append(Paragraph("Comprehensive Test Suite, Live Cloud Deployment & Product Roadmap", h1_style))
    story.append(Spacer(1, 8))

    summary_cards = [
        [
            Table([
                [Paragraph("<b>24/24 Automated Tests (100% Pass Rate)</b>", card_title)],
                [Paragraph("• <b>test_complete_suite.py (18 Tests):</b> Covers Tone Calibrator, Claims Checker, Visual Inspector, Clarity Engine, PDF Generator, Sole Admin Lock (Aman Sharma), Stage-Gate Lifecycle, Audit Vault JSON, and Cyber Cursor.<br/>• <b>test_round3_features.py (6 Tests):</b> Validates Public Certificate Verifier (/verify), Developer Hub (/integrations), Competitor Battlecards, Brand Voice DNA, and CI/CD Quality Gate API (/api/v1/gate/check).<br/>• 100% assertions satisfied with zero regressions.", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_GREEN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)]),

            Table([
                [Paragraph("<b>Production Cloud Deployment (Render)</b>", card_title)],
                [Paragraph("• <b>Render Cloud PaaS:</b> Publicly active at <b>https://brandgovernanceai.onrender.com</b>.<br/>• <b>Gunicorn WSGI Server:</b> High-concurrency production server dynamically binding to <code>0.0.0.0:$PORT</code>.<br/>• <b>Automated CI/CD:</b> Git push to branch <b>main</b> triggers live cloud build.<br/>• <b>Zero-Downtime Healthcheck:</b> Dedicated <code>/healthz</code> route for load balancers.<br/>• <b>Live Repository:</b> github.com/CodingWithAman1/BrandGovernanceAI", body_muted)]
            ], colWidths=[340], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_BLUE)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 8)])
        ]
    ]
    t_summary = Table(summary_cards, colWidths=[360, 360])
    t_summary.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_summary)
    story.append(Spacer(1, 8))

    # Product Roadmap & Team Credits Box
    closing_box = [
        [
            Paragraph("<b>FUTURE ROADMAP &amp; EXECUTIVE CREDITS • TEAM SYNAPSE</b>", eyebrow_style)
        ],
        [
            Paragraph("<b>Aman Sharma</b> (Sole Administrator &amp; Backend Lead)  •  <b>Janhavi Kanojia</b> (Frontend &amp; UI/UX Lead)", card_title)
        ],
        [
            Paragraph("• <b>Phase 1 (Q1 2027):</b> Headless Browser Crawler (Puppeteer/Playwright) to parse dynamic client-rendered React/Vue competitor web applications.<br/>"
                      "• <b>Phase 2 (Q2 2027):</b> Native Figma &amp; Google Docs desktop plugins delivering real-time brand voice feedback inline during drafting.<br/>"
                      "• <b>Phase 3 (Q3 2027):</b> Public Blockchain Timestamp Anchoring (Hedera/Polygon) for court-admissible audit proof in regulatory due diligence.<br/>"
                      "<b>Live Application:</b> <font color='#2563EB'>https://brandgovernanceai.onrender.com</font> &bull; <b>GitHub:</b> <font color='#2563EB'>https://github.com/CodingWithAman1/BrandGovernanceAI.git</font>", body_muted)
        ]
    ]
    t_closing = Table(closing_box, colWidths=[720])
    t_closing.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(C_CYAN)),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_closing)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated executive presentation PDF: {output_filename}")


if __name__ == '__main__':
    build_pdf()
