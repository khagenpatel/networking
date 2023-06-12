import re
import csv

# Open the input file and create the CSV file for writing
with open('input.txt', 'r') as file, open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Hostname', 'Subnet'])

    # Pattern for matching the hostname and subnet
    pattern = r"^(.*?)#\r?\n(?:.*?\r?\n)*?(C\s+([\d./]+))"

    # Iterate through each line of the file
    for line in file:
        # Search for the pattern in each line
        match = re.search(pattern, line)
        if match:
            hostname = match.group(1)
            subnet = match.group(3)
            writer.writerow([hostname, subnet])
