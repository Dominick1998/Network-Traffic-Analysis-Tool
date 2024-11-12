from backend.database import get_db_session
from backend.models import Notification
from datetime import datetime

def create_notification(user_id, message, notification_type="info", alert_id=None):
    """
    Create a new notification for a user or for an alert.

    Args:
        user_id (int): ID of the user to notify. If for an alert, set user_id to None.
        message (str): The content of the notification.
        notification_type (str): Type of notification (e.g., 'info', 'warning', 'error').
        alert_id (int): ID of the alert that triggered the notification (optional).

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        notification = Notification(
            user_id=user_id,
            alert_id=alert_id,
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

def get_notifications(user_id=None, alert_id=None):
    """
    Retrieve notifications for a specific user or alert.

    Args:
        user_id (int): ID of the user (optional, if not filtering by user).
        alert_id (int): ID of the alert (optional, if not filtering by alert).

    Returns:
        list: A list of notifications for the user or alert.
    """
    session = get_db_session()
    try:
        query = session.query(Notification)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if alert_id is not None:
            query = query.filter_by(alert_id=alert_id)

        notifications = query.all()
        return [
            {
                'message': notification.message,
                'type': notification.notification_type,
                'timestamp': notification.created_at.isoformat()
            }
            for notification in notifications
        ]
    except Exception as e:
        print(f"Error retrieving notifications: {e}")
        return []
    finally:
        session.close()

def clear_notifications(user_id=None, alert_id=None):
    """
    Clear notifications for a specific user or alert.

    Args:
        user_id (int): ID of the user (optional).
        alert_id (int): ID of the alert (optional).

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        query = session.query(Notification)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if alert_id is not None:
            query = query.filter_by(alert_id=alert_id)

        deleted_count = query.delete()
        session.commit()
        return {'message': f'{deleted_count} notifications cleared.'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to clear notifications: {e}"}
    finally:
        session.close()
