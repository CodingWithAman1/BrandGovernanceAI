import os
from models import db, User, BrandGuideline, ApprovedFact, BrandAsset, Submission, EvaluationFlag, ReviewLog, ReviewComment

def seed_database(app):
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if already seeded
        if User.query.first():
            print("Database already contains data. Ensuring Aman Sharma is sole Admin...")
            admin_user = User.query.filter_by(email="aman@synapse.ai").first()
            if admin_user:
                admin_user.role = "ADMIN"
                db.session.commit()
            return

        print("Seeding BrandGuard AI Database...")

        # 1. Users: Aman Sharma is the SOLE ADMIN
        users = [
            # SOLE ADMIN
            User(name="Aman Sharma", email="aman@synapse.ai", role="ADMIN", department="Executive Governance", organization="Team Synapse"),
            
            # AUTHORIZED REVIEWERS
            User(name="Elena Rostova", email="elena@inkloom.ai", role="REVIEWER", department="Brand Operations", organization="Inkloom AI"),
            User(name="David Chen", email="david@inkloom.ai", role="REVIEWER", department="Legal & Compliance", organization="Inkloom AI"),
            
            # CLIENTS & CONTENT CREATORS
            User(name="Priya Sharma", email="priya@inkloom.ai", role="CREATOR", department="Content Marketing", organization="Growth Agency"),
            User(name="Marcus Vance", email="marcus@inkloom.ai", role="CREATOR", department="Creative Design", organization="Design Co"),
            User(name="Janhavi Kanojia", email="janhavi@synapse.ai", role="CREATOR", department="Frontend & UX", organization="Team Synapse")
        ]
        
        for u in users:
            u.set_password("password123")
            db.session.add(u)
        db.session.commit()

        # 2. Brand Guidelines
        guidelines = [
            BrandGuideline(
                rule_code="BG-TONE-01",
                category="TONE",
                rule_title="Eliminate Robotic AI Jargon",
                rule_description="Avoid repetitive LLM cliches such as 'delve into', 'rich tapestry', 'testament to', and 'game-changer'. Replace with active verbs and specific outcomes.",
                severity="SUGGESTION",
                forbidden_patterns="delve into, a testament to, rich tapestry, game-changer, in today's fast-paced world",
                recommended_replacement="explore / evidence of / diverse range",
                citation_ref="Brand Voice Guide § 2.1 (Clarity & Authenticity)"
            ),
            BrandGuideline(
                rule_code="BG-TONE-02",
                category="TONE",
                rule_title="Consultative, Non-Aggressive Phrasing",
                rule_description="Never use hyper-aggressive or flippant phrases like 'crush the competition' or 'obviously'. Maintain an authoritative yet empathetic consultative tone.",
                severity="WARNING",
                forbidden_patterns="crush the competition, obviously, needless to say, clearly you must",
                recommended_replacement="lead industry benchmarks / we recommend",
                citation_ref="Brand Voice Guide § 2.4 (Empathetic Enterprise Voice)"
            ),
            BrandGuideline(
                rule_code="BG-CLAIM-01",
                category="CLAIM",
                rule_title="Substantiate Promotional Rankings & Superlatives",
                rule_description="Absolute superlatives like '#1 in the world', 'world's best', and 'unrivaled' expose the company to FTC Section 5 penalties unless backed by independent third-party audit data.",
                severity="CRITICAL",
                forbidden_patterns="#1, number one in the world, world's best, unrivaled, unbeatable platform",
                recommended_replacement="an award-winning industry leader / proven benchmark",
                citation_ref="FTC Act Section 5 / Operation AI Comply Evidentiary Standard"
            ),
            BrandGuideline(
                rule_code="BG-CLAIM-02",
                category="CLAIM",
                rule_title="Prohibit Absolute Operational Guarantees",
                rule_description="Claims promising '100% guaranteed results', 'foolproof uptime', or 'zero risk' are legally unenforceable and misleading to enterprise buyers.",
                severity="CRITICAL",
                forbidden_patterns="100% guaranteed, 100% foolproof, zero risk, never fails, miracle tool",
                recommended_replacement="reliable, backed by enterprise 99.95% uptime SLA",
                citation_ref="Legal Compliance Handbook § 4.3 (Commercial Warranties)"
            ),
            BrandGuideline(
                rule_code="BG-TERM-01",
                category="TERMINOLOGY",
                rule_title="Forbidden Deprecated Product Naming",
                rule_description="Legacy nomenclature 'Inkloom Classic' and 'Inkloom v1.0' must no longer be published in public copy. Always use 'Inkloom Enterprise Cloud'.",
                severity="WARNING",
                forbidden_patterns="Inkloom Classic, Inkloom v1, Inkloom Legacy",
                recommended_replacement="Inkloom Enterprise Cloud",
                citation_ref="Product Marketing Taxonomy 2026"
            ),
            BrandGuideline(
                rule_code="BG-TERM-02",
                category="TERMINOLOGY",
                rule_title="Competitor Trademark Neutrality",
                rule_description="Do not disparage competitor trademarks by name in ad copy. Use neutral generic categories like 'traditional legacy platforms'.",
                severity="WARNING",
                forbidden_patterns="Slack-killer, Salesforce-killer, inferior tools",
                recommended_replacement="traditional legacy enterprise tools",
                citation_ref="Brand Protection & Legal Policy § 5.1"
            ),
            BrandGuideline(
                rule_code="BG-VIS-01",
                category="VISUAL",
                rule_title="Brand Color Palette Conformity",
                rule_description="All marketing collateral and visual graphics must adhere to approved brand hex codes (Primary #0F172A, Blue #2563EB, Cyan #0EA5E9). Off-palette neon or unapproved shades are prohibited.",
                severity="WARNING",
                forbidden_patterns="#FF00FF, #00FF00, #FF4500",
                recommended_replacement="#2563EB / #0EA5E9",
                citation_ref="Brand Design System § 1.3 (Color Tokens)"
            ),
            BrandGuideline(
                rule_code="BG-ACC-01",
                category="ACCESSIBILITY",
                rule_title="WCAG 2.1 AA Contrast Ratio (Minimum 4.5:1)",
                rule_description="Text elements placed over solid or background graphics must satisfy a minimum relative luminance contrast ratio of 4.5:1 for normal text and 3:1 for large display titles.",
                severity="CRITICAL",
                forbidden_patterns="low-contrast text",
                recommended_replacement="Adjust background luminance or text darkness to reach >= 4.5:1",
                citation_ref="WCAG 2.1 Level AA / ADA Title III Standard"
            )
        ]
        for g in guidelines:
            db.session.add(g)
        db.session.commit()

        # 3. Approved Facts Bank
        facts = [
            ApprovedFact(
                topic="Global Customer Scale",
                claim_statement="Serving over 50,000 active enterprise organizations across 85 countries.",
                approved_source_link="https://inkloom.ai/investor-metrics-q3-2026",
                evidence_excerpt="Audited by Ernst & Young Q3 2026 financial and customer count report.",
                expiration_date="2027-12-31"
            ),
            ApprovedFact(
                topic="Enterprise Security Certifications",
                claim_statement="Independently audited SOC 2 Type II certified, ISO 27001 conformant, and GDPR compliant.",
                approved_source_link="https://inkloom.ai/trust-center",
                evidence_excerpt="Annual SOC 2 Type II report issued by Schellman Compliance LLC.",
                expiration_date="2027-06-30"
            ),
            ApprovedFact(
                topic="Infrastructure Uptime SLA",
                claim_statement="Engineered with 99.95% verified cloud availability backed by financially supported SLAs.",
                approved_source_link="https://status.inkloom.ai",
                evidence_excerpt="Live multi-region status monitor benchmarked over trailing 12 months.",
                expiration_date="2027-12-31"
            )
        ]
        for f in facts:
            db.session.add(f)
        db.session.commit()

        # 4. Brand Design Tokens
        assets = [
            BrandAsset(name="Primary Deep Navy", asset_type="PALETTE", asset_value="#0F172A", metadata_json='{"usage": "Main text, dark hero backgrounds"}'),
            BrandAsset(name="Brand Electric Blue", asset_type="PALETTE", asset_value="#2563EB", metadata_json='{"usage": "Primary CTA buttons, links, accents"}'),
            BrandAsset(name="Accent Sky Cyan", asset_type="PALETTE", asset_value="#0EA5E9", metadata_json='{"usage": "Highlights, progress bars, active tags"}'),
            BrandAsset(name="Slate Dark", asset_type="PALETTE", asset_value="#1E293B", metadata_json='{"usage": "Cards, table headers"}'),
            BrandAsset(name="Off-White Canvas", asset_type="PALETTE", asset_value="#F8FAFC", metadata_json='{"usage": "Page background"}'),
            BrandAsset(name="Pure White", asset_type="PALETTE", asset_value="#FFFFFF", metadata_json='{"usage": "Card surfaces"}')
        ]
        for a in assets:
            db.session.add(a)
        db.session.commit()

        # 5. Sample Submission
        priya = User.query.filter_by(email="priya@inkloom.ai").first()
        elena = User.query.filter_by(email="elena@inkloom.ai").first()

        sample_text_1 = (
            "In today's fast-paced world, our revolutionary, #1 AI platform in the world guarantees 100% perfect marketing "
            "results with zero risk. While competitors struggle, our game-changer tool helps you crush the competition. "
            "Obviously, any company using Inkloom Classic should upgrade immediately. A rich tapestry of enterprise tools delves into your data."
        )

        sub1 = Submission(
            title="Q4 Enterprise Cloud Product Launch Campaign",
            content_type="TEXT",
            raw_content=sample_text_1,
            original_content=sample_text_1,
            creator_id=priya.id,
            reviewer_id=elena.id,
            status="PENDING",
            compliance_score=48,
            tone_score=55,
            claim_score=35,
            visual_score=100
        )
        db.session.add(sub1)
        db.session.commit()

        # Sample Flags
        db.session.add(EvaluationFlag(
            submission_id=sub1.id,
            guideline_id=3,
            flag_type="CLAIM",
            flagged_snippet="#1 AI platform in the world",
            explanation="FTC Section 5 Risk: Absolute superlative ranking requires verified third-party audit data.",
            suggested_fix="an industry-recognized, award-winning platform",
            severity="CRITICAL",
            status="PENDING"
        ))
        db.session.add(EvaluationFlag(
            submission_id=sub1.id,
            guideline_id=4,
            flag_type="CLAIM",
            flagged_snippet="guarantees 100% perfect marketing results with zero risk",
            explanation="FTC Section 5 Risk: Absolute guarantee is legally misleading.",
            suggested_fix="is engineered for proven, reliable marketing performance",
            severity="CRITICAL",
            status="PENDING"
        ))
        db.session.add(EvaluationFlag(
            submission_id=sub1.id,
            guideline_id=1,
            flag_type="TONE",
            flagged_snippet="In today's fast-paced world",
            explanation="Robotic AI Phrasing: Cut bloated intro cliches; start directly with the value proposition.",
            suggested_fix="Currently,",
            severity="SUGGESTION",
            status="PENDING"
        ))
        db.session.add(ReviewLog(
            submission_id=sub1.id,
            actor_id=priya.id,
            action="SUBMIT",
            comment="Submitted draft for pre-publication review and compliance check."
        ))

        db.session.commit()
        print("Database seeded successfully: Aman Sharma is the sole Admin!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    seed_database(app)
