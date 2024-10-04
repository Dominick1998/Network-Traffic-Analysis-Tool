from backend.database import get_db_session
from backend.models import NetworkTraffic
from collections import Counter

def detect_ddos(traffic_list):
    """
    Detect potential Distributed Denial of Service (DDoS) attacks.

    Args:
        traffic_list (list): List of network traffic data.

    Returns:
        list: Detected DDoS threats.
    """
    ddos_threshold = 1000  # Example threshold for DDoS detection
    ip_counter = Counter([traffic['source'] for traffic in traffic_list])

    # Find IPs with traffic exceeding the threshold
    ddos_ips = [ip for ip, count in ip_counter.items() if count > ddos_threshold]

    threats = []
    for ip in ddos_ips:
        threats.append({
            'type': 'DDoS Attack',
            'source_ip': ip,
            'traffic_count': ip_counter[ip]
        })

    return threats

def detect_port_scan(traffic_list):
    """
    Detect potential port scanning activities.

    Args:
        traffic_list (list): List of network traffic data.

    Returns:
        list: Detected port scan threats.
    """
    port_threshold = 100  # Example threshold for detecting port scans
    traffic_by_ip = {}

    # Aggregate traffic by source IP and destination port
    for traffic in traffic_list:
        source_ip = traffic['source']
        destination_port = traffic.get('destination_port', 0)
        if source_ip not in traffic_by_ip:
            traffic_by_ip[source_ip] = set()
        traffic_by_ip[source_ip].add(destination_port)

    # Detect IPs scanning multiple ports
    port_scan_ips = [ip for ip, ports in traffic_by_ip.items() if len(ports) > port_threshold]

    threats = []
    for ip in port_scan_ips:
        threats.append({
            'type': 'Port Scan',
            'source_ip': ip,
            'scanned_ports': len(traffic_by_ip[ip])
        })

    return threats

def detect_suspicious_ip_ranges(traffic_list, suspicious_ranges):
    """
    Detect traffic from suspicious IP ranges.

    Args:
        traffic_list (list): List of network traffic d
