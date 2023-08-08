import pandas as pd
import re

# Load the csv files into pandas DataFrames
csvfile1 = pd.read_csv('csvfile1.csv')
csvfile2 = pd.read_csv('csvfile2.csv')

# Load OUI file with utf-8 encoding and create dictionary
oui_dict = {}
with open('oui.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if "(hex)" in lines[i]:
            oui_hex = lines[i].split()[0].replace('-', '').lower()
            vendor = lines[i].split('\t')[1]
            oui_dict[oui_hex] = vendor
        elif "(base 16)" in lines[i]:
            oui_base16 = lines[i].split()[0].lower()
            vendor = lines[i].split('\t')[1]
            oui_dict[oui_base16] = vendor

# Rename the columns for easy access
csvfile1.columns = ['Hostname', 'IP', 'VLAN', 'Interface', 'MAC_Address']
csvfile2.columns = ['ARP_IP', 'MAC_Address']

# Convert MAC Address format in both dataframes
def convert_mac_format(mac):
    mac = mac.replace('.', '')
    mac = ":".join(mac[i:i+2] for i in range(0, len(mac), 2))
    return mac

csvfile1['MAC_Address'] = csvfile1['MAC_Address'].apply(convert_mac_format)
csvfile2['MAC_Address'] = csvfile2['MAC_Address'].apply(convert_mac_format)

# Merge two dataframes on 'MAC_Address' column
merged = pd.merge(csvfile1, csvfile2, on='MAC_Address', how='left')

# Replace NaN with 'not found'
merged['ARP_IP'] = merged['ARP_IP'].fillna('not found')

# Lookup MAC Address vendor (OEM)
def lookup_vendor(mac):
    oui = mac.replace(':', '').lower()[:6]
    return oui_dict.get(oui, 'not found')

merged['OEM'] = merged['MAC_Address'].apply(lookup_vendor)

# You can now save the merged DataFrame as a new csv
merged.to_csv('csvfile1_new.csv', index=False)
