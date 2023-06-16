import os
import csv
import glob

# Directory containing your text files
directory = 'your_directory'

# Output CSV file
output_file = 'output.csv'

# Get list of all text files
files = glob.glob(os.path.join(directory, '*.txt'))

# Prepare CSV file
with open(output_file, 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(['IP_Address', 'MAC_Address', 'Interface', 'Error'])  # Add Error to Header

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
                        csv_output.writerow([columns[1], columns[3], columns[5]])  # IP_Address, MAC_Address, Interface

        except Exception as e:
            csv_output.writerow([None, None, None, str(e)])  # If there's an error, write it to the Error column
