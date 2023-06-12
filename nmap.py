import subprocess
import csv
import concurrent.futures

def get_live_host(subnet):
    command = f"nmap -sn {subnet}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    
    live_host = "N/A"
    live_ip = "N/A"
    
    for line in output.splitlines():
        if "Nmap scan report for" in line:
            parts = line.split()
            live_host = parts[4]
            live_ip = parts[5][1:-1]
            break
    
    return live_host, live_ip

def process_subnet(row):
    hostname = row[0].rstrip("#")
    subnet = row[1]
    interface = row[2]
    live_host, live_ip = get_live_host(subnet)
    
    return [hostname, subnet, interface, live_host, live_ip]

def main():
    with open('input.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row
        data = list(reader)
    
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header + ['Live_Host', "Live_host's_IP"])
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_subnet, data)
            writer.writerows(results)
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
