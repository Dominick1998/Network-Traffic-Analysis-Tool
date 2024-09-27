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
from backend.threat_detection import detect_ddos
from backend.performance_monitoring import get_cpu_usage, get_memory_usage, track_response_time

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
    Detect potential threats in the network traffic, such as DDoS attacks.

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
                'timestamp': traffic.timestamp.isoformat()
            }
            for traffic in traffic_data
        ]

        # Detect DDoS attacks or other threats
        threats = detect_ddos(traffic_list)

        return jsonify(threats), 200
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
