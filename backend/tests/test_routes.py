import unittest
from unittest.mock import patch
from backend.app import app


class ExtendedRouteTests(unittest.TestCase):
    """
    Extended tests for all API routes in the Flask application.
    """

    def setUp(self):
        """
        Set up the test client before each test case.
        """
        self.app = app.test_client()
        self.app.testing = True

    # ---------- Health Check ----------
    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'Server is running'})

    # ---------- Firewall Management ----------
    @patch('backend.routes.get_firewall_rules')
    def test_get_firewall_rules(self, mock_get_firewall_rules):
        """
        Test retrieving firewall rules.
        """
        mock_rules = [
            "Rule 1: Allow 192.168.1.1",
            "Rule 2: Deny 10.0.0.1"
        ]
        mock_get_firewall_rules.return_value = mock_rules

        response = self.app.get(
            '/api/firewall/rules',
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'rules': mock_rules})

    @patch('backend.routes.add_firewall_rule')
    def test_add_firewall_rule(self, mock_add_firewall_rule):
        """
        Test adding a new firewall rule.
        """
        mock_add_firewall_rule.return_value = {'message': 'Firewall rule added successfully.'}

        response = self.app.post(
            '/api/firewall/rules',
            json={'rule': 'Allow 192.168.1.1'},
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Firewall rule added successfully.'})

    @patch('backend.routes.delete_firewall_rule')
    def test_delete_firewall_rule(self, mock_delete_firewall_rule):
        """
        Test deleting a firewall rule.
        """
        mock_delete_firewall_rule.return_value = {'message': 'Firewall rule deleted successfully.'}

        response = self.app.delete(
            '/api/firewall/rules',
            json={'rule': 'Deny 10.0.0.1'},
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Firewall rule deleted successfully.'})

    # ---------- Anomaly Logs ----------
    @patch('backend.routes.get_anomaly_logs')
    def test_get_anomaly_logs(self, mock_get_anomaly_logs):
        """
        Test retrieving anomaly logs.
        """
        mock_logs = [
            {'source_ip': '192.168.1.1', 'destination_ip': '10.0.0.1', 'protocol': 'TCP', 'length': 1500, 'timestamp': '2023-11-01T12:00:00Z'},
            {'source_ip': '172.16.0.1', 'destination_ip': '192.168.1.1', 'protocol': 'UDP', 'length': 200, 'timestamp': '2023-11-01T13:00:00Z'}
        ]
        mock_get_anomaly_logs.return_value = mock_logs

        response = self.app.get(
            '/api/anomaly_logs',
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_logs)

    # ---------- System Health Monitoring ----------
    @patch('backend.routes.get_system_health')
    def test_get_system_health(self, mock_get_system_health):
        """
        Test retrieving system health metrics.
        """
        mock_health_data = {
            'cpu_usage': 25.0,
            'memory_usage': 50.0,
            'disk_usage': 70.0,
            'network_latency': 10.0
        }
        mock_get_system_health.return_value = mock_health_data

        response = self.app.get(
            '/api/system_health',
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_health_data)

    # ---------- Role-Based Access Control ----------
    def test_access_denied_for_user_role(self):
        """
        Test that endpoints requiring 'Admin' role return access denied for regular users.
        """
        response = self.app.post(
            '/api/firewall/rules',
            json={'rule': 'Allow 192.168.1.1'},
            headers={'Authorization': 'Bearer user_token'}  # Simulating a regular user token
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Access denied: Insufficient privileges!'})

    def test_access_granted_for_admin_role(self):
        """
        Test that endpoints requiring 'Admin' role work for administrators.
        """
        response = self.app.post(
            '/api/firewall/rules',
            json={'rule': 'Allow 192.168.1.1'},
            headers={'Authorization': 'Bearer admin_token'}  # Simulating an admin token
        )
        self.assertEqual(response.status_code, 200)

    # ---------- Edge Cases ----------
    def test_missing_authorization_header(self):
        """
        Test that endpoints return appropriate error for missing Authorization header.
        """
        response = self.app.get('/api/traffic')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token is missing!'})

    def test_expired_token(self):
        """
        Test accessing an endpoint with an expired token.
        """
        response = self.app.get(
            '/api/traffic',
            headers={'Authorization': 'Bearer expired_token'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token has expired!'})

    def test_invalid_json_payload(self):
        """
        Test an endpoint with invalid JSON payload.
        """
        response = self.app.post(
            '/api/incidents',
            data="invalid_payload",  # Sending invalid JSON
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 400)  # Expecting a bad request error
        self.assertEqual(response.json, {'error': 'Invalid input data format'})


if __name__ == "__main__":
    unittest.main()
