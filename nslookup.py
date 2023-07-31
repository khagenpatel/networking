import paramiko
import csv

# Substitute with your real credentials and server details
hostname = 'your.jump.server.ip'
username = 'your-username'
password = 'your-password'

# Load the hostnames from a file
with open('hosts.txt', 'r') as f:
    hostnames = [line.strip() for line in f]

# Create a new SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)

# Connect to the SSH server
client.connect(hostname, username=username, password=password)

# Prepare the csv file for output
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Hostname", "IP"])

    for host in hostnames:
        command = f"nslookup {host}"

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        
        # Get the command output
        output = stdout.read().decode()

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

# Disconnect from the SSH server
client.close()
