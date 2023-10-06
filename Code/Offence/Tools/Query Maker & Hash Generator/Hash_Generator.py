import hashlib

def generate_hash(mac_address, salt):
    # Concatenate the MAC address and salt
    mac_with_salt = mac_address + salt

    # Create a SHA224 hash object
    sha224_hash = hashlib.sha224(mac_with_salt.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    sha224_hex = sha224_hash.hexdigest()

    return sha224_hex

def process_mac_file(input_file, output_file, salt):
    with open(input_file, 'r') as file:
        mac_addresses = file.read().splitlines()

    with open(output_file_with_MACs, 'w') as file:
        for mac_address in mac_addresses:
            sha224_hash = generate_hash(mac_address, salt)
            file.write(f'{mac_address}: {sha224_hash}\n')
    with open(output_file, 'w') as file:
        for mac_address in mac_addresses:
            sha224_hash = generate_hash(mac_address, salt)
            file.write(f'{sha224_hash}\n')

# Example usage
input_file = './formatted_macs.txt'
output_file = 'hashed_mac_addresses.txt'
output_file_with_MACs = 'hashed_mac_addresses_with_mac.txt'
salt = ' 111111111111' #Salt Value Here; Add space before salt value

process_mac_file(input_file, output_file, salt)
print(f"Hashed MAC addresses saved to '{output_file}'.")