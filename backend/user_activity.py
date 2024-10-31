from datetime import datetime
from backend.database import get_db_session
from backend.models import UserActivity
import logging

# Initialize file logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/audit.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_user_activity(user_id, activity, role="User"):
    """
    Log a user activity in the database and optionally log sensitive activities to a file.

    Args:
        user_id (int): The ID of the user performing the activity.
        activity (str): Description of the activity performed.
        role (str): The role of the user (default is "User").
    """
    session = get_db_session()
    try:
        log_entry = UserActivity(
            user_id=user_id,
            activity=activity,
            timestamp=datetime.utcnow()
        )
        session.add(log_entry)
        session.commit()

        # Log to audit file if the activity is performed by an Admin or sensitive
        if role == "Admin" or "export" in activity.lower() or "login" in activity.lower():
            logger.info(f"User ID: {user_id} | Role: {role} | Activity: {activity}")
    except Exception as e:
        print(f"Error logging user activity: {e}")
        session.rollback()
    finally:
        session.close()

def log_event(user_id, event_type, description, role="User"):
    """
    Log a significant event with additional role context for security-sensitive actions.

    Args:
        user_id (int): The ID of the user who triggered the event.
        event_type (str): The type of event (e.g., 'login', 'data_export').
        description (str): Detailed description of the event.
        role (str): The role of the user (e.g., Admin, User).
    """
    session = get_db_session()
    try:
        # Log to database
        log_entry = UserActivity(
            user_id=user_id,
            activity=description,
            timestamp=datetime.utcnow()
        )
        session.add(log_entry)
        session.commit()

        # Log to audit log file for tracking security events
        logger.info(f"User ID: {user_id} | Role: {role} | Event: {event_type} | Description: {description}")
    except Exception as e:
        print(f"Error logging event: {e}")
        session.rollback()
    finally:
        session.close()

def get_user_activity_logs():
    """
    Retrieve all user activity logs from the database.

    Returns:
        list: A list of user activity log entries.
    """
    session = get_db_session()
    try:
        logs = session.query(UserActivity).all()
        activity_logs = [
            {
                'user_id': log.user_id,
                'activity': log.activity,
                'timestamp': log.timestamp.isoformat()
            }
            for log in logs
        ]
        return activity_logs
    except Exception as e:
        print(f"Error fetching user activity logs: {e}")
        return []
    finally:
        session.close()

def log_admin_action(user_id, action_description):
    """
    Specifically log actions taken by admin users in both database and file logs for additional security tracking.

    Args:
        user_id (int): The ID of the admin user performing the action.
        action_description (str): Description of the action performed.
    """
    log_event(user_id, event_type="Admin Action", description=action_description, role="Admin")
