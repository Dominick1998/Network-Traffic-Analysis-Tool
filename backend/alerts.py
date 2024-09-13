def check_alert_conditions(traffic_data):
    """
    Check for specific conditions in traffic data that trigger alerts.

    Args:
        traffic_data (list): List of network traffic records.

    Returns:
        list: A list of triggered alerts based on traffic conditions.
    """
    alerts = []

    # Example condition: trigger alert if a packet exceeds 2000 in length
    for traffic in traffic_data:
        if traffic['length'] > 2000:
            alerts.append({
                'type': 'Large Packet',
                'message': f"Packet from {traffic['source']} to {traffic['destination']} with size {traffic['length']} exceeds threshold."
            })

    # Example condition: trigger alert if a specific protocol is detected
    for traffic in traffic_data:
        if traffic['protocol'].lower() == 'icmp':
            alerts.append({
                'type': 'ICMP Detected',
                'message': f"ICMP packet detected from {traffic['source']} to {traffic['destination']}."
            })

    return alerts
