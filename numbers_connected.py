import csv
import concurrent.futures
from netmiko import ConnectHandler

# Read the list of devices from the text file
with open("devices.txt", "r") as file:
    devices = [line.strip() for line in file]

# SSH credentials
username = "your_username"
password = "your_password"

# Function to send commands to a device and count output lines
def count_output_lines(device):
    connection = ConnectHandler(device_type="cisco_ios", ip=device, username=username, password=password)
    output1 = connection.send_command("show ip int br | i up")
    output2 = connection.send_command("show interface status | i connected")
    connection.disconnect()
    return device, len(output1.split("\n")), len(output2.split("\n"))

# Use a thread pool to send commands to all devices concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(count_output_lines, devices))

# Write the results to a CSV file
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["hostname", "number of up interfaces", "number of connected interfaces"])
    writer.writerows(results)
