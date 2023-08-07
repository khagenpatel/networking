import csv
import concurrent.futures
from netmiko import ConnectHandler, SSHException, NetmikoTimeoutException

def get_device_info(device_ip, username, password):
    try:
        # SSH into the device
        device = ConnectHandler(device_type='arista_eos', ip=device_ip, username=username, password=password)

        # Run command
        output = device.send_command("show mac address | i /", use_textfsm=True)

        # Parse the output to extract hostname, interface, and MAC address
        lines = output.split("\n")
        for line in lines:
            if '/' in line:
                parts = line.split()
                hostname = device.find_prompt()[:-1] # Get hostname from prompt
                mac_address = parts[0]
                interface = parts[-1]
                return (hostname, device_ip, interface, mac_address)
    except (SSHException, NetmikoTimeoutException) as e:
        print(f"Failed to connect to {device_ip} due to {str(e)}")
    
    return (None, None, None, None)

def main():
    username = 'your-username'
    password = 'your-password'
    
    # Open the IP addresses file
    with open('ip_addresses.txt', 'r') as file:
        ip_addresses = file.read().splitlines()

    # Prepare CSV file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hostname", "IP", "Interface", "MAC Address"])

        # For each IP address, get the device info and write it to the CSV
        # Using concurrent futures to run get_device_info() in parallel for each IP
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_ip = {executor.submit(get_device_info, ip, username, password): ip for ip in ip_addresses}
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    info = future.result()
                except Exception as e:
                    print(f"An error occurred with {ip}: {e}")
                else:
                    writer.writerow(info)

if __name__ == "__main__":
    main()
