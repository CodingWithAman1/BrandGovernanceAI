"""
Unit and Integration Test Suite: BrandGuard AI Co-Pilot & AI Enhancements
========================================================================
Verifies:
1. AI Copilot Engine local semantic harmonization
2. FTC / SEC safe harbor disclaimer synthesis
3. AI governance chat advisory
4. AI brand guideline auto-synthesis
5. Programmatic REST API endpoints (/api/v1/ai/*)
6. Scanner Studio AI actions (/scanner/ai-harmonize and /scanner/append-safe-harbor)
"""

import unittest
from app import create_app
from models import db, User, Submission, EvaluationFlag
from engines.ai_copilot import ai_copilot


class TestAIFeatures(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    # =========================================================================
    # 1. ENGINE UNIT TESTS
    # =========================================================================
    def test_01_harmonize_draft(self):
        """Verify that AI harmonization cleanses robotic AI cliches & superlatives."""
        raw = "In today's fast-paced world, our game-changer platform delves into data to crush the competition with 100% risk free performance."
        res = ai_copilot.harmonize_draft(raw)
        self.assertTrue(res['success'])
        self.assertIn('harmonized_text', res)
        # Check that cliches were replaced
        self.assertNotIn("delves into", res['harmonized_text'])
        self.assertNotIn("crush the competition", res['harmonized_text'])
        self.assertNotIn("100% risk free", res['harmonized_text'])
        self.assertTrue(len(res['improvements']) > 0)

    def test_02_safe_harbor_generation(self):
        """Verify that safe harbor generator includes FTC & SEC regulatory notices."""
        raw = "Our AI system delivers 99.9% uptime and will accelerate your upcoming roadmap."
        res = ai_copilot.generate_safe_harbor(raw)
        self.assertTrue(res['success'])
        self.assertIn("FTC 16 CFR § 255", res['disclaimer'])
        self.assertIn("Private Securities Litigation Reform Act", res['disclaimer'])
        self.assertIn("WCAG 2.1 AA", res['disclaimer'])

    def test_03_ai_chat_advisor(self):
        """Verify that AI chat returns structured, knowledgeable compliance advice."""
        q1 = ai_copilot.chat("What are the FTC Section 5 rules for superlatives?")
        self.assertIn("FTC Section 5", q1['reply'])

        q2 = ai_copilot.chat("What contrast ratio does WCAG require?")
        self.assertIn("4.5:1", q2['reply'])

        q3 = ai_copilot.chat("Why is 'delve into' flagged?")
        self.assertIn("Delve into", q3['reply'])

    def test_04_synthesize_guideline(self):
        """Verify that AI guideline synthesizer outputs complete rule schema."""
        res = ai_copilot.synthesize_guideline("Carbon Neutral Greenwashing")
        self.assertTrue(res['success'])
        g = res['guideline']
        self.assertIn('rule_code', g)
        self.assertIn('rule_title', g)
        self.assertIn('category', g)
        self.assertIn('forbidden_patterns', g)
        self.assertIn('citation_ref', g)

    # =========================================================================
    # 2. REST API INTEGRATION TESTS
    # =========================================================================
    def test_05_api_ai_harmonize(self):
        """Verify POST /api/v1/ai/harmonize endpoint."""
        payload = {
            "content": "Our revolutionary tool is a testament to excellence and will crush the competition."
        }
        resp = self.client.post('/api/v1/ai/harmonize', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        self.assertIn('harmonized_text', data)

    def test_06_api_ai_safe_harbor(self):
        """Verify POST /api/v1/ai/safe-harbor endpoint."""
        payload = {
            "content": "Our solution achieves 45% revenue increase in benchmark testing."
        }
        resp = self.client.post('/api/v1/ai/safe-harbor', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        self.assertIn('FTC', data['disclaimer'])

    def test_07_api_ai_chat(self):
        """Verify POST /api/v1/ai/chat endpoint."""
        payload = {
            "message": "How do I make my copy compliant with FTC Section 5?",
            "context": "Our software is #1 in the market"
        }
        resp = self.client.post('/api/v1/ai/chat', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(len(data['reply']) > 20)

    def test_08_api_ai_suggest_guideline(self):
        """Verify POST /api/v1/ai/suggest-guideline endpoint."""
        payload = {"topic": "AI Copyright and Training Data"}
        resp = self.client.post('/api/v1/ai/suggest-guideline', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['guideline']['rule_code'].startswith("BG-"))

    # =========================================================================
    # 3. SCANNER ROUTE AI ACTIONS
    # =========================================================================
    def test_09_scanner_ai_harmonize_route(self):
        """Verify that authenticated creator can execute 1-click full AI harmonization."""
        creator = User.query.filter_by(role='CREATOR').first()
        self.assertIsNotNone(creator)

        # Login as creator
        with self.client:
            self.client.post('/auth/client/login', data={
                'email': creator.email,
                'password': 'password123'
            })

            # Create test submission
            sub = Submission(
                title="AI Harmonization Test",
                content_type="TEXT",
                raw_content="Our platform delves into deep data to crush the competition.",
                original_content="Our platform delves into deep data to crush the competition.",
                creator_id=creator.id,
                status="SCANNED",
                compliance_score=50,
                tone_score=50,
                claim_score=50,
                visual_score=100
            )
            db.session.add(sub)
            db.session.commit()

            # Execute AI harmonization
            resp = self.client.post(f'/scanner/ai-harmonize/{sub.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            # Verify updated submission in database
            updated_sub = db.session.get(Submission, sub.id)
            self.assertNotIn("delves into", updated_sub.raw_content)
            self.assertNotIn("crush the competition", updated_sub.raw_content)
            self.assertGreaterEqual(updated_sub.compliance_score, 90)

    def test_10_scanner_append_safe_harbor_route(self):
        """Verify that authenticated creator can append AI Safe Harbor disclaimers."""
        creator = User.query.filter_by(role='CREATOR').first()
        self.assertIsNotNone(creator)

        with self.client:
            self.client.post('/auth/client/login', data={
                'email': creator.email,
                'password': 'password123'
            })

            sub = Submission(
                title="Safe Harbor Test",
                content_type="TEXT",
                raw_content="Benchmark testing proves 99.9% uptime.",
                original_content="Benchmark testing proves 99.9% uptime.",
                creator_id=creator.id,
                status="SCANNED",
                compliance_score=60
            )
            db.session.add(sub)
            db.session.commit()

            resp = self.client.post(f'/scanner/append-safe-harbor/{sub.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            updated_sub = db.session.get(Submission, sub.id)
            self.assertIn("COMPLIANCE DISCLAIMER:", updated_sub.raw_content)
            self.assertIn("FTC", updated_sub.raw_content)


if __name__ == '__main__':
    unittest.main()
