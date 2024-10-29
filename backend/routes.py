from flask import Blueprint, jsonify, request, send_file
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required, role_required
from backend.rate_limiter import rate_limit
from backend.throttling import throttle
from backend.email_notifications import send_email_notification
from backend.anomaly_detection import detect_anomalies
from backend.network_summary import generate_network_summary
from backend.cleanup import delete_old_traffic_data
from backend.export import export_to_csv, export_to_json
from backend.import_data import import_from_csv
from backend.logs import get_logs, download_logs
from backend.rate_limiting import rate_limit
from backend.threat_detection import detect_ddos, detect_port_scan, detect_suspicious_ip_ranges
from backend.performance_monitoring import get_cpu_usage, get_memory_usage, track_response_time
from backend.firewall_rules import apply_firewall_rule, delete_firewall_rule
from backend.user_activity import log_user_activity, get_user_activity_logs
from backend.alerts import create_alert, get_alerts, delete_alert
from backend.anomaly_logging import log_anomaly, get_anomaly_logs
from backend.email_alerts import send_custom_alert_email
from backend.notification_system import create_notification, get_notifications
from backend.incident_reporting import create_incident_report, get_incident_reports
from backend.system_health_monitoring import get_system_health
from backend.log_rotation import setup_log_rotation
from backend.backup_management import create_backup, restore_backup
from backend.audit_logging import log_event
from backend.security_monitoring import detect_unauthorized_access, detect_ddos, log_security_event
from backend.firewall_management import get_firewall_rules, add_firewall_rule, delete_firewall_rule
from backend.performance_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_latency
from backend.notification_center import add_notification, get_notifications, clear_notifications

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return jsonify({'status': 'Server is running'}), 200

@api_bp.route('/api/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate the user and return a JWT token.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = authenticate_user(username, password)  # Replace with actual auth logic

    if user:
        token = generate_token(user.id, user.role)
        log_user_activity(user_id=user.id, activity="User logged in")
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

@api_bp.route('/api/traffic', methods=['GET'])
@token_required
@rate_limit(max_requests=5, window_seconds=60)
@throttle(max_requests=10, slowdown_seconds=5)
def get_traffic_data():
    """
    Retrieve the network traffic data from the database.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()
        traffic_list = [{
            'source': sanitize_input(traffic.source),
            'destination': sanitize_input(traffic.destination),
            'protocol': sanitize_input(traffic.protocol),
            'length': traffic.length,
            'timestamp': traffic.timestamp.isoformat(),
            'destination_port': traffic.destination_port
        } for traffic in traffic_data]

        return jsonify(traffic_list), 200
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return jsonify({'error': 'Unable to fetch traffic data'}), 500
    finally:
        session.close()

@api_bp.route('/api/anomalies', methods=['GET'])
@token_required
@rate_limit(max_requests=5, window_seconds=60)
@throttle(max_requests=10, slowdown_seconds=5)
def get_anomalous_traffic():
    """
    Retrieve anomalous network traffic based on anomaly detection.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()
        traffic_list = [{
            'source': sanitize_input(traffic.source),
            'destination': sanitize_input(traffic.destination),
            'protocol': sanitize_input(traffic.protocol),
            'length': traffic.length,
            'timestamp': traffic.timestamp.isoformat()
        } for traffic in traffic_data]

        anomalies = detect_anomalies(traffic_list)
        for anomaly in anomalies:
            log_anomaly(anomaly['source'], anomaly['destination'], anomaly['protocol'], anomaly['length'], "Anomalous Traffic")

        if anomalies:
            send_email_notification(to_email="admin@example.com", subject="Anomalous Network Traffic Detected",
                                    message=f"Anomalies detected in network traffic: {len(anomalies)} anomalies found.")
        return jsonify(anomalies), 200
    except Exception as e:
        print(f"Error fetching anomalous traffic: {e}")
        return jsonify({'error': 'Unable to fetch anomalous traffic'}), 500
    finally:
        session.close()

@api_bp.route('/api/alerts', methods=['POST'])
@token_required
@role_required("Admin")
def create_alert_route():
    """
    Create a new alert rule.
    Restricted to Admin role.
    """
    data = request.json
    name = data.get('name')
    condition = data.get('condition')
    action = data.get('action')
    result = create_alert(name=name, condition=condition, action=action)
    if 'message' in result:
        send_custom_alert_email(alert_name=name, condition=condition, action=action)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts_route():
    """
    Retrieve all alert rules.
    """
    try:
        alerts = get_alerts()
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch alerts'}), 500

@api_bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@token_required
@role_required("Admin")
def delete_alert_route(alert_id):
    """
    Delete an alert rule by its ID.
    Restricted to Admin role.
    """
    result = delete_alert(alert_id=alert_id)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/export/csv', methods=['GET'])
@token_required
def get_csv_export():
    """
    Export network traffic data as CSV.
    """
    log_user_activity(user_id=request.user_id, activity="User exported traffic data as CSV")
    return export_to_csv()

@api_bp.route('/api/export/json', methods=['GET'])
@token_required
def get_json_export():
    """
    Export network traffic data as JSON.
    """
    log_user_activity(user_id=request.user_id, activity="User exported traffic data as JSON")
    return export_to_json()

@api_bp.route('/api/firewall/rules', methods=['POST'])
@token_required
@role_required("Admin")
def create_firewall_rule():
    """
    Add a new firewall rule.
    Restricted to Admin role.
    """
    data = request.json
    rule = data.get('rule')
    result = add_firewall_rule(rule)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/firewall/rules', methods=['DELETE'])
@token_required
@role_required("Admin")
def remove_firewall_rule():
    """
    Delete an existing firewall rule.
    Restricted to Admin role.
    """
    data = request.json
    rule = data.get('rule')
    result = delete_firewall_rule(rule)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/notifications', methods=['GET'])
@token_required
def list_notifications():
    """
    Retrieve all notifications.
    """
    try:
        notifications = get_notifications()
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve notifications: {e}"}), 500

@api_bp.route('/api/notifications', methods=['POST'])
@token_required
@role_required("Admin")
def create_notification():
    """
    Add a new notification.
    Restricted to Admin role.
    """
    data = request.json
    notification = {
        'type': data.get('type', 'info'),
        'message': data.get('message'),
    }
    if not notification['message']:
        return jsonify({'error': 'Notification message is required'}), 400
    result = add_notification(notification)
    return jsonify(result), 200

@api_bp.route('/api/notifications/clear', methods=['POST'])
@token_required
@role_required("Admin")
def clear_all_notifications():
    """
    Clear all notifications.
    Restricted to Admin role.
    """
    try:
        result = clear_notifications()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f"Failed to clear notifications: {e}"}), 500

@api_bp.route('/api/incidents', methods=['POST'])
@token_required
@role_required("Admin")
def submit_incident_report():
    """
    Create a new incident report.
    Restricted to Admin role.
    """
    user_id = request.user_id
    data = request.json
    title = data.get('title')
    description = data.get('description')
    severity = data.get('severity', 'low')
    result = create_incident_report(user_id, title, description, severity)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/incidents', methods=['GET'])
@token_required
@role_required("Admin")
def get_all_incident_reports():
    """
    Retrieve all incident reports.
    Restricted to Admin role.
    """
    try:
        reports = get_incident_reports()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch incident reports'}), 500

@api_bp.route('/api/system_health', methods=['GET'])
@token_required
@role_required("Admin")
def get_system_health_metrics():
    """
    Retrieve the current system health metrics.
    Restricted to Admin role.
    """
    try:
        health_data = get_system_health()
        return jsonify(health_data), 200
    except Exception as e:
        print(f"Error fetching system health metrics: {e}")
        return jsonify({'error': 'Unable to fetch system health metrics'}), 500

# ... more routes as per your requirements
