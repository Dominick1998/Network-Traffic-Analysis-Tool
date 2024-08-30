import unittest
from alembic import command
from alembic.config import Config

class MigrationTests(unittest.TestCase):
    """
    A set of tests to ensure that Alembic migrations are applied correctly.
    """

    def setUp(self):
        """
        Set up the Alembic configuration before each test case.
        """
        self.config = Config("alembic.ini")

    def test_migration_upgrade(self):
        """
        Test that the upgrade command runs successfully.
        """
        try:
            command.upgrade(self.config, 'head')
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Upgrade failed: {e}")

    def test_migration_downgrade(self):
        """
        Test that the downgrade command runs successfully.
        """
        try:
            command.downgrade(self.config, 'base')
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Downgrade failed: {e}")

if __name__ == '__main__':
    unittest.main()
