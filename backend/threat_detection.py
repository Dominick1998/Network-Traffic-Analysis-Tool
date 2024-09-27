from collections import defaultdict

def detect_ddos(traffic_data, threshold=100):
    """
    Detect potential DDoS attacks by checking for a high number of requests
    from a single IP address in a short time frame.

    Args:
        traffic_data (list): A list of traffic records.
        threshold (int): The number of requests from a single source IP that
                         triggers the detection of a potential DDoS attack.

    Returns:
        list: A list of detected DDoS attacks.
    """
    ip_counts = defaultdict(int)

    for traffic in traffic_data:
        source_ip = traffic['source']
        ip_counts[source_ip] += 1

    ddos_attacks = [
        {'source_ip': ip, 'count': count}
        if count > threshold else None
        for ip, count in ip_counts.items()
    ]

    return [attack for attack in ddos_attacks if attack]
