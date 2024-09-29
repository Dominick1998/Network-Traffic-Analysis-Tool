from datetime import datetime
from backend.database import get_db_session
from backend.models import UserActivity

def log_user_activity(user_id, activity):
    """
    Log a user activity in the database.

    Args:
        user_id (int): The ID of the user performing the activity.
        activity (str): Description of the activity performed.
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
    except Exception as e:
        print(f"Error logging user activity: {e}")
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
