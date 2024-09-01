from flask import Blueprint, jsonify, request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from backend.security import validate_ip_address, sanitize_input

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

@api_bp.route('/api/traffic', methods=['GET'])
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

@api_bp.route('/api/traffic', methods=['POST'])
def add_traffic_data():
    """
    Add network traffic data to the database.

    Returns:
        JSON response with a message indicating success or failure.
    """
    session = get_db_session()
    try:
        data = request.json
        source = data.get('source')
        destination = data.get('destination')
        protocol = data.get('protocol')
        length = data.get('length')

        # Validate inputs
        if not validate_ip_address(source) or not validate_ip_address(destination):
            return jsonify({'error': 'Invalid IP address format'}), 400

        # Sanitize inputs
        protocol = sanitize_input(protocol)

        # Create a new NetworkTraffic record
        traffic_record = NetworkTraffic(
            source=source,
            destination=destination,
            protocol=protocol,
            length=length
        )
        session.add(traffic_record)
        session.commit()
        return jsonify({'message': 'Traffic data added successfully'}), 201
    except Exception as e:
        session.rollback()
        print(f"Error adding traffic data: {e}")
        return jsonify({'error': 'Unable to add traffic data'}), 500
    finally:
        session.close()
