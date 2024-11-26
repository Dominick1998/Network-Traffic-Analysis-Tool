import unittest
from unittest.mock import patch
from backend.firewall_management import get_firewall_rules, add_firewall_rule, delete_firewall_rule


class FirewallManagementTests(unittest.TestCase):
    """
    A set of tests for the firewall management system.
    """

    @patch('backend.firewall_management.subprocess.run')
    def test_get_firewall_rules_linux(self, mock_subprocess):
        """
        Test retrieving firewall rules on a Linux system.
        """
        mock_subprocess.return_value.stdout = b"ACCEPT all -- anywhere anywhere"
        rules = get_firewall_rules()
        self.assertIn("ACCEPT all -- anywhere anywhere", rules)

    @patch('backend.firewall_management.subprocess.run')
    def test_add_firewall_rule_linux(self, mock_subprocess):
        """
        Test adding a firewall rule on a Linux system.
        """
        mock_subprocess.return_value.returncode = 0
        result = add_firewall_rule("INPUT -s 192.168.0.1 -j DROP")
        self.assertEqual(result['message'], 'Firewall rule added successfully.')

    @patch('backend.firewall_management.subprocess.run')
    def test_delete_firewall_rule_linux(self, mock_subprocess):
        """
        Test deleting a firewall rule on a Linux system.
        """
        mock_subprocess.return_value.returncode = 0
        result = delete_firewall_rule("INPUT -s 192.168.0.1 -j DROP")
        self.assertEqual(result['message'], 'Firewall rule deleted successfully.')

    @patch('backend.firewall_management.platform.system', return_value="Windows")
    @patch('backend.firewall_management.subprocess.run')
    def test_get_firewall_rules_windows(self, mock_subprocess, mock_platform):
        """
        Test retrieving firewall rules on a Windows system.
        """
        mock_subprocess.return_value.stdout = b"Rule Name: Allow All"
        rules = get_firewall_rules()
        self.assertIn("Rule Name: Allow All", rules)

    @patch('backend.firewall_management.platform.system', return_value="Windows")
    @patch('backend.firewall_management.subprocess.run')
    def test_add_firewall_rule_windows(self, mock_subprocess, mock_platform):
        """
        Test adding a firewall rule on a Windows system.
        """
        mock_subprocess.return_value.returncode = 0
        result = add_firewall_rule("name=BlockIP dir=in action=block remoteip=192.168.0.1")
        self.assertEqual(result['message'], 'Firewall rule added successfully.')

    @patch('backend.firewall_management.platform.system', return_value="Windows")
    @patch('backend.firewall_management.subprocess.run')
    def test_delete_firewall_rule_windows(self, mock_subprocess, mock_platform):
        """
        Test deleting a firewall rule on a Windows system.
        """
        mock_subprocess.return_value.returncode = 0
        result = delete_firewall_rule("name=BlockIP")
        self.assertEqual(result['message'], 'Firewall rule deleted successfully.')

    @patch('backend.firewall_management.platform.system', return_value="UnknownOS")
    def test_get_firewall_rules_unsupported_os(self, mock_platform):
        """
        Test retrieving firewall rules on an unsupported operating system.
        """
        rules = get_firewall_rules()
        self.assertEqual(rules, [])

    @patch('backend.firewall_management.platform.system', return_value="UnknownOS")
    def test_add_firewall_rule_unsupported_os(self, mock_platform):
        """
        Test adding a firewall rule on an unsupported operating system.
        """
        result = add_firewall_rule("rule")
        self.assertEqual(result['error'], 'Unsupported system')

    @patch('backend.firewall_management.platform.system', return_value="UnknownOS")
    def test_delete_firewall_rule_unsupported_os(self, mock_platform):
        """
        Test deleting a firewall rule on an unsupported operating system.
        """
        result = delete_firewall_rule("rule")
        self.assertEqual(result['error'], 'Unsupported system')


if __name__ == "__main__":
    unittest.main()
