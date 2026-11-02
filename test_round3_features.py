"""
Unit and Integration Test Suite: Round 3 Enterprise Improvements
================================================================
Verifies:
1. Public Cryptographic Certificate Verifier (/verify & /verify/<hash>)
2. Enterprise Integrations & Developer Hub (/integrations)
3. Competitive Intelligence & Sales Battlecard Studio (/scanner/competitor-studio)
4. Dynamic Brand Voice DNA Profiler (/brand-dna & /guidelines/brand-dna)
5. CI/CD Pre-Publication Stage-Gate API (/api/v1/gate/check)
"""

import unittest
import hashlib
from app import create_app
from models import db, User, Submission, BrandGuideline


class TestRound3Features(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def _login_as_admin(self):
        """Helper to login as Aman Sharma (Admin)."""
        admin = User.query.filter_by(email="aman@synapse.ai").first()
        self.client.get(f'/quick-switch/{admin.id}', follow_redirects=True)
        return admin

    def _login_as_creator(self):
        """Helper to login as Client/Creator."""
        creator = User.query.filter_by(role="CREATOR").first()
        self.client.get(f'/quick-switch/{creator.id}', follow_redirects=True)
        return creator

    # =========================================================================
    # 1. PUBLIC CRYPTOGRAPHIC CERTIFICATE VERIFIER (/verify)
    # =========================================================================
    def test_01_verify_index_public_access(self):
        """Verify that /verify is publicly accessible without login."""
        resp = self.client.get('/verify')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Cryptographic Certificate Verifier", resp.data)
        self.assertIn(b"SHA-256", resp.data)

    def test_02_verify_cert_valid_and_invalid(self):
        """Verify valid certificate hash lookup and invalid hash rejection."""
        approved = Submission.query.filter_by(status='APPROVED').first()
        self.assertIsNotNone(approved, "Should have at least one approved submission in seed data")

        raw_str = f"{approved.id}-{approved.title}-{approved.compliance_score}"
        full_hash = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
        short_hash = full_hash[:16].upper()

        # Lookup valid
        resp_valid = self.client.get(f'/verify/{short_hash}')
        self.assertEqual(resp_valid.status_code, 200)
        self.assertIn(b"CRYPTOGRAPHICALLY VERIFIED", resp_valid.data)
        self.assertIn(approved.title.encode('utf-8'), resp_valid.data)

        # Lookup invalid
        resp_invalid = self.client.get('/verify/INVALIDHASH999999')
        self.assertEqual(resp_invalid.status_code, 404)
        self.assertIn(b"CERTIFICATE VERIFICATION FAILED", resp_invalid.data)

    # =========================================================================
    # 2. ENTERPRISE INTEGRATIONS & DEVELOPER HUB (/integrations)
    # =========================================================================
    def test_03_integrations_hub(self):
        """Verify that /integrations developer hub renders GitHub Actions & API docs."""
        resp = self.client.get('/integrations')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Developer Hub &amp; Enterprise CI/CD Gate", resp.data)
        self.assertIn(b"brandguard-gate.yml", resp.data)
        self.assertIn(b"/api/v1/gate/check", resp.data)

    # =========================================================================
    # 3. COMPETITOR BATTLECARD STUDIO (/scanner/competitor-studio)
    # =========================================================================
    def test_04_competitor_studio_auth_and_synthesis(self):
        """Verify that Competitor Studio requires login and synthesizes sales battlecards."""
        # Must require login
        resp_anon = self.client.get('/scanner/competitor-studio')
        self.assertEqual(resp_anon.status_code, 302)

        # Logged in access
        self._login_as_creator()
        resp_get = self.client.get('/scanner/competitor-studio')
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn(b"Sales Battlecard Studio", resp_get.data)

        # Synthesize Battlecard via POST
        post_data = {
            "competitor_name": "RivalCorp AI",
            "content": "Our platform is undisputed #1 in enterprise cloud reliability with 100% guaranteed zero downtime."
        }
        resp_post = self.client.post('/scanner/competitor-studio', data=post_data)
        self.assertEqual(resp_post.status_code, 200)
        self.assertIn(b"Strategic Battlecard Dossier", resp_post.data)
        self.assertIn(b"AE SALES TALKING POINT", resp_post.data)
        self.assertIn(b"SOCIAL POSITIONING", resp_post.data)
        self.assertIn(b"EXECUTIVE PR POSITIONING", resp_post.data)

    # =========================================================================
    # 4. BRAND VOICE DNA PROFILER (/brand-dna & /guidelines/brand-dna)
    # =========================================================================
    def test_05_brand_dna_extraction_and_rule_commit(self):
        """Verify Brand Voice DNA extraction and 1-click rulebook commitment."""
        self._login_as_admin()

        # Test route alias
        resp_alias = self.client.get('/brand-dna')
        self.assertEqual(resp_alias.status_code, 302)  # Redirects to guidelines.brand_dna

        # GET profiler
        resp_get = self.client.get('/guidelines/brand-dna')
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn(b"Brand Voice DNA Profiler", resp_get.data)

        # POST analyze
        manifesto = (
            "We believe in simplicity, clarity, and empirical proof. We eliminate marketing hyperbole "
            "and speak to enterprise decision-makers as trusted technical advisors."
        )
        resp_post = self.client.post('/guidelines/brand-dna', data={
            "action": "analyze",
            "manifesto_text": manifesto
        })
        self.assertEqual(resp_post.status_code, 200)
        self.assertIn(b"Calibrated Voice Polarities", resp_post.data)
        self.assertIn(b"Synthesized Brand Governance Rule", resp_post.data)

        # POST commit rule to rulebook
        rule_data = {
            "action": "save_rule",
            "rule_title": "Voice DNA: Empirical Clarity Rule",
            "rule_desc": "Mandates substantiated evidence for performance claims.",
            "banned_patterns": "world's best, revolutionary, 100% guarantee",
            "replacement": "audited benchmark result"
        }
        resp_save = self.client.post('/guidelines/brand-dna', data=rule_data, follow_redirects=True)
        self.assertEqual(resp_save.status_code, 200)
        self.assertIn(b"committed to Rulebook", resp_save.data)

        # Check DB
        saved_rule = BrandGuideline.query.filter_by(rule_title="Voice DNA: Empirical Clarity Rule").first()
        self.assertIsNotNone(saved_rule)
        self.assertTrue(saved_rule.rule_code.startswith("BG-DNA-"))

    # =========================================================================
    # 5. CI/CD QUALITY GATE API (/api/v1/gate/check)
    # =========================================================================
    def test_06_ci_cd_quality_gate_api(self):
        """Verify that /api/v1/gate/check evaluates compliance scores and blocks violations."""
        # Non-compliant copy with superlatives (should return 422 Unprocessable Entity - Blocked)
        bad_copy = "We are the #1 world's best platform with 100% guaranteed zero downtime."
        resp_bad = self.client.post('/api/v1/gate/check', json={
            "content": bad_copy,
            "threshold": 85,
            "jurisdiction": "GLOBAL"
        })
        self.assertEqual(resp_bad.status_code, 422)
        data_bad = resp_bad.get_json()
        self.assertFalse(data_bad['passed'])
        self.assertEqual(data_bad['status'], 'BLOCKED_STAGE_GATE')
        self.assertTrue(len(data_bad['critical_violations']) > 0)

        # Clean consultative copy (should return 200 OK - Approved)
        good_copy = "Our enterprise platform provides audited, SLA-backed performance with verified 99.95% availability."
        resp_good = self.client.post('/api/v1/gate/check', json={
            "content": good_copy,
            "threshold": 75,
            "jurisdiction": "GLOBAL"
        })
        self.assertEqual(resp_good.status_code, 200)
        data_good = resp_good.get_json()
        self.assertTrue(data_good['passed'])
        self.assertEqual(data_good['status'], 'APPROVED_STAGE_GATE')


if __name__ == '__main__':
    unittest.main()
