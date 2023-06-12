import subprocess
import csv

def get_live_host(ip):
    command = f"nmap -sn {ip}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    
    live_host = "N/A"
    live_ip = "N/A"
    
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            parts = line.split()
            live_host = parts[4]
            live_ip = parts[5][1:-1]
            break
    
    return live_host, live_ip

def main():
    with open('input.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row
        data = list(reader)
    
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header + ['Live_Host', "Live_host's_IP"])
        
        for row in data:
            hostname = row[0].rstrip("#")
            subnet = row[1]
            interface = row[2]
            live_host, live_ip = get_live_host(subnet)
            writer.writerow([hostname, subnet, interface, live_host, live_ip])
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
