import paramiko
import threading
import time

username = 'admin'
password = 'cisco'
enable_password = 'cisco'

def get_device_info(device_ip):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(device_ip, username=username, password=password,
                          allow_agent=False, look_for_keys=False)

        # Get hostname
        hostname = ssh_client.get_hostname()

        # Get show mac add
        output = ssh_client.exec_command('show mac add')
        show_mac_add = output[0].decode('utf-8')

        # Get show ip arp
        output = ssh_client.exec_command('show ip arp')
        show_ip_arp = output[0].decode('utf-8')

        # Save device info to notepad
        with open('notepad.txt', 'a') as f:
            f.write(f'Hostname: {hostname}\n')
            f.write(f'Show mac add: {show_mac_add}\n')
            f.write(f'Show ip arp: {show_ip_arp}\n')

    except Exception as e:
        print(f'Error connecting to device: {device_ip}')
        print(e)

if __name__ == '__main__':
    with open('device_list.txt', 'r') as f:
        devices = []
        for line in f:
            ip = line.strip()
            devices.append(ip)

    for device_ip in devices:
        thread = threading.Thread(target=get_device_info, args=(device_ip,))
        thread.start()

    # Wait for all threads to finish
    for thread in threading.enumerate():
        if thread.is_alive():
            thread.join()

    print('Done!')
