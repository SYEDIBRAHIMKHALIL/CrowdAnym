#!/bin/bash

# Replace wlan0 with your wireless interface name
interface="wlan0"

# Path to the text file containing MAC addresses, one per line
mac_list_file="MACs2.txt"

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

# Function to change MAC address with retries
function change_mac_with_retry() {
    local max_attempts=5
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt to change MAC address to $1"
        sudo macchanger -m "$1" "$interface"

        # Get the current MAC address of the wireless interface
        current_mac=$(sudo macchanger -s "$interface" | awk '/Current/ {print $3}')

        if [ "$current_mac" = "$1" ]; then
            echo "MAC address successfully changed to $1"
            break
        else
            echo "Failed to change MAC address. Retrying..."
            attempt=$((attempt + 1))
        fi
    done
}

# Function to perform "sudo iw scan" with retries
function perform_iw_scan_with_retry() {
    local max_attempts=10
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt to perform 'sudo iw $interface scan'"
        sudo iw "$interface" scan

        # Check if the scan operation was successful
        if [ $? -eq 0 ]; then
            echo "Scan operation successful."
            break
        else
            echo "Scan operation failed. Retrying..."
            attempt=$((attempt + 1))
        fi
    done
}

# Create or overwrite the CSV file with column headers
echo "Time,Mac Address" > "$output_csv"

# Read MAC addresses from the file and send Probe Request frames for each MAC address
while IFS= read -r mac_address; do
    # Get the current time in HH:MM:SECONDS format
    current_time=$(date +"%H:%M:%S")

    # Format the MAC address to XX:XX:XX:XX:XX:XX format
    formatted_mac=$(format_mac "$mac_address")

    if [ ${#formatted_mac} -ne 17 ]; then
        echo "Invalid MAC address: $mac_address"
        continue
    fi

    echo "Sending Probe Request for MAC: $formatted_mac"

    # Change the MAC address of the wireless interface (with retries)
    change_mac_with_retry "$formatted_mac"

    # Perform "sudo iw scan" with retries
    perform_iw_scan_with_retry


    # Append the data to the CSV file
    echo "$current_time,$formatted_mac" >> "$output_csv"

done < "$mac_list_file"
