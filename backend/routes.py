from flask import Blueprint, jsonify, request, send_file
from backend.database import get_db_session
from backend.models import NetworkTraffic, Notification, AuditLog
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
from backend.alerts import create_alert, get_alerts, delete_alert, evaluate_alerts
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

@api_bp.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_as_read(notification_id):
    """
    Mark a notification as read.
    """
    session = get_db_session()
    try:
        notification = session.query(Notification).filter_by(id=notification_id, user_id=request.user_id).first()
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        notification.read = True
        session.commit()
        return jsonify({'message': 'Notification marked as read'}), 200
    except Exception as e:
        print(f"Error marking notification as read: {e}")
        return jsonify({'error': 'Failed to mark notification as read'}), 500
    finally:
        session.close()

@api_bp.route('/api/traffic/insights', methods=['GET'])
@token_required
def get_traffic_insights():
    """
    Retrieve aggregated traffic data insights.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()
        total_traffic = len(traffic_data)

        protocol_counts = {}
        source_counts = {}
        destination_counts = {}

        for traffic in traffic_data:
            protocol_counts[traffic.protocol] = protocol_counts.get(traffic.protocol, 0) + 1
            source_counts[traffic.source] = source_counts.get(traffic.source, 0) + 1
            destination_counts[traffic.destination] = destination_counts.get(traffic.destination, 0) + 1

        top_protocols = sorted(protocol_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_destinations = sorted(destination_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return jsonify({
            'total_traffic': total_traffic,
            'top_protocols': top_protocols,
            'top_sources': top_sources,
            'top_destinations': top_destinations
        }), 200
    except Exception as e:
        print(f"Error retrieving traffic insights: {e}")
        return jsonify({'error': 'Failed to retrieve traffic insights'}), 500
    finally:
        session.close()

# Additional routes are unchanged from the existing file.

# Remaining routes...
