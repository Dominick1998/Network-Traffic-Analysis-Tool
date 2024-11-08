from datetime import datetime
from backend.database import get_db_session
from backend.models import Alert
from backend.email_alerts import send_custom_alert_email
from backend.audit_logging import log_admin_action

# Default threshold for high traffic alerts (can be made configurable)
DEFAULT_HIGH_TRAFFIC_THRESHOLD = 500  # Example in Mbps

def create_alert(name, condition, action, threshold=DEFAULT_HIGH_TRAFFIC_THRESHOLD):
    """
    Create a new alert rule with a customizable threshold.

    Args:
        name (str): Name of the alert.
        condition (str): Condition to trigger the alert (e.g., 'High Traffic').
        action (str): Action to take when alert is triggered (e.g., 'Email Notification').
        threshold (int): Threshold for triggering the alert (default: high traffic at 500 Mbps).

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        alert = Alert(
            name=name,
            condition=condition,
            action=action,
            threshold=threshold,
            created_at=datetime.utcnow()
        )
        session.add(alert)
        session.commit()
        
        log_admin_action(user_id=1, action_description=f"Created alert '{name}' with condition '{condition}'")
        send_custom_alert_email(
            alert_name=name,
            condition=condition,
            action=action,
            threshold=threshold,
            message=f"Alert '{name}' created with condition '{condition}' and threshold {threshold}."
        )
        
        return {'message': 'Alert created successfully.'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to create alert: {e}"}
    finally:
        session.close()

def evaluate_alerts(traffic_data):
    """
    Evaluate all alerts based on current traffic data and trigger any that meet conditions.

    Args:
        traffic_data (list): List of current traffic data.
    
    Returns:
        list: List of triggered alerts with actions taken.
    """
    session = get_db_session()
    triggered_alerts = []
    try:
        alerts = session.query(Alert).all()
        
        for alert in alerts:
            if alert.condition == "High Traffic" and is_high_traffic(traffic_data, alert.threshold):
                triggered_alerts.append({
                    'name': alert.name,
                    'action': alert.action,
                    'condition': alert.condition
                })
                send_custom_alert_email(
                    alert_name=alert.name,
                    condition=alert.condition,
                    action=alert.action,
                    message=f"Alert '{alert.name}' triggered for {alert.condition}. Taking action: {alert.action}."
                )
                log_admin_action(user_id=1, action_description=f"Triggered alert '{alert.name}'")
                
        return triggered_alerts
    except Exception as e:
        print(f"Error evaluating alerts: {e}")
        return []
    finally:
        session.close()

def is_high_traffic(traffic_data, threshold):
    """
    Check if current traffic rate exceeds the specified threshold.

    Args:
        traffic_data (list): Current network traffic data.
        threshold (int): Traffic rate threshold in Mbps.

    Returns:
        bool: True if traffic rate exceeds threshold, else False.
    """
    current_rate = sum(entry['length'] for entry in traffic_data) / len(traffic_data)
    return current_rate > threshold
