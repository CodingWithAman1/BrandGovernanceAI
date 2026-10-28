import os
import time
import unittest
from app import create_app
from models import db, User

class TestPortalAndFirebaseAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False

    def setUp(self):
        # Create a fresh client with fresh session cookies for each test
        self.client = self.app.test_client()

    def test_01_anonymous_root_redirect(self):
        """Anonymous visit to / redirects to /login (Portal Gateway)"""
        resp = self.client.get('/', follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.headers['Location'] or '/portals' in resp.headers['Location'])

    def test_02_portal_selector_render(self):
        """Portal selector renders all 3 distinct portals"""
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        content = resp.data.decode('utf-8')
        self.assertIn('Client & Creator Portal', content)
        self.assertIn('Reviewer & Manager Desk', content)
        self.assertIn('Executive Admin Portal', content)
        self.assertIn('Aman Sharma', content)

    def test_03_client_direct_signup_and_dashboard(self):
        """New Client registers via /client/signup, gets CREATOR role, lands on /client/dashboard"""
        ts = int(time.time() * 1000)
        client_email = f"client_{ts}@synapsetest.com"
        signup_data = {
            'name': 'Test Client User',
            'email': client_email,
            'password': 'Password123!',
            'organization': 'Acme Corp',
            'department': 'Global Marketing'
        }
        resp = self.client.post('/client/signup', data=signup_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('/client' in resp.request.path or '/portal/client' in resp.request.path)

        # Verify role in DB
        with self.app.app_context():
            u = User.query.filter_by(email=client_email).first()
            self.assertIsNotNone(u)
            self.assertEqual(u.role, 'CREATOR')
            self.assertFalse(u.is_admin)

    def test_04_reviewer_direct_signup_and_dashboard(self):
        """New Reviewer registers via /reviewer/signup, gets REVIEWER role, lands on Reviewer Desk"""
        ts = int(time.time() * 1000)
        rev_email = f"reviewer_{ts}@synapsetest.com"
        signup_data = {
            'name': 'Test Legal Reviewer',
            'email': rev_email,
            'password': 'Password123!',
            'organization': 'BrandGuard Internal',
            'department': 'Regulatory Compliance'
        }
        resp = self.client.post('/reviewer/signup', data=signup_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('/reviewer' in resp.request.path or '/portal/reviewer' in resp.request.path)

        # Verify role in DB
        with self.app.app_context():
            u = User.query.filter_by(email=rev_email).first()
            self.assertIsNotNone(u)
            self.assertEqual(u.role, 'REVIEWER')
            self.assertFalse(u.is_admin)

    def test_05_client_cannot_access_reviewer_or_admin(self):
        """Client is strictly blocked from accessing Reviewer Queue and Admin Dashboard"""
        client_c = self.app.test_client()
        client_c.post('/client/login', data={'email': 'priya@inkloom.ai', 'password': 'password123'})
        
        # Attempt to access Reviewer Desk
        resp_rev = client_c.get('/reviewer/dashboard', follow_redirects=False)
        self.assertEqual(resp_rev.status_code, 302)
        self.assertTrue('/client' in resp_rev.headers['Location'])

        # Attempt to access Review Queue
        resp_q = client_c.get('/reviews/queue', follow_redirects=False)
        self.assertEqual(resp_q.status_code, 302)
        self.assertTrue('/client' in resp_q.headers['Location'])

        # Attempt to access Admin Dashboard
        resp_admin = client_c.get('/admin/dashboard', follow_redirects=False)
        self.assertEqual(resp_admin.status_code, 302)
        self.assertTrue('/client' in resp_admin.headers['Location'])

    def test_06_reviewer_cannot_access_admin_dashboard(self):
        """Reviewer is strictly blocked from accessing Admin Dashboard"""
        rev_c = self.app.test_client()
        rev_c.post('/reviewer/login', data={'email': 'elena@inkloom.ai', 'password': 'password123'})
        resp = rev_c.get('/admin/dashboard', follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/reviewer' in resp.headers['Location'])

    def test_07_admin_login_rejects_unauthorized_emails(self):
        """Admin portal login strictly blocks anyone other than aman@synapse.ai"""
        resp = self.client.post('/admin/login', data={'email': 'imposter@synapse.ai', 'password': 'password123'}, follow_redirects=True)
        self.assertIn('Access Denied', resp.data.decode('utf-8'))

    def test_08_sole_admin_login_success(self):
        """Aman Sharma logs into Admin Portal with full executive control"""
        resp = self.client.post('/admin/login', data={'email': 'aman@synapse.ai', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('/admin' in resp.request.path)
        content = resp.data.decode('utf-8')
        self.assertIn('EXECUTIVE COMMAND PORTAL', content)
        self.assertIn('Aman Sharma', content)
        self.assertIn('Platform User Governance', content)

    def test_09_firebase_sync_endpoint(self):
        """REST endpoint for client-side Firebase Auth token sync"""
        payload = {
            'id_token': 'dummy_firebase_id_token',
            'email': 'priya@inkloom.ai',
            'firebase_uid': 'firebase_uid_test_123',
            'portal': 'client'
        }
        resp = self.client.post('/auth/api/firebase-sync', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('user', {}).get('role'), 'CREATOR')

    def test_10_navbar_is_separate_per_role(self):
        """Verify navigation bar adapts strictly to each role's portal"""
        # 1. Client navbar: has Client Workspace, no Review Queue link
        client_c = self.app.test_client()
        client_c.post('/client/login', data={'email': 'priya@inkloom.ai', 'password': 'password123'})
        resp_c = client_c.get('/client/dashboard')
        c_html = resp_c.data.decode('utf-8')
        self.assertIn('CLIENT WORKSPACE', c_html)
        self.assertIn('My Client Dashboard', c_html)
        self.assertNotIn('Stage-Gate Queue', c_html)
        self.assertNotIn('Admin Command', c_html)

        # 2. Reviewer navbar: has Reviewer Desk & Stage-Gate Queue, no Studio
        rev_c = self.app.test_client()
        rev_c.post('/reviewer/login', data={'email': 'elena@inkloom.ai', 'password': 'password123'})
        resp_r = rev_c.get('/reviewer/dashboard')
        r_html = resp_r.data.decode('utf-8')
        self.assertIn('REVIEWER & LEGAL DESK', r_html)
        self.assertIn('Stage-Gate Queue', r_html)
        self.assertNotIn('My Client Dashboard', r_html)

        # 3. Admin navbar: has Admin Command & User Management
        admin_c = self.app.test_client()
        admin_c.post('/admin/login', data={'email': 'aman@synapse.ai', 'password': 'password123'})
        resp_a = admin_c.get('/admin/dashboard')
        a_html = resp_a.data.decode('utf-8')
        self.assertIn('ADMIN CONTROL PLANE', a_html)
        self.assertIn('Admin Command', a_html)

if __name__ == '__main__':
    unittest.main()
