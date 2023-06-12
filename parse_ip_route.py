import re
import csv
import logging

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO)

try:
    # Open your text file
    with open('path_to_your_textfile.txt', 'r') as file:
        data = file.read()

    # Split the data by the command "show ip route connected"
    sections = data.split('show ip route connected')

    # Prepare data for CSV
    csv_data = []

    for section in sections[1:]:  # Skip the first section, which is empty
        # Find the hostname in the section (strip the "#" and any trailing whitespace)
        hostname = re.search(r'([\w\-]+#)', section)
        if hostname:
            hostname = hostname.group().rstrip('#').strip()

        # Find the IP routes and interfaces in the section
        routes = re.findall(r'(C\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}) is directly connected, (\w+))', section)
        for route in routes:
            csv_data.append([hostname, route[1], route[2]])

    # Write data to CSV
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["hostname", "subnet_in_cidr", "interface"])
        writer.writerows(csv_data)
except Exception as e:
    logging.exception("Exception occurred")

