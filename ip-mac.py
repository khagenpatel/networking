from netmiko import ConnectHandler, NetmikoTimeoutException
import time

# List of switch IP addresses
switch_ips = ['192.168.1.1', '192.168.1.2', '192.168.1.3']

# SSH credentials
username = 'abcd'
password = 'defg'

# Linux jump server credentials and IP
jump_server_ip = '192.168.2.1'
jump_server_username = 'jumpuser'
jump_server_password = 'jumppassword'

# Open a file to save the output
with open('switch_info.txt', 'w') as file:

    # Loop through each switch IP
    for ip in switch_ips:
        # SSH device parameters
        cisco_switch = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }

        try:
            # Try to establish SSH connection directly to the switch
            net_connect = ConnectHandler(**cisco_switch)
        except NetmikoTimeoutException:
            # If direct connection fails, use Linux jump server
            print(f"Direct connection to {ip} failed. Using jump server.")
            jump_server = {
                'device_type': 'linux',
                'ip': jump_server_ip,
                'username': jump_server_username,
                'password': jump_server_password,
            }
            try:
                net_connect = ConnectHandler(**jump_server)
                # SSH from jump server to switch
                net_connect.write_channel(f'ssh {username}@{ip}\n')
                time.sleep(1)
                net_connect.write_channel(f'{password}\n')
                time.sleep(1)
            except NetmikoTimeoutException:
                # If connection through jump server fails, write error to file and continue
                file.write(f"Failed to connect to switch {ip} through jump server\n")
                continue

        # Execute commands
        hostname = net_connect.send_command('show run | include hostname')
        mac_address_table = net_connect.send_command('show mac address-table')
        arp_table = net_connect.send_command('show ip arp')

        # Write output to file
        file.write(f'==== {hostname} ====\n')
        file.write('---- MAC Address Table ----\n')
        file.write(mac_address_table + '\n')
        file.write('---- ARP Table ----\n')
        file.write(arp_table + '\n')

        # Close SSH connection
        net_connect.disconnect()

        # Optional sleep to prevent overwhelming the switches
        time.sleep(1)

print("Switch information saved to switch_info.txt")
