from flask import Blueprint, jsonify, request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input
from backend.auth import generate_token, token_required
from flask import Flask
from backend.routes import api_bp
from backend.logging_config import setup_logging
from backend.logging_middleware import log_request_and_response
from flask import Flask
from backend.routes import api_bp
from backend.logging_middleware import log_request_and_response
from backend.log_rotation import setup_log_rotation

# Set up log rotation
setup_log_rotation()

# Initialize the Flask application
app = Flask(__name__)

# Apply logging middleware to log requests and responses
app = log_request_and_response(app)

# Register the Blueprint for API routes
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)

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

        return jsonify(traffic_list), 200
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return jsonify({'error': 'Unable to fetch traffic data'}), 500
    finally:
        session.close()
