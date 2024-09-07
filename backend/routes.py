from flask import Blueprint, jsonify, request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required
from backend.rate_limiter import rate_limit
from backend.throttling import throttle
from backend.email_notifications import send_email_notification

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
