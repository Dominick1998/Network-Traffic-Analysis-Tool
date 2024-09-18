import time
from threading import Thread
from backend.log_rotation import setup_log_rotation
from backend.email_notifications import send_email_notification
from backend.routes import scheduler_pause_event

def scheduled_task(interval, task_function):
    """
    Run a given task at a fixed interval in a separate thread, with pause/resume support.
    """
    def run_task():
        while True:
            if not scheduler_pause_event.is_set():
                task_function()
            time.sleep(interval)

    task_thread = Thread(target=run_task)
    task_thread.daemon = True
    task_thread.start()

def send_daily_summary():
    """
    Task that sends a daily summary email to administrators.
    """
    # Here you could query your database and summarize traffic
    send_email_notification(
        to_email='admin@example.com',
        subject='Daily Traffic Summary',
        message='Here is your daily network traffic summary...'
    )

def rotate_logs_task():
    """
    Task to rotate logs periodically.
    """
    setup_log_rotation()

def start_scheduler():
    """
    Start the scheduler and set up periodic tasks.
    """
    # Set up periodic tasks (e.g., send daily summary every 24 hours and rotate logs every hour)
    scheduled_task(86400, send_daily_summary)  # Daily summary task
    scheduled_task(3600, rotate_logs_task)     # Log rotation task
