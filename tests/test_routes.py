import unittest
from backend.app import app
from backend.auth import generate_token

class RouteTests(unittest.TestCase):
    """
    A set of tests for the API routes in the Flask application.
    """

    def setUp(self):
        """
        Set up the test client and a mock JWT token before each test case.
        """
        self.app = app.test_client()
        self.app.testing = True
        self.mock_token = generate_token(user_id=1, role="Admin")  # Mock token for testing

    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'Server is running'})

    def test_login_success(self):
        """
        Test login with valid credentials.
        """
        response = self.app.post('/api/login', json={'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_failure(self):
        """
        Test login with invalid credentials.
        """
        response = self.app.post('/api/login', json={'username': 'admin', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'Invalid credentials'})

    def test_get_traffic_data_unauthenticated(self):
        """
        Test retrieving traffic data without authentication.
        """
        response = self.app.get('/api/traffic')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token is missing!'})

    def test_get_traffic_data_authenticated(self):
        """
        Test retrieving traffic data with a valid token.
        """
        response = self.app.get('/api/traffic', headers={'Authorization': self.mock_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['traffic_data'], list)
        self.assertIn('threats', response.json)

    def test_create_alert_no_permission(self):
        """
        Test creating an alert without admin permissions.
        """
        token = generate_token(user_id=2, role="User")  # Non-admin user
        response = self.app.post('/api/alerts', headers={'Authorization': token}, json={
            'name': 'Test Alert',
            'condition': 'length > 1000',
            'action': 'Notify Admin'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Access denied: Insufficient privileges!'})

    def test_create_alert_with_permission(self):
        """
        Test creating an alert with admin permissions.
        """
        response = self.app.post('/api/alerts', headers={'Authorization': self.mock_token}, json={
            'name': 'Test Alert',
            'condition': 'length > 1000',
            'action': 'Notify Admin'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_get_system_health(self):
        """
        Test retrieving system health metrics.
        """
        response = self.app.get('/api/system_health', headers={'Authorization': self.mock_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('cpu_usage', response.json)
        self.assertIn('memory_usage', response.json)

if __name__ == "__main__":
    unittest.main()
