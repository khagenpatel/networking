import re
import csv

# Regular expressions for parsing the MAC address table entries
hostname_regex = re.compile(r'==== (.+?) ====')
mac_entry_regex = re.compile(r'\s*\S+\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+\S+\s+(?:\S+\s+)*([\w/]+)')

# Open CSV file to save the output
with open('mac_addresses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['hostname', 'mac_address', 'interface'])

    # Initialize hostname
    hostname = None

    # Read the notepad file line by line
    with open('mac_table.txt', 'r') as file:
        for line in file:
            # Check for hostname
            hostname_match = hostname_regex.match(line)
            if hostname_match:
                hostname = hostname_match.group(1).strip()

            # Check for MAC address entry
            mac_entry_match = mac_entry_regex.match(line)
            if mac_entry_match and hostname:
                mac_address, interface = mac_entry_match.groups()
                writer.writerow([hostname, mac_address, interface])

print("MAC address information saved to mac_addresses.csv")
