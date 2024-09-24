import csv
from flask import request
from backend.database import get_db_session
from backend.models import NetworkTraffic
from io import StringIO

def import_from_csv(file):
    """
    Import network traffic data from a CSV file.

    Args:
        file (FileStorage): The CSV file to import.

    Returns:
        dict: A response indicating success or failure.
    """
    session = get_db_session()
    try:
        # Read the file and parse CSV data
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)

        for row in csv_reader:
            traffic = NetworkTraffic(
                source=row['Source'],
                destination=row['Destination'],
                protocol=row['Protocol'],
                length=int(row['Length']),
                timestamp=row['Timestamp']
            )
            session.add(traffic)

        session.commit()
        return {'message': 'Data imported successfully'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to import data: {e}"}
    finally:
        session.close()
