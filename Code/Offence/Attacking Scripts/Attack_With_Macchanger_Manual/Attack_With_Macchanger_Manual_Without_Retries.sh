#!/bin/bash

# Replace wlan0 with your wireless interface name
interface="wlan0"

# Path to the text file containing MAC addresses, one per line
mac_list_file="MACs1.txt"

# Path to the CSV output file
output_csv="scan_results.csv"

# Function to format MAC address to XX:XX:XX:XX:XX:XX format
function format_mac() {
    # Remove any non-hexadecimal characters
    mac=$(echo "$1" | tr -d '[:space:]' | tr -cd '[:xdigit:]')
    # Insert colons after every two characters
    formatted_mac=$(sed 's/\(..\)/\1:/g; s/.$//' <<< "$mac")
    echo "$formatted_mac"
}

# Create or overwrite the CSV file with column headers
echo "Time,Mac Address" > "$output_csv"

# Read MAC addresses from the file and send Probe Request frames for each MAC address
while IFS= read -r mac_address; do
    # Get the current time in HH:MM:SS format
    current_time=$(date +"%H:%M:%S")

    # Format the MAC address to XX:XX:XX:XX:XX:XX format
    formatted_mac=$(format_mac "$mac_address")

    if [ ${#formatted_mac} -ne 17 ]; then
        echo "Invalid MAC address: $mac_address"
        continue
    fi

    echo "Sending Probe Request for MAC: $formatted_mac"

    # Change the MAC address of the wireless interface
    sudo macchanger -m "$formatted_mac" "$interface"

    # Perform "sudo iw scan"
    sudo iw "$interface" scan

    # Append the data to the CSV file
    echo "$current_time,$formatted_mac" >> "$output_csv"
    
done < "$mac_list_file"
