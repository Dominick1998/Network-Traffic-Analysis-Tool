import unittest
from backend.security import validate_ip_address, sanitize_input

class SecurityTests(unittest.TestCase):
    """
    A set of tests for the security-related functions.
    """

    def test_validate_ip_address(self):
        """
        Test the IP address validation function.
        """
        self.assertTrue(validate_ip_address("192.168.1.1"))
        self.assertFalse(validate_ip_address("256.256.256.256"))
        self.assertFalse(validate_ip_address("not.an.ip"))

    def test_sanitize_input(self):
        """
        Test the input sanitization function.
        """
        self.assertEqual(sanitize_input("valid-input_123"), "valid-input_123")
        self.assertEqual(sanitize_input("<script>alert('xss')</script>"), "scriptalertxssscript")
        self.assertEqual(sanitize_input("normal_string!@#$"), "normal_string")

if __name__ == '__main__':
    unittest.main()
