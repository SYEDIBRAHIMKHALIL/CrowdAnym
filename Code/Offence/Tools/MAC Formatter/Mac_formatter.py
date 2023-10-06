def format_mac_addresses(input_file, output_file):
    with open(input_file, 'r') as f:
        mac_addresses = f.read().splitlines()

    formatted_mac_addresses = []
    for mac in mac_addresses:
        # Remove any existing colons and other separators
        mac = mac.replace(":", "").replace("-", "").replace(".", "").upper()

        # Add colons after every two digits
        formatted_mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
        formatted_mac_addresses.append(formatted_mac)

    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_mac_addresses))

if __name__ == "__main__":
    input_file_path = "mac_lists.txt"   # Replace with your input file path
    output_file_path = "formatted_macs.txt"  # Replace with your output file path

    format_mac_addresses(input_file_path, output_file_path)
    print("MAC address formatting completed. Formatted addresses saved to 'formatted_macs.txt'.")
