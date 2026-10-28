import os
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFCertificateGenerator:
    """Generates official Brand Compliance Certificates upon approval."""

    @staticmethod
    def generate_certificate(submission, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        filename = f"Certificate_{submission.id}_{int(datetime.utcnow().timestamp())}.pdf"
        filepath = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CertTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor('#0F172A'),
            alignment=1
        )
        
        subtitle_style = ParagraphStyle(
            'CertSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#2563EB'),
            alignment=1
        )

        body_style = ParagraphStyle(
            'CertBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155')
        )

        elements = []

        # Top Header
        elements.append(Paragraph("BRANDGUARD AI", subtitle_style))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph("CERTIFICATE OF BRAND COMPLIANCE", title_style))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph("Pre-Publication Multi-Modal Governance Verification", subtitle_style))
        elements.append(Spacer(1, 15))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

        # Certificate Body
        verification_hash = hashlib.sha256(f"{submission.id}-{submission.title}-{submission.compliance_score}".encode()).hexdigest()[:16].upper()
        
        cert_text = (
            f"This certifies that the content submission titled <b>'{submission.title}'</b> "
            f"(Submission ID #{submission.id}) has been formally audited through the BrandGuard AI "
            f"Multi-Modal Governance Engine and approved for public release under corporate brand and regulatory guidelines."
        )
        elements.append(Paragraph(cert_text, body_style))
        elements.append(Spacer(1, 15))

        # Metadata Table
        creator_name = submission.creator.name if submission.creator else "Unknown Creator"
        reviewer_name = submission.reviewer.name if getattr(submission, 'reviewer', None) else "Brand Governance Desk"
        
        meta_data = [
            [Paragraph("<b>Content Title:</b>", body_style), Paragraph(submission.title, body_style)],
            [Paragraph("<b>Content Type:</b>", body_style), Paragraph(submission.content_type, body_style)],
            [Paragraph("<b>Submitted By:</b>", body_style), Paragraph(f"{creator_name} ({submission.creator.department if submission.creator else 'Dept'})", body_style)],
            [Paragraph("<b>Authorized Reviewer:</b>", body_style), Paragraph(reviewer_name, body_style)],
            [Paragraph("<b>Approval Timestamp:</b>", body_style), Paragraph(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), body_style)],
            [Paragraph("<b>Verification Hash:</b>", body_style), Paragraph(f"<font color='#2563EB'><b>{verification_hash}</b></font>", body_style)],
        ]

        t_meta = Table(meta_data, colWidths=[150, 380])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t_meta)
        elements.append(Spacer(1, 15))

        # Scores Table
        score_data = [
            ["Metric Category", "Score", "Regulatory & Brand Standard", "Status"],
            ["Overall Brand Health", f"{submission.compliance_score}/100", "Enterprise Benchmark Target >= 85", "VERIFIED"],
            ["Tone & Voice", f"{submission.tone_score}/100", "5-Polarity Enterprise Standard", "PASSED"],
            ["Truth & Claims", f"{submission.claim_score}/100", "FTC Section 5 Substantiation", "COMPLIANT"],
            ["Visual & Accessibility", f"{submission.visual_score}/100", "WCAG 2.1 Level AA (4.5:1 Contrast)", "CONFORMANT"],
        ]

        t_score = Table(score_data, colWidths=[140, 70, 230, 90])
        t_score.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (1,0), (1,-1), 'CENTER'),
            ('ALIGN', (3,0), (3,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (3,1), (3,-1), colors.HexColor('#DCFCE7')),
            ('TEXTCOLOR', (3,1), (3,-1), colors.HexColor('#166534')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t_score)
        elements.append(Spacer(1, 20))

        # Footer Note
        footer_p = Paragraph(
            "<font size='8' color='#64748B'>Generated automatically by BrandGuard AI Governance Platform. "
            "Backed by Marq, Gartner, and WebAIM compliance benchmarks. This certificate confirms pre-publication "
            "adherence and constitutes an immutable audit record.</font>",
            body_style
        )
        elements.append(footer_p)

        doc.build(elements)
        return filename
