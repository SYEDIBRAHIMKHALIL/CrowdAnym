#!/usr/bin/env python3

import sys
import re
import subprocess
import codecs

import time

from scapy.layers.dot11 import Dot11, Dot11ProbeReq, Dot11Elt, RadioTap, Ether
from scapy.all import *

#!/usr/bin/env python3

from scapy.all import RadioTap, Dot11, Dot11ProbeReq, Dot11Elt, sendp

def create_probe_request_packet(new_mac_address, ssid):


# """     ssid = "SSG"
#     supported_rates = [1, 2, 5.5, 11, 6, 9, 12, 18]
#     extended_rates = [24, 36, 48, 54]
#     ht_capabilities = 0x09e7
#     extended_capabilities = 0x0400c88014000000
#     vendor_specific_info = "506f9a16030103650101" """

    # Create the Probe Request packet
    packet = (
     RadioTap()
        / Dot11(type=0, subtype=4, addr1="ff:ff:ff:ff:ff:ff", addr2=new_mac_address, addr3="ff:ff:ff:ff:ff:ff")
        / Dot11ProbeReq()
        / Dot11Elt(ID=0, len=len(ssid), info=ssid)
        / Dot11Elt(ID=1, len=8, info=[1, 2, 5, 11, 6, 9, 12, 18])
        / Dot11Elt(ID=2, len=4, info=[24, 36, 48, 54])
        )
    packet.show()
    
    return packet

def send_probe_requests(iface, mac_addresses, ssid):
    for mac in mac_addresses:
        packet = create_probe_request_packet(mac, ssid)
        sendp(packet, iface=iface)
        print("Sent probe requests with the SSID:", ssid)
        print("Mac is:", mac)

def main():
    counter = 0
    file_path = "./MACs.txt"
    mac_to_change_to = []

    # Hardcoded SSID for the probe requests
    ssid = ""
    iface = "wlan1mon"  # Change to your network interface

    with open(file_path, 'r') as file:
        for line in file:
            mac_to_change_to.append(line.strip())

    send_probe_requests(iface, mac_to_change_to, ssid)

if __name__ == "__main__":
    main()
