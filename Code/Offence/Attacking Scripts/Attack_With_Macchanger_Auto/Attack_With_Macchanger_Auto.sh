#!/bin/bash

# Path to the text file to save MAC addresses
mac_file="mac_addresses.txt"
mac_timestamp_file="mac_addresses_with_timestamp.txt"

# Path to the CSV output file
output_csv="generated_macs.csv"

# Function to generate a random MAC address using macchanger and record the timestamp
generate_random_mac() {
    mac_address=$(sudo macchanger -r wlan0 2>&1 | awk '/New MAC/ {print $3}')
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$mac_address|$timestamp"
}

# Function to change MAC address sequentially from 1 to 100
change_sequential_mac() {
    while IFS= read -r new_mac; do
        sudo macchanger -m "$new_mac" wlan0
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")
        echo "Changed MAC to: $new_mac | Timestamp: $timestamp"
        sudo iw wlan0 scan
    done < "$mac_file"
}

# Create empty files to store MAC addresses and MAC addresses with timestamps
> "$mac_file"
> "$mac_timestamp_file"

# Create or overwrite the CSV file with column headers
echo "MAC Address,Timestamp" > "$output_csv"

# Loop to generate random MAC addresses and save them to the files
count=0
while [ $count -lt 1500 ]; do
    mac_with_timestamp=$(generate_random_mac)
    mac_address=$(echo "$mac_with_timestamp" | cut -d "|" -f 1)
    if [ -n "$mac_address" ]; then
        echo "$mac_address" >> "$mac_file"
        echo "$mac_with_timestamp" >> "$mac_timestamp_file"
        echo "Generated MAC: $mac_address"
        count=$((count + 1))
        
        # Append the data to the CSV file
        echo "$mac_address,$timestamp" >> "$output_csv"
    fi
done

# Read the file and change MAC addresses sequentially
change_sequential_mac

echo "MAC address changing complete."
