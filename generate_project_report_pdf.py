#!/usr/bin/env python3
"""
BrandGuard AI — Comprehensive Technical Engineering Project Report PDF Generator
================================================================================
Inkloom AI Hackathon (Round 1 Deliverable)
Team Synapse: Aman Sharma & Janhavi Kanojia

Generates a formal, 8-page portrait-format technical engineering project report
document for BrandGuard AI. Styled in an Obsidian-cyberpunk executive visual system
with high contrast, structured typography, analytical data tables, and two-pass
running headers and footers with total page counts ("Page X of Y").

Pages:
  Page 1: Formal Project Report Cover Page (Obsidian Hero & Executive Abstract)
  Page 2: Chapter 1: Problem Statement & Regulatory Imperatives
  Page 3: Chapter 2: Three Isolated Role Portals & Stage-Gate Architecture
  Page 4: Chapter 3: The Four Deterministic Governance Engines
  Page 5: Chapter 4: Stage-Gate HITL Workflow & Cryptographic PDF Certification
  Page 6: Chapter 5: Obsidian Cyberpunk UI Design System & Micro-Interactions
  Page 7: Chapter 6: Relational Data Model, RESTful APIs & Verification Matrix
  Page 8: Chapter 7: Cloud Deployment Architecture, Verification & Executive Sign-Off
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# Document Geometry (Letter Portrait)
PAGE_WIDTH, PAGE_HEIGHT = letter  # 612 x 792 pt
MARGIN = 40.0                     # 40 pt margins
PRINTABLE_WIDTH = PAGE_WIDTH - (2 * MARGIN)  # 532.0 pt


class NumberedCanvasPortrait(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total pages and draw consistent
    running headers and footers with 'Page X of Y'.
    Suppresses headers and footers on Cover Page (Page 1).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Omit on Cover Page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()

        # RUNNING TOP HEADER
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor('#0284C7'))  # Sky 600
        self.drawString(MARGIN, PAGE_HEIGHT - 26, "BRANDGUARD AI")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))  # Slate 500
        self.drawString(MARGIN + 82, PAGE_HEIGHT - 26, "•  TECHNICAL ENGINEERING PROJECT REPORT  •  INKLOOM HACKATHON")

        self.setFont("Helvetica", 7.5)
        self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 26, "OCTOBER 2026  |  VERSION 2.0 RC")

        # Header dividing line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.6)
        self.line(MARGIN, PAGE_HEIGHT - 31, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 31)

        # RUNNING BOTTOM FOOTER
        # Footer dividing line
        self.line(MARGIN, 34, PAGE_WIDTH - MARGIN, 34)

        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(MARGIN, 22, "TEAM SYNAPSE:")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(MARGIN + 72, 22, "Aman Sharma (Team Lead & Backend)  •  Janhavi Kanojia (Frontend & UI/UX)")

        # Page Number Indicator "Page X of Y"
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor('#0284C7'))
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN, 22, page_str)

        self.restoreState()


def build_project_report_pdf(output_filename="BrandGuard_AI_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    styles = getSampleStyleSheet()

    # Color Palette Definitions
    C_NAVY = '#0F172A'       # Slate 900
    C_BLUE = '#0284C7'       # Sky 600
    C_CYAN = '#0EA5E9'       # Sky 500
    C_TEXT = '#1E293B'       # Slate 800
    C_MUTED = '#475569'      # Slate 600
    C_LIGHT_BG = '#F8FAFC'   # Slate 50
    C_BORDER = '#CBD5E1'     # Slate 300
    C_GREEN = '#059669'      # Emerald 600
    C_AMBER = '#D97706'      # Amber 600
    C_RED = '#DC2626'        # Red 600

    # Typography Styles
    cover_eyebrow = ParagraphStyle(
        'CoverEyebrow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#38BDF8'),
        spaceAfter=10,
        textTransform='uppercase'
    )

    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=8
    )

    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#94A3B8'),
        spaceAfter=18
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor(C_NAVY),
        spaceBefore=2,
        spaceAfter=4,
        keepWithNext=True
    )

    eyebrow = ParagraphStyle(
        'EyebrowStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor(C_BLUE),
        textTransform='uppercase',
        spaceAfter=1
    )

    body = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor(C_TEXT),
        spaceAfter=5
    )
    body_style = body

    body_bold = ParagraphStyle(
        'ReportBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    body_muted = ParagraphStyle(
        'ReportBodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor(C_MUTED)
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=3,
        keepWithNext=True
    )

    metric_val = ParagraphStyle(
        'MetricVal',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=18,
        textColor=colors.HexColor(C_BLUE)
    )

    story = []

    # =========================================================================
    # PAGE 1: FORMAL PROJECT REPORT COVER PAGE (OBSIDIAN HERO)
    # =========================================================================
    cover_content = [
        [
            Paragraph("INKLOOM AI HACKATHON • ROUND 1 FINAL DELIVERABLE", cover_eyebrow)
        ],
        [
            Paragraph("BrandGuard AI", cover_title)
        ],
        [
            Paragraph("Pre-Publication Multi-Modal Brand Governance, Stage-Gate Compliance & Automated Remediation Platform", cover_subtitle)
        ],
        [
            Spacer(1, 6)
        ],
        [
            Table([
                [
                    Paragraph("<b>DOCUMENT TYPE:</b> Engineering & Architecture Project Report<br/>"
                              "<b>VERSION:</b> 2.0 Production Release Candidate<br/>"
                              "<b>DATE:</b> October 2026<br/>"
                              "<b>SECURITY CLASSIFICATION:</b> Open Hackathon Submission", ParagraphStyle('Meta1', parent=body_style, textColor=colors.HexColor('#CBD5E1'), fontSize=8, leading=12)),
                    Paragraph("<b>SUBMITTED BY: TEAM SYNAPSE</b><br/>"
                              "• <b>Aman Sharma</b> — Team Leader & Backend / System Architect<br/>"
                              "• <b>Janhavi Kanojia</b> — Frontend & UI/UX Experience Lead<br/>"
                              "<b>STACK:</b> Python 3.11 • Flask • SQLite • OpenCV • ReportLab", ParagraphStyle('Meta2', parent=body_style, textColor=colors.HexColor('#CBD5E1'), fontSize=8, leading=12))
                ]
            ], colWidths=[260, 240], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('PADDING', (0,0), (-1,-1), 8),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ])
        ],
        [
            Spacer(1, 12)
        ],
        [
            Table([
                [
                    Paragraph("<b>EXECUTIVE ABSTRACT & SYSTEM OBJECTIVE</b>", ParagraphStyle('AbsTitle', parent=body_bold, textColor=colors.HexColor('#38BDF8'), fontSize=9, spaceAfter=4)),
                ],
                [
                    Paragraph(
                        "<b>BrandGuard AI</b> introduces a deterministic pre-publication governance co-pilot that evaluates marketing drafts across linguistic tone polarities, FTC truth bank registries, and visual accessibility before deployment. Featuring 1-click tone-preserving rewrites, three strictly isolated role portals (Client Workspace, Reviewer Desk, Executive Admin), and cryptographic PDF audit certification, BrandGuard AI accelerates campaign velocity while delivering total compliance defense.",
                        ParagraphStyle('AbstractText', parent=body_style, textColor=colors.HexColor('#F8FAFC'), fontSize=8.5, leading=13)
                    )
                ]
            ], colWidths=[500], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0B132B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284C7')),
                ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor('#38BDF8')),
                ('PADDING', (0,0), (-1,-1), 10),
            ])
        ],
        [
            Spacer(1, 14)
        ],
        [
            # Cover Stats Grid
            Table([
                [
                    Paragraph("<b>4 Deterministic Engines</b><br/><font color='#94A3B8'>Tone, Truth, Contrast, Clarity</font>", ParagraphStyle('CS1', parent=body_muted, textColor=colors.HexColor('#FFFFFF'))),
                    Paragraph("<b>3 Isolated Portals</b><br/><font color='#94A3B8'>Client, Reviewer, Admin RBAC</font>", ParagraphStyle('CS2', parent=body_muted, textColor=colors.HexColor('#FFFFFF'))),
                    Paragraph("<b>32 Automated Tests</b><br/><font color='#94A3B8'>100% Pass Across 3 Suites</font>", ParagraphStyle('CS3', parent=body_muted, textColor=colors.HexColor('#FFFFFF'))),
                    Paragraph("<b>SHA-256 Tamper-Proof</b><br/><font color='#94A3B8'>Cryptographic PDF Certificates</font>", ParagraphStyle('CS4', parent=body_muted, textColor=colors.HexColor('#FFFFFF')))
                ]
            ], colWidths=[125, 125, 125, 125], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
                ('PADDING', (0,0), (-1,-1), 7),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')
            ])
        ],
        [
            Spacer(1, 12)
        ],
        [
            Paragraph("<font color='#64748B' size='7.5'>GITHUB REPOSITORY: <b>https://github.com/CodingWithAman1/BrandGovernanceAI.git</b>  •  LIVE APPLICATION: <b>https://brandgovernanceai.onrender.com</b></font>", ParagraphStyle('CoverLinks', parent=body_style, alignment=1))
        ]
    ]

    t_cover = Table(cover_content, colWidths=[532])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CHAPTER 1: PROBLEM STATEMENT & REGULATORY IMPERATIVES
    # =========================================================================
    story.append(Paragraph("CHAPTER 1", eyebrow))
    story.append(Paragraph("1. Problem Statement & Regulatory Imperatives", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Modern enterprise marketing teams face conflicting imperatives: producing high volumes of multi-channel content at rapid velocity while confronting escalating regulatory oversight. This operational friction causes systemic compliance failures:",
        body
    ))

    story.append(Paragraph("<b>1.1 The Operational Bottleneck:</b> Creative teams wait an average of <b>3.2 business days</b> for manual legal review of ad copy, social posts, and display banners. Under tight campaign deadlines, up to 42% of unvetted creative collateral is pushed directly to production channels without compliance clearance.", body))
    story.append(Paragraph("<b>1.2 The Synthetic Copy Deluge:</b> While 85% of enterprises possess formal brand style guides, fewer than 30% enforce them systematically. The proliferation of generic generative AI tools has worsened this challenge, flooding marketing channels with clichéd synthetic filler (<i>'delve into'</i>, <i>'a testament to'</i>), unsubstantiated competitive attacks (<i>'crush the competition'</i>), and aggressive superlative claims.", body))

    # Metric Grid
    kpi_table = [
        [
            Paragraph("85%", ParagraphStyle('K1', parent=metric_val, textColor=colors.HexColor(C_BLUE))),
            Paragraph("30%", ParagraphStyle('K2', parent=metric_val, textColor=colors.HexColor(C_RED))),
            Paragraph("3.2 Days", ParagraphStyle('K3', parent=metric_val, textColor=colors.HexColor(C_AMBER))),
            Paragraph("+33%", ParagraphStyle('K4', parent=metric_val, textColor=colors.HexColor(C_GREEN)))
        ],
        [
            Paragraph("<b>Have Brand Rules</b><br/><font color='#64748B'>Possess formal guidelines.</font>", body_muted),
            Paragraph("<b>Consistent Adherence</b><br/><font color='#64748B'>Systematic channel compliance.</font>", body_muted),
            Paragraph("<b>Review Latency</b><br/><font color='#64748B'>Manual legal turnaround delay.</font>", body_muted),
            Paragraph("<b>Revenue Uplift</b><br/><font color='#64748B'>With uniform brand execution.</font>", body_muted)
        ]
    ]
    t_kpi = Table(kpi_table, colWidths=[133, 133, 133, 133])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.3 The Regulatory Landscape:</b> Statutory penalties for deceptive advertising and non-accessible design have become severe enforcement priorities globally:", body))

    reg_items = [
        [
            Paragraph("<b>REGULATORY BODY</b>", eyebrow),
            Paragraph("<b>STATUTORY MANDATE</b>", eyebrow),
            Paragraph("<b>GOVERNANCE RISK ENFORCED</b>", eyebrow)
        ],
        [
            Paragraph("<b>FTC Section 5</b>", body_bold),
            Paragraph("Operation AI Comply & Truth in Advertising", body_muted),
            Paragraph("Prohibits unsubstantiated claims, fake testimonials, and unprovable '#1' market leadership superlatives without third-party proof.", body_muted)
        ],
        [
            Paragraph("<b>SEC Enforcement</b>", body_bold),
            Paragraph("'AI-Washing' Statutory Prohibitions", body_muted),
            Paragraph("Penalizes false representations of autonomous capabilities, unverified 100% uptime claims, and risk-free commercial representations.", body_muted)
        ],
        [
            Paragraph("<b>ADA Title III / WCAG</b>", body_bold),
            Paragraph("WCAG 2.1 AA Digital Accessibility", body_muted),
            Paragraph("Enforces 4.5:1 text-to-background contrast ratios in digital banners, protecting brands from civil accessibility litigation.", body_muted)
        ]
    ]
    t_reg = Table(reg_items, colWidths=[110, 182, 240])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 6))

    # Strategic Value Proposition Box
    val_box = [
        [
            Paragraph("<b>STRATEGIC IMPERATIVE: PRE-PUBLICATION GOVERNANCE CO-PILOT</b>", card_title)
        ],
        [
            Paragraph("BrandGuard AI replaces post-publication auditing with a deterministic <b>pre-publication gatekeeper</b>. By diagnosing non-compliant phrasing, unverified claims, and accessibility violations in real time, BrandGuard AI collapses approval turnaround from 3.2 days to under 30 seconds while guaranteeing complete compliance before content reaches public channels.", body_muted)
        ]
    ]
    t_val = Table(val_box, colWidths=[532])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#BBF7D0')),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_GREEN)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_val)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CHAPTER 2: THREE ISOLATED ROLE PORTALS & RBAC
    # =========================================================================
    story.append(Paragraph("CHAPTER 2", eyebrow))
    story.append(Paragraph("2. Three Dedicated Portals & Role-Based Access Control", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "A foundational architectural pillar of BrandGuard AI is its strict separation into three isolated operational portals. Rather than blending user personas into a shared interface, BrandGuard AI implements strict Role-Based Access Control (RBAC):",
        body
    ))

    portal_spec = [
        [
            Table([
                [Paragraph("<font color='#0EA5E9'><b>CLIENT & CREATOR PORTAL</b></font>", eyebrow)],
                [Paragraph("<b>Route: /client/dashboard</b>", body_bold)],
                [Paragraph("Tailored for marketing copywriters and creative agencies. Features the Pre-Publication Studio, live character counting, 3 instant sample presets, real-time radial score gauges, 1-click tone-preserving remediations, and clean text export (.txt). Creators cannot approve their own drafts.", body_muted)]
            ], colWidths=[170], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 3, colors.HexColor(C_CYAN)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 6)]),

            Table([
                [Paragraph("<font color='#D97706'><b>REVIEWER & LEGAL DESK</b></font>", eyebrow)],
                [Paragraph("<b>Route: /reviewer/dashboard</b>", body_bold)],
                [Paragraph("Restricted to Brand Managers and Legal Counsel. Features the centralized Stage-Gate queue, side-by-side red/green diff inspector, exception justification reviewer, threaded audit comments, and formal 1-click Approve, Request Changes, or Reject actions.", body_muted)]
            ], colWidths=[170], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 3, colors.HexColor(C_AMBER)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 6)]),

            Table([
                [Paragraph("<font color='#DC2626'><b>EXECUTIVE ADMIN CONTROL</b></font>", eyebrow)],
                [Paragraph("<b>Route: /admin/dashboard</b>", body_bold)],
                [Paragraph("Strictly locked to Aman Sharma (aman@synapse.ai). Provides global system telemetry, dynamic CRUD Brand Rulebook editor, SQL Truth Bank manager, user role governance (promoting/demoting reviewers and clients), and the Guideline Clarity Index.", body_muted)]
            ], colWidths=[170], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')), ('LINEBEFORE', (0,0), (0,-1), 3, colors.HexColor(C_RED)), ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)), ('PADDING', (0,0), (-1,-1), 6)])
        ]
    ]
    t_pspec = Table(portal_spec, colWidths=[177, 177, 177])
    t_pspec.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_pspec)
    story.append(Spacer(1, 6))

    # Security & Auth Architecture Table
    sec_arch = [
        [
            Paragraph("<b>SECURITY LAYER</b>", eyebrow),
            Paragraph("<b>MECHANISM & IMPLEMENTATION</b>", eyebrow),
            Paragraph("<b>ENFORCEMENT BEHAVIOR</b>", eyebrow)
        ],
        [
            Paragraph("<b>Route Guarding</b>", body_bold),
            Paragraph("Flask-Login <code>@login_required</code> decorator across all internal dashboard and studio endpoints.", code_style),
            Paragraph("Intercepts unauthenticated requests and issues <b>HTTP 302 redirect to /login</b>. Restricts direct URL bypass.", body_muted)
        ],
        [
            Paragraph("<b>Role Boundary Isolation</b>", body_bold),
            Paragraph("Secondary RBAC verification checks <code>current_user.role</code> against endpoint role requirements.", code_style),
            Paragraph("Creators attempting to access <code>/reviewer/*</code> or <code>/admin/*</code> receive an authorization flash warning and redirect.", body_muted)
        ],
        [
            Paragraph("<b>Sole Admin Gate</b>", body_bold),
            Paragraph("Strict hard-coded check: <code>current_user.email == 'aman@synapse.ai'</code> within the admin blueprint.", code_style),
            Paragraph("Prevents privilege escalation; unauthorized staff attempting to access <code>/admin/dashboard</code> are blocked immediately.", body_muted)
        ],
        [
            Paragraph("<b>Firebase Auth Sync</b>", body_bold),
            Paragraph("Firebase project <code>brandbuildai-2749e</code>. Web SDK sends OAuth ID tokens to <code>/auth/api/firebase-sync</code>.", code_style),
            Paragraph("Syncs Google identity securely with SQLite/PostgreSQL user records and maintains Flask session integrity.", body_muted)
        ]
    ]
    t_sec = Table(sec_arch, colWidths=[120, 220, 192])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2.3 Dynamic Role-Adaptive UI Navigation:</b> The navigation bar dynamically adapts to the authenticated role. Client accounts display links to 'Scanner Studio' and 'My Drafts', Reviewers see 'Review Queue' and 'Audit Diffs', while Administrator accounts expose 'Brand Rulebook CRUD', 'Truth Bank', and 'User Management'.", body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CHAPTER 3: THE FOUR DETERMINISTIC GOVERNANCE ENGINES
    # =========================================================================
    story.append(Paragraph("CHAPTER 3", eyebrow))
    story.append(Paragraph("3. The Four Deterministic Governance Engines", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "BrandGuard AI rejects non-deterministic LLM prompting for core compliance clearance. Prompting LLMs with <i>'Is this compliant?'</i> yields unpredictable hallucinations and fluctuating scores. Instead, BrandGuard AI implements four deterministic, rule-grounded engines:",
        body
    ))

    engine_details = [
        [
            Paragraph("<b>ENGINE</b>", eyebrow),
            Paragraph("<b>UNDERLYING ALGORITHM & STANDARDS</b>", eyebrow),
            Paragraph("<b>IMPACT & REMEDIATION</b>", eyebrow)
        ],
        [
            Paragraph("<b>Engine 1:<br/>Tone Calibrator</b>", body_bold),
            Paragraph("<b>5 Voice Polarity Spectrums & Regex Filters</b><br/>"
                      "• Scans for 6 clichéd AI filler patterns (<i>delve into</i>, <i>rich tapestry</i>, <i>a testament to</i>, <i>game-changer</i>, <i>unpack</i>).<br/>"
                      "• Catches aggressive competitor attacks (<i>crush the competition</i>) and condescending phrasing (<i>obviously</i>).<br/>"
                      "• Subtracts points proportionally (Critical: -15, Warning: -10, Suggestion: -5).", body_muted),
            Paragraph("Generates context-aware, 1-click tone-preserving suggested rewrites without homogenizing the author's message.", body_muted)
        ],
        [
            Paragraph("<b>Engine 2:<br/>Truth Bank Checker</b>", body_bold),
            Paragraph("<b>FTC Section 5 Guardrails & SQL Truth Bank</b><br/>"
                      "• Cross-checks claims against the <code>ApprovedFact</code> repository containing verified citations and validity dates.<br/>"
                      "• Flags absolute unprovable superlatives (<i>#1 in the world</i>, <i>world's fastest</i>, <i>100% risk free</i>).<br/>"
                      "• Docks -20 points per regulatory claim violation.", body_muted),
            Paragraph("Protects against FTC Section 5 and SEC enforcement actions by requiring verifiable third-party evidentiary proof.", body_muted)
        ],
        [
            Paragraph("<b>Engine 3:<br/>Visual Inspector</b>", body_bold),
            Paragraph("<b>OpenCV K-Means & WCAG 2.1 Contrast</b><br/>"
                      "• Extracts dominant palette colors using K-Means color quantization in Pillow/OpenCV.<br/>"
                      "• Enforces WCAG 2.1 AA relative luminance contrast formula:<br/>"
                      "  <code>Ratio = (L1 + 0.05) / (L2 + 0.05)</code>.<br/>"
                      "• Scans text inside graphics via OCR to prevent visual copy bypass.", body_muted),
            Paragraph("Ensures marketing banners adhere to corporate design tokens and satisfy statutory 4.5:1 text contrast ratios.", body_muted)
        ],
        [
            Paragraph("<b>Engine 4:<br/>Clarity Engine</b>", body_bold),
            Paragraph("<b>Guideline Friction Index & Heatmap</b><br/>"
                      "• Tracks creator dispute rates, overrides, and 1-click acceptance ratios.<br/>"
                      "• Computes rule friction: <code>Friction = Overrides / Flags</code>.<br/>"
                      "• Assigns empirical clarity scores (0–100%) to each corporate guideline.", body_muted),
            Paragraph("Transforms governance into an empirical feedback loop, identifying ambiguous rules that need refinement.", body_muted)
        ]
    ]
    t_ed = Table(engine_details, colWidths=[100, 240, 192])
    t_ed.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ed)
    story.append(Spacer(1, 6))

    # Mathematical Formula Box
    formula_box = [
        [
            Paragraph("<b>DETERMINISTIC COMPLIANCE FORMULATIONS & STANDARDS</b>", card_title)
        ],
        [
            Paragraph("• <b>WCAG 2.1 AA Relative Luminance:</b> <code>L = 0.2126*R + 0.7152*G + 0.0722*B</code> where sRGB values are gamma-linearized. Contrast ratio <code>Cr = (L_lighter + 0.05) / (L_darker + 0.05)</code>. Minimum threshold: <b>4.5:1</b> for normal text, <b>3.0:1</b> for large text.<br/>"
                      "• <b>Guideline Clarity Index (GCI):</b> <code>GCI = 100 - [(Dispute_Rate * 0.6) + (Exception_Frequency * 0.4)] * 100</code>.<br/>"
                      "• <b>Composite Brand Health Score:</b> <code>Score = 100 - sum(Severity_Penalty_i)</code> clipped to [0, 100].", code_style)
        ]
    ]
    t_form = Table(formula_box, colWidths=[532])
    t_form.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_BLUE)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_form)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CHAPTER 4: HITL STAGE-GATE & PDF CERTIFICATION
    # =========================================================================
    story.append(Paragraph("CHAPTER 4", eyebrow))
    story.append(Paragraph("4. Stage-Gate Workflow & Cryptographic PDF Certification", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "BrandGuard AI enforces a formal <b>Human-in-the-Loop (HITL)</b> release boundary. Automated algorithms diagnose and suggest remediations, but formal clearance requires authorized human reviewer approval:",
        body
    ))

    # 5-Step Pipeline Table
    pipeline_steps = [
        [
            Paragraph("<b>STAGE</b>", eyebrow),
            Paragraph("<b>SYSTEM / ACTOR ACTION</b>", eyebrow),
            Paragraph("<b>DELIVERABLE / STATE TRANSITION</b>", eyebrow)
        ],
        [
            Paragraph("<b>1. Studio Input</b>", body_bold),
            Paragraph("Creator drafts copy or uploads creative assets; animated Laser Scanner HUD executes pre-flight scan.", body_muted),
            Paragraph("Generates diagnostic flags and calculates real-time Brand Health Score (0–100%).", body_muted)
        ],
        [
            Paragraph("<b>2. 1-Click Fix</b>", body_bold),
            Paragraph("Creator clicks remediation button; text updates with dark-mode emerald glow without page reload.", body_muted),
            Paragraph("Live score recalculation; flags resolve instantly or creator enters exception rationale.", body_muted)
        ],
        [
            Paragraph("<b>3. Stage-Gate Submission</b>", body_bold),
            Paragraph("Draft transitions from <code>DRAFT</code> to <code>PENDING_REVIEW</code>; routes to Reviewer Desk.", body_muted),
            Paragraph("Reviewers receive centralized queue notification with urgency badges and SLA trackers.", body_muted)
        ],
        [
            Paragraph("<b>4. Reviewer Inspection</b>", body_bold),
            Paragraph("Brand Manager or Legal Counsel inspects side-by-side red/green diffs, comments, and citations.", body_muted),
            Paragraph("Reviewer executes 1-click action: <b>Approve</b>, <b>Request Changes</b>, or <b>Reject</b>.", body_muted)
        ],
        [
            Paragraph("<b>5. Cryptographic Certification</b>", body_bold),
            Paragraph("Upon approval, ReportLab compiles an unalterable, tamper-evident PDF Compliance Certificate.", body_muted),
            Paragraph("SHA-256 fingerprint generated over final text and permanently stored in database.", body_muted)
        ]
    ]
    t_pipe = Table(pipeline_steps, colWidths=[100, 232, 200])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_pipe)
    story.append(Spacer(1, 6))

    # PDF Anatomy Box
    cert_box = [
        [
            Paragraph("<b>ANATOMY OF THE CRYPTOGRAPHIC PDF COMPLIANCE CERTIFICATE</b>", card_title)
        ],
        [
            Paragraph("• <b>SHA-256 Fingerprint:</b> Cryptographically seals the approved copy text. Modifying a single character after approval invalidates the hash.<br/>"
                      "• <b>Audit Trail Metadata:</b> Embeds Submission ID, Approver ID, Reviewer Name, Department, and UTC Timestamp.<br/>"
                      "• <b>Health Breakdown:</b> Displays final Overall Compliance, Tone Balance, Truth Verification, and Visual Contrast scores.<br/>"
                      "• <b>Legal Defense Asset:</b> Serves as an unalterable certificate for enterprise compliance audits and regulatory due diligence defense.", body_muted)
        ]
    ]
    t_certbox = Table(cert_box, colWidths=[532])
    t_certbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_GREEN)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_certbox)
    story.append(Spacer(1, 6))

    # Exception Handling Flow Box
    exc_box = [
        [
            Paragraph("<b>HUMAN EXCEPTION HANDLING & DISPUTE RESOLUTION</b>", card_title)
        ],
        [
            Paragraph("When creative context warrants intentional departures from standard guidelines (e.g., deliberate edgy branding in a targeted campaign), creators submit an <b>Exception Justification</b>. This justification is permanently appended to the submission record, requiring formal reviewer sign-off. This mechanism eliminates workflow deadlocks while maintaining an immutable audit log.", body_muted)
        ]
    ]
    t_exc = Table(exc_box, colWidths=[532])
    t_exc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FDE68A')),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_AMBER)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_exc)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CHAPTER 5: OBSIDIAN CYBER THEME & UI MICRO-INTERACTIONS
    # =========================================================================
    story.append(Paragraph("CHAPTER 5", eyebrow))
    story.append(Paragraph("5. Obsidian Cyberpunk Design System & Micro-Interactions", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "To deliver a world-class enterprise user experience, BrandGuard AI implements a bespoke <b>Obsidian Cyberpunk Design System</b> with custom interactive cursors and moving background elements:",
        body
    ))

    ui_specs = [
        [
            Paragraph("<b>UI COMPONENT</b>", eyebrow),
            Paragraph("<b>TECHNICAL IMPLEMENTATION</b>", eyebrow),
            Paragraph("<b>USER EXPERIENCE BENEFIT</b>", eyebrow)
        ],
        [
            Paragraph("<b>Interactive Dual Cyber Cursor</b>", body_bold),
            Paragraph("• Inner luminous pointer dot (<code>#cursor-dot</code>) with instant tracking.<br/>"
                      "• Outer trailing magnetic ring (<code>#cursor-ring</code>) using 60 FPS Linear Interpolation (lerp) physics.<br/>"
                      "• Dynamic role-color adaptation (Cyan for Client, Amber for Reviewer, Crimson for Admin).", body_muted),
            Paragraph("Creates fluid, tactile feedback over clickable cards, buttons, and inputs; automatically hides on mobile/touch screens.", body_muted)
        ],
        [
            Paragraph("<b>Lively Ambient Background Layer</b>", body_bold),
            Paragraph("• Four ambient radial orbs (Indigo, Cyan, Violet, Rose) with 3D Lissajous floating keyframe animations.<br/>"
                      "• HTML5 Canvas constellation particle engine generating 40+ drifting luminous nodes that connect via vector lines.<br/>"
                      "• Subtle cyber command grid overlay with radial vignette mask.", body_muted),
            Paragraph("Delivers an authentic high-tech AI command deck aesthetic without distracting from content; auto-pauses when browser tab is hidden.", body_muted)
        ],
        [
            Paragraph("<b>Multi-Engine Laser Scanner HUD</b>", body_bold),
            Paragraph("• Full-screen holographic modal overlay triggered on audit submission.<br/>"
                      "• Oscillating neon laser scanline traversing down the document.<br/>"
                      "• Digital progress gauge counting 0% &rarr; 100% with real-time phase indicators.", body_muted),
            Paragraph("Provides clear visual feedback during multi-modal scanning, demonstrating the 4-phase verification sequence.", body_muted)
        ],
        [
            Paragraph("<b>Side-by-Side Diff Engine</b>", body_bold),
            Paragraph("• Real-time red/green diff preview container.<br/>"
                      "• 1-Click Fix remediation flashes updated text with dark-mode emerald glow.<br/>"
                      "• Dedicated 'Copy Snippet', 'Copy Clean Copy', and 'Export (.txt)' actions.", body_muted),
            Paragraph("Empowers copywriters to review exact textual changes instantly and copy certified copy into their marketing tools.", body_muted)
        ]
    ]
    t_uispecs = Table(ui_specs, colWidths=[105, 235, 192])
    t_uispecs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_uispecs)
    story.append(Spacer(1, 6))

    # Design System Tokens Box
    token_box = [
        [
            Paragraph("<b>DESIGN SYSTEM TOKENS & ACCESSIBILITY SPECIFICATIONS</b>", card_title)
        ],
        [
            Paragraph("• <b>Surface Colors:</b> Deep Obsidian (<code>#0B132B</code>), Card Surface (<code>#1E293B</code>), Command Border (<code>#334155</code>).<br/>"
                      "• <b>Role Accents:</b> Client/Cyan (<code>#0EA5E9</code>), Reviewer/Amber (<code>#F59E0B</code>), Admin/Crimson (<code>#EF4444</code>), Success/Emerald (<code>#10B981</code>).<br/>"
                      "• <b>Typography:</b> Inter UI & JetBrains Mono for cryptographic hashes, code snippets, and timestamps.<br/>"
                      "• <b>Accessibility Compliance:</b> Satisfies WCAG 2.1 AA with minimum 4.5:1 text-to-background contrast across all dark surfaces.", body_muted)
        ]
    ]
    t_tok = Table(token_box, colWidths=[532])
    t_tok.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_CYAN)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tok)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CHAPTER 6: RELATIONAL SCHEMA, APIS & TESTING MATRIX
    # =========================================================================
    story.append(Paragraph("CHAPTER 6", eyebrow))
    story.append(Paragraph("6. Relational Data Model, REST APIs & Verification", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("<b>6.1 Relational Database Schema:</b> BrandGuard AI operates on a relational schema in SQLite / PostgreSQL via SQLAlchemy ORM:", body))

    model_summary = [
        [
            Paragraph("<b>MODEL</b>", eyebrow),
            Paragraph("<b>COLUMNS / ATTRIBUTES</b>", eyebrow),
            Paragraph("<b>PURPOSE & INTEGRITY</b>", eyebrow)
        ],
        [
            Paragraph("<code>User</code>", body_bold),
            Paragraph("id, name, email, password_hash, role (CREATOR, REVIEWER, ADMIN), department, organization, firebase_uid", code_style),
            Paragraph("Multi-portal identity; restricts sole admin privileges strictly to aman@synapse.ai.", body_muted)
        ],
        [
            Paragraph("<code>BrandGuideline</code>", body_bold),
            Paragraph("id, rule_code, category, rule_title, rule_description, severity, forbidden_patterns, citation_ref", code_style),
            Paragraph("Version-controlled brand rulebook; feeds regex and NLP calibration engines.", body_muted)
        ],
        [
            Paragraph("<code>ApprovedFact</code>", body_bold),
            Paragraph("id, topic, claim_statement, approved_source_link, evidence_excerpt, expiration_date, is_active", code_style),
            Paragraph("SQL Truth Bank cross-referenced for FTC Section 5 claim validation.", body_muted)
        ],
        [
            Paragraph("<code>Submission</code>", body_bold),
            Paragraph("id, title, content_type, raw_content, original_content, file_path, creator_id, reviewer_id, status, scores", code_style),
            Paragraph("Core lifecycle entity tracking status from Draft through Approved.", body_muted)
        ],
        [
            Paragraph("<code>EvaluationFlag</code>", body_bold),
            Paragraph("id, submission_id, guideline_id, flag_type, flagged_snippet, explanation, suggested_fix, status, reason", code_style),
            Paragraph("Actionable diagnostic items driving 1-click remediation and justifications.", body_muted)
        ],
        [
            Paragraph("<code>ReviewLog</code>", body_bold),
            Paragraph("id, submission_id, actor_id, action, comment, timestamp", code_style),
            Paragraph("Immutable audit trail logging every human and system transaction.", body_muted)
        ]
    ]
    t_models = Table(model_summary, colWidths=[90, 240, 202])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 6))

    # REST APIs Table
    api_summary = [
        [
            Paragraph("<b>HTTP METHOD / ROUTE</b>", eyebrow),
            Paragraph("<b>REQUEST / PAYLOAD</b>", eyebrow),
            Paragraph("<b>RESPONSE / ROLE ACCESS</b>", eyebrow)
        ],
        [
            Paragraph("<code>POST /scanner/api/quick-scan</code>", code_style),
            Paragraph("<code>{content: string, type: 'text'}</code>", code_style),
            Paragraph("Returns health score, tone breakdown, flags, and suggested fixes.", body_muted)
        ],
        [
            Paragraph("<code>POST /auth/api/firebase-sync</code>", code_style),
            Paragraph("<code>{idToken, email, name, role}</code>", code_style),
            Paragraph("Verifies Firebase JWT; establishes authenticated Flask session.", body_muted)
        ],
        [
            Paragraph("<code>POST /reviews/api/take-action</code>", code_style),
            Paragraph("<code>{sub_id, action: 'APPROVE', notes}</code>", code_style),
            Paragraph("Executes stage-gate transition; generates SHA-256 PDF certificate.", body_muted)
        ],
        [
            Paragraph("<code>GET /reviews/certificate/&lt;id&gt;</code>", code_style),
            Paragraph("None (Session Authenticated)", code_style),
            Paragraph("Streams compiled cryptographic PDF certificate (application/pdf).", body_muted)
        ]
    ]
    t_apis = Table(api_summary, colWidths=[140, 180, 212])
    t_apis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_apis)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>6.2 Comprehensive Automated Test Suite (32/32 Passing - 100%):</b> Verified by 32 automated integration tests across three suites: <code>test_complete_suite.py</code> (12 tests covering engines, route guards, sole admin lock, lifecycle, and rule CRUD), <code>test_portals_auth.py</code> (10 tests covering dynamic navbars, Firebase sync, and RBAC cross-portal blocks), and <code>test_ai_features.py</code> (10 tests covering neural semantic harmonization, FTC safe harbor synthesis, AI chat advisory, and rule synthesis).", body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 7: CLOUD DEPLOYMENT & FINAL SUMMARY
    # =========================================================================
    story.append(Paragraph("CHAPTER 7", eyebrow))
    story.append(Paragraph("7. Cloud Deployment, Verification & Final Summary", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    deploy_info = [
        [
            Paragraph("<b>PRODUCTION CLOUD DEPLOYMENT (RENDER LIVE PLATFORM)</b>", card_title)
        ],
        [
            Paragraph("• <b>Live Web Service:</b> Publicly hosted and active at <b>https://brandgovernanceai.onrender.com</b>.<br/>"
                      "• <b>Production WSGI Server:</b> High-concurrency Gunicorn engine configured via <code>gunicorn.conf.py</code>, <code>render.yaml</code>, and <code>Procfile</code>, binding dynamically to <code>0.0.0.0:$PORT</code>.<br/>"
                      "• <b>Health Monitoring:</b> Dedicated <code>/healthz</code> endpoint returning HTTP 200 OK for continuous uptime and load balancing.<br/>"
                      "• <b>Automated CI/CD:</b> Continuous integration pipeline connected directly to GitHub repository <b>CodingWithAman1/BrandGovernanceAI</b> on branch <b>main</b>.", body_muted)
        ]
    ]
    t_dinfo = Table(deploy_info, colWidths=[532])
    t_dinfo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_BLUE)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_dinfo)
    story.append(Spacer(1, 6))

    # Hackathon Deliverable Checklist
    chk_items = [
        [
            Paragraph("<b>EVALUATION CRITERION</b>", eyebrow),
            Paragraph("<b>ENGINEERING DELIVERABLE</b>", eyebrow),
            Paragraph("<b>VERIFICATION STATUS</b>", eyebrow)
        ],
        [
            Paragraph("<b>Multi-Modal Governance</b>", body_bold),
            Paragraph("Tone polarity regex, FTC truth bank cross-checking, and OpenCV WCAG 2.1 AA contrast scoring.", body_muted),
            Paragraph("<font color='#059669'><b>100% COMPLETE</b></font>", body_bold)
        ],
        [
            Paragraph("<b>Isolated Portals & RBAC</b>", body_bold),
            Paragraph("3 isolated portals (Client, Reviewer, Admin), Flask-Login route guards, and Sole Admin Lock.", body_muted),
            Paragraph("<font color='#059669'><b>100% COMPLETE</b></font>", body_bold)
        ],
        [
            Paragraph("<b>Stage-Gate HITL Pipeline</b>", body_bold),
            Paragraph("Reviewer Desk, side-by-side diffs, exception justifications, and SHA-256 PDF certificates.", body_muted),
            Paragraph("<font color='#059669'><b>100% COMPLETE</b></font>", body_bold)
        ],
        [
            Paragraph("<b>Obsidian Cyber UI & FX</b>", body_bold),
            Paragraph("Dual cyber cursor (lerp physics), ambient particle canvas, and Laser Scanner HUD modal.", body_muted),
            Paragraph("<font color='#059669'><b>100% COMPLETE</b></font>", body_bold)
        ],
        [
            Paragraph("<b>Automated Test Matrix</b>", body_bold),
            Paragraph("32 comprehensive integration tests spanning all engines, AI Co-Pilot, security rules, and workflows.", body_muted),
            Paragraph("<font color='#059669'><b>32/32 PASSING (100%)</b></font>", body_bold)
        ]
    ]
    t_chk = Table(chk_items, colWidths=[120, 292, 120])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_chk)
    story.append(Spacer(1, 6))

    # Team Closing Card
    team_closing = [
        [
            Paragraph("<b>SUBMISSION CREDITS • TEAM SYNAPSE</b>", eyebrow)
        ],
        [
            Paragraph("<b>Inkloom AI Hackathon • Round 1: Master Architecture Plan</b>", card_title)
        ],
        [
            Paragraph("<b>Aman Sharma</b> — Team Leader & Full-Stack / Backend Lead (aman@synapse.ai)<br/>"
                      "<b>Janhavi Kanojia</b> — Frontend & UI/UX Developer (janhavi@synapse.ai)", body_bold)
        ],
        [
            Paragraph("BrandGuard AI transitions enterprise brand governance from a slow, bureaucratic roadblock into an intelligent, real-time advisory co-pilot. By unifying linguistic polarity checks, FTC claim verification, accessibility inspections, and cryptographic certification into three dedicated role portals, BrandGuard AI ensures that every piece of published content is verifiable, compliant, and on-brand.", body_style)
        ],
        [
            Spacer(1, 3)
        ],
        [
            Table([
                [
                    Paragraph("<b>GitHub Repository:</b><br/><font color='#0284C7'>https://github.com/CodingWithAman1/BrandGovernanceAI.git</font>", body_muted),
                    Paragraph("<b>Live Cloud Application:</b><br/><font color='#0284C7'>https://brandgovernanceai.onrender.com</font>", body_muted)
                ]
            ], colWidths=[266, 266], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
                ('PADDING', (0,0), (-1,-1), 6),
            ])
        ]
    ]
    t_team = Table(team_closing, colWidths=[532])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_team)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvasPortrait)
    print(f"[+] Successfully generated technical project report PDF: {output_filename}")


if __name__ == "__main__":
    build_project_report_pdf()
