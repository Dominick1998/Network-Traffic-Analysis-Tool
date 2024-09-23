from flask import Blueprint, jsonify, request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required
from backend.rate_limiter import rate_limit
from backend.throttling import throttle
from backend.email_notifications import send_email_notification
from backend.anomaly_detection import detect_anomalies
from backend.network_summary import generate_network_summary
from backend.alerts import check_alert_conditions
from backend.export import export_to_csv, export_to_json
from flask import send_file
from flask import jsonify
from threading import Event
import os

@api_bp.route('/api/export/csv', methods=['GET'])
@token_required
def get_csv_export():
    """
    Export network traffic data as CSV.

    Returns:
        Response with CSV data.
    """
    return export_to_csv()

@api_bp.route('/api/export/json', methods=['GET'])
@token_required
def get_json_export():
    """
    Export network traffic data as JSON.

    Returns:
        Response with JSON data.
    """
    return export_to_json()

# Global event to control scheduler pause/resume
scheduler_pause_event = Event()

notifications_log = []

def log_notification(message):
    """
    Log a notification message in memory for later retrieval.
    """
    notifications_log.append({'message': message})

@api_bp.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications():
    """
    Retrieve a list of notifications for the admin.

    Returns:
        JSON response with a list of notifications.
    """
    return jsonify(notifications_log), 200

@api_bp.route('/api/scheduler/pause', methods=['POST'])
@token_required
def pause_scheduler():
    """
    Pause the scheduler tasks.
    """
    scheduler_pause_event.set()
    return jsonify({'message': 'Scheduler paused'}), 200

@api_bp.route('/api/scheduler/resume', methods=['POST'])
@token_required
def resume_scheduler():
    """
    Resume the scheduler tasks.
    """
    scheduler_pause_event.clear()
    return jsonify({'message': 'Scheduler resumed'}), 200

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

    # In a real implementation, this value would be stored in a settings table or configuration file
    print(f"Updating data retention policy to {days} days.")

    # Placeholder for updating the policy
    return jsonify({'message': f'Data retention policy updated to {days} days'}), 200

@api_bp.route('/api/logs', methods=['GET'])
@token_required
def get_logs():
    """
    Serve the request logs for viewing.
    
    Returns:
        The log file contents.
    """
    log_file = 'request_logs.log'
    if os.path.exists(log_file):
        return send_file(log_file)
    else:
        return jsonify({'error': 'Log file not found'}), 404

@api_bp.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts():
    """
    Retrieve alerts based on network traffic data conditions.

    Returns:
        JSON response with a list of alerts.
    """
    session = get_db_session()
    try:
        # Query all network traffic data
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

        # Check for alert conditions
        alerts = check_alert_conditions(traffic_list)

        return jsonify(alerts), 200
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return jsonify({'error': 'Unable to fetch alerts'}), 500
    finally:
        session.close()

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
        # Query all network traffic data
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

        # Check if any traffic exceeds a threshold (e.g., packet length > 1000)
        for traffic in traffic_data:
            if traffic.length > 1000:
                send_email_notification(
                    to_email='admin@example.com',
                    subject='Traffic Alert: Large Packet Detected',
                    message=f"Large packet detected from {traffic.source} to {traffic.destination} with length {traffic.length}."
                )

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
        # Query all network traffic data
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

        return jsonify(anomalies), 200
    except Exception as e:
        print(f"Error fetching anomalous traffic: {e}")
        return jsonify({'error': 'Unable to fetch anomalous traffic'}), 500
    finally:
        session.close()

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
        # Query all network traffic data
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
