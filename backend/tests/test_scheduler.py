import unittest
import time
from threading import Event
from backend.scheduler import scheduled_task
from backend.routes import scheduler_pause_event

class SchedulerTests(unittest.TestCase):
    """
    A set of tests for the scheduler system.
    """

    def setUp(self):
        """
        Set up the scheduler before each test case.
        """
        self.task_ran = False
        self.task_interval = 1  # 1-second interval for testing

        def test_task():
            self.task_ran = True

        self.task_thread = scheduled_task(self.task_interval, test_task)

    def test_task_execution(self):
        """
        Test that a task runs at the expected interval.
        """
        time.sleep(2)
        self.assertTrue(self.task_ran)

    def test_scheduler_pause_resume(self):
        """
        Test that the scheduler pauses and resumes correctly.
        """
        scheduler_pause_event.set()  # Pause the scheduler
        self.task_ran = False
        time.sleep(2)
        self.assertFalse(self.task_ran)  # Task should not run while paused

        scheduler_pause_event.clear()  # Resume the scheduler
        time.sleep(2)
        self.assertTrue(self.task_ran)  # Task should run again after resume

if __name__ == '__main__':
    unittest.main()
