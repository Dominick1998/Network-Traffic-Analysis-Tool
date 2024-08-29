from scapy.all import sniff, IP, TCP, UDP
import logging
from backend.traffic_processor import save_packet_to_db

# Configure logging to write captured packets to a file
logging.basicConfig(filename='network_traffic.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def process_packet(packet):
    """
    Process a captured network packet, log its details, and save it to the database.

    Args:
        packet: A network packet captured by Scapy.

    Returns:
        None
    """
    if IP in packet:
        ip_layer = packet[IP]
        protocol = None

        if TCP in packet:
            protocol = 'TCP'
        elif UDP in packet:
            protocol = 'UDP'
        else:
            protocol = 'Other'

        # Prepare packet data
        packet_data = {
            'source': ip_layer.src,
            'destination': ip_layer.dst,
            'protocol': protocol,
            'length': len(packet)
        }

        # Log the packet details
        logging.info(f"Source: {packet_data['source']} | Destination: {packet_data['destination']} | Protocol: {packet_data['protocol']} | Length: {packet_data['length']}")

        # Save the packet to the database
        save_packet_to_db(packet_data)

def start_sniffing(interface=None, packet_count=0):
    """
    Start capturing network traffic on a specified interface.

    Args:
        interface (str): The network interface to capture packets on. If None, captures on all interfaces.
        packet_count (int): The number of packets to capture. 0 for unlimited.

    Returns:
        None
    """
    print(f"Starting packet capture on interface: {interface if interface else 'all interfaces'}")
    sniff(iface=interface, prn=process_packet, count=packet_count)

if __name__ == '__main__':
    start_sniffing(packet_count=10)
