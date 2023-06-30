import re
import csv

# Regular expressions for parsing the MAC address table entries
hostname_regex = re.compile(r'==== (.+?) ====')
mac_entry_regex = re.compile(r'\s*\S+\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+\S+\s+(?:\S+\s+)*([\w/]+)')

# Read the notepad file
with open('switch_info.txt', 'r') as file:
    content = file.read()

# Parse the content
matches = hostname_regex.split(content)[1:]

# Open CSV file to save the output
with open('mac_addresses.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['hostname', 'mac_address', 'interface'])

    # Iterate over the matched groups (hostname and corresponding MAC entries)
    for i in range(0, len(matches), 2):
        hostname = matches[i].strip()
        mac_section = matches[i + 1]

        # Find MAC address entries
        for mac_entry in mac_entry_regex.findall(mac_section):
            mac_address, interface = mac_entry
            writer.writerow([hostname, mac_address, interface])

print("MAC address information saved to mac_addresses.csv")
