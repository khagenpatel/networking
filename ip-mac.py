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
        output += shell.recv(1024).decode()
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
                mac_addresses = output[output.find('mac address-table'):output.find('Type:')].strip()
                arp_table = output[output.find('ip arp'):].strip()
                output_file.write(f"Hostname of {device}: {hostname}\n")
                output_file.write(f"MAC addresses on {device}:\n{mac_addresses}\n")
                output_file.write(f"IP ARP table on {device}:\n{arp_table}\n")
                ssh.close()
            except paramiko.AuthenticationException:
                output_file.write(f"Failed to authenticate to {device}\n")
            except paramiko.SSHException as e:
                output_file.write(f"SSH error occurred while connecting to {device}: {str(e)}\n")
            except Exception as e:
                output_file.write(f"An error occurred while processing {device}: {str(e)}\n")
            output_file.flush()

if __name__ == "__main__":
    main()
