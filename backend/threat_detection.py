from backend.database import get_db_session
from backend.models import ThreatLog
from datetime import datetime
from collections import Counter

def detect_ddos(traffic_data):
    """
    Detect potential DDoS attacks based on a high frequency of requests from a single source IP.
    
    Args:
        traffic_data (list): List of network traffic dictionaries.
        
    Returns:
        list: List of sources flagged for DDoS-like behavior.
    """
    source_ips = [traffic['source'] for traffic in traffic_data]
    counter = Counter(source_ips)
    ddos_sources = [ip for ip, count in counter.items() if count > 100]  # Threshold for DDoS
    
    if ddos_sources:
        log_threat("DDoS", f"Potential DDoS sources: {', '.join(ddos_sources)}")
        
    return ddos_sources

def detect_port_scan(traffic_data):
    """
    Detect potential port scanning activity by identifying multiple destination ports from a single source IP.
    
    Args:
        traffic_data (list): List of network traffic dictionaries.
        
    Returns:
        list: List of source IPs flagged for port scanning behavior.
    """
    port_scan_sources = []
    source_ports = {}

    for traffic in traffic_data:
        source = traffic['source']
        destination_port = traffic['destination_port']
        
        if source not in source_ports:
            source_ports[source] = set()
        source_ports[source].add(destination_port)

        if len(source_ports[source]) > 10:  # Threshold for port scanning
            port_scan_sources.append(source)
            log_threat("Port Scan", f"Port scanning detected from IP: {source}")
    
    return list(set(port_scan_sources))

def detect_suspicious_ip_ranges(traffic_data, suspicious_ranges):
    """
    Identify traffic originating from specified suspicious IP ranges.
    
    Args:
        traffic_data (list): List of network traffic dictionaries.
        suspicious_ranges (list): List of IP address ranges considered suspicious.
        
    Returns:
        list: List of traffic entries flagged as originating from suspicious IP ranges.
    """
    suspicious_ips = []

    for traffic in traffic_data:
        source_ip = traffic['source']
        if any(source_ip.startswith(range_prefix) for range_prefix in suspicious_ranges):
            suspicious_ips.append(source_ip)
            log_threat("Suspicious IP", f"Traffic from suspicious IP: {source_ip}")
    
    return suspicious_ips

def log_threat(threat_type, description):
    """
    Log identified threats in the database for auditing and notification purposes.
    
    Args:
        threat_type (str): Type of threat detected (e.g., DDoS, Port Scan).
        description (str): Detailed description of the threat.
    """
    session = get_db_session()
    try:
        threat_log = ThreatLog(
            threat_type=threat_type,
            description=description,
            timestamp=datetime.utcnow()
        )
        session.add(threat_log)
        session.commit()
    except Exception as e:
        print(f"Failed to log threat: {e}")
        session.rollback()
    finally:
        session.close()
