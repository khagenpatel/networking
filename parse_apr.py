import os
import csv
import glob

def format_mac(mac):
    """Converts a MAC address to the standard 6 octet representation"""
    return ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))

def load_oui_dict():
    """Load OUI dictionary from the IEEE file"""
    oui_dict = {}
    with open('oui.txt', 'r') as f:
        for line in f:
            if '(hex)' in line:
                try:
                    oui, company = line.split('(hex)')
                    oui = oui.strip().replace('-', ':').lower()
                    company = company.strip()
                    oui_dict[oui] = company
                except ValueError:
                    pass
    return oui_dict

# Directory containing your text files
directory = 'your_directory'

# Output CSV file
output_file = 'output.csv'

# Load OUI dictionary
oui_dict = load_oui_dict()

# Get list of all text files
files = glob.glob(os.path.join(directory, '*.txt'))

# Prepare CSV file
with open(output_file, 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(['IP_Address', 'MAC_Address', 'Company', 'Interface', 'Error'])  # Add Error to Header

    # Process each file
    for file in files:
        try:
            with open(file, 'r') as f_input:
                lines = f_input.readlines()

                # Process each line
                for line in lines:
                    # Split line into columns
                    columns = line.split()

                    # Check if line is an ARP entry (Internet protocol)
                    if columns[0] == 'Internet':
                        mac = format_mac(columns[3].replace('.', ''))
                        oui = mac[:8]  # Get OUI part of the MAC address
                        company = oui_dict.get(oui, 'Unknown')  # Get company from OUI dictionary, or 'Unknown' if not found
                        csv_output.writerow([columns[1], mac, company, columns[5]])  # IP_Address, MAC_Address, Company, Interface

        except Exception as e:
            csv_output.writerow([None, None, None, None, str(e)])  # If there's an error, write it to the Error column
