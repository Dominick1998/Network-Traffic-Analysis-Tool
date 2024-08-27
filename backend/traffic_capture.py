from scapy.all import sniff, IP, TCP, UDP
import logging

# Configure logging to write captured packets to a file
logging.basicConfig(filename='network_traffic.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def process_packet(packet):
    """
    Process a captured network packet and log its details.

    Args:
        packet: A network packet captured by Scapy.

    Returns:
        None
    """
    # Check if the packet has an IP layer
    if IP in packet:
        ip_layer = packet[IP]
        protocol = None

        # Determine the protocol and extract relevant details
        if TCP in packet:
            protocol = 'TCP'
            transport_layer = packet[TCP]
        elif UDP in packet:
            protocol = 'UDP'
            transport_layer = packet[UDP]
        else:
            protocol = 'Other'
            transport_layer = None

        # Log the packet details
        logging.info(f'Source: {ip_layer.src} | Destination: {ip_layer.dst} | '
                     f'Protocol: {protocol} | Length: {len(packet)}')

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
    # Example: Capture 10 packets on the default interface
    start_sniffing(packet_count=10)
