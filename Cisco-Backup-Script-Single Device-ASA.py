from netmiko import Netmiko
from getpass import getpass
import time, datetime
import os
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from netmiko import ConnectHandler

os.system('cls')

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("                        Khagen Patel")
print("               https://github.com/khagenpatel")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

# getting required information from user through terminal
ip_addr = input("Enter IP Address Of A Cisco ASA: ")
username = input("Please enter device username :")
password = getpass("Please enter device password :")
enable_pass = getpass("Please enter enable password if needed :")

# introduce devices
cisco_1 = {
    "device_type": "cisco_asa",
    "ip": ip_addr,
    "username": username,
    "password": password,
    "secret": enable_pass,
    "port": "22",
}

devices = [cisco_1]

# Print recent time to create folder name
clock = datetime.datetime.now().strftime("%B-%d-%Y %I-%M%p")

print("_____________________________________________________________________________")

# Create Directory - name: including Date and Time
home_dir = ("Backup on " + clock)
if not os.path.isdir(home_dir):
    os.makedirs(home_dir, exist_ok=True)
    print("Home directory ''%s'' was created." % home_dir)
    os.chdir(home_dir)  # To change the directory for backup file.
time.sleep(3)

for dev in devices:
    name = dev["ip"]
    try:
        net_connect = ConnectHandler(**dev)
    except NetMikoTimeoutException:
        print('Device not reachable.')
        continue
    except AuthenticationException:
        print('Authentication Failure.')
        continue
    except SSHException:
        print('Make sure SSH is enabled in device.')
        continue
    net_connect.enable()
    find_hostname = net_connect.find_prompt()
    hostname = find_hostname.replace("#", "")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Connected to " + name)
    print("Hostname is " + hostname)
    print("Initiate Configuration Backup for " + hostname)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    time.sleep(3)
    output = net_connect.send_command('show run')
    print(output)
    time.sleep(0.5)  # <-- You can change this time as per your device
    Save_File = open(name + "-" + hostname + ".txt", 'w')
    Save_File.write(output)
    Save_File.close
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Finished Config Backup for " + name)
    print("Backup File Location ''/" + clock + "/" + name + "-" + hostname + ".txt" "''")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    time.sleep(2)
