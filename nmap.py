import subprocess
import csv

def get_live_hosts(ip_range):
    command = f"nmap -sn {ip_range}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    live_hosts = []
    
    lines = output.split("\n")
    for line in lines:
        if "Nmap scan report for" in line:
            host_line = line.split("Nmap scan report for ")[1]
            host = host_line.split(" (")[0]
            ip = host_line.split(" (")[1].split(")")[0]
            live_hosts.append((host, ip))
    
    return live_hosts

def main():
    with open('input.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row
        ip_range_index = header.index('Subnet')
        data = list(reader)
    
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header + ['Live_Host', "Live_host's_IP"])
        
        for row in data:
            ip_range = row[ip_range_index]
            live_hosts = get_live_hosts(ip_range)
            live_host_info = live_hosts.pop(0) if live_hosts else ("N/A", "N/A")
            writer.writerow(row + live_host_info)
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
