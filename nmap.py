import subprocess
import csv

def get_live_host(hostname, ip):
    command = f"nmap -sn {ip}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if "Host is up" in output:
        live_host = hostname.strip("#")
        live_ip = output.split("for ")[1].split()[0]
        return live_host, live_ip
    else:
        return None, None

input_file = "input.csv"
output_file = "live_hosts.csv"

live_hosts = []
with open(input_file, "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        hostname, subnet, interface = row
        live_host, live_ip = get_live_host(hostname, subnet)
        if live_host and live_ip:
            live_hosts.append([hostname, subnet, interface, live_host, live_ip])

with open(output_file, "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Hostname", "Subnet", "Interface", "Live Host", "Live IP"])
    csv_writer.writerows(live_hosts)

print(f"Output saved to {output_file}.")
