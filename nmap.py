import subprocess
import csv
import concurrent.futures

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

def process_row(row):
    try:
        hostname = row[0].rstrip("#")
        subnet = row[1]
        interface = row[2]
        live_hosts = get_live_hosts(subnet)
        
        output_rows = []
        
        for i, (live_host, live_ip) in enumerate(live_hosts):
            if i == 0:
                output_rows.append(row + [live_host, live_ip])
            else:
                output_rows.append([hostname, subnet, interface, live_host, live_ip])
        
        return output_rows
    
    except IndexError:
        error_row = row + ['Error: Missing Values']
        return [error_row]

def main():
    with open('input.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row
        data = list(reader)
    
    output_rows = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_row, data)
        
        for result in results:
            output_rows.extend(result)
    
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header + ['Live_Host', 'Live_IP'])
        writer.writerows(output_rows)
    
    print("Output saved to output.csv")

if __name__ == "__main__":
    print("Processing...")
    main()
    print("Completed!")
