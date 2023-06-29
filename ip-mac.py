import threading
import paramiko

# Define the filename to save the output
output_filename = 'device_info.txt'

def save_device_info(device_info):
    """Save device information to a file."""
    with open(output_filename, 'a') as f:
        f.write(device_info)
        f.write('\n\n')

def get_cisco_ios_info(device):
    """Retrieve hostname, MAC addresses, and ARP table from a Cisco IOS device."""
    hostname = device['hostname']
    username = device['username']
    password = device['password']
    enable_password = device['enable_password']

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Enable privilege mode if an enable password is provided
        if enable_password:
            enable_cmd = f'enable\n{enable_password}\n'
            client.send(enable_cmd)
            client.recv(1000)  # Read the prompt

        # Run show commands
        commands = [
            'show run | include hostname',
            'show mac address-table',
            'show ip arp',
        ]

        device_info = f'Device: {hostname}\n\n'

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            device_info += f'Command: {command}\n'
            device_info += output
            device_info += '\n'

        save_device_info(device_info)

        client.close()

        print(f'Retrieved information from {hostname}.')

    except paramiko.AuthenticationException:
        print(f'Authentication failed for {hostname}.')
    except paramiko.SSHException as e:
        print(f'Error occurred while connecting to {hostname}: {str(e)}')

def get_cisco_nxos_info(device):
    """Retrieve hostname, MAC addresses, and ARP table from a Cisco Nexus device."""
    hostname = device['hostname']
    username = device['username']
    password = device['password']

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Run show commands
        commands = [
            'show hostname',
            'show mac address-table',
            'show ip arp',
        ]

        device_info = f'Device: {hostname}\n\n'

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            device_info += f'Command: {command}\n'
            device_info += output
            device_info += '\n'

        save_device_info(device_info)

        client.close()

        print(f'Retrieved information from {hostname}.')

    except paramiko.AuthenticationException:
        print(f'Authentication failed for {hostname}.')
    except paramiko.SSHException as e:
        print(f'Error occurred while connecting to {hostname}: {str(e)}')

def process_device(device):
    """Process a single device based on its device type."""
    device_type = device.get('device_type')
    if device_type == 'cisco_ios':
        get_cisco_ios_info(device)
    elif device_type == 'cisco_nxos':
        get_cisco_nxos_info(device)
    else:
        print(f'Unknown device type for {device["hostname"]}')

def main():
    # Read device information
        # Read device information from the file
    with open('device_list.txt', 'r') as f:
        device_lines = f.read().splitlines()

    # Create a list to store device dictionaries
    devices = []

    # Parse device information from each line
    for line in device_lines:
        if line.strip():  # Skip empty lines
            hostname, device_type = line.split(',')
            devices.append({
                'hostname': hostname.strip(),
                'username': 'your_username',
                'password': 'your_password',
                'device_type': device_type.strip(),
                'enable_password': 'your_enable_password'
            })

    # Create a list to store threads
    threads = []

    # Process each device using multithreading
    for device in devices:
        t = threading.Thread(target=process_device, args=(device,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print('Script execution completed.')

if __name__ == '__main__':
    main()
