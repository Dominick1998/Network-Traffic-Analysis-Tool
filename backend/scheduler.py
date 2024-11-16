import time
from threading import Thread, Event
from backend.log_rotation import setup_log_rotation
from backend.email_notifications import send_email_notification
from backend.cleanup import delete_old_traffic_data
from backend.alerts import evaluate_alerts
from backend.system_health_monitoring import log_system_health

# Global pause event for the scheduler
scheduler_pause_event = Event()
scheduler_pause_event.set()  # Initially allow tasks to run

def start_scheduler():
    """
    Start the scheduler and set up periodic tasks.
    """
    print("Starting scheduler...")
    scheduled_task(86400, send_daily_summary)  # Daily summary task (24 hours)
    scheduled_task(3600, rotate_logs_task)     # Log rotation task (1 hour)
    scheduled_task(604800, cleanup_task)       # Cleanup task (7 days)
    scheduled_task(900, evaluate_alerts_task)  # Alert evaluation task (15 minutes)
    scheduled_task(600, health_monitor_task)   # System health monitoring task (10 minutes)

def scheduled_task(interval, task_function):
    """
    Run a given task at a fixed interval in a separate thread, with pause/resume support.
    Args:
        interval (int): Time interval between task executions in seconds.
        task_function (function): The function to execute as a scheduled task.
    """
    def run_task():
        while True:
            if not scheduler_pause_event.is_set():
                print(f"Executing task: {task_function.__name__}")
                try:
                    task_function()
                except Exception as e:
                    print(f"Error executing task {task_function.__name__}: {e}")
            time.sleep(interval)

    task_thread = Thread(target=run_task)
    task_thread.daemon = True
    task_thread.start()

def send_daily_summary():
    """
    Task that sends a daily summary email to administrators.
    """
    try:
        send_email_notification(
            to_email="admin@example.com",
            subject="Daily Traffic Summary",
            message="Here is your daily network traffic summary..."
        )
        print("Daily summary email sent successfully.")
    except Exception as e:
        print(f"Error in send_daily_summary: {e}")

def rotate_logs_task():
    """
    Task to rotate logs periodically.
    """
    try:
        setup_log_rotation()
        print("Log rotation completed successfully.")
    except Exception as e:
        print(f"Error in rotate_logs_task: {e}")

def cleanup_task():
    """
    Task to clean up old traffic data and notify admin on completion.
    """
    try:
        delete_old_traffic_data(30)  # Delete traffic data older than 30 days
        print("Traffic data cleanup completed successfully.")
    except Exception as e:
        print(f"Error in cleanup_task: {e}")

def evaluate_alerts_task():
    """
    Task to evaluate alerts periodically.
    """
    try:
        evaluate_alerts()
        print("Alert evaluation completed successfully.")
    except Exception as e:
        print(f"Error in evaluate_alerts_task: {e}")

def health_monitor_task():
    """
    Task to log system health metrics periodically.
    """
    try:
        log_system_health()
        print("System health metrics logged successfully.")
    except Exception as e:
        print(f"Error in health_monitor_task: {e}")

def pause_scheduler():
    """
    Pause the execution of all scheduled tasks.
    """
    scheduler_pause_event.clear()
    print("Scheduler paused.")

def resume_scheduler():
    """
    Resume the execution of all scheduled tasks.
    """
    scheduler_pause_event.set()
    print("Scheduler resumed.")
