from backend.database import get_db_session
from backend.models import Alert
from backend.notification_system import create_notification
from backend.audit_logging import log_event
from datetime import datetime
import json

def evaluate_alerts(traffic_data):
    """
    Evaluate network traffic data against active alert conditions and trigger alerts as needed.
    
    Args:
        traffic_data (list): List of network traffic entries.

    Returns:
        list: List of triggered alerts with details.
    """
    session = get_db_session()
    triggered_alerts = []

    try:
        active_alerts = session.query(Alert).all()
        for alert in active_alerts:
            condition = json.loads(alert.condition)
            action = alert.action

            # Check each condition in the alert against traffic data
            for entry in traffic_data:
                if evaluate_condition(entry, condition):
                    triggered_alerts.append({
                        'alert_id': alert.id,
                        'name': alert.name,
                        'triggered_at': datetime.utcnow().isoformat(),
                        'action': action
                    })

                    # Send notification for triggered alert
                    notification_message = f"Alert triggered: {alert.name}. Action: {action}"
                    create_notification(alert.id, notification_message, "alert")
                    
                    # Log alert event
                    log_event(
                        user_id=1,  # Replace with actual user ID if applicable
                        event_type="Alert Triggered",
                        description=notification_message
                    )

    except Exception as e:
        print(f"Error evaluating alerts: {e}")
    finally:
        session.close()

    return triggered_alerts

def evaluate_condition(entry, condition):
    """
    Evaluate a traffic entry against a condition.
    
    Args:
        entry (dict): A single traffic entry to evaluate.
        condition (dict): Condition to evaluate against.

    Returns:
        bool: True if the condition is met, False otherwise.
    """
    try:
        # Example condition logic: simple comparisons
        for key, value in condition.items():
            if key in entry and entry[key] != value:
                return False
        return True
    except Exception as e:
        print(f"Error evaluating condition: {e}")
        return False
