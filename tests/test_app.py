import unittest
from backend.app import app

class BasicTests(unittest.TestCase):
    """
    A set of basic tests for the Flask application.
    """

    def setUp(self):
        """
        Set up the test client before each test case.
        """
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'Server is running'})

    def test_traffic_data(self):
        """
        Test the traffic data endpoint.
        """
        response = self.app.get('/api/traffic')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

if __name__ == "__main__":
    unittest.main()