import logging
from datetime import datetime
from backend.database import get_db_session
from backend.models import UserActivity

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/audit.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_event(user_id, event_type, description, role="User"):
    """
    Log a significant event in the system with detailed context.

    Args:
        user_id (int): The ID of the user who triggered the event.
        event_type (str): The type of event (e.g., login, data_export).
        description (str): Detailed description of the event.
        role (str): The role of the user (e.g., Admin, User).
    """
    session = get_db_session()
    try:
        # Log in the database for persistent tracking
        activity = UserActivity(user_id=user_id, activity=description, timestamp=datetime.utcnow())
        session.add(activity)
        session.commit()

        # Log the action in the audit log file
        logger.info(f"User ID: {user_id} | Role: {role} | Event: {event_type} | Description: {description}")
    except Exception as e:
        logger.error(f"Failed to log event: {e}")
        session.rollback()
    finally:
        session.close()

def log_admin_action(user_id, action_description):
    """
    Specifically log actions taken by admin users for additional security tracking.

    Args:
        user_id (int): The ID of the admin user performing the action.
        action_description (str): Description of the action performed.
    """
    log_event(user_id, event_type="Admin Action", description=action_description, role="Admin")
