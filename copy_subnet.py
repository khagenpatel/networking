import csv

def move_duplicates_to_another_tab(file_path):
    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Find duplicate subnets
    duplicate_subnets = set()
    unique_subnets = set()

    for row in rows:
        subnet = row['Subnet']
        if subnet in unique_subnets:
            duplicate_subnets.add(subnet)
        else:
            unique_subnets.add(subnet)

    # Create a new CSV file for duplicates
    duplicate_file_path = file_path.replace('.csv', '_duplicates.csv')
    with open(duplicate_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Write rows with duplicate subnets to the new file
        for row in rows:
            if row['Subnet'] in duplicate_subnets:
                writer.writerow(row)

    print(f"Duplicates have been moved to {duplicate_file_path}.")

# Specify the file path
file_path = 'your_file_path.csv'

# Call the function
move_duplicates_to_another_tab(file_path)
