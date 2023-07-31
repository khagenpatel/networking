import csv
import concurrent.futures
from sshtunnel import SSHTunnelForwarder
from netmiko import ConnectHandler, NetMikoTimeoutException

# Read the list of devices from the text file
with open("devices.txt", "r") as file:
    devices = [line.strip() for line in file]

# SSH credentials
username = "your_username"
password = "your_password"

# Jump server details
jump_server_ip = "jump_server_ip"
jump_server_username = "jump_server_username"
jump_server_password = "jump_server_password"

# Function to send commands to a device and count output lines
def count_output_lines(device):
    with SSHTunnelForwarder(
        jump_server_ip,
        ssh_username=jump_server_username,
        ssh_password=jump_server_password,
        remote_bind_address=(device, 22)
    ) as tunnel:
        try:
            connection = ConnectHandler(
                device_type="cisco_ios",
                ip='127.0.0.1',
                port=tunnel.local_bind_port,
                username=username,
                password=password,
                timeout=30  # Increase this value if necessary
            )
            output1 = connection.send_command("show ip int br | i up")
            output2 = connection.send_command("show interface status | i connected")
            connection.disconnect()
            return device, len(output1.split("\n")), len(output2.split("\n"))
        except NetMikoTimeoutException:
            return device, "Error", "Error connecting via jump server"

# Use a thread pool to send commands to all devices concurrently, but limit to 5 concurrent tasks
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(count_output_lines, devices))

# Write the results to a CSV file
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["hostname", "number of up interfaces", "number of connected interfaces"])
    writer.writerows(results)
