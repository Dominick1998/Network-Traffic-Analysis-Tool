import unittest
from unittest.mock import patch
from backend.email_notifications import send_email_notification

class EmailNotificationTests(unittest.TestCase):
    """
    A set of tests for the email notifications module.
    """

    @patch('smtplib.SMTP')
    def test_send_email_notification_success(self, mock_smtp):
        """
        Test sending an email notification successfully.
        """
        mock_smtp_instance = mock_smtp.return_value
        send_email_notification('test@example.com', 'Test Subject', 'Test message')
        mock_smtp_instance.sendmail.assert_called_with(
            'your-email@example.com',
            'test@example.com',
            mock_smtp_instance.sendmail.call_args[0][2]
        )

    @patch('smtplib.SMTP')
    def test_send_email_notification_failure(self, mock_smtp):
        """
        Test sending an email notification when an error occurs.
        """
        mock_smtp.side_effect = Exception('SMTP server error')
        with self.assertLogs(level='ERROR') as log:
            send_email_notification('test@example.com', 'Test Subject', 'Test message')
            self.assertIn('ERROR:root:Failed to send email', log.output)

if __name__ == '__main__':
    unittest.main()
