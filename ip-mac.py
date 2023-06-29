import paramiko
import time

def ssh_connect(device, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device, username=username, password=password)
    return ssh

def execute_commands(ssh, commands, sleep_time=2):
    shell = ssh.invoke_shell()
    output = ""
    for command in commands:
        shell.send(command + '\n')
        time.sleep(sleep_time)
    while shell.recv_ready():
        output += shell.recv(1024)
    return output

def main():
    username = 'abcd'
    password = 'defg'
    commands = ['term len 0', 'show mac address-table', 'show ip arp']

    with open('device_list.txt', 'r') as f:
        devices = f.read().splitlines()

    with open('output.txt', 'w') as output_file:
        for device in devices:
            try:
                ssh = ssh_connect(device, username, password)
                output = execute_commands(ssh, commands)
                hostname = output.splitlines()[0].strip()
                
                # Extracting the MAC addresses and ARP table from the output
                mac_start = output.find('mac address-table')
                arp_start = output.find('ip arp')
                mac_addresses = output[mac_start:arp_start].strip()
                arp_table = output[arp_start:].strip()
                
                output_file.write(hostname)
                output_file.write("MAC addresses on {0}:\n{1}\n".format(device, mac_addresses))
                output_file.write("IP ARP table on {0}:\n{1}\n".format(device, arp_table))
                ssh.close()
            except paramiko.AuthenticationException:
                output_file.write("Failed to authenticate to {0}\n".format(device))
            except paramiko.SSHException as e:
                output_file.write("SSH error occurred while connecting to {0}: {1}\n".format(device, str(e)))
            except Exception as e:
                output_file.write("An error occurred while processing {0}: {1}\n".format(device, str(e)))
            output_file.flush()

if __name__ == "__main__":
    main()
