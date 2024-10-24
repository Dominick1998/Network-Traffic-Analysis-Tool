from flask import Blueprint, jsonify, request, send_file
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required
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

    Returns:
        JSON response with a message indicating server status.
    """
    return jsonify({'status': 'Server is running'}), 200

@api_bp.route('/api/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate the user and return a JWT token.

    Returns:
        JSON response with a JWT token or an error message.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Simple authentication logic (replace with database lookup)
    if username == "admin" and password == "password":
        token = generate_token(username)
        # Log the user activity for successful login
        log_user_activity(user_id=1, activity="User logged in")
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

    Returns:
        JSON response with network traffic data.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat(),
                'destination_port': traffic.get('destination_port', 0)
            }
            for traffic in traffic_data
        ]

        return jsonify(traffic_list), 200
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return jsonify({'error': 'Unable to fetch traffic data'}), 500
    finally:
        session.close()

@api_bp.route('/api/anomalies', methods=['GET'])
@token_required
def get_anomalous_traffic():
    """
    Retrieve anomalous network traffic based on anomaly detection.

    Returns:
        JSON response with anomalous network traffic.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat()
            }
            for traffic in traffic_data
        ]

        # Detect anomalies
        anomalies = detect_anomalies(traffic_list)

        # Log anomalies if detected
        for anomaly in anomalies:
            log_anomaly(
                source_ip=anomaly['source'],
                destination_ip=anomaly['destination'],
                protocol=anomaly['protocol'],
                length=anomaly['length'],
                anomaly_type="Anomalous Traffic"
            )

        # Send email notification if anomalies are detected
        if anomalies:
            send_email_notification(
                to_email="admin@example.com",
                subject="Anomalous Network Traffic Detected",
                message=f"Anomalies detected in network traffic: {len(anomalies)} anomalies found."
            )

        return jsonify(anomalies), 200
    except Exception as e:
        print(f"Error fetching anomalous traffic: {e}")
        return jsonify({'error': 'Unable to fetch anomalous traffic'}), 500
    finally:
        session.close()

@api_bp.route('/api/anomaly_logs', methods=['GET'])
@token_required
def get_anomaly_logs_route():
    """
    Retrieve all logged anomaly records.

    Returns:
        JSON response with a list of anomaly logs.
    """
    try:
        logs = get_anomaly_logs()
        return jsonify(logs), 200
    except Exception as e:
        print(f"Error fetching anomaly logs: {e}")
        return jsonify({'error': 'Unable to fetch anomaly logs'}), 500

@api_bp.route('/api/summary', methods=['GET'])
@token_required
def get_network_summary():
    """
    Retrieve a summary of the network traffic data.

    Returns:
        JSON response with the network traffic summary.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat()
            }
            for traffic in traffic_data
        ]

        # Generate the network summary
        summary = generate_network_summary(traffic_list)

        return jsonify(summary), 200
    except Exception as e:
        print(f"Error fetching network summary: {e}")
        return jsonify({'error': 'Unable to fetch network summary'}), 500
    finally:
        session.close()

@api_bp.route('/api/alerts', methods=['POST'])
@token_required
def create_alert_route():
    """
    Create a new alert rule.

    Returns:
        JSON response with success or failure message.
    """
    data = request.json
    name = data.get('name')
    condition = data.get('condition')
    action = data.get('action')

    if not name or not condition or not action:
        return jsonify({'error': 'All fields are required'}), 400

    result = create_alert(name=name, condition=condition, action=action)
    
    # Trigger an email notification when the alert is created
    if 'message' in result:
        send_custom_alert_email(alert_name=name, condition=condition, action=action)

    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts_route():
    """
    Retrieve all alert rules.

    Returns:
        JSON response with a list of alert rules.
    """
    try:
        alerts = get_alerts()
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch alerts'}), 500

@api_bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@token_required
def delete_alert_route(alert_id):
    """
    Delete an alert rule by its ID.

    Returns:
        JSON response with success or failure message.
    """
    result = delete_alert(alert_id=alert_id)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/export/csv', methods=['GET'])
@token_required
def get_csv_export():
    """
    Export network traffic data as CSV.

    Returns:
        Response with CSV data.
    """
    # Log the user activity for CSV export
    log_user_activity(user_id=1, activity="User exported traffic data as CSV")
    return export_to_csv()

@api_bp.route('/api/export/json', methods=['GET'])
@token_required
def get_json_export():
    """
    Export network traffic data as JSON.

    Returns:
        Response with JSON data.
    """
    # Log the user activity for JSON export
    log_user_activity(user_id=1, activity="User exported traffic data as JSON")
    return export_to_json()

@api_bp.route('/api/import/csv', methods=['POST'])
@token_required
def upload_csv():
    """
    Upload and import network traffic data from a CSV file.

    Returns:
        JSON response indicating success or failure.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):
        result = import_from_csv(file)
        # Log the user activity for importing CSV data
        log_user_activity(user_id=1, activity="User imported traffic data from CSV")
        return jsonify(result), 200 if 'message' in result else 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@api_bp.route('/api/logs', methods=['GET'])
@token_required
def view_logs():
    """
    View the server logs.

    Returns:
        JSON response containing the log file contents.
    """
    return get_logs()

@api_bp.route('/api/logs/download', methods=['GET'])
@token_required
def download_server_logs():
    """
    Download the server logs.

    Returns:
        Response that triggers the download of the log file.
    """
    # Log the user activity for log download
    log_user_activity(user_id=1, activity="User downloaded server logs")
    return download_logs()

@api_bp.route('/api/settings/retention', methods=['POST'])
@token_required
def update_retention_policy():
    """
    Update the data retention policy for traffic data.

    Returns:
        JSON response with a message indicating the result of the update.
    """
    data = request.json
    days = data.get('days', 30)

    if days < 1:
        return jsonify({'error': 'Invalid retention period'}), 400

    print(f"Updating data retention policy to {days} days.")

    return jsonify({'message': f'Data retention policy updated to {days} days'}), 200

@api_bp.route('/api/threats', methods=['GET'])
@token_required
def detect_threats():
    """
    Detect potential threats in the network traffic, such as DDoS attacks, port scans, and suspicious IP ranges.

    Returns:
        JSON response with a list of detected threats.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat(),
                'destination_port': traffic.get('destination_port', 0)
            }
            for traffic in traffic_data
        ]

        # Detect DDoS attacks
        ddos_threats = detect_ddos(traffic_list)

        # Detect port scans
        port_scan_threats = detect_port_scan(traffic_list)

        # Detect traffic from suspicious IP ranges (e.g., IPs starting with "192.168")
        suspicious_ranges = ["192.168", "10.0"]
        suspicious_ip_threats = detect_suspicious_ip_ranges(traffic_list, suspicious_ranges)

        # Combine all detected threats
        all_threats = ddos_threats + port_scan_threats + suspicious_ip_threats

        return jsonify(all_threats), 200
    except Exception as e:
        print(f"Error detecting threats: {e}")
        return jsonify({'error': 'Unable to detect threats'}), 500
    finally:
        session.close()

@api_bp.route('/api/performance', methods=['GET'])
@token_required
def get_performance_metrics():
    """
    Retrieve the current system performance metrics, such as CPU and memory usage.

    Returns:
        JSON response with performance metrics.
    """
    try:
        performance_data = {
            'cpu_usage': get_cpu_usage(),
            'memory_usage': get_memory_usage()
        }

        return jsonify(performance_data), 200
    except Exception as e:
        print(f"Error fetching performance metrics: {e}")
        return jsonify({'error': 'Unable to fetch performance metrics'}), 500

@api_bp.route('/api/user_activity', methods=['GET'])
@token_required
def get_activity_logs():
    """
    Retrieve all user activity logs.

    Returns:
        JSON response with a list of user activity logs.
    """
    try:
        activity_logs = get_user_activity_logs()
        return jsonify(activity_logs), 200
    except Exception as e:
        print(f"Error fetching user activity logs: {e}")
        return jsonify({'error': 'Unable to fetch activity logs'}), 500

@api_bp.route('/api/firewall', methods=['POST'])
@token_required
def apply_firewall_rule_route():
    """
    Apply a firewall rule based on user input.

    Returns:
        JSON response with success or failure message.
    """
    data = request.json
    action = data.get('action')
    ip_address = data.get('ip_address')
    port = data.get('port')
    protocol = data.get('protocol')

    if not action or not ip_address:
        return jsonify({'error': 'Action and IP address are required'}), 400

    result = apply_firewall_rule(action=action, ip_address=ip_address, port=port, protocol=protocol)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/firewall', methods=['DELETE'])
@token_required
def delete_firewall_rule_route():
    """
    Delete a firewall rule based on user input.

    Returns:
        JSON response with success or failure message.
    """
    data = request.json
    ip_address = data.get('ip_address')
    port = data.get('port')
    protocol = data.get('protocol')

    if not ip_address:
        return jsonify({'error': 'IP address is required'}), 400

    result = delete_firewall_rule(ip_address=ip_address, port=port, protocol=protocol)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/traffic', methods=['GET'])
@token_required
@rate_limit(max_requests=5, window_seconds=60)  # Rate limiting applied here
def get_traffic_data():
    """
    Retrieve the network traffic data from the database.

    Returns:
        JSON response with network traffic data.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat(),
                'destination_port': traffic.get('destination_port', 0)
            }
            for traffic in traffic_data
        ]

        return jsonify(traffic_list), 200
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return jsonify({'error': 'Unable to fetch traffic data'}), 500
    finally:
        session.close()

@api_bp.route('/api/anomalies', methods=['GET'])
@token_required
@rate_limit(max_requests=5, window_seconds=60)  # Rate limiting applied
@throttle(max_requests=10, slowdown_seconds=5)  # Throttling applied here
def get_anomalous_traffic():
    """
    Retrieve anomalous network traffic based on anomaly detection.

    Returns:
        JSON response with anomalous network traffic.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': sanitize_input(traffic.source),
                'destination': sanitize_input(traffic.destination),
                'protocol': sanitize_input(traffic.protocol),
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat()
            }
            for traffic in traffic_data
        ]

        # Detect anomalies
        anomalies = detect_anomalies(traffic_list)

        # Log anomalies if detected
        for anomaly in anomalies:
            log_anomaly(
                source_ip=anomaly['source'],
                destination_ip=anomaly['destination'],
                protocol=anomaly['protocol'],
                length=anomaly['length'],
                anomaly_type="Anomalous Traffic"
            )

        # Send email notification if anomalies are detected
        if anomalies:
            send_email_notification(
                to_email="admin@example.com",
                subject="Anomalous Network Traffic Detected",
                message=f"Anomalies detected in network traffic: {len(anomalies)} anomalies found."
            )

        return jsonify(anomalies), 200
    except Exception as e:
        print(f"Error fetching anomalous traffic: {e}")
        return jsonify({'error': 'Unable to fetch anomalous traffic'}), 500
    finally:
        session.close()

@api_bp.route('/api/notifications', methods=['GET'])
@token_required
def get_user_notifications():
    """
    Retrieve all notifications for the authenticated user.

    Returns:
        JSON response with a list of notifications.
    """
    user_id = request.user_id  # Assumes user_id is set by the token_required decorator
    try:
        notifications = get_notifications(user_id)
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch notifications'}), 500

@api_bp.route('/api/notifications', methods=['POST'])
@token_required
def create_user_notification():
    """
    Create a notification for the authenticated user.

    Returns:
        JSON response indicating success or failure.
    """
    user_id = request.user_id  # Assumes user_id is set by the token_required decorator
    data = request.json
    message = data.get('message')
    notification_type = data.get('type', 'info')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    result = create_notification(user_id, message, notification_type)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/incidents', methods=['POST'])
@token_required
def submit_incident_report():
    """
    Create a new incident report.

    Returns:
        JSON response indicating success or failure.
    """
    user_id = request.user_id  # Assumes user_id is set by the token_required decorator
    data = request.json
    title = data.get('title')
    description = data.get('description')
    severity = data.get('severity', 'low')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    result = create_incident_report(user_id, title, description, severity)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/incidents', methods=['GET'])
@token_required
def get_all_incident_reports():
    """
    Retrieve all incident reports.

    Returns:
        JSON response with a list of incident reports.
    """
    try:
        reports = get_incident_reports()
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch incident reports'}), 500

@api_bp.route('/api/system_health', methods=['GET'])
@token_required
def get_system_health_metrics():
    """
    Retrieve the current system health metrics, such as CPU, memory, disk, and network usage.

    Returns:
        JSON response with system health data.
    """
    try:
        health_data = get_system_health()
        return jsonify(health_data), 200
    except Exception as e:
        print(f"Error fetching system health metrics: {e}")
        return jsonify({'error': 'Unable to fetch system health metrics'}), 500

@api_bp.route('/api/logs', methods=['GET'])
@token_required
def view_logs():
    """
    View the server logs.

    Returns:
        JSON response containing the log file contents.
    """
    return get_logs()

@api_bp.route('/api/logs/download', methods=['GET'])
@token_required
def download_server_logs():
    """
    Download the server logs.

    Returns:
        Response that triggers the download of the log file.
    """
    log_user_activity(user_id=1, activity="User downloaded server logs")
    return download_logs()

@api_bp.route('/api/log_rotation/settings', methods=['POST'])
@token_required
def update_log_rotation_settings():
    """
    Update the log rotation settings (max file size, backup count).

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    max_file_size = data.get('max_file_size', 5)  # Default 5 MB
    backup_count = data.get('backup_count', 5)  # Default 5 backups

    try:
        handler = logging.getLogger().handlers[0]
        if isinstance(handler, RotatingFileHandler):
            handler.maxBytes = max_file_size * 1024 * 1024
            handler.backupCount = backup_count
        return jsonify({'message': 'Log rotation settings updated successfully.'}), 200
    except Exception as e:
        print(f"Error updating log rotation settings: {e}")
        return jsonify({'error': 'Failed to update log rotation settings'}), 500

@api_bp.route('/api/backup/create', methods=['POST'])
@token_required
def create_database_backup():
    """
    Create a new backup of the database.

    Returns:
        JSON response indicating success or failure.
    """
    database_path = 'path/to/your/database.db'  # Replace with actual database path
    result = create_backup(database_path)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/backup/restore', methods=['POST'])
@token_required
def restore_database_backup():
    """
    Restore the database from a backup file.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    backup_filename = data.get('backup_filename')

    if not backup_filename:
        return jsonify({'error': 'Backup filename is required'}), 400

    database_path = 'path/to/your/database.db'  # Replace with actual database path
    result = restore_backup(backup_filename, database_path)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate the user and return a JWT token.

    Returns:
        JSON response with a JWT token or an error message.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == "admin" and password == "password":
        token = generate_token(username)
        log_event(user_id=1, event_type="login", description="User successfully logged in")
        return jsonify({'token': token}), 200
    else:
        log_event(user_id=1, event_type="failed_login", description="User failed to log in with invalid credentials")
        return jsonify({'error': 'Invalid credentials'}), 403

@api_bp.route('/api/backup/create', methods=['POST'])
@token_required
def create_database_backup():
    """
    Create a new backup of the database.

    Returns:
        JSON response indicating success or failure.
    """
    database_path = 'path/to/your/database.db'  # Replace with actual database path
    result = create_backup(database_path)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/backup/restore', methods=['POST'])
@token_required
def restore_database_backup():
    """
    Restore the database from a backup file.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    backup_filename = data.get('backup_filename')

    if not backup_filename:
        return jsonify({'error': 'Backup filename is required'}), 400

    database_path = 'path/to/your/database.db'  # Replace with actual database path
    result = restore_backup(backup_filename, database_path)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/traffic', methods=['GET'])
@token_required
def get_traffic_data():
    """
    Retrieve the network traffic data from the database.

    Returns:
        JSON response with network traffic data.
    """
    user_ip = request.remote_addr
    unauthorized_access_check = detect_unauthorized_access(user_ip, '/api/traffic')
    
    if 'warning' in unauthorized_access_check:
        return jsonify(unauthorized_access_check), 403

    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert query results to a list of dictionaries
        traffic_list = [
            {
                'source': traffic.source,
                'destination': traffic.destination,
                'protocol': traffic.protocol,
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat(),
                'destination_port': traffic.destination_port
            }
            for traffic in traffic_data
        ]

        # Detect DDoS attacks
        ddos_sources = detect_ddos(traffic_list)
        if ddos_sources:
            log_security_event('ddos_detected', f"DDoS attack detected from IP(s): {', '.join(ddos_sources)}")
            return jsonify({'warning': 'DDoS attack detected', 'sources': ddos_sources}), 200

        return jsonify(traffic_list), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch traffic data'}), 500
    finally:
        session.close()

@api_bp.route('/api/firewall/rules', methods=['GET'])
@token_required
def list_firewall_rules():
    """
    List all firewall rules.

    Returns:
        JSON response with a list of firewall rules.
    """
    try:
        rules = get_firewall_rules()
        return jsonify({'rules': rules}), 200
    except Exception as e:
        return jsonify({'error': f"Failed to fetch firewall rules: {e}"}), 500

@api_bp.route('/api/firewall/rules', methods=['POST'])
@token_required
def create_firewall_rule():
    """
    Add a new firewall rule.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    rule = data.get('rule')

    if not rule:
        return jsonify({'error': 'Firewall rule is required'}), 400

    result = add_firewall_rule(rule)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/firewall/rules', methods=['DELETE'])
@token_required
def remove_firewall_rule():
    """
    Delete an existing firewall rule.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    rule = data.get('rule')

    if not rule:
        return jsonify({'error': 'Firewall rule is required'}), 400

    result = delete_firewall_rule(rule)
    return jsonify(result), 200 if 'message' in result else 500

@api_bp.route('/api/performance/cpu', methods=['GET'])
@token_required
def get_cpu_metrics():
    """
    Retrieve the current CPU usage.

    Returns:
        JSON response with CPU usage percentage.
    """
    try:
        cpu_data = get_cpu_usage()
        return jsonify(cpu_data), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve CPU metrics: {e}"}), 500

@api_bp.route('/api/performance/memory', methods=['GET'])
@token_required
def get_memory_metrics():
    """
    Retrieve the current memory usage.

    Returns:
        JSON response with memory usage data.
    """
    try:
        memory_data = get_memory_usage()
        return jsonify(memory_data), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve memory metrics: {e}"}), 500

@api_bp.route('/api/performance/disk', methods=['GET'])
@token_required
def get_disk_metrics():
    """
    Retrieve the current disk usage.

    Returns:
        JSON response with disk usage data.
    """
    try:
        disk_data = get_disk_usage()
        return jsonify(disk_data), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve disk metrics: {e}"}), 500

@api_bp.route('/api/performance/latency', methods=['GET'])
@token_required
def get_network_latency_metrics():
    """
    Retrieve the current network latency.

    Returns:
        JSON response with network latency data.
    """
    try:
        latency_data = get_network_latency()
        return jsonify(latency_data), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve network latency: {e}"}), 500

@api_bp.route('/api/notifications', methods=['GET'])
@token_required
def list_notifications():
    """
    Retrieve all notifications.

    Returns:
        JSON response with a list of notifications.
    """
    try:
        notifications = get_notifications()
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve notifications: {e}"}), 500

@api_bp.route('/api/notifications', methods=['POST'])
@token_required
def create_notification():
    """
    Add a new notification.

    Returns:
        JSON response indicating success or failure.
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
def clear_all_notifications():
    """
    Clear all notifications.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        result = clear_notifications()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f"Failed to clear notifications: {e}"}), 500
