import csv
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# Initialize list for results
results = []

# Open device list and iterate over devices
with open('list_device.csv', 'r') as file:
    devices = csv.reader(file)
    next(devices)  # Skip the header
    for row in devices:
        ip = row[0]
        device_type = row[1]

        # Define device
        device = {
            'device_type': device_type,
            'ip': ip,
            'username': 'YOUR_USERNAME',
            'password': 'YOUR_PASSWORD',
            # Add more fields as necessary for your connection
        }

        try:
            # Connect to the device
            connection = ConnectHandler(**device)

            # Determine command based on device type
            command_template = None
            if device_type == 'cisco_nxos':
                command_template = 'show ip bgp | include {}'
            elif device_type == 'juniper':
                command_template = 'show route protocol bgp active-path | grep {}'

            # Check each AS number and add to results
            for as_number in range(65201, 65536):  # 65536 is exclusive
                command = command_template.format(as_number)
                output = connection.send_command(command)
                available = 'No' if output else 'Yes'
                results.append([ip, as_number, available])

            # Disconnect from the device
            connection.disconnect()

        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f'Failed to connect to {ip}: {str(e)}')

# Write results to CSV
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hostname', 'AS#', 'Available'])
    writer.writerows(results)
