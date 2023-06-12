import re
import csv
from datetime import datetime

input_file = "input.txt"
output_file = f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

section_pattern = r"([^\n]+)\n([\s\S]+?)(?=\n\n|$)"
subnet_pattern = r"(?:C|L)\s+([\d./]+)\s+is\s+directly\s+connected,\s+(\S+)"
compliant_sections = []
non_compliant_sections = []

with open(input_file, "r") as file:
    data = file.read()

sections = re.findall(section_pattern, data)

for section in sections:
    hostname = section[0].strip()
    output = section[1].strip()

    if "show ip route connected" not in output:
        non_compliant_sections.append((hostname, "show ip route connected not found"))
        continue

    subnets = re.findall(subnet_pattern, output)
    if not subnets:
        non_compliant_sections.append((hostname, "Invalid line format"))
        continue

    compliant_sections.extend([(hostname, subnet[0], subnet[1]) for subnet in subnets])

if compliant_sections:
    print("Compliant sections:")
    for section in compliant_sections:
        print("\t".join(section))

if non_compliant_sections:
    print("\nNon-compliant sections:")
    for section in non_compliant_sections:
        print(f"{section[0]} - Reason: {section[1]}")

if compliant_sections:
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Hostname", "Subnet", "Interface"])
        writer.writerows(compliant_sections)

    print(f"\nOutput saved to {output_file}")
