from datetime import datetime
import numpy as np
from backend.models import NetworkTraffic
from backend.audit_logging import log_anomaly
from backend.notifications import send_alert_notification

# Constants for thresholds (can later be made configurable)
LENGTH_THRESHOLD = 1500  # Packet length threshold in bytes
TRAFFIC_RATE_THRESHOLD = 1000  # Example threshold for traffic rate

def detect_anomalies(traffic_data):
    """
    Detect anomalies in network traffic based on length and traffic rate thresholds.

    Args:
        traffic_data (list): List of network traffic data entries.

    Returns:
        list: List of anomalies detected in the traffic data.
    """
    anomalies = []

    # Analyzing each traffic entry for anomalies
    for entry in traffic_data:
        if entry['length'] > LENGTH_THRESHOLD:
            anomaly = {
                'type': 'High Packet Length',
                'source': entry['source'],
                'destination': entry['destination'],
                'protocol': entry['protocol'],
                'length': entry['length'],
                'timestamp': entry['timestamp']
            }
            log_anomaly(
                source_ip=entry['source'],
                destination_ip=entry['destination'],
                protocol=entry['protocol'],
                length=entry['length'],
                anomaly_type="High Packet Length"
            )
            anomalies.append(anomaly)

    # Calculate traffic rate (packets per second)
    timestamps = [entry['timestamp'] for entry in traffic_data]
    if len(timestamps) > 1:
        rate = len(timestamps) / (timestamps[-1] - timestamps[0]).total_seconds()
        if rate > TRAFFIC_RATE_THRESHOLD:
            for entry in traffic_data:
                anomaly = {
                    'type': 'High Traffic Rate',
                    'source': entry['source'],
                    'destination': entry['destination'],
                    'protocol': entry['protocol'],
                    'timestamp': entry['timestamp']
                }
                anomalies.append(anomaly)
                log_anomaly(
                    source_ip=entry['source'],
                    destination_ip=entry['destination'],
                    protocol=entry['protocol'],
                    length=entry['length'],
                    anomaly_type="High Traffic Rate"
                )
            send_alert_notification(
                to_email="admin@example.com",
                subject="High Traffic Rate Detected",
                message=f"A high traffic rate of {rate} packets/sec was detected."
            )

    return anomalies
