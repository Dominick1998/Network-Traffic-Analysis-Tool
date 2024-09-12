from collections import Counter

def generate_network_summary(traffic_data):
    """
    Generate a summary of network traffic data.

    Args:
        traffic_data (list): List of network traffic records.

    Returns:
        dict: A summary of the network traffic, including total packets, average length, 
              top sources, and top destinations.
    """
    total_packets = len(traffic_data)
    if total_packets == 0:
        return {
            "total_packets": 0,
            "average_length": 0,
            "top_sources": [],
            "top_destinations": []
        }

    total_length = sum(traffic['length'] for traffic in traffic_data)
    average_length = total_length / total_packets

    sources = [traffic['source'] for traffic in traffic_data]
    destinations = [traffic['destination'] for traffic in traffic_data]

    top_sources = Counter(sources).most_common(3)
    top_destinations = Counter(destinations).most_common(3)

    return {
        "total_packets": total_packets,
        "average_length": average_length,
        "top_sources": top_sources,
        "top_destinations": top_destinations
    }
