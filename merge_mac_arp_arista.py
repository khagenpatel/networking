import pandas as pd

# Load the csv files into pandas DataFrames
csvfile1 = pd.read_csv('csvfile1.csv')
csvfile2 = pd.read_csv('csvfile2.csv')

# Rename the columns for easy access
csvfile1.columns = ['Hostname', 'IP', 'VLAN', 'Interface', 'MAC_Address']
csvfile2.columns = ['ARP_IP', 'MAC_Address']

# Merge two dataframes on 'MAC_Address' column
merged = pd.merge(csvfile1, csvfile2, on='MAC_Address', how='left')

# Replace NaN with 'not found'
merged['ARP_IP'] = merged['ARP_IP'].fillna('not found')

# You can now save the merged DataFrame as a new csv
merged.to_csv('csvfile1_new.csv', index=False)
