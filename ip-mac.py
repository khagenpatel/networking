import getpass
import threading
import paramiko

# Define the filename to save the output
output_filename = 'device_info.txt'

def save_device_info(device_info):
    """Save device information to a file."""
    with open(output_filename, 'a', encoding='utf-8') as f:
        f.write(device_info)
        f.write('\n\n')

def get_device_info(device):
    """Retrieve hostname, MAC addresses, and ARP table from a Cisco device."""
    hostname = device['hostname']
    username = device['username']
    password = device['password']

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Determine device type based on the prompt symbol
        stdin, stdout, stderr = client.exec_command('')
        prompt = stdout.read().decode('utf-8')

        if '>' in prompt:
            device_type = "cisco_ios"
        elif '#' in prompt:
            device_type = "cisco_nxos"
        else:
            device_type = "unknown"

        # Run show commands
        commands = [
            'show run | include hostname',
            'show mac address-table',
            'show ip arp',
        ]

        device_info = 'Device: ' + hostname + '\n\n'

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            device_info += 'Command: ' + command + '\n'
            device_info += output
            device_info += '\n'

        save_device_info(device_info)

        client.close()

        print 'Retrieved information from {}. Device Type: {}'.format(hostname, device_type)

    except paramiko.AuthenticationException:
        print 'Authentication failed for {}.'.format(hostname)
    except paramiko.SSHException as e:
        print 'Error occurred while connecting to {}: {}'.format(hostname, str(e))

def process_device(device):
    """Process a single device."""
    get_device_info(device)

def main():
    # Specify the username and password
    try:
        username = getpass.getpass('Enter your username: ')
        password = getpass.getpass('Enter your password: ')
    except EOFError:
        print('User pressed Ctrl+D to end input.')
        sys.exit()

    # Read device information from the file
    with open('device_list.txt', 'r') as f:
        device_lines = f.read().splitlines()

    # Create a list to store device dictionaries
    devices = []

    # Parse device information from each line
    for line in device_lines:
        if line.strip():  # Skip empty lines
            hostname = line.strip()
            devices.append({
                'hostname': hostname,
                'username': username,
                'password': password,
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

    print 'Script execution completed.'

if __name__ == '__main__':
    main()
