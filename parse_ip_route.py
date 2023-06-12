import re
import csv
import datetime

input_file = "input.txt"
output_file = f"output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

non_compliant_sections = []
compliant_sections = []

# Regex pattern to match the hostname line
hostname_pattern = r"^([^#]+)#"

# Regex pattern to match the subnet and interface lines
subnet_pattern = r"^C\s+([\d.]+/\d+)\s+is directly connected,\s+([\w/]+)"

with open(input_file, 'r') as file:
    lines = file.readlines()

# Iterate over the lines in the input file
i = 0
while i < len(lines):
    line = lines[i].strip()
    if re.match(hostname_pattern, line):
        hostname = re.match(hostname_pattern, line).group(1)
        i += 1
        if i < len(lines) and lines[i].strip() == "show ip route connected":
            i += 1
            if i < len(lines) and not lines[i].startswith(" ") and not lines[i].startswith("show ip route"):
                non_compliant_sections.append((hostname, "show ip route connected not found"))
                i += 1
            else:
                i += 1
                section = []
                while i < len(lines) and lines[i].strip() != "":
                    line = lines[i].strip()
                    if re.match(subnet_pattern, line):
                        subnet = re.match(subnet_pattern, line).group(1)
                        interface = re.match(subnet_pattern, line).group(2)
                        section.append((hostname, subnet, interface))
                    else:
                        non_compliant_sections.append((hostname, "Invalid line format"))
                    i += 1
                compliant_sections.extend(section)
        else:
            non_compliant_sections.append((hostname, "Invalid section format"))
    else:
        non_compliant_sections.append(("Unknown", "Invalid line format"))
        i += 1

# Print non-compliant sections
print("Non-compliant sections:")
for section in non_compliant_sections:
    print(f"{section[0]} - Reason: {section[1]}")
print()

# Print compliant sections
print("Compliant sections:")
for section in compliant_sections:
    print(f"{section[0]} | {section[1]} | {section[2]}")
print()

# Save compliant sections to CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["hostname", "subnet", "interface"])
    writer.writerows(compliant_sections)

print(f"Output saved to {output_file}")
