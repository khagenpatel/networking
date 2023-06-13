import csv
from openpyxl import Workbook
from openpyxl.styles import PatternFill

# Initialize Workbook
wb = Workbook()
ws = wb.active

# Open CSV file and write to Excel
with open('input.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        ws.append(row)

# Highlight duplicates
subnets = {}
red_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
    for cell in row:
        if cell.value in subnets:
            # Highlight this cell and the earlier cell that had the same value
            cell.fill = red_fill
            subnets[cell.value].fill = red_fill
        else:
            subnets[cell.value] = cell

# Save the workbook to a file
wb.save("output.xlsx")
