import csv
from flask import jsonify, Response
from io import StringIO
from backend.database import get_db_session
from backend.models import NetworkTraffic

def export_to_csv():
    """
    Export network traffic data to CSV format.

    Returns:
        CSV data as a Flask response.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Create a CSV output in memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Source', 'Destination', 'Protocol', 'Length', 'Timestamp'])

        for traffic in traffic_data:
            writer.writerow([
                traffic.source,
                traffic.destination,
                traffic.protocol,
                traffic.length,
                traffic.timestamp.isoformat()
            ])

        output.seek(0)
        return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=traffic_data.csv"})
    finally:
        session.close()

def export_to_json():
    """
    Export network traffic data to JSON format.

    Returns:
        JSON data as a Flask response.
    """
    session = get_db_session()
    try:
        traffic_data = session.query(NetworkTraffic).all()

        # Convert traffic data to list of dictionaries
        traffic_list = [
            {
                'source': traffic.source,
                'destination': traffic.destination,
                'protocol': traffic.protocol,
                'length': traffic.length,
                'timestamp': traffic.timestamp.isoformat()
            }
            for traffic in traffic_data
        ]

        return jsonify(traffic_list)
    finally:
        session.close()
