from datetime import datetime
import logging

SECURITY_LOG_FILE = 'logs/security.log'

# Set up the security logger
security_logger = logging.getLogger('security_logger')
security_logger.setLevel(logging.INFO)

# Create a file handler for the security log
file_handler = logging.FileHandler(SECURITY_LOG_FILE)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the security logger
security_logger.addHandler(file_handler)

def log_security_event(event_type, description):
    """
    Log a security event.

    Args:
        event_type (str): Type of the security event (e.g., 'unauthorized_access', 'ddos_detected').
        description (str): Detailed description of the security event.

    Returns:
        None
    """
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    security_message = f"Event: {event_type} | Description: {description} | Timestamp: {timestamp}"
    security_logger.info(security_message)

def detect_unauthorized_access(user_ip, endpoint):
    """
    Detect unauthorized access attempts based on suspicious IP addresses or actions.

    Args:
        user_ip (str): IP address of the user making the request.
        endpoint (str): The API endpoint that was accessed.

    Returns:
        dict: Result of the detection.
    """
    # Example: Check if the IP is on a blocklist
    blocklisted_ips = ["192.168.1.100", "10.0.0.50"]
    if user_ip in blocklisted_ips:
        log_security_event('unauthorized_access', f"Blocked IP {user_ip} attempted to access {endpoint}")
        return {'warning': 'Unauthorized access attempt detected'}

    return {'message': 'No unauthorized access detected'}

def detect_ddos(traffic_data):
    """
    Detect DDoS attack patterns based on abnormal traffic behavior.

    Args:
        traffic_data (list): List of traffic data dictionaries.

    Returns:
        list: A list of detected DDoS patterns.
    """
    # Example: Look for high traffic volumes from a single source
    source_ip_counts = {}
    ddos_threshold = 100  # Example threshold

    for traffic in traffic_data:
        source_ip = traffic.get('source')
        if source_ip not in source_ip_counts:
            source_ip_counts[source_ip] = 0
        source_ip_counts[source_ip] += 1

    ddos_sources = [ip for ip, count in source_ip_counts.items() if count > ddos_threshold]

    if ddos_sources:
        for ip in ddos_sources:
            log_security_event('ddos_detected', f"Potential DDoS detected from IP: {ip}")
        return ddos_sources

    return []
