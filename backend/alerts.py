from backend.database import get_db_session
from backend.models import Alert
from datetime import datetime

def create_alert(name, condition, action):
    """
    Create a new alert rule.

    Args:
        name (str): Name of the alert.
        condition (str): Condition for triggering the alert.
        action (str): Action to take when the alert is triggered.

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        new_alert = Alert(name=name, condition=condition, action=action, created_at=datetime.utcnow())
        session.add(new_alert)
        session.commit()
        return {'message': 'Alert created successfully'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to create alert: {e}"}
    finally:
        session.close()

def get_alerts():
    """
    Retrieve all defined alerts.

    Returns:
        list: List of alert rules.
    """
    session = get_db_session()
    try:
        alerts = session.query(Alert).all()
        return [
            {'id': alert.id, 'name': alert.name, 'condition': alert.condition, 'action': alert.action, 'created_at': alert.created_at}
            for alert in alerts
        ]
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []
    finally:
        session.close()

def delete_alert(alert_id):
    """
    Delete an alert by its ID.

    Args:
        alert_id (int): ID of the alert to delete.

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        alert = session.query(Alert).filter_by(id=alert_id).first()
        if not alert:
            return {'error': 'Alert not found'}

        session.delete(alert)
        session.commit()
        return {'message': 'Alert deleted successfully'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to delete alert: {e}"}
    finally:
        session.close()
