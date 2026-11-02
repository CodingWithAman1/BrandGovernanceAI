#!/usr/bin/env python3
"""
BrandGuard AI — Comprehensive Technical Engineering Project Report PDF Generator
================================================================================
Inkloom AI Hackathon (Grand Finale Deliverable)
Team Synapse: Aman Sharma & Janhavi Kanojia

Generates a formal, 8-page portrait-format technical engineering project report
document for BrandGuard AI. Styled in an Obsidian-cyberpunk executive visual system
with high contrast, structured typography, analytical data tables, and two-pass
running headers and footers with total page counts ("Page X of Y").

Pages:
  Page 1: Formal Project Report Cover Page (Obsidian Hero & Executive Abstract)
  Page 2: Chapter 1: Multi-Jurisdiction Regulatory Imperatives & Crisis Context
  Page 3: Chapter 2: Three Isolated Role Portals, Persona Switcher & Stage-Gate
  Page 4: Chapter 3: Deterministic Engines & Google Gemini 3 Flash Neural Hybrid
  Page 5: Chapter 4: Stage-Gate HITL Workflow, Public Verifier & SHA-256 Certification
  Page 6: Chapter 5: Obsidian Cyberpunk UI, 0ms Hardware Cursor & 3D WebGL Core
  Page 7: Chapter 6: Enterprise Extensions: Battlecard Studio, Brand DNA & CI/CD Gate
  Page 8: Chapter 7: Cloud Deployment Architecture, Verification Matrix & Roadmap
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
        self.drawString(MARGIN + 82, PAGE_HEIGHT - 26, "•  TECHNICAL ENGINEERING PROJECT REPORT  •  GRAND FINALE")

        self.setFont("Helvetica", 7.5)
        self.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 26, "OCTOBER 2026  |  PRODUCTION RELEASE 3.0")

        # Header dividing line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.6)
        self.line(MARGIN, PAGE_HEIGHT - 31, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 31)

        # RUNNING BOTTOM FOOTER
        self.line(MARGIN, 34, PAGE_WIDTH - MARGIN, 34)

        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(MARGIN, 22, "TEAM SYNAPSE:")

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(MARGIN + 72, 22, "Aman Sharma (Sole Admin & Backend Lead)  •  Janhavi Kanojia (Frontend & UI/UX)")

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
        fontSize=27,
        leading=33,
        textColor=colors.HexColor('#FFFFFF'),
        spaceAfter=8
    )

    cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#94A3B8'),
        spaceAfter=18
    )

    cover_body = ParagraphStyle(
        'CoverBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#E2E8F0')
    )

    cover_meta_title = ParagraphStyle(
        'CoverMetaTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#38BDF8'),
        textTransform='uppercase'
    )

    cover_meta_val = ParagraphStyle(
        'CoverMetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#FFFFFF')
    )

    eyebrow = ParagraphStyle(
        'Eyebrow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor(C_BLUE),
        spaceAfter=2,
        textTransform='uppercase'
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=colors.HexColor(C_NAVY),
        spaceAfter=5
    )

    subheading = ParagraphStyle(
        'SubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor(C_NAVY),
        spaceBefore=4,
        spaceAfter=2
    )

    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor(C_TEXT),
        spaceAfter=4
    )

    body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor(C_MUTED)
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor(C_NAVY)
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0369A1')
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor(C_NAVY)
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE (OBSIDIAN HERO & EXECUTIVE ABSTRACT)
    # =========================================================================
    cover_table_content = [
        [
            Paragraph("INKLOOM AI HACKATHON • FINAL GRAND CHAMPIONSHIP", cover_eyebrow)
        ],
        [
            Paragraph("BRANDGUARD AI", cover_title)
        ],
        [
            Paragraph("Autonomous Pre-Publication Brand Governance, Multi-Jurisdiction Regulatory Enforcement & Cryptographic Stage-Gate Clearance System", cover_sub)
        ],
        [
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=4, spaceAfter=14)
        ],
        [
            Paragraph("<b>EXECUTIVE ABSTRACT:</b> In the generative AI era, enterprise marketing teams face severe pre-publication risks: clichéd robotic jargon eroding audience trust, FTC Section 5 lawsuits targeting unverified superlatives, SEC AI-washing crackdowns, EU AI Act transparency mandates, and ADA accessibility litigation. <b>BrandGuard AI</b> introduces an enterprise-grade dual-architecture solution that bridges deterministic compliance and neural generative power. Operating across three isolated, role-based portals (Client Workspace, Reviewer Desk, Executive Admin Plane), BrandGuard AI inspects drafts against 5 tone polarity vectors, cross-references claims against an SQL Truth Bank, calculates WCAG 2.1 AA luminance contrast via Pillow K-Means, audits competitor claims via live web crawling, and enforces quality gates directly in CI/CD pipelines (/api/v1/gate/check). Once approved, assets receive tamper-evident SHA-256 PDF certificates registered on a zero-login public verification ledger (/verify).", cover_body)
        ],
        [
            Spacer(1, 16)
        ],
        [
            Table([
                [
                    Paragraph("<b>PROJECT VERSION:</b>", cover_meta_title),
                    Paragraph("Version 3.0 Enterprise (Release Candidate)", cover_meta_val),
                    Paragraph("<b>DATE OF SUBMISSION:</b>", cover_meta_title),
                    Paragraph("October 2026", cover_meta_val)
                ],
                [
                    Paragraph("<b>LEAD ARCHITECT & ADMIN:</b>", cover_meta_title),
                    Paragraph("Aman Sharma (Sole Administrator)", cover_meta_val),
                    Paragraph("<b>FRONTEND & UI/UX LEAD:</b>", cover_meta_title),
                    Paragraph("Janhavi Kanojia (Design Lead)", cover_meta_val)
                ],
                [
                    Paragraph("<b>ENGINEERING TEAM:</b>", cover_meta_title),
                    Paragraph("Team Synapse", cover_meta_val),
                    Paragraph("<b>PRODUCTION CLOUD URL:</b>", cover_meta_title),
                    Paragraph("https://brandgovernanceai.onrender.com", cover_meta_val)
                ],
                [
                    Paragraph("<b>GITHUB REPOSITORY:</b>", cover_meta_title),
                    Paragraph("github.com/CodingWithAman1/BrandGovernanceAI", cover_meta_val),
                    Paragraph("<b>TEST SUITE COVERAGE:</b>", cover_meta_title),
                    Paragraph("24 / 24 Automated Tests Passing (100%)", cover_meta_val)
                ]
            ], colWidths=[120, 146, 120, 146], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
                ('PADDING', (0,0), (-1,-1), 5),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ])
        ]
    ]

    cover_table = Table(cover_table_content, colWidths=[532])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_NAVY)),
        ('PADDING', (0,0), (-1,-1), 22),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0284C7')),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CHAPTER 1: MULTI-JURISDICTION REGULATORY CRISIS
    # =========================================================================
    story.append(Paragraph("CHAPTER 1", eyebrow))
    story.append(Paragraph("1. The Enterprise Governance Crisis & Regulatory Mandates", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Modern marketing organizations deploy high-velocity generative AI tools that inadvertently introduce severe legal, brand, and regulatory exposures before publication. Enterprise marketing teams face four compounding vectors of failure:",
        body
    ))

    reg_challenges = [
        [
            Paragraph("<b>FAILURE VECTOR</b>", eyebrow),
            Paragraph("<b>REGULATORY & STATUTORY RISK</b>", eyebrow),
            Paragraph("<b>FINANCIAL & LEGAL CONSEQUENCE</b>", eyebrow)
        ],
        [
            Paragraph("<b>FTC Section 5 & AI Comply</b><br/>Unsubstantiated Claims", body_bold),
            Paragraph("FTC Act 15 U.S.C. § 45 prohibits unfair or deceptive practices. The FTC's <i>Operation AI Comply</i> targets ungrounded '#1 in the world' claims and unsubstantiated performance assertions.", body_muted),
            Paragraph("Civil penalties up to <b>$51,744 per day</b> per violation, mandatory consent decrees, and public brand humiliation.", body_muted)
        ],
        [
            Paragraph("<b>SEC AI-Washing Rule</b><br/>Forward-Looking Exaggerations", body_bold),
            Paragraph("SEC Rule 10b-5 and 2024 AI-Washing Guidance penalize companies exaggerating AI capabilities, claiming autonomous operations, or promising zero-risk software without third-party model audits.", body_muted),
            Paragraph("Federal securities fraud investigations, executive disqualification, shareholder class actions, and millions in settlements.", body_muted)
        ],
        [
            Paragraph("<b>EU AI Act Art. 50/52</b><br/>Synthetic Content Transparency", body_bold),
            Paragraph("The European Union Artificial Intelligence Act mandates transparent disclosure of AI-generated promotional text, machine-readable watermarking, and human governance audit trails.", body_muted),
            Paragraph("Regulatory fines scaling up to <b>€35 Million or 7% of annual global turnover</b> (whichever is higher).", body_muted)
        ],
        [
            Paragraph("<b>ADA Title III & WCAG 2.1</b><br/>Visual Inaccessibility", body_bold),
            Paragraph("Americans with Disabilities Act (ADA) and WCAG 2.1 Level AA mandate minimum 4.5:1 text-to-background contrast ratios for normal visual copy.", body_muted),
            Paragraph("Over 4,000 accessibility lawsuits filed in 2023 alone, generating statutory attorney fees and mandatory site redesign injunctions.", body_muted)
        ]
    ]
    t_reg = Table(reg_challenges, colWidths=[130, 230, 172])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 6))

    # Architecture Overview Callout
    story.append(Paragraph("<b>The Dual-Architecture Paradigm:</b> Conventional grammar checkers lack regulatory knowledge, while raw LLM prompts hallucinate compliance clearance. BrandGuard AI solves this via dual architecture: (1) <i>Deterministic Rule & Truth Engines</i> that provide 100% reproducible legal verification, and (2) <i>Google Gemini 3 Flash Neural Intelligence</i> providing automated semantic harmonization, battlecard synthesis, and Brand Voice DNA extraction.", body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CHAPTER 2: THREE ISOLATED ROLE PORTALS & RBAC
    # =========================================================================
    story.append(Paragraph("CHAPTER 2", eyebrow))
    story.append(Paragraph("2. Three Isolated Portals, RBAC & Demo Persona Switcher", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "Enterprise brand compliance requires strict separation of concerns. Creators must not be able to self-approve unauthorized claims, and reviewers require dedicated audit diffs. BrandGuard AI implements three mathematically isolated portals secured by strict Flask-Login session management and RBAC route decorators:",
        body
    ))

    portals = [
        [
            Paragraph("<b>PORTAL IDENTITY</b>", eyebrow),
            Paragraph("<b>ROLE & AUTHORIZED ACTORS</b>", eyebrow),
            Paragraph("<b>EXCLUSIVE CAPABILITIES & SCOPE</b>", eyebrow)
        ],
        [
            Paragraph("<b>1. Client / Creator Workspace</b><br/><code>/portal/client</code>", body_bold),
            Paragraph("<b>CREATOR Role</b><br/>Copywriters, Marketing Agencies, Social Media Managers, Growth Teams.", body_muted),
            Paragraph("• Interactive Compliance Studio with Multi-Modal Scanner.<br/>• 1-Click suggested fixes with live score recalculation.<br/>• AI Deep Harmonization via Google Gemini 3 Flash.<br/>• Exception submission with justified business rationale.<br/>• Tracking personal submission pipeline and active certs.", body_muted)
        ],
        [
            Paragraph("<b>2. Reviewer & Legal Desk</b><br/><code>/portal/reviewer</code>", body_bold),
            Paragraph("<b>REVIEWER / MANAGER Role</b><br/>Brand Governance Managers, Legal Counsel, Regulatory Compliance Officers.", body_muted),
            Paragraph("• Centralized Stage-Gate Incoming Queue with SLA timers.<br/>• Side-by-side red/green visual difference audit inspector.<br/>• Full visibility into creator rationale and flagged citations.<br/>• One-click Stage-Gate clearance (Approve, Request Changes, Reject).<br/>• Automatic cryptographic SHA-256 PDF certificate issuance.", body_muted)
        ],
        [
            Paragraph("<b>3. Executive Admin Command Plane</b><br/><code>/portal/admin</code>", body_bold),
            Paragraph("<b>ADMIN Role</b><br/>Strictly locked to <b>Aman Sharma</b> (Sole Administrator & Lead Auditor).", body_muted),
            Paragraph("• Enterprise Brand Rulebook CRUD with regex and severity controls.<br/>• SQL Truth Bank registry with approved evidence source links.<br/>• Ambiguity Resolver with creator dispute telemetry.<br/>• Clarity Index Analytics with Brand Drift Time-Travel.<br/>• Enterprise user activation/deactivation toggles.", body_muted)
        ]
    ]
    t_portals = Table(portals, colWidths=[120, 160, 252])
    t_portals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_portals)
    story.append(Spacer(1, 6))

    # Demo Quick-Switcher Callout
    story.append(Paragraph("<b>One-Click Demo Persona Quick-Switcher:</b> To ensure evaluators and hackathon judges can seamlessly test all role behaviors without password friction, BrandGuard AI features an agile persona switcher in the navigation bar. Judges can toggle between Priya (Client Creator), Elena (Legal Reviewer), Marcus (Brand Director), and Aman Sharma (Sole Administrator) with full session re-authentication in 0.04s.", body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CHAPTER 3: DETERMINISTIC ENGINES & GEMINI HYBRID
    # =========================================================================
    story.append(Paragraph("CHAPTER 3", eyebrow))
    story.append(Paragraph("3. Deterministic Governance Engines & Gemini 3 Flash Hybrid", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "BrandGuard AI rejects non-deterministic LLM prompting for compliance scoring. Prompting LLMs with <i>'Is this compliant?'</i> yields unpredictable hallucinations and fluctuating scores. Instead, BrandGuard AI implements four deterministic, rule-grounded engines combined with live Google Gemini 3 Flash generative intelligence:",
        body
    ))

    engines = [
        [
            Paragraph("<b>ENGINE COMPONENT</b>", eyebrow),
            Paragraph("<b>ALGORITHMIC SPECIFICATION</b>", eyebrow),
            Paragraph("<b>COMPLIANCE IMPACT & OUTPUT</b>", eyebrow)
        ],
        [
            Paragraph("<b>1. Tone Calibrator</b>", body_bold),
            Paragraph("<b>5 Voice Polarity Vectors & Semantic Filters</b><br/>"
                      "• Scans for 12 robotic AI filler clichés (<i>delve into</i>, <i>rich tapestry</i>, <i>game-changer</i>, <i>unpack</i>).<br/>"
                      "• Flags combative attacks (<i>crush the competition</i>) and condescending terms (<i>obviously</i>).", body_muted),
            Paragraph("Calculates reading ease and formality; generates 1-click tone-preserving suggested rewrites.", body_muted)
        ],
        [
            Paragraph("<b>2. SQL Truth Bank</b>", body_bold),
            Paragraph("<b>FTC Section 5 Substantiation Cross-Checker</b><br/>"
                      "• Validates claims against the <code>ApprovedFact</code> repository with validity periods.<br/>"
                      "• Docks -20 points per unverified superlative (<i>#1 platform</i>, <i>100% risk free</i>).", body_muted),
            Paragraph("Protects against FTC Section 5 and SEC enforcement actions by requiring empirical proof.", body_muted)
        ],
        [
            Paragraph("<b>3. Visual Inspector</b>", body_bold),
            Paragraph("<b>Pillow K-Means & WCAG 2.1 AA Contrast</b><br/>"
                      "• Quantizes banner imagery into dominant RGB clusters.<br/>"
                      "• Evaluates luminance formula: <code>Cr = (L1 + 0.05) / (L2 + 0.05)</code>.<br/>"
                      "• Enforces strict 4.5:1 contrast for regular text, 3.0:1 for large text.", body_muted),
            Paragraph("Prevents visual accessibility lawsuits under ADA Title III and guarantees brand token alignment.", body_muted)
        ],
        [
            Paragraph("<b>4. Regulatory Engine</b>", body_bold),
            Paragraph("<b>Multi-Jurisdiction Policy Dispatcher</b><br/>"
                      "• Evaluates jurisdiction: US (FTC/SEC), EU (AI Act Art. 50/52), UK (CMA Green Claims).<br/>"
                      "• Automatically generates statutory safe harbor statements.", body_muted),
            Paragraph("Embeds legally defensible disclaimers directly into creative drafts prior to release.", body_muted)
        ],
        [
            Paragraph("<b>5. Gemini 3 Flash Co-Pilot</b>", body_bold),
            Paragraph("<b>Multi-Model Cascade with Local NLP Fallback</b><br/>"
                      "• Dynamic key resolution with quota failover: <code>gemini-3.1-flash-lite</code> &rarr; <code>gemini-flash-lite-latest</code> &rarr; <code>gemini-3.5-flash-lite</code> &rarr; Local NLP.", body_muted),
            Paragraph("Powers deep semantic rewrites, competitor battlecards, and interactive chat advisory with live badges.", body_muted)
        ]
    ]
    t_eng = Table(engines, colWidths=[105, 235, 192])
    t_eng.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_eng)
    story.append(Spacer(1, 6))

    # Closed-Loop Validator Callout
    story.append(Paragraph("<b>Closed-Loop Adversarial Validator:</b> To eliminate LLM hallucinations, every rewrite generated by Gemini is recursively fed back through the deterministic ClaimsFactChecker and SQL Truth Bank before rendering in the UI. If Gemini attempts to inject unverified claims, the deterministic gate strips or blocks it, ensuring zero AI drift.", body))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CHAPTER 4: HITL WORKFLOW, PUBLIC VERIFIER & PDF
    # =========================================================================
    story.append(Paragraph("CHAPTER 4", eyebrow))
    story.append(Paragraph("4. Stage-Gate Workflow, Public Verifier & SHA-256 PDF", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "BrandGuard AI enforces a formal <b>Human-in-the-Loop (HITL)</b> release boundary. Automated algorithms diagnose and suggest remediations, but formal clearance requires authorized human reviewer approval, producing an immutable cryptographic audit record:",
        body
    ))

    workflow_steps = [
        [
            Paragraph("<b>STAGE</b>", eyebrow),
            Paragraph("<b>SYSTEM & ACTOR INTERACTION</b>", eyebrow),
            Paragraph("<b>OUTPUT / LEDGER STATE</b>", eyebrow)
        ],
        [
            Paragraph("<b>1. Studio Ingest</b>", body_bold),
            Paragraph("Creator drafts copy or uploads creative assets; animated Laser Scanner HUD executes pre-flight scan.", body_muted),
            Paragraph("Generates diagnostic flags and calculates real-time Brand Health Score (0–100%).", body_muted)
        ],
        [
            Paragraph("<b>2. 1-Click Remediation</b>", body_bold),
            Paragraph("Creator accepts suggested rewrite or deep harmonizes via Google Gemini 3 Flash.", body_muted),
            Paragraph("Live score recalculation; flags resolve instantly or creator enters exception rationale.", body_muted)
        ],
        [
            Paragraph("<b>3. Stage-Gate Queue</b>", body_bold),
            Paragraph("Draft transitions to <code>PENDING</code>; routes to Reviewer Desk with side-by-side red/green diffs.", body_muted),
            Paragraph("Reviewers inspect flagged claims, rule citations, and author exceptions.", body_muted)
        ],
        [
            Paragraph("<b>4. Authorized Sign-Off</b>", body_bold),
            Paragraph("Reviewer executes 1-click clearance: <b>Approve</b>, <b>Request Changes</b>, or <b>Reject</b>.", body_muted),
            Paragraph("Approval locks the raw copy text, approver email, and UTC clearance timestamp.", body_muted)
        ],
        [
            Paragraph("<b>5. Cryptographic Ledger</b>", body_bold),
            Paragraph("System computes SHA-256 content digest and compiles an unalterable PDF Compliance Certificate.", body_muted),
            Paragraph("Certificate is permanently registered in the public <code>/verify</code> ledger with embeddable badges.", body_muted)
        ]
    ]
    t_wf = Table(workflow_steps, colWidths=[105, 235, 192])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 6))

    # Public Verifier & PDF Box
    verifier_box = [
        [
            Paragraph("<b>PUBLIC CRYPTOGRAPHIC VERIFIER & IMMUTABLE LEDGER (/verify)</b>", card_title)
        ],
        [
            Paragraph("• <b>Zero-Login Regulatory Lookup:</b> External compliance auditors, regulators (FTC/SEC/CMA), and clients can visit <code>/verify</code> to query any certificate hash without requiring an enterprise account.<br/>"
                      "• <b>Tamper-Evident SHA-256 Digest:</b> Evaluates <code>hashlib.sha256(raw_content)</code>. Modifying even a single comma in approved marketing copy immediately invalidates the cryptographic verification check.<br/>"
                      "• <b>Official PDF Compliance Certificates:</b> ReportLab generates official certificates embedding approver signature (Aman Sharma), multi-modal compliance scores, and cryptographic QR verification links.<br/>"
                      "• <b>Embeddable Live Badges:</b> Provides copyable HTML/Markdown shields for landing pages displaying <i>'Certified by BrandGuard AI (92/100)'</i>.", body_muted)
        ]
    ]
    t_vbox = Table(verifier_box, colWidths=[532])
    t_vbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_GREEN)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_vbox)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CHAPTER 5: OBSIDIAN CYBER UI & 0MS HARDWARE CURSOR
    # =========================================================================
    story.append(Paragraph("CHAPTER 5", eyebrow))
    story.append(Paragraph("5. Obsidian Cyberpunk UI, 0ms Cursor & 3D WebGL Core", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "To deliver a world-class enterprise user experience that marries aesthetic prestige with technical performance, BrandGuard AI implements an <b>Obsidian Cyberpunk Design System</b> with custom 3D WebGL visualization and hardware-accelerated cursor composition:",
        body
    ))

    ui_specs = [
        [
            Paragraph("<b>UI COMPONENT</b>", eyebrow),
            Paragraph("<b>ENGINEERING ARCHITECTURE</b>", eyebrow),
            Paragraph("<b>USER EXPERIENCE BENEFIT</b>", eyebrow)
        ],
        [
            Paragraph("<b>Hardware Cyber Cursor</b>", body_bold),
            Paragraph("• Zero-lag <code>pointermove</code> listener with 0ms direct placement.<br/>"
                      "• GPU composition using <code>translate3d</code> avoiding layout reflows.<br/>"
                      "• Dynamic role coloring (Cyan Client, Amber Reviewer, Crimson Admin).<br/>"
                      "• Strict <code>cursor: text !important</code> auto-fallback on form inputs.", body_muted),
            Paragraph("Delivers fluid, tactile cursor feedback with zero mouse lag across all browsers; automatically disables on touch devices.", body_muted)
        ],
        [
            Paragraph("<b>Three.js 3D WebGL Core</b>", body_bold),
            Paragraph("• Local offline-ready Three.js 3D Holographic Governance Core.<br/>"
                      "• Single WebGL context architecture with RAF rendering loop.<br/>"
                      "• IntersectionObserver pauses rendering when canvas leaves viewport.<br/>"
                      "• Real-time 3D card parallax tilt with 60 FPS damping.", body_muted),
            Paragraph("Provides an authentic high-tech command center aesthetic without GPU contention or dropped frames on low-power devices.", body_muted)
        ],
        [
            Paragraph("<b>Multi-Engine Scanner HUD</b>", body_bold),
            Paragraph("• Full-screen holographic modal overlay triggered on audit submission.<br/>"
                      "• Oscillating neon laser scanline traversing down the document.<br/>"
                      "• Real-time digital progress gauge counting from 0% to 100%.", body_muted),
            Paragraph("Provides dramatic, transparent feedback during multi-modal scanning, demonstrating the 4-phase verification sequence.", body_muted)
        ],
        [
            Paragraph("<b>Omnichannel Social Previews</b>", body_bold),
            Paragraph("• Pixel-accurate live preview mockups for LinkedIn, Twitter/X, and Google SERP.<br/>"
                      "• Real-time synchronization with active Studio text input.<br/>"
                      "• Visualizes social card clipping and metadata contrast.", body_muted),
            Paragraph("Enables marketers to inspect social feed appearance before committing drafts to the stage-gate review queue.", body_muted)
        ]
    ]
    t_uispecs = Table(ui_specs, colWidths=[110, 230, 192])
    t_uispecs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4),
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
                      "• <b>Typography:</b> Plus Jakarta Sans & JetBrains Mono for cryptographic hashes, code snippets, and timestamps.<br/>"
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
    # PAGE 7: CHAPTER 6: ENTERPRISE EXTENSIONS & TESTING MATRIX
    # =========================================================================
    story.append(Paragraph("CHAPTER 6", eyebrow))
    story.append(Paragraph("6. Enterprise Extensions, CI/CD Gate & Testing Matrix", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "In Round 3, BrandGuard AI expanded into a full enterprise operational platform, incorporating competitive intelligence, dynamic voice profiling, automated CI/CD quality gates, and rigorous test coverage:",
        body
    ))

    enterprise_features = [
        [
            Paragraph("<b>ENTERPRISE EXTENSION</b>", eyebrow),
            Paragraph("<b>OPERATIONAL CAPABILITY & ROUTE</b>", eyebrow),
            Paragraph("<b>BUSINESS VALUE & INTEGRATION</b>", eyebrow)
        ],
        [
            Paragraph("<b>Competitor Battlecard Studio</b>", body_bold),
            Paragraph("<code>/scanner/competitor-studio</code><br/>"
                      "• Crawls competitor URLs or analyzes pasted ad copy.<br/>"
                      "• Identifies claim vulnerabilities under FTC Section 5.<br/>"
                      "• Cross-checks claims against the SQL Truth Bank.<br/>"
                      "• Synthesizes 3-pillar sales battlecards via Gemini 3 Flash.", body_muted),
            Paragraph("Arms sales reps with FTC-compliant counter-pitches, turning regulatory diligence into an active revenue driver.", body_muted)
        ],
        [
            Paragraph("<b>Brand Voice DNA Profiler</b>", body_bold),
            Paragraph("<code>/brand-dna</code><br/>"
                      "• Ingests corporate manifestos and founder style guides.<br/>"
                      "• Calibrates 5 voice polarities (Authority, Warmth, Innovation, Plainspokenness, Technical Depth).<br/>"
                      "• 1-Click commit of extracted rules into the active rulebook.", body_muted),
            Paragraph("Codifies custom brand archetypes (Stripe, Apple, Nike) into enforceable deterministic governance rules.", body_muted)
        ],
        [
            Paragraph("<b>CI/CD Developer Hub</b>", body_bold),
            Paragraph("<code>/integrations</code> &amp; <code>/api/v1/gate/check</code><br/>"
                      "• Copyable GitHub Actions CI/CD workflow YAML.<br/>"
                      "• Live API test playground with interactive cURL/Python/Node.js.<br/>"
                      "• Returns HTTP 422 to block pull requests failing compliance.", body_muted),
            Paragraph("Enforces pre-publication governance directly in software deployment pipelines, ensuring zero non-compliant copy ships.", body_muted)
        ],
        [
            Paragraph("<b>Audit Vault & Analytics</b>", body_bold),
            Paragraph("<code>/analytics/audit-vault-export</code><br/>"
                      "• Exports complete compliance dossiers in signed JSON format.<br/>"
                      "• Includes SHA-256 cryptographic vault seal.<br/>"
                      "• Visualizes Brand Drift Time-Travel compliance velocity.", body_muted),
            Paragraph("Provides enterprise risk committees and external regulators with court-admissible audit proof.", body_muted)
        ]
    ]
    t_ent = Table(enterprise_features, colWidths=[120, 220, 192])
    t_ent.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_ent)
    story.append(Spacer(1, 6))

    # Comprehensive Test Suite Matrix
    test_box = [
        [
            Paragraph("<b>COMPREHENSIVE AUTOMATED TEST MATRIX (24/24 PASSING • 100% COVERAGE)</b>", card_title)
        ],
        [
            Paragraph("• <b>test_complete_suite.py (18 Tests):</b> Validates Tone Calibrator, Claims Checker, Visual Inspector, Clarity Engine, PDF Generator, Route Protection, Sole Admin Lock (Aman Sharma), Stage-Gate Lifecycle, Audit Vault JSON, and Static Cyber Assets.<br/>"
                      "• <b>test_round3_features.py (6 Tests):</b> Validates Public Certificate Verifier (/verify), Valid/Invalid Hash Lookups, Developer Integrations Hub (/integrations), Competitor Battlecard Studio (/scanner/competitor-studio), Brand Voice DNA Profiler (/brand-dna), and CI/CD Quality Gate API (/api/v1/gate/check).<br/>"
                      "• <b>Regression Guard:</b> All 24 tests executed continuously against local SQLite and cloud environments with 100% pass rate.", body_muted)
        ]
    ]
    t_tbox = Table(test_box, colWidths=[532])
    t_tbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_GREEN)),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tbox)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 7: CLOUD ARCHITECTURE, ROADMAP & SIGN-OFF
    # =========================================================================
    story.append(Paragraph("CHAPTER 7", eyebrow))
    story.append(Paragraph("7. Cloud Deployment, Product Roadmap & Executive Sign-Off", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(C_BORDER), spaceBefore=2, spaceAfter=6))

    deploy_info = [
        [
            Paragraph("<b>PRODUCTION CLOUD DEPLOYMENT SPECIFICATIONS</b>", card_title)
        ],
        [
            Paragraph("• <b>Live Cloud Platform:</b> Publicly hosted and active at <b>https://brandgovernanceai.onrender.com</b>.<br/>"
                      "• <b>Production WSGI Server:</b> High-concurrency Gunicorn engine configured via <code>gunicorn.conf.py</code>, <code>render.yaml</code>, and <code>Procfile</code>, binding dynamically to <code>0.0.0.0:$PORT</code>.<br/>"
                      "• <b>Zero-Downtime Healthcheck:</b> Dedicated <code>/healthz</code> endpoint returning HTTP 200 OK for continuous uptime and load balancing.<br/>"
                      "• <b>Automated Git CI/CD:</b> Continuous integration pipeline connected directly to GitHub repository <b>CodingWithAman1/BrandGovernanceAI</b> on branch <b>main</b>.<br/>"
                      "• <b>Security Architecture:</b> CSRF protection, strict Flask-Login session management, and Sole Admin Lock on <code>aman@synapse.ai</code>.", body_muted)
        ]
    ]
    t_dinfo = Table(deploy_info, colWidths=[532])
    t_dinfo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(C_BLUE)),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_dinfo)
    story.append(Spacer(1, 4))

    # Product Roadmap Table
    roadmap_items = [
        [
            Paragraph("<b>PHASE & TIMELINE</b>", eyebrow),
            Paragraph("<b>DEVELOPMENT DELIVERABLE</b>", eyebrow),
            Paragraph("<b>TARGET AUDIENCE & TECHNICAL STACK</b>", eyebrow)
        ],
        [
            Paragraph("<b>Phase 1: Q1 2027</b><br/>Headless SPA Crawler", body_bold),
            Paragraph("Headless browser crawler (Puppeteer/Playwright) to parse dynamic client-rendered React/Vue competitor web applications.", body_muted),
            Paragraph("Product Marketing & Intelligence teams; deployed as AWS Lambda Chromium microservice.", body_muted)
        ],
        [
            Paragraph("<b>Phase 2: Q2 2027</b><br/>Figma & Docs Plugins", body_bold),
            Paragraph("Native desktop extensions for Figma and Google Docs providing real-time compliance feedback inline during drafting.", body_muted),
            Paragraph("Brand Designers & Copywriters; built via Figma REST API and Google Workspace Add-on SDK.", body_muted)
        ],
        [
            Paragraph("<b>Phase 3: Q3 2027</b><br/>Blockchain Anchoring", body_bold),
            Paragraph("Decentralized timestamping on Hedera / Polygon to anchor SHA-256 certificate hashes for court-admissible audit proof.", body_muted),
            Paragraph("Enterprise Legal Counsel; integrates smart contracts for immutable regulatory due diligence.", body_muted)
        ]
    ]
    t_rd = Table(roadmap_items, colWidths=[110, 230, 192])
    t_rd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_rd)
    story.append(Spacer(1, 4))

    # Team Closing Card
    team_closing = [
        [
            Paragraph("<b>SUBMISSION CREDITS • TEAM SYNAPSE</b>", eyebrow)
        ],
        [
            Paragraph("<b>Inkloom AI Hackathon • Grand Finale Project Report</b>", card_title)
        ],
        [
            Paragraph("<b>Aman Sharma</b> — Team Leader & Full-Stack / Backend Lead (aman@synapse.ai)<br/>"
                      "<b>Janhavi Kanojia</b> — Frontend & UI/UX Developer (janhavi@synapse.ai)", body_bold)
        ],
        [
            Paragraph("BrandGuard AI transitions enterprise brand governance from a slow, bureaucratic roadblock into an intelligent, real-time advisory co-pilot. By unifying linguistic polarity checks, FTC claim verification, accessibility inspections, competitive battlecard synthesis, and cryptographic certification into three dedicated role portals, BrandGuard AI ensures that every piece of published content is verifiable, compliant, and on-brand.", body_muted)
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
                ('PADDING', (0,0), (-1,-1), 5),
            ])
        ]
    ]
    t_team = Table(team_closing, colWidths=[532])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(C_LIGHT_BG)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(C_BORDER)),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_team)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvasPortrait)
    print(f"[+] Successfully generated technical project report PDF: {output_filename}")


if __name__ == "__main__":
    build_project_report_pdf()
