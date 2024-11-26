import unittest
from backend.notification_system import create_notification, get_notifications
from backend.database import get_db_session
from backend.models import Notification
from datetime import datetime

class NotificationSystemTests(unittest.TestCase):
    """
    A set of tests for the notification system.
    """

    def setUp(self):
        """
        Set up a test database session and sample user data.
        """
        self.session = get_db_session()
        self.test_user_id = 1

        # Clean up notifications for the test user
        self.session.query(Notification).filter_by(user_id=self.test_user_id).delete()
        self.session.commit()

    def tearDown(self):
        """
        Tear down the test environment by closing the session.
        """
        self.session.query(Notification).filter_by(user_id=self.test_user_id).delete()
        self.session.commit()
        self.session.close()

    def test_create_notification(self):
        """
        Test creating a new notification.
        """
        result = create_notification(
            user_id=self.test_user_id,
            message="Test notification",
            notification_type="info"
        )
        self.assertEqual(result['message'], 'Notification created successfully.')

        # Verify notification in the database
        notification = self.session.query(Notification).filter_by(user_id=self.test_user_id).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.message, "Test notification")
        self.assertEqual(notification.notification_type, "info")

    def test_get_notifications(self):
        """
        Test retrieving notifications for a user.
        """
        # Create sample notifications
        create_notification(self.test_user_id, "Notification 1", "info")
        create_notification(self.test_user_id, "Notification 2", "warning")

        notifications = get_notifications(self.test_user_id)
        self.assertEqual(len(notifications), 2)

        messages = [n['message'] for n in notifications]
        self.assertIn("Notification 1", messages)
        self.assertIn("Notification 2", messages)

    def test_create_and_retrieve_notifications(self):
        """
        Combined test for creating and retrieving notifications.
        """
        create_notification(self.test_user_id, "Notification Test Combined", "error")

        notifications = get_notifications(self.test_user_id)
        self.assertEqual(len(notifications), 1)

        notification = notifications[0]
        self.assertEqual(notification['message'], "Notification Test Combined")
        self.assertEqual(notification['type'], "error")

if __name__ == "__main__":
    unittest.main()
