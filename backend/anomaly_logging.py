from backend.database import get_db_session
from backend.models import AnomalyLog
from datetime import datetime

def log_anomaly(source_ip, destination_ip, protocol, length, anomaly_type):
    """
    Log a detected network anomaly.

    Args:
        source_ip (str): The source IP of the traffic.
        destination_ip (str): The destination IP of the traffic.
        protocol (str): The protocol used in the traffic.
        length (int): The length of the packet.
        anomaly_type (str): The type of anomaly detected.
    """
    session = get_db_session()
    try:
        anomaly_log = AnomalyLog(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            length=length,
            anomaly_type=anomaly_type,
            timestamp=datetime.utcnow()
        )
        session.add(anomaly_log)
        session.commit()
    except Exception as e:
        print(f"Error logging anomaly: {e}")
        session.rollback()
    finally:
        session.close()

def get_anomaly_logs():
    """
    Retrieve all logged network anomalies.

    Returns:
        list: A list of anomaly logs.
    """
    session = get_db_session()
    try:
        logs = session.query(AnomalyLog).all()
        return [
            {
                'source_ip': log.source_ip,
                'destination_ip': log.destination_ip,
                'protocol': log.protocol,
                'length': log.length,
                'anomaly_type': log.anomaly_type,
                'timestamp': log.timestamp.isoformat()
            }
            for log in logs
        ]
    except Exception as e:
        print(f"Error fetching anomaly logs: {e}")
        return []
    finally:
        session.close()
