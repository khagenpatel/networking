from netmiko import ConnectHandler
import csv

# Substitute with your real credentials and server details
linux_device = {
    'device_type': 'linux',
    'ip':   'your.jump.server.ip',
    'username': 'your-username',
    'password': 'your-password',
    'secret': 'your-password',  # if needed
}

def ssh_command(device, hostnames):
    connection = ConnectHandler(**device)

    # Prepare the csv file for output
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hostname", "IP"])

        for host in hostnames:
            command = f"nslookup {host}"
            output = connection.send_command(command).strip("\n")

            # Find the line in the output that contains the IP address
            ip = None
            for line in output.split('\n'):
                if "Address" in line:
                    ip = line.split(":")[1].strip()
                    writer.writerow([host, ip])
                    print(f"The IP for {host} is: {ip}")
                    break

            # Raise an exception if no IP was found for the hostname
            if ip is None:
                raise ValueError(f"No IP found for hostname {host}")

    connection.disconnect()

# Load the hostnames from a file
with open('hosts.txt', 'r') as f:
    hostnames = [line.strip() for line in f]

ssh_command(linux_device, hostnames)
