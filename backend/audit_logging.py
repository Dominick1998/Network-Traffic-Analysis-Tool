import logging
from datetime import datetime

AUDIT_LOG_FILE = 'logs/audit.log'

# Set up the audit logger
audit_logger = logging.getLogger('audit_logger')
audit_logger.setLevel(logging.INFO)

# Create a file handler for the audit log
file_handler = logging.FileHandler(AUDIT_LOG_FILE)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the audit logger
audit_logger.addHandler(file_handler)

def log_event(user_id, event_type, description):
    """
    Log an audit event.

    Args:
        user_id (int): ID of the user who triggered the event.
        event_type (str): Type of the event (e.g., 'login', 'backup', 'db_modification').
        description (str): Detailed description of the event.

    Returns:
        None
    """
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    event_message = f"User {user_id} | Event: {event_type} | Description: {description} | Timestamp: {timestamp}"
    audit_logger.info(event_message)
