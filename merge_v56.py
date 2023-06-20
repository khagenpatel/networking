import openpyxl
import csv
import re
from collections import defaultdict

# Load Excel workbook
wb = openpyxl.load_workbook('input1.xlsx')
ws = wb.active

# Read csv file and create a dictionary for easier search
csv_data = defaultdict(lambda: ["Not found"]*5)
with open('input2.csv', 'r', encoding='ISO-8859-1') as f:
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
for col, header in enumerate(['Owning Transaction Cycle', 'CDR', 'IT Business Service', 'IT Service Instance', 'ITSI Environment'], start=ws.max_column+1):
    ws.cell(row=1, column=col, value=header)

# Regular expression pattern for hostname
pattern = re.compile(r"(.+?)[.\s]")

# Process rows in Excel
for row_idx in range(2, ws.max_row + 1):
    cell = ws.cell(row=row_idx, column=live_host_idx)
    match = pattern.match(cell.value)
    if match:
        live_host = match.group(1).lower()  # Get Live_Host and convert to lowercase
        new_data = csv_data[live_host]  # Get new data from csv file
        # Add new data to the end of the row
        for col, data in enumerate(new_data, start=ws.max_column-len(new_data)+1):
            ws.cell(row=row_idx, column=col, value=data)
    else:
        print(f"Could not parse Live_Host value: {cell.value}")

# Save workbook
wb.save('input1_modified.xlsx')
