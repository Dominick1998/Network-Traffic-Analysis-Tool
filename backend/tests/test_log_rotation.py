import unittest
import logging
from logging.handlers import RotatingFileHandler
import os

class LogRotationTests(unittest.TestCase):
    """
    A set of tests for the log rotation system.
    """

    def setUp(self):
        """
        Set up the test log rotation handler before each test case.
        """
        self.log_file = 'test_log.log'
        self.handler = RotatingFileHandler(self.log_file, maxBytes=100, backupCount=1)
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(self.handler)

    def tearDown(self):
        """
        Clean up log files after each test.
        """
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        if os.path.exists(f"{self.log_file}.1"):
            os.remove(f"{self.log_file}.1")

    def test_log_rotation(self):
        """
        Test that log rotation works when the log file reaches the maximum size.
        """
        logger = logging.getLogger()
        for _ in range(20):
            logger.info("This is a test log message.")

        # Check if the rotated log file exists
        self.assertTrue(os.path.exists(self.log_file))
        self.assertTrue(os.path.exists(f"{self.log_file}.1"))

if __name__ == '__main__':
    unittest.main()
