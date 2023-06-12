import re
import csv
from datetime import datetime

# Read input from the file
with open('input.txt', 'r') as file:
    routing_table = file.read()

# Split the routing table into sections
sections = re.split(r'\n\n', routing_table)

# Process each section and save output to CSV
fieldnames = ['hostname', 'subnet', 'interface', 'timestamp']
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterating through each section
    for section in sections:
        # Extracting hostname from above the output section
        hostname_match = re.search(r'([\w#-]+)\nshow ip route', section)
        if hostname_match:
            hostname = hostname_match.group(1).strip()
        else:
            continue  # Skip section if hostname is not found

        # Extracting entries from the output section
        entries = re.findall(r'C\s+(\S+)\s+is directly connected,\s+(\w+)', section)

        # Iterating through each entry in the output section
        for entry in entries:
            subnet, interface = entry
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow({'hostname': hostname, 'subnet': subnet, 'interface': interface, 'timestamp': timestamp})
            
            # Print the current entry
            print(f"Hostname: {hostname}, Subnet: {subnet}, Interface: {interface}")

# Output CSV file is saved in every loop iteration
print("Output saved to output.csv")
