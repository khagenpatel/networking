import paramiko
import threading
import csv
import re

class DeviceConnector(threading.Thread):
    def __init__(self, ip, username, password, enable_password, output_lock):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.output_lock = output_lock
    
    def run(self):
        print "Connecting to {0}".format(self.ip)
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.ip, username=self.username, password=self.password)

            # Create an interactive shell session
            remote_conn = ssh_client.invoke_shell()
            
            # Send the enable command
            remote_conn.send("enable\n")
            while not remote_conn.recv_ready():
                pass
            remote_conn.send("{0}\n".format(self.enable_password))

            # Get hostname from command prompt
            output = remote_conn.recv(1000).decode('ascii')
            hostname = output.split("#")[0].strip()

            print "Connected to {0} (hostname: {1})".format(self.ip, hostname)

            # Get MAC addresses of physical interfaces
            remote_conn.send('show mac address-table\n')
            while not remote_conn.recv_ready():
                pass
            mac_address_output = remote_conn.recv(5000).decode()

            # Get ARP table
            remote_conn.send('show ip arp\n')
            while not remote_conn.recv_ready():
                pass
            arp_table = remote_conn.recv(5000).decode()

            # Regex to match physical interface patterns
            interface_pattern = re.compile(r'^\d+(/\d+)+$')

            # Parse the information
            for line in mac_address_output.split('\n'):
                parts = line.split()
                if len(parts) > 4 and interface_pattern.match(parts[3]):
                    interface = parts[3]
                    mac_address = parts[1]
                    
                    # Find IP address from ARP table
                    ip_address_from_arp = "Not Found"
                    for arp_line in arp_table.split('\n'):
                        if mac_address in arp_line:
                            ip_address_from_arp = arp_line.split()[1]
                            break
                    
                    # Output the information
                    with self.output_lock:
                        with open('output.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([hostname, self.ip, interface, mac_address, ip_address_from_arp])
                            print "Data written for {0}".format(self.ip)
                else:
                    print "No matching interfaces found on {0}".format(self.ip)
            
            ssh_client.close()

        except Exception as e:
            print "Error connecting to {0}: {1}".format(self.ip, str(e))

# Read device IPs from file
with open("device_list.txt", "r") as file:
    device_ips = file.readlines()

# Define credentials
username = 'your_username'
password = 'your_password'
enable_password = 'your_enable_password'

# Lock to synchronize output to file
output_lock = threading.Lock()

# Create the output.csv file with headers
with open('output.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['hostname', 'IP address of the switch', 'interface', 'mac address', 'ip address from arp'])
    print "Created output.csv file with headers"

# Create and start threads
threads = []
for ip in device_ips:
    connector = DeviceConnector(ip.strip(), username, password, output_lock)
    threads.append(connector)
    connector.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print "Data collection complete"
