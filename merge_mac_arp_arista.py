import pandas as pd

# Load data
df1 = pd.read_csv('csvfile1.csv')
df2 = pd.read_csv('csvfile2.csv')

# Rename columns to match df1
df2 = df2.rename(columns={'ARP IP': 'IP', 'MAC Address': 'MAC Address'})

# Merge the dataframes on the 'MAC Address' column
merged = pd.merge(df1, df2, on='MAC Address', how='left')

# Check and replace NaN values in the 'IP' column from df1 with the 'IP' from df2 (ARP IP)
merged['IP_x'] = merged.apply(lambda row: row['IP_y'] if pd.isnull(row['IP_x']) else row['IP_x'], axis=1)

# Drop the 'IP_y' column as it's no longer needed
merged = merged.drop(columns=['IP_y'])

# Rename 'IP_x' back to 'IP'
merged = merged.rename(columns={'IP_x': 'IP'})

# Save the new CSV
merged.to_csv('csvfile1_updated.csv', index=False)
