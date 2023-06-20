import csv
import re
from openpyxl import load_workbook

try:
    # Load the Excel file
    workbook = load_workbook('input1.xlsx')
    sheet = workbook.active

    # Load the CSV file
    with open('input2.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row

        # Create a dictionary to store the mapping between hostnames and the other columns
        csv_data = {}
        for row in csvreader:
            live_host = row[0].lower()  # Convert Live_Host to lowercase
            csv_data[live_host] = row[1:]  # Store the remaining columns in the dictionary

    # Iterate through the rows in the Excel file
    for row in sheet.iter_rows(min_row=2, values_only=True):
        live_host_full = row[3]  # Extract the full Live_Host value
        match = re.search(r'(\S+)\s', live_host_full)  # Extract the hostname using regex
        if match:
            live_host = match.group(1).lower()  # Convert Live_Host to lowercase
            if live_host in csv_data:
                # Get the values from the CSV file
                values = csv_data[live_host]

                # Add the values to the Excel file
                sheet.cell(row=row[0].row, column=8).value = values[0]  # Owning Transaction Cycle
                sheet.cell(row=row[0].row, column=9).value = values[1]  # CDR
                sheet.cell(row=row[0].row, column=10).value = values[2]  # IT Business Service
                sheet.cell(row=row[0].row, column=11).value = values[3]  # IT Service Instance
                sheet.cell(row=row[0].row, column=12).value = values[4]  # ITSI Environment

    # Save the modified Excel file
    workbook.save('output.xlsx')

    print("Data successfully updated in the Excel file!")

except Exception as e:
    print("An error occurred:", str(e))
