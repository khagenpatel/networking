import csv
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
import textfsm

# Load device info from CSV
def load_devices(file_name):
    devices = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            devices.append(row)
    return devices

# Get CDP neighbor info
def get_cdp_neighbors(device):
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("show cdp neighbors")
        connection.disconnect()

        # Parse the output using ntc-template
        with open("ntc-templates/templates/cisco_ios_show_cdp_neighbors.textfsm") as template:
            fsm = textfsm.TextFSM(template)
            parsed_output = fsm.ParseText(output)
            return parsed_output

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Failed to connect to {device['host']} - {e}")
        return []

def main():
    devices = load_devices("devices.csv")
    all_neighbors = []

    for device in devices:
        neighbors = get_cdp_neighbors(device)
        all_neighbors.extend(neighbors)

    # Write the parsed output to CSV
    with open("cdp_neighbors.csv", "w", newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Local Device", "Local Port", "Neighbor", "Neighbor Port", "Platform", "Capability", "Version", "Holdtime", "Advertisment Protocol", "Remote ID"])
        # Write data
        for neighbor in all_neighbors:
            writer.writerow(neighbor)

if __name__ == "__main__":
    main()