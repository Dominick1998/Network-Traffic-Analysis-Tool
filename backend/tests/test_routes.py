import unittest
from unittest.mock import patch
from backend.app import app


class FullRouteTests(unittest.TestCase):
    """
    Comprehensive tests for all API routes in the Flask application.
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

    @patch('backend.routes.setup_log_rotation')
    def test_rotate_logs(self, mock_setup_log_rotation):
        """
        Test the log rotation endpoint.
        """
        mock_setup_log_rotation.return_value = True

        response = self.app.post(
            '/api/logs/rotate',
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Log rotation initiated successfully.'})

    @patch('backend.routes.create_backup')
    def test_create_backup(self, mock_create_backup):
        """
        Test creating a database backup.
        """
        mock_create_backup.return_value = {'message': 'Backup created successfully.'}

        response = self.app.post(
            '/api/backup/create',
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Backup created successfully.'})

    @patch('backend.routes.restore_backup')
    def test_restore_backup(self, mock_restore_backup):
        """
        Test restoring a database backup.
        """
        mock_restore_backup.return_value = {'message': 'Backup restored successfully.'}

        response = self.app.post(
            '/api/backup/restore',
            json={'backup_filename': 'backup_file_20231101.db'},
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Backup restored successfully.'})

    @patch('backend.routes.get_notifications')
    def test_get_notifications(self, mock_get_notifications):
        """
        Test retrieving user notifications.
        """
        mock_notifications = [
            {'message': 'Test notification 1', 'type': 'info', 'timestamp': '2023-11-01T12:00:00Z'},
            {'message': 'Test notification 2', 'type': 'warning', 'timestamp': '2023-11-01T14:00:00Z'}
        ]
        mock_get_notifications.return_value = mock_notifications

        response = self.app.get(
            '/api/notifications',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_notifications)

    @patch('backend.routes.create_incident_report')
    def test_create_incident_report(self, mock_create_incident_report):
        """
        Test creating an incident report.
        """
        mock_create_incident_report.return_value = {'message': 'Incident report created successfully.'}

        response = self.app.post(
            '/api/incidents',
            json={
                'title': 'Network Issue',
                'description': 'A major issue with network connectivity.',
                'severity': 'high'
            },
            headers={'Authorization': 'Bearer admin_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Incident report created successfully.'})

    @patch('backend.routes.evaluate_alerts')
    def test_evaluate_alerts(self, mock_evaluate_alerts):
        """
        Test evaluating alerts against traffic data.
        """
        mock_alerts = [
            {'name': 'High Traffic Alert', 'triggered': True, 'condition': 'traffic > 1000'},
            {'name': 'DDoS Alert', 'triggered': False, 'condition': 'connections > 500'}
        ]
        mock_evaluate_alerts.return_value = mock_alerts

        response = self.app.get(
            '/api/traffic',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['triggered_alerts'], mock_alerts)

    def test_invalid_token(self):
        """
        Test accessing a route with an invalid token.
        """
        response = self.app.get(
            '/api/traffic',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Invalid token!'})

    def test_rate_limit_exceeded(self):
        """
        Test exceeding the rate limit for a route.
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
