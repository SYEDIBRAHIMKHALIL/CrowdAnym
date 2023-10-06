from scapy.layers.dot11 import Dot11, Dot11ProbeReq, Dot11Elt
from scapy.layers.dot11 import RadioTap
from scapy.all import *

# Define a function to process packets and extract MAC addresses
def extract_probe_request_mac_addresses(pcap_file):
    # Initialize an empty list to store the MAC addresses
    mac_addresses = []

    # Load the PCAP file
    packets = rdpcap(pcap_file)

    # Iterate through the packets
    for packet in packets:
        if Dot11ProbeReq in packet:
            # Check if it's a Probe Request packet
            ssid = packet[Dot11Elt][0].info.decode("utf-8", errors="ignore")
            if ssid == "":
                # If SSID is empty, it's a wildcard SSID
                src_mac = packet.addr2
                mac_addresses.append(src_mac)

    return mac_addresses

# Define a function to save MAC addresses to a text file
def save_mac_addresses_to_file(mac_addresses, output_file):
    with open(output_file, "w") as file:
        for mac in mac_addresses:
            file.write(mac + "\n")

# Usage example:
pcap_file = "Gruner Markt.pcap"  # Replace with your PCAP file path
output_file = "GRUNER2_mac_addresses.txt"  # Replace with the desired output file name
mac_addresses = extract_probe_request_mac_addresses(pcap_file)
save_mac_addresses_to_file(mac_addresses, output_file)
