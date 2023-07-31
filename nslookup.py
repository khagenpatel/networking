import re
import csv

# Load the nslookup output from a file
with open('nslookup.txt', 'r') as f:
    nslookup_output = f.read()

# Split the output into separate nslookup results
nslookup_results = nslookup_output.split('\n\n')

# Prepare the csv file for output
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Hostname", "IP"])

    for result in nslookup_results:
        # Find the hostname and IP address in the nslookup result
        match = re.search(r'Non-authoritative answer:\nName:\s+(.+)\nAddress:\s+(.+)', result)
        if match:
            hostname = match.group(1)
            ip = match.group(2)
            writer.writerow([hostname, ip])
            print(f"The IP for {hostname} is: {ip}")
