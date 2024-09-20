from datetime import datetime, timedelta
from backend.database import get_db_session
from backend.models import NetworkTraffic

def delete_old_traffic_data(days_old=30):
    """
    Delete network traffic data that is older than the specified number of days.

    Args:
        days_old (int): The age of the data to be deleted, in days.
    """
    session = get_db_session()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        old_traffic = session.query(NetworkTraffic).filter(NetworkTraffic.timestamp < cutoff_date).all()

        if old_traffic:
            print(f"Deleting {len(old_traffic)} old traffic records older than {days_old} days.")
            for record in old_traffic:
                session.delete(record)
            session.commit()
        else:
            print(f"No traffic data older than {days_old} days found.")
    except Exception as e:
        print(f"Error deleting old traffic data: {e}")
    finally:
        session.close()
