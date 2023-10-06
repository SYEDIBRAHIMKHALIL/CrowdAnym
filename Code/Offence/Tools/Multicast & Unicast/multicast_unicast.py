def is_multicast_mac(mac_address):
    # Check if the least significant bit (LSB) of the first octet is 1 (indicating multicast address)
    first_octet = int(mac_address.split(':')[0], 16)
    lsb = first_octet & 1
    return lsb == 1

def check_mac_addresses(input_file, output_file):
    with open(input_file, 'r') as f:
        mac_addresses = f.read().splitlines()

    results = []
    for mac in mac_addresses:
        mac_type = 'multicast' if is_multicast_mac(mac) else 'unicast'
        results.append(f"{mac} : {mac_type}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(results))

if __name__ == "__main__":
    input_file_path = "formatted_macs.txt"   # Replace with your input file path
    output_file_path = "multicast_unicast.txt"  # Replace with your output file path

    check_mac_addresses(input_file_path, output_file_path)
    print("MAC address analysis completed. Results saved to 'multicast_unicast.txt'.")
