import paramiko

# Read the device IP addresses from device_list.txt
with open('device_list.txt', 'r') as file:
    ip_addresses = file.read().splitlines()

# Define the common credentials
username = 'abcd'
password = 'defg'

# Open the notepad file in append mode
output_file = open('output.txt', 'a')

for ip_address in ip_addresses:
    # Create a new SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the device
        client.connect(hostname=ip_address, username=username, password=password)

        # Send the necessary commands and retrieve the output
        commands = ['show hostname', 'show mac address-table', 'show ip arp']
        for command in commands:
            client.send(command + '\n')
            client.expect('#')
            output = client.recv(65535).decode('utf-8')

            # Write the output to the notepad file
            output_file.write('\nDevice: {}\n'.format(ip_address))
            output_file.write('Command: {}\n'.format(command))
            output_file.write(output)

    except Exception as e:
        print('Error connecting to {}: {}'.format(ip_address, str(e)))

    finally:
        # Close the SSH connection
        client.close()

# Close the notepad file
output_file.close()
