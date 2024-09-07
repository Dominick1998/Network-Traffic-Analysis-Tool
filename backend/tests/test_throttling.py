import unittest
from time import time
from backend.app import app

class ThrottlingTests(unittest.TestCase):
    """
    A set of tests for the throttling mechanism.
    """

    def setUp(self):
        """
        Set up the test client before each test case.
        """
        self.app = app.test_client()

    def test_throttling_delays_response(self):
        """
        Test that the throttling mechanism delays the response after exceeding the request limit.
        """
        start_time = time()
        for _ in range(11):
            self.app.get('/api/traffic')

        end_time = time()
        self.assertTrue(end_time - start_time > 5)  # Ensure there's a delay of at least 5 seconds

if __name__ == '__main__':
    unittest.main()
