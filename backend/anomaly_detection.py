import numpy as np

def detect_anomalies(traffic_data, threshold=1.5):
    """
    Detect anomalies in network traffic based on packet length.

    Args:
        traffic_data (list): List of network traffic records, each containing packet lengths.
        threshold (float): The z-score threshold for detecting anomalies.

    Returns:
        list: A list of traffic records that are considered anomalies.
    """
    # Extract packet lengths from traffic data
    packet_lengths = [traffic['length'] for traffic in traffic_data]

    # Calculate the mean and standard deviation of packet lengths
    mean_length = np.mean(packet_lengths)
    std_length = np.std(packet_lengths)

    anomalies = []
    for traffic in traffic_data:
        z_score = (traffic['length'] - mean_length) / std_length
        if abs(z_score) > threshold:
            anomalies.append(traffic)

    return anomalies
