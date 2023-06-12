import subprocess
import csv

def get_live_hosts(subnet):
    command = f"nmap -sn {subnet}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode().strip()
    
    live_hosts = []
    
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            parts = line.split()
            live_host = parts[4]
            live_ip = parts[5][1:-1]
            live_hosts.append((live_host, live_ip))
    
    return live_hosts

def main():
    with open('input.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row
        data = list(reader)
    
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header + ['Live_Hosts'])
        
        for row in data:
            hostname = row[0].rstrip("#")
            subnet = row[1]
            interface = row[2]
            live_hosts = get_live_hosts(subnet)
            live_hosts_str = ', '.join([f"{host} ({ip})" for host, ip in live_hosts])
            writer.writerow(row + [live_hosts_str])
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
