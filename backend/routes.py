from flask import Blueprint, jsonify, request, send_file
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required, role_required
from backend.audit_logging import log_user_activity, log_event, log_admin_action
from backend.rate_limiter import rate_limit
from backend.throttling import throttle
from backend.email_notifications import send_email_notification
from backend.anomaly_detection import detect_anomalies
from backend.network_summary import generate_network_summary
from backend.cleanup import delete_old_traffic_data
from backend.export import export_to_csv, export_to_json
from backend.import_data import import_from_csv
from backend.logs import get_logs, download_logs
from backend.threat_detection import detect_ddos, detect_port_scan, detect_suspicious_ip_ranges
from backend.performance_monitoring import get_cpu_usage, get_memory_usage, track_response_time
from backend.firewall_rules import apply_firewall_rule, delete_firewall_rule
from backend.user_activity import get_user_activity_logs
from backend.alerts import create_alert, get_alerts, delete_alert, evaluate_alerts  # Added evaluate_alerts
from backend.anomaly_logging import log_anomaly, get_anomaly_logs
from backend.email_alerts import send_custom_alert_email
from backend.notification_system import create_notification, get_notifications
from backend.incident_reporting import create_incident_report, get_incident_reports
from backend.system_health_monitoring import get_system_health
from backend.log_rotation import setup_log_rotation
from backend.backup_management import create_backup, restore_backup
from backend.security_monitoring import detect_unauthorized_access, log_security_event
from backend.firewall_management import get_firewall_rules, add_firewall_rule, delete_firewall_rule
from backend.performance_monitor import get_cpu_usage, get_memory_usage, get_disk_usage, get_network_latency
from backend.notification_center import add_notification, clear_notifications

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
        log_event(user_id=user.id, event_type="Login", description="User logged in", role=user.role)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

@api_bp.route('/api/traffic', methods=['GET'])
@token_required
@rate_limit(max_requests=5, window_seconds=60)
@throttle(max_requests=10, slowdown_seconds=5)
def get_traffic_data():
    """
    Retrieve the network traffic data from the database and evaluate alerts based on the data.
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

        # Evaluate alerts
        triggered_alerts = evaluate_alerts(traffic_list)

        # Threat detection
        ddos_sources = detect_ddos(traffic_list)
        port_scan_sources = detect_port_scan(traffic_list)
        suspicious_ips = detect_suspicious_ip_ranges(traffic_list, ["192.168", "10.0"])

        return jsonify({
            "traffic_data": traffic_list,
            "threats": {
                "ddos_sources": ddos_sources,
                "port_scan_sources": port_scan_sources,
                "suspicious_ips": suspicious_ips
            },
            "triggered_alerts": triggered_alerts
        }), 200
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
    log_admin_action(user_id=request.user_id, action_description=f"Created alert: {name}")
    if 'message' in result:
        send_custom_alert_email(alert_name=name, condition=condition, action=action)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@token_required
@role_required("Admin")
def delete_alert_route(alert_id):
    """
    Delete an alert rule by its ID.
    Restricted to Admin role.
    """
    result = delete_alert(alert_id=alert_id)
    log_admin_action(user_id=request.user_id, action_description=f"Deleted alert with ID: {alert_id}")
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/export/csv', methods=['GET'])
@token_required
def get_csv_export():
    """
    Export network traffic data as CSV.
    """
    log_user_activity(user_id=request.user_id, activity="Exported traffic data as CSV")
    return export_to_csv()

@api_bp.route('/api/export/json', methods=['GET'])
@token_required
def get_json_export():
    """
    Export network traffic data as JSON.
    """
    log_user_activity(user_id=request.user_id, activity="Exported traffic data as JSON")
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
    log_admin_action(user_id=request.user_id, action_description=f"Added firewall rule: {rule}")
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
    log_admin_action(user_id=request.user_id, action_description=f"Deleted firewall rule: {rule}")
    return jsonify(result), 200 if 'message' in result else 500

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
    log_admin_action(user_id, f"Submitted incident report: {title}, Severity: {severity}")
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/system_health', methods=['GET'])
@token_required
@role_required("Admin")
def get_system_health_metrics():
    """
    Retrieve the current system health metrics.
    Restricted to Admin role.
    """
    user_id = request.user_id
    log_admin_action(user_id, "Viewed system health metrics")
    try:
        health_data = get_system_health()
        return jsonify(health_data), 200
    except Exception as e:
        print(f"Error fetching system health metrics: {e}")
        return jsonify({'error': 'Unable to fetch system health metrics'}), 500

@api_bp.route('/api/logs/rotate', methods=['POST'])
@token_required
@role_required("Admin")
def rotate_logs():
    """
    Trigger log rotation.
    """
    try:
        setup_log_rotation()
        return jsonify({'message': 'Log rotation initiated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f"Failed to rotate logs: {e}"}), 500

@api_bp.route('/api/backup/create', methods=['POST'])
@token_required
@role_required("Admin")
def create_database_backup_route():
    """
    Create a database backup.
    """
    db_path = "path/to/database.db"  # Specify the actual path to your database
    result = create_backup(db_path)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/backup/restore', methods=['POST'])
@token_required
@role_required("Admin")
def restore_database_backup_route():
    """
    Restore database from a backup.
    """
    data = request.json
    backup_filename = data.get("backup_filename")
    db_path = "path/to/database.db"  # Specify the actual path to your database
    result = restore_backup(backup_filename, db_path)
    return jsonify(result), 200 if 'message' in result else 500
