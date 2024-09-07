import unittest
import logging
from io import StringIO
from backend.app import app

class LoggingMiddlewareTests(unittest.TestCase):
    """
    A set of tests for the logging middleware.
    """

    def setUp(self):
        """
        Set up the test client and logging handler before each test case.
        """
        self.app = app.test_client()
        self.log_output = StringIO()
        logging.getLogger().handlers = [logging.StreamHandler(self.log_output)]

    def test_log_request(self):
        """
        Test that a request is logged correctly.
        """
        self.app.get('/api/health')
        self.assertIn('Request: GET', self.log_output.getvalue())

    def test_log_response(self):
        """
        Test that a response is logged correctly.
        """
        self.app.get('/api/health')
        self.assertIn('Response: 200', self.log_output.getvalue())

if __name__ == '__main__':
    unittest.main()
