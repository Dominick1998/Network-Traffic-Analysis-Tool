import unittest
from backend.app import app
from unittest.mock import patch

class RouteTests(unittest.TestCase):
    """
    A set of tests for the API routes in the Flask application.
    """

    def setUp(self):
        """
        Set up the test client before each test case.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'Server is running'})

    @patch('backend.routes.get_traffic_data')
    def test_traffic_data(self, mock_get_traffic_data):
        """
        Test the traffic data endpoint with mock data.
        """
        mock_traffic_data = [
            {
                'source': '192.168.1.1',
                'destination': '192.168.1.2',
                'protocol': 'TCP',
                'length': 64,
                'timestamp': '2023-11-01T12:00:00Z'
            }
        ]
        mock_get_traffic_data.return_value = mock_traffic_data

        response = self.app.get('/api/traffic')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_traffic_data)

    @patch('backend.routes.login')
    def test_login_success(self, mock_login):
        """
        Test the login endpoint with valid credentials.
        """
        mock_login.return_value = {'token': 'valid_token'}

        response = self.app.post('/api/login', json={
            'username': 'admin',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    @patch('backend.routes.login')
    def test_login_failure(self, mock_login):
        """
        Test the login endpoint with invalid credentials.
        """
        mock_login.return_value = None

        response = self.app.post('/api/login', json={
            'username': 'admin',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'Invalid credentials'})

    @patch('backend.routes.get_system_health')
    def test_system_health_metrics(self, mock_get_system_health):
        """
        Test the system health endpoint with mock data.
        """
        mock_health_data = {
            'cpu_usage': '15%',
            'memory_usage': '40%',
            'disk_usage': '20%',
            'network_latency': '5ms'
        }
        mock_get_system_health.return_value = mock_health_data

        response = self.app.get('/api/system_health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_health_data)

    @patch('backend.routes.create_alert_route')
    def test_create_alert(self, mock_create_alert):
        """
        Test creating an alert via the API.
        """
        mock_create_alert.return_value = {'message': 'Alert created successfully'}

        response = self.app.post('/api/alerts', json={
            'name': 'High Traffic Alert',
            'condition': 'traffic > 1000',
            'action': 'Notify Admin'
        }, headers={'Authorization': 'Bearer valid_token'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Alert created successfully'})

    def test_invalid_route(self):
        """
        Test that invalid routes return a 404 error.
        """
        response = self.app.get('/invalid_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Resource not found'})

if __name__ == "__main__":
    unittest.main()
