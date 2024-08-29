from backend.database import get_db_session
from backend.models import NetworkTraffic

def save_packet_to_db(packet_data):
    """
    Save captured packet data to the database.

    Args:
        packet_data (dict): A dictionary containing packet information.
    
    Returns:
        None
    """
    session = get_db_session()
    try:
        # Create a new NetworkTraffic object from packet data
        traffic_record = NetworkTraffic(
            source=packet_data['source'],
            destination=packet_data['destination'],
            protocol=packet_data['protocol'],
            length=packet_data['length']
        )
        # Add and commit the record to the database
        session.add(traffic_record)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving packet to DB: {e}")
    finally:
        session.close()
