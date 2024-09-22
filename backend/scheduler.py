import time
from threading import Thread
from backend.log_rotation import setup_log_rotation
from backend.email_notifications import send_email_notification
from backend.routes import scheduler_pause_event
from backend.cleanup import delete_old_traffic_data
from backend.notifications import send_admin_notification

def start_scheduler():
    """
    Start the scheduler and set up periodic tasks.
    """
    # Set up periodic tasks (e.g., send daily summary every 24 hours, rotate logs every hour, cleanup every 7 days)
    scheduled_task(86400, send_daily_summary)  # Daily summary task
    scheduled_task(3600, rotate_logs_task)     # Log rotation task
    scheduled_task(604800, lambda: delete_old_traffic_data(30))  # Cleanup task, runs every 7 days

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
    try:
        send_admin_notification(
            subject="Daily Traffic Summary",
            message="Here is your daily network traffic summary..."
        )
    except Exception as e:
        send_admin_notification(
            subject="Error in Daily Summary Task",
            message=f"An error occurred while sending the daily summary: {e}"
        )

def rotate_logs_task():
    """
    Task to rotate logs periodically, with notification on completion.
    """
    try:
        setup_log_rotation()
        send_admin_notification(
            subject="Log Rotation Complete",
            message="Log rotation was completed successfully."
        )
    except Exception as e:
        send_admin_notification(
            subject="Error in Log Rotation Task",
            message=f"An error occurred during log rotation: {e}"
        )

def cleanup_task():
    """
    Task to clean up old traffic data and notify admin on completion.
    """
    try:
        delete_old_traffic_data(30)
        send_admin_notification(
            subject="Traffic Data Cleanup Complete",
            message="Old traffic data older than 30 days was deleted successfully."
        )
    except Exception as e:
        send_admin_notification(
            subject="Error in Traffic Data Cleanup Task",
            message=f"An error occurred while cleaning up old traffic data: {e}"
        )
        
def start_scheduler():
    """
    Start the scheduler and set up periodic tasks.
    """
    # Set up periodic tasks (e.g., send daily summary every 24 hours and rotate logs every hour)
    scheduled_task(86400, send_daily_summary)  # Daily summary task
    scheduled_task(3600, rotate_logs_task)     # Log rotation task
