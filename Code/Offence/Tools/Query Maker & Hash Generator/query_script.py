def add_mac_addresses_to_query(query, mac_addresses):
    mac_conditions = [f"mac_address = '{mac}'" for mac in mac_addresses]
    mac_condition_str = " OR ".join(mac_conditions)
    modified_query = query + f"AND ({mac_condition_str})"
    return modified_query

# Example usage
query = "SELECT distinct (mac_address), eventtype, epocutc, zone, rssi, techtype, salt \nFROM testschemadb.flowtrack_raw_with_salt where zone = 'bz2454' AND eventtype= 'status' AND epocutc between '2023-07-27 13:00:00' AND '2023-07-27 15:00:00'\n"
hashed_mac_addresses = "./hashed_mac_addresses.txt"
query_text = "./query_text.txt"

with open(hashed_mac_addresses, 'r') as file:
    mac_addresses = [line.strip() for line in file.readlines()]

# Add MAC addresses to the query
modified_query = add_mac_addresses_to_query(query, mac_addresses)
final_query = modified_query + "\nORDER by epocutc"

with open(query_text, 'w') as file:
      file.write(f'{final_query}\n')
# Print the modified query
print("Modified query:")
print(final_query)



