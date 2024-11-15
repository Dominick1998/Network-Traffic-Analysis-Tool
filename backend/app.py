from flask import Flask, jsonify, request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import sanitize_input
from backend.auth import generate_token, token_required
from backend.routes import api_bp
from backend.logging_config import setup_logging
from backend.logging_middleware import log_request_and_response
from backend.scheduler import start_scheduler
from backend.log_rotation import setup_log_rotation
import os

# App Factory Function
def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Initialize logging configuration
    setup_logging()

    # Set up log rotation
    setup_log_rotation()

    # Start the scheduler for periodic tasks
    start_scheduler()

    # Apply logging middleware to log requests and responses
    app = log_request_and_response(app)

    # Register the Blueprint for API routes
    app.register_blueprint(api_bp)

    # Register error handlers
    register_error_handlers(app)

    return app

# Error Handlers
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'An internal error occurred'}), 500

# Health check endpoint (added as part of the blueprint)
@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return jsonify({'status': 'Server is running'}), 200

# Login endpoint (added as part of the blueprint)
@api_bp.route('/api/login', methods=['POST'])
def login():
    """
    Login endpoint to authenticate the user and return a JWT token.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Replace with actual authentication logic (database lookup)
    if username == "admin" and password == "password":
        token = generate_token(username)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

# Traffic data retrieval endpoint (added as part of the blueprint)
@api_bp.route('/api/traffic', methods=['GET'])
@token_required
def get_traffic_data():
    """
    Retrieve the network traffic data from the database.
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

# Entry Point
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
