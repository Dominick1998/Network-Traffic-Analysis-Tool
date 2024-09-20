import unittest
from datetime import datetime, timedelta
from backend.cleanup import delete_old_traffic_data
from backend.database import get_db_session
from backend.models import NetworkTraffic

class CleanupTests(unittest.TestCase):
    """
    A set of tests for the data cleanup functionality.
    """

    def setUp(self):
        """
        Set up the test database before each test case.
        """
        self.session = get_db_session()

        # Create some test traffic data
        old_traffic = NetworkTraffic(
            source="192.168.1.1",
            destination="192.168.1.2",
            protocol="TCP",
            length=100,
            timestamp=datetime.utcnow() - timedelta(days=40)
        )
        recent_traffic = NetworkTraffic(
            source="192.168.1.3",
            destination="192.168.1.4",
            protocol="UDP",
            length=200,
            timestamp=datetime.utcnow() - timedelta(days=10)
        )
        self.session.add(old_traffic)
        self.session.add(recent_traffic)
        self.session.commit()

    def tearDown(self):
        """
        Clean up the test database after each test case.
        """
        self.session.query(NetworkTraffic).delete()
        self.session.commit()
        self.session.close()

    def test_delete_old_traffic_data(self):
        """
        Test that old traffic data is deleted, and recent data is retained.
        """
        delete_old_traffic_data(30)

        remaining_traffic = self.session.query(NetworkTraffic).all()
        self.assertEqual(len(remaining_traffic), 1)
        self.assertEqual(remaining_traffic[0].source, "192.168.1.3")  # Recent traffic should remain

if __name__ == '__main__':
    unittest.main()
