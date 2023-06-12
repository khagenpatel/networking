import re
import csv
import logging

# Configure logging
logging.basicConfig(filename='parse.log', level=logging.DEBUG)

def parse_data():
    try:
        # Read the data from "input.txt"
        with open("input.txt", "r") as file:
            data = file.read()

        # Split the data into sections
        sections = re.split('show ip route connected', data)

        output_data = []

        # Loop over the sections
        for section in sections:
            # Find the hostname in the section
            hostname_search = re.search(r'(\S+)#$', section, re.M)
            if hostname_search:
                hostname = hostname_search.group(1)
            else:
                continue  # Skip this section if there's no hostname

            # Find all connected routes in the section
            connected_routes = re.findall(r'(C        \S+ is directly connected, \S+)', section)

            for route in connected_routes:
                subnet_in_cidr, interface = re.search(r'C        (\S+) is directly connected, (\S+)', route).groups()
                output_data.append([hostname, subnet_in_cidr, interface])

        # Write output to "output.csv"
        with open("output.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["hostname", "subnet_in_cidr", "interface"])
            writer.writerows(output_data)

        logging.info("Parsing complete, data written to output.csv")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    parse_data()
