from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# A simple route to check if the server is running
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.
    
    Returns:
        JSON response with a message indicating server status.
    """
    return jsonify({'status': 'Server is running'}), 200

# A route to simulate capturing network traffic (stub)
@app.route('/api/traffic', methods=['GET'])
def get_traffic_data():
    """
    Simulates the capture and return of network traffic data.
    
    Returns:
        JSON response with dummy network traffic data.
    """
    # This is a placeholder for the actual traffic data
    dummy_data = [
        {'source': '192.168.1.1', 'destination': '192.168.1.2', 'protocol': 'TCP', 'length': 60},
        {'source': '192.168.1.2', 'destination': '192.168.1.3', 'protocol': 'UDP', 'length': 120},
        {'source': '192.168.1.1', 'destination': '192.168.1.4', 'protocol': 'ICMP', 'length': 30},
    ]
    return jsonify(dummy_data), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
