import openpyxl
import csv
import re
from collections import defaultdict

# Load Excel workbook
wb = openpyxl.load_workbook('input1.xlsx')
ws = wb.active

# Read csv file and create a dictionary for easier search
csv_data = defaultdict(lambda: ["Not found"]*5)
with open('input2.csv', 'r') as f:
    csv_reader = csv.reader(f)
    headers = next(csv_reader)
    for row in csv_reader:
        csv_data[row[0].lower()] = row[1:6]

# Find the index of 'Live_Host' column in Excel file
live_host_idx = None
for i, column in enumerate(ws.iter_cols(1, ws.max_column)):
    if column[0].value == 'Live_Host':
        live_host_idx = i + 1
        break

# Verify that 'Live_Host' column is found in Excel file
if live_host_idx is None:
    print("Couldn't find 'Live_Host' column in the Excel file.")
    exit()

# Append new columns in Excel
ws.append(['Owning Transaction Cycle', 'CDR', 'IT Business Service', 'IT Service Instance', 'ITSI Environment'])

# Regular expression pattern for hostname
pattern = re.compile(r"(.+?)[.\s]")

# Process rows in Excel
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    match = pattern.match(row[live_host_idx-1].value)
    if match:
        live_host = match.group(1).lower()  # Get Live_Host and convert to lowercase
        new_data = csv_data[live_host]  # Get new data from csv file
        for i, cell in enumerate(row[-5:], start=1):
            cell.value = new_data[i-1]  # Update cell values
    else:
        print(f"Could not parse Live_Host value: {row[live_host_idx-1].value}")


# Save workbook
wb.save('input1_modified.xlsx')
