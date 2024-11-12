# backend/notification_system.py

from backend.database import get_db_session
from backend.models import Notification
from datetime import datetime

def create_notification(user_id, message, notification_type="info"):
    """
    Create a new notification for a user.

    Args:
        user_id (int): ID of the user to notify.
        message (str): The content of the notification.
        notification_type (str): Type of notification (e.g., 'info', 'warning', 'error').

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        notification = Notification(
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            created_at=datetime.utcnow()
        )
        session.add(notification)
        session.commit()
        return {'message': 'Notification created successfully.'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to create notification: {e}"}
    finally:
        session.close()

def get_notifications(user_id):
    """
    Retrieve notifications for a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        list: A list of notifications for the user.
    """
    session = get_db_session()
    try:
        notifications = session.query(Notification).filter_by(user_id=user_id).all()
        return [
            {
                'message': notification.message,
                'type': notification.notification_type,
                'timestamp': notification.created_at.isoformat()
            }
            for notification in notifications
        ]
    except Exception as e:
        return []
    finally:
        session.close()

def clear_notifications(user_id):
    """
    Clear all notifications for a user.

    Args:
        user_id (int): ID of the user whose notifications should be cleared.

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        session.query(Notification).filter_by(user_id=user_id).delete()
        session.commit()
        return {'message': 'Notifications cleared successfully.'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to clear notifications: {e}"}
    finally:
        session.close()
