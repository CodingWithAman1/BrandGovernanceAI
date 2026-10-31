import os
import time
import unittest
from app import create_app
from models import db, User, Submission, EvaluationFlag, BrandGuideline, ApprovedFact, ReviewLog
from engines.tone_calibrator import ToneCalibrator
from engines.claims_checker import ClaimsFactChecker
from engines.visual_inspector import VisualInspector
from engines.clarity_engine import ClarityEngine
from engines.pdf_cert import PDFCertificateGenerator


class CompleteBrandGuardTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False

    def setUp(self):
        self.client = self.app.test_client()

    # =========================================================================
    # 1. CORE COMPLIANCE ENGINE TESTS
    # =========================================================================

    def test_01_tone_calibrator_engine(self):
        """ToneCalibrator flags hyperbolic claims, buzzwords, and calculates polarity score"""
        with self.app.app_context():
            guidelines = BrandGuideline.query.filter_by(is_active=True).all()
            tone_engine = ToneCalibrator(guidelines)
            
            # Text with multiple forbidden tone/voice patterns
            risky_text = "In today's fast-paced world, our game-changer tool helps you crush the competition. Obviously, any enterprise should delve into our rich tapestry."
            res = tone_engine.evaluate(risky_text)
            
            self.assertIn('score', res)
            self.assertIn('flags', res)
            self.assertLess(res['score'], 80, "Hyperbolic text score should be below 80%")
            self.assertTrue(len(res['flags']) >= 3, "Multiple tone flags should be detected")

    def test_02_claims_fact_checker_engine(self):
        """ClaimsFactChecker verifies claims against SQL Truth Bank and flags unverified claims"""
        with self.app.app_context():
            guidelines = BrandGuideline.query.filter_by(is_active=True).all()
            approved_facts = ApprovedFact.query.filter_by(is_active=True).all()
            claims_engine = ClaimsFactChecker(approved_facts, guidelines)

            # Text with multiple unverified superlatives and guarantees
            unverified_text = "Our platform is the #1 AI platform in the world with 100% guaranteed results and unrivaled performance that never fails."
            res = claims_engine.evaluate(unverified_text)

            self.assertIn('score', res)
            self.assertIn('flags', res)
            self.assertLess(res['score'], 80, "Unverified claim score must be below 80%")
            self.assertTrue(len(res['flags']) >= 2, "Should flag multiple FTC Section 5 claims")

    def test_03_visual_inspector_engine(self):
        """VisualInspector calculates WCAG 2.1 AA luminance contrast and handles palette clustering"""
        # Test WCAG contrast ratio calculation: Black (#000000) on White (#FFFFFF) is 21:1
        ratio = VisualInspector.calculate_contrast_ratio('#000000', '#ffffff')
        self.assertAlmostEqual(ratio, 21.0, delta=0.5)

        # Poor contrast test: Light gray on white
        poor_ratio = VisualInspector.calculate_contrast_ratio('#cccccc', '#ffffff')
        self.assertLess(poor_ratio, 4.5, "Contrast should fail WCAG 2.1 AA (4.5:1)")

    def test_04_clarity_engine_analytics(self):
        """ClarityEngine computes rule friction index, dispute rates, and clarity metrics"""
        with self.app.app_context():
            insights = ClarityEngine.get_clarity_insights()
            self.assertIsInstance(insights, list)
            if len(insights) > 0:
                item = insights[0]
                self.assertIn('rule_code', item)
                self.assertIn('clarity_score', item)
                self.assertIn('total_flags', item)

    def test_05_pdf_certificate_generator(self):
        """PDFCertificateGenerator creates valid cryptographic compliance certificates"""
        with self.app.app_context():
            sub = Submission.query.filter_by(status='APPROVED').first()
            if not sub:
                sub = Submission.query.first()
            output_dir = os.path.join(self.app.config['UPLOAD_FOLDER'], 'certificates')
            os.makedirs(output_dir, exist_ok=True)
            cert_filename = PDFCertificateGenerator.generate_certificate(sub, output_dir)
            
            full_path = os.path.join(output_dir, cert_filename)
            self.assertTrue(os.path.exists(full_path), "PDF Certificate file must be written to disk")
            self.assertGreater(os.path.getsize(full_path), 500, "PDF Certificate must not be empty")

    # =========================================================================
    # 2. AUTHENTICATION & ROUTE GUARDS (RBAC)
    # =========================================================================

    def test_06_unauthenticated_routes_blocked(self):
        """Every sensitive endpoint redirects unauthenticated requests (HTTP 302 to /login)"""
        protected_endpoints = [
            '/',
            '/client/dashboard',
            '/reviewer/dashboard',
            '/admin/dashboard',
            '/scanner/studio',
            '/scanner/report/1',
            '/reviews/queue',
            '/reviews/detail/1',
            '/guidelines/',
            '/analytics/'
        ]
        for ep in protected_endpoints:
            resp = self.client.get(ep, follow_redirects=False)
            self.assertEqual(resp.status_code, 302, f"Endpoint {ep} must return 302 Redirect")
            self.assertIn('/login', resp.headers['Location'], f"Endpoint {ep} must redirect to /login")

    def test_07_sole_admin_lock(self):
        """Executive Admin portal is strictly locked to Aman Sharma (aman@synapse.ai)"""
        # Imposter attempt
        resp_imposter = self.client.post('/admin/login', data={'email': 'hacker@synapse.ai', 'password': 'password123'}, follow_redirects=True)
        self.assertIn('Access Denied', resp_imposter.data.decode('utf-8'))

        # Sole admin login success
        admin_c = self.app.test_client()
        resp_admin = admin_c.post('/admin/login', data={'email': 'aman@synapse.ai', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(resp_admin.status_code, 200)
        self.assertTrue('/admin' in resp_admin.request.path)
        self.assertIn('Aman Sharma', resp_admin.data.decode('utf-8'))

    def test_08_client_portal_isolation(self):
        """Client account cannot access Reviewer Desk or Admin Portal"""
        client_c = self.app.test_client()
        client_c.post('/client/login', data={'email': 'priya@inkloom.ai', 'password': 'password123'})

        # Try reviewer dashboard
        resp_rev = client_c.get('/reviewer/dashboard', follow_redirects=False)
        self.assertEqual(resp_rev.status_code, 302)
        self.assertTrue('/client' in resp_rev.headers['Location'])

        # Try admin dashboard
        resp_adm = client_c.get('/admin/dashboard', follow_redirects=False)
        self.assertEqual(resp_adm.status_code, 302)
        self.assertTrue('/client' in resp_adm.headers['Location'])

    def test_09_reviewer_portal_isolation(self):
        """Reviewer account can access Review Queue but is blocked from Admin Portal"""
        rev_c = self.app.test_client()
        rev_c.post('/reviewer/login', data={'email': 'elena@inkloom.ai', 'password': 'password123'})

        # Reviewer can access queue
        resp_q = rev_c.get('/reviews/queue')
        self.assertEqual(resp_q.status_code, 200)

        # Reviewer blocked from admin
        resp_adm = rev_c.get('/admin/dashboard', follow_redirects=False)
        self.assertEqual(resp_adm.status_code, 302)
        self.assertTrue('/reviewer' in resp_adm.headers['Location'])

    # =========================================================================
    # 3. END-TO-END GOVERNANCE LIFECYCLE
    # =========================================================================

    def test_10_full_audit_workflow_and_one_click_fix(self):
        """Full lifecycle: Client scans draft -> gets report -> applies 1-click fix -> submits to queue -> Reviewer approves"""
        # Step 1: Client logs in
        client_c = self.app.test_client()
        client_c.post('/client/login', data={'email': 'priya@inkloom.ai', 'password': 'password123'})

        # Step 2: Client submits a draft to Pre-Publication Studio
        scan_data = {
            'title': 'Automated Test Q4 Launch Campaign',
            'content': "In today's fast-paced world, our revolutionary #1 AI platform in the world guarantees 100% results with zero risk."
        }
        resp_scan = client_c.post('/scanner/analyze', data=scan_data, follow_redirects=False)
        self.assertEqual(resp_scan.status_code, 302)
        sub_id = int(resp_scan.headers['Location'].split('/')[-1])

        # Step 3: View generated report
        resp_report = client_c.get(f'/scanner/report/{sub_id}')
        self.assertEqual(resp_report.status_code, 200)
        report_html = resp_report.data.decode('utf-8')
        self.assertIn('Automated Test Q4 Launch Campaign', report_html)
        self.assertIn('HEALTH SCORE', report_html)

        # Step 4: Apply 1-Click Fix via API
        with self.app.app_context():
            sub = db.session.get(Submission, sub_id)
            init_score = sub.compliance_score
            flag = EvaluationFlag.query.filter_by(submission_id=sub.id, status='PENDING').first()
            flag_id = flag.id if flag else None

        if flag_id:
            resp_fix = client_c.post(f'/scanner/apply-fix/{flag_id}', headers={'X-Requested-With': 'XMLHttpRequest'})
            self.assertEqual(resp_fix.status_code, 200)
            fix_data = resp_fix.get_json()
            self.assertTrue(fix_data.get('success'))
            self.assertGreater(fix_data.get('new_score'), init_score, "Score must increase after remediation")

        # Step 5: Route submission to Stage-Gate Review Queue
        resp_submit = client_c.post(f'/scanner/submit-for-review/{sub_id}', follow_redirects=False)
        self.assertEqual(resp_submit.status_code, 302)

        # Step 6: Reviewer logs in and inspects the queue
        rev_c = self.app.test_client()
        rev_c.post('/reviewer/login', data={'email': 'elena@inkloom.ai', 'password': 'password123'})
        resp_queue = rev_c.get('/reviews/queue')
        self.assertEqual(resp_queue.status_code, 200)
        self.assertIn('Automated Test Q4 Launch Campaign', resp_queue.data.decode('utf-8'))

        # Step 7: Reviewer opens detail page
        resp_detail = rev_c.get(f'/reviews/detail/{sub_id}')
        self.assertEqual(resp_detail.status_code, 200)

        # Step 8: Reviewer takes action (APPROVE)
        resp_action = rev_c.post(f'/reviews/action/{sub_id}', data={'action': 'APPROVE', 'comment': 'Release approved by Legal.'}, follow_redirects=True)
        self.assertEqual(resp_action.status_code, 200)

        # Verify status in DB
        with self.app.app_context():
            sub_after = db.session.get(Submission, sub_id)
            self.assertEqual(sub_after.status, 'APPROVED')

    # =========================================================================
    # 4. RULEBOOK & ANALYTICS
    # =========================================================================

    def test_11_guideline_and_analytics_management(self):
        """Admin can view and add brand guidelines, and review clarity index"""
        admin_c = self.app.test_client()
        admin_c.post('/admin/login', data={'email': 'aman@synapse.ai', 'password': 'password123'})

        # View guidelines
        resp_g = admin_c.get('/guidelines/')
        self.assertEqual(resp_g.status_code, 200)
        self.assertIn('Brand Rulebook', resp_g.data.decode('utf-8'))

        # Add new brand rule
        ts = int(time.time() * 1000)
        rule_code = f"TEST-RULE-{ts}"
        rule_data = {
            'rule_code': rule_code,
            'category': 'TONE',
            'rule_title': 'Avoid Passive Hyperbole',
            'rule_description': 'Passive hyperbole dilutes clarity and causes reader skepticism.',
            'severity': 'WARNING',
            'forbidden_patterns': 'unrivaled in every aspect, flawless technology',
            'recommended_replacement': 'rigorously verified, benchmark-proven',
            'citation_ref': 'Brand Book Section 4.1'
        }
        resp_add = admin_c.post('/guidelines/rule/add', data=rule_data, follow_redirects=True)
        self.assertEqual(resp_add.status_code, 200)

        with self.app.app_context():
            saved_rule = BrandGuideline.query.filter_by(rule_code=rule_code).first()
            self.assertIsNotNone(saved_rule)
            self.assertEqual(saved_rule.rule_title, 'Avoid Passive Hyperbole')

        # View clarity analytics
        resp_analytics = admin_c.get('/analytics/')
        self.assertEqual(resp_analytics.status_code, 200)
        self.assertIn('Clarity', resp_analytics.data.decode('utf-8'))

    # =========================================================================
    # 5. CYBER UI & STATIC ASSETS
    # =========================================================================

    def test_12_static_cyber_assets(self):
        """Verify presence of cyber cursor, ambient particle engine, and design system assets"""
        css_path = os.path.join(self.app.root_path, 'static', 'css', 'style.css')
        scanner_js_path = os.path.join(self.app.root_path, 'static', 'js', 'scanner.js')
        effects_js_path = os.path.join(self.app.root_path, 'static', 'js', 'cyber-effects.js')

        self.assertTrue(os.path.exists(css_path), "style.css must exist")
        self.assertTrue(os.path.exists(scanner_js_path), "scanner.js must exist")
        self.assertTrue(os.path.exists(effects_js_path), "cyber-effects.js must exist")

        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            self.assertIn('.cursor-dot', css_content)
            self.assertIn('.cursor-glow-ring', css_content)
            self.assertIn('.ambient-orb', css_content)
            self.assertIn('.scanner-hud-overlay', css_content)

        with open(effects_js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
            self.assertIn('initCyberCursor', js_content)
            self.assertIn('initAmbientParticles', js_content)
            self.assertIn('showToast', js_content)

    # =========================================================================
    # 6. ENTERPRISE POWERHOUSE SUITE (REGULATORY, URL SCANNER, GATES, AMBIGUITY)
    # =========================================================================

    def test_13_regulatory_compliance_engine(self):
        """RegulatoryComplianceEngine audits SEC AI-Washing, EU AI Act Art. 50/52, and UK CMA Green Claims"""
        from engines.regulatory_engine import regulatory_engine

        # Test SEC AI-Washing
        sec_text = "Our fully autonomous platform operates with zero hallucinations and eliminates all errors."
        sec_res = regulatory_engine.evaluate(sec_text, jurisdiction="US")
        self.assertLess(sec_res['score'], 80, "SEC AI-washing text should deduct points")
        self.assertTrue(any(f['rule_code'].startswith('SEC') for f in sec_res['flags']))

        # Test EU AI Act
        eu_text = "Our emotion recognition and synthetic persona features autonomous hiring filter technology."
        eu_res = regulatory_engine.evaluate(eu_text, jurisdiction="EU")
        self.assertTrue(any(f['rule_code'].startswith('EU') for f in eu_res['flags']))

        # Test UK CMA Green Claims
        uk_text = "Deploy on our 100% eco-friendly, zero carbon, climate-neutral cloud compute."
        uk_res = regulatory_engine.evaluate(uk_text, jurisdiction="UK")
        self.assertTrue(any(f['rule_code'].startswith('UK') for f in uk_res['flags']))

        # Test Disclaimer generation
        disclaimer = regulatory_engine.generate_tailored_disclaimer("AI model", jurisdiction="GLOBAL")
        self.assertIn("GLOBAL REGULATORY COMPLIANCE DISCLOSURE", disclaimer)

    def test_14_url_scanner_and_competitor_claims(self):
        """URLScannerEngine parses HTML, audits competitor copy against SQL Truth Bank, and synthesizes battlecard"""
        from engines.url_scanner import url_scanner_engine

        competitor_copy = "We are the #1 unrivaled platform in the world with 100% guaranteed zero downtime and zero hallucinations."
        with self.app.app_context():
            approved_facts = ApprovedFact.query.all()
            audit_res = url_scanner_engine.audit_competitor_claims(
                content=competitor_copy,
                title="Rival Announcement",
                approved_facts=approved_facts,
                competitor_name="RivalCorp"
            )

            self.assertTrue(audit_res['success'])
            self.assertGreater(audit_res['vulnerability_score'], 50)
            self.assertTrue(len(audit_res['vulnerabilities']) >= 2)
            self.assertIn('battlecard', audit_res)
            self.assertIn('sales_pitch', audit_res['battlecard'])
            self.assertIn('linkedin_angle', audit_res['battlecard'])

    def test_15_ci_cd_quality_gate(self):
        """CI/CD Quality Gate (/api/v1/gate/check) blocks critical violations (HTTP 422) and passes compliant copy (HTTP 200)"""
        # Blocked call (HTTP 422)
        risky_payload = {
            "content": "Our #1 tool guarantees 100% zero downtime with conscious AI and zero hallucinations.",
            "threshold": 85,
            "block_on_critical": True
        }
        resp_blocked = self.client.post('/api/v1/gate/check', json=risky_payload)
        self.assertEqual(resp_blocked.status_code, 422)
        data_blocked = resp_blocked.get_json()
        self.assertFalse(data_blocked['pass'])
        self.assertEqual(data_blocked['status'], 'BLOCKED_STAGE_GATE')
        self.assertGreater(len(data_blocked['blocking_violations']), 0)

        # Passing call (HTTP 200)
        clean_payload = {
            "content": "Inkloom Enterprise Cloud provides independently verified 99.95% availability for enterprise teams.",
            "threshold": 75,
            "block_on_critical": True
        }
        resp_pass = self.client.post('/api/v1/gate/check', json=clean_payload)
        self.assertEqual(resp_pass.status_code, 200)
        data_pass = resp_pass.get_json()
        self.assertTrue(data_pass['pass'])
        self.assertEqual(data_pass['status'], 'APPROVED_STAGE_GATE')

    def test_16_ai_ambiguity_resolver(self):
        """AI Ambiguity Resolver remediates disputed rules via API and resolves creator friction"""
        from engines.ai_copilot import ai_copilot

        res = ai_copilot.remediate_rule_ambiguity(
            rule_code="BG-TONE-01",
            current_title="Eliminate Robotic AI Jargon",
            current_description="Avoid repetitive LLM cliches.",
            current_patterns="delve into, rich tapestry",
            current_replacement="explore",
            override_reasons=["Rule is too aggressive on industry standard whitepapers."]
        )
        self.assertTrue(res['success'])
        self.assertIn('amended_title', res)
        self.assertIn('amended_description', res)

        # Test API endpoint
        api_res = self.client.post('/api/v1/guidelines/auto-remediate', json={"rule_code": "BG-TONE-01"})
        self.assertEqual(api_res.status_code, 200)
        self.assertTrue(api_res.get_json()['success'])

    def test_17_brand_drift_and_audit_vault_export(self):
        """Analytics calculates Department-level profiling, Brand Drift, and provides Audit Vault Dossier export"""
        admin_c = self.app.test_client()
        admin_c.post('/admin/login', data={'email': 'aman@synapse.ai', 'password': 'password123'})

        # Analytics page with department heatmap
        res_idx = admin_c.get('/analytics/')
        self.assertEqual(res_idx.status_code, 200)
        html_idx = res_idx.data.decode('utf-8')
        self.assertIn('Department-Level Risk Profiling', html_idx)
        self.assertIn('Brand Drift', html_idx)

        # Audit Vault Dossier HTML View
        res_dossier = admin_c.get('/analytics/audit-vault-export')
        self.assertEqual(res_dossier.status_code, 200)
        html_dossier = res_dossier.data.decode('utf-8')
        self.assertIn('Regulatory Audit Dossier', html_dossier)
        self.assertIn('Cryptographic Vault Seal', html_dossier)

        # Audit Vault JSON Export
        res_json = admin_c.get('/analytics/audit-vault-export?format=json')
        self.assertEqual(res_json.status_code, 200)
        self.assertEqual(res_json.mimetype, 'application/json')
        vault_data = res_json.get_json()
        self.assertIn('cryptographic_seal', vault_data)
        self.assertIn('submissions_summary', vault_data)

    def test_18_url_scanner_and_social_previews(self):
        """Live URL scanner routes and social preview visual mockups render cleanly"""
        client_c = self.app.test_client()
        client_c.post('/client/login', data={'email': 'priya@inkloom.ai', 'password': 'password123'})

        # URL Scanner GET
        res_get = client_c.get('/scanner/url-scan')
        self.assertEqual(res_get.status_code, 200)
        self.assertIn('Live URL & Competitor Claim Scanner', res_get.data.decode('utf-8'))

        # URL Scanner POST with competitor copy
        res_post = client_c.post('/scanner/url-scan', data={
            'competitor_name': 'RivalCloud',
            'content': 'Our #1 platform guarantees zero downtime with conscious AI and zero hallucinations.'
        })
        self.assertEqual(res_post.status_code, 200)
        html_post = res_post.data.decode('utf-8')
        self.assertIn('Competitor Vulnerabilities', html_post)
        self.assertIn('Counter-Messaging Battlecard', html_post)

        # Studio with Social Previews
        res_studio = client_c.get('/scanner/studio')
        self.assertEqual(res_studio.status_code, 200)
        html_studio = res_studio.data.decode('utf-8')
        self.assertIn('Omnichannel Live Content Previews', html_studio)
        self.assertIn('LinkedIn', html_studio)
        self.assertIn('Google SERP', html_studio)



if __name__ == '__main__':
    unittest.main()
