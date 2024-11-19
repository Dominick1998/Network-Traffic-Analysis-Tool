import unittest
from unittest.mock import patch
from backend.app import app


class ExtendedRouteTests(unittest.TestCase):
    """
    Extended tests for the API routes in the Flask application.
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
    def test_traffic_data_unauthenticated(self, mock_get_traffic_data):
        """
        Test the traffic data endpoint without authentication.
        """
        response = self.app.get('/api/traffic')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token is missing!'})

    @patch('backend.routes.get_traffic_data')
    def test_traffic_data_authenticated(self, mock_get_traffic_data):
        """
        Test the traffic data endpoint with a valid token.
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

        response = self.app.get(
            '/api/traffic',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['traffic_data'], mock_traffic_data)

    @patch('backend.routes.get_system_health')
    def test_system_health_unauthenticated(self, mock_get_system_health):
        """
        Test the system health endpoint without authentication.
        """
        response = self.app.get('/api/system_health')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token is missing!'})

    @patch('backend.routes.get_system_health')
    def test_system_health_authenticated(self, mock_get_system_health):
        """
        Test the system health endpoint with a valid token.
        """
        mock_health_data = {
            'cpu_usage': '15%',
            'memory_usage': '40%',
            'disk_usage': '20%',
            'network_latency': '5ms'
        }
        mock_get_system_health.return_value = mock_health_data

        response = self.app.get(
            '/api/system_health',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_health_data)

    @patch('backend.routes.create_alert_route')
    def test_create_alert_no_auth(self, mock_create_alert):
        """
        Test creating an alert without a valid token.
        """
        response = self.app.post(
            '/api/alerts',
            json={
                'name': 'High Traffic Alert',
                'condition': 'traffic > 1000',
                'action': 'Notify Admin'
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token is missing!'})

    @patch('backend.routes.create_alert_route')
    def test_create_alert_admin(self, mock_create_alert):
        """
        Test creating an alert with admin privileges.
        """
        mock_create_alert.return_value = {'message': 'Alert created successfully'}

        response = self.app.post(
            '/api/alerts',
            json={
                'name': 'High Traffic Alert',
                'condition': 'traffic > 1000',
                'action': 'Notify Admin'
            },
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Alert created successfully'})

    @patch('backend.routes.get_anomalous_traffic')
    def test_anomalies_data(self, mock_get_anomalous_traffic):
        """
        Test the anomalies data endpoint.
        """
        mock_anomalies = [
            {
                'source': '192.168.1.1',
                'destination': '10.0.0.1',
                'protocol': 'TCP',
                'length': 128,
                'timestamp': '2023-11-01T12:30:00Z',
                'anomaly_type': 'Suspicious Activity'
            }
        ]
        mock_get_anomalous_traffic.return_value = mock_anomalies

        response = self.app.get(
            '/api/anomalies',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_anomalies)

    def test_invalid_route(self):
        """
        Test that invalid routes return a 404 error.
        """
        response = self.app.get('/nonexistent_endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Resource not found'})

    def test_rate_limiting(self):
        """
        Simulate hitting the same endpoint multiple times to test rate limiting.
        """
        for _ in range(6):  # Assuming a rate limit of 5 requests per minute
            response = self.app.get(
                '/api/traffic',
                headers={'Authorization': 'Bearer valid_token'}
            )
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.json, {'message': 'Rate limit exceeded. Try again later.'})


if __name__ == "__main__":
    unittest.main()
