import paramiko
import time

# Define the SSH credentials
username = 'abcd'
password = 'defg'

# Read the device list from a file
with open('device_list.txt', 'r') as f:
    devices = f.read().splitlines()

# Create a file to save the output
output_file = open('output.txt', 'w')

# Connect to each device and execute commands
for device in devices:
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device
        ssh.connect(device, username=username, password=password)

        # Start an interactive shell
        shell = ssh.invoke_shell()

        # Send the commands
        shell.send('show run | include hostname\n')
        shell.send('show mac address-table\n')
        shell.send('show ip arp\n')
        time.sleep(1)  # Wait for the commands to complete

        # Read the output
        output = ''
        while shell.recv_ready():
            output += shell.recv(1024)

        print("Output for {0}:\n{1}".format(device, output))  # Print the output for debugging

        # Retrieve the hostname
        hostname_start = output.find('hostname ')
        if hostname_start != -1:
            hostname_end = output.find('\n', hostname_start)
            if hostname_end != -1:
                hostname = output[hostname_start + len('hostname '):hostname_end].strip()
            else:
                hostname = 'Unknown'
        else:
            hostname = 'Unknown'

        output_file.write("Hostname of {0}: {1}\n".format(device, hostname))

        # Retrieve the MAC addresses
        mac_start = output.find('mac address-table')
        mac_end = output.find('Type:', mac_start)
        if mac_start != -1 and mac_end != -1:
            mac_addresses = output[mac_start:mac_end].strip()
        else:
            mac_addresses = 'Unknown'

        output_file.write("MAC addresses on {0}:\n{1}\n".format(device, mac_addresses))

        # Retrieve the IP ARP table
        arp_start = output.find('ip arp')
        if arp_start != -1:
            arp_table = output[arp_start + len('ip arp'):].strip()
        else:
            arp_table = 'Unknown'

        output_file.write("IP ARP table on {0}:\n{1}\n".format(device, arp_table))

        # Close the SSH connection
        ssh.close()

    except paramiko.AuthenticationException:
        output_file.write("Failed to authenticate to {0}\n".format(device))
    except paramiko.SSHException as e:
        output_file.write("SSH error occurred while connecting to {0}: {1}\n".format(device, str(e)))
    except paramiko.ssh_exception.NoValidConnectionsError:
        output_file.write("Unable to connect to {0}\n".format(device))

# Close the output file
output_file.close()
