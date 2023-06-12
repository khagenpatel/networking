import subprocess
import csv

def get_live_hosts(subnet):
    command = f"nmap -sn {subnet}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    
    live_hosts = []
    
    for line in process.stdout:
        line = line.decode().strip()
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
        writer.writerow(header + ['Live_Host', 'Live_IP'])
        
        for row in data:
            hostname = row[0].rstrip("#")
            subnet = row[1]
            interface = row[2]
            live_hosts = get_live_hosts(subnet)
            
            for i, (live_host, live_ip) in enumerate(live_hosts):
                if i == 0:
                    writer.writerow(row + [live_host, live_ip])
                else:
                    writer.writerow([hostname, subnet, interface, live_host, live_ip])
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
