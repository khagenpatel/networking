import paramiko

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

        # Retrieve the hostname
        stdin, stdout, stderr = ssh.exec_command('show run | include hostname')
        hostname = stdout.read().strip().split(' ')[1]

        output_file.write("Hostname of {}: {}\n".format(device, hostname))

        # Show MAC addresses
        stdin, stdout, stderr = ssh.exec_command('show mac address-table')
        mac_addresses = stdout.read()

        output_file.write("MAC addresses on {}:\n{}\n".format(device, mac_addresses))

        # Show IP ARP table
        stdin, stdout, stderr = ssh.exec_command('show ip arp')
        arp_table = stdout.read()

        output_file.write("IP ARP table on {}:\n{}\n".format(device, arp_table))

        # Close the SSH connection
        ssh.close()

    except paramiko.AuthenticationException:
        output_file.write("Failed to authenticate to {}\n".format(device))
    except paramiko.SSHException as e:
        output_file.write("SSH error occurred while connecting to {}: {}\n".format(device, str(e)))
    except paramiko.ssh_exception.NoValidConnectionsError:
        output_file.write("Unable to connect to {}\n".format(device))

# Close the output file
output_file.close()
