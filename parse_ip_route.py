import re
import csv

# Read input from the file
with open('input.txt', 'r') as file:
    routing_table = file.read()

# Split the routing table into sections by 'show ip route connected'
sections = re.split(r'show ip route connected', routing_table)

# Process each section and save output to CSV
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['hostname', 'subnet', 'interface']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # Iterating through each section
    for section in sections:
        # Extracting hostname from the section
        hostname_match = re.search(r'([^\n]+)#', section)
        if hostname_match:
            hostname = hostname_match.group(1).strip()
            print(f"Hostname: {hostname}")
        else:
            continue  # Skip section if hostname is not found

        # Extracting entries from the section
        entries = re.findall(r'C\s+([\d./]+)\s+is directly connected,\s+(\w+)', section)
        print("Entries:")
        print(entries)

        # Iterating through each line in the section
        for entry in entries:
            subnet, interface = entry
            writer.writerow({'hostname': hostname, 'subnet': subnet, 'interface': interface})
