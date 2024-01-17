#!/bin/bash

# Input file containing IP addresses, one per line
inputFile="ip_list.txt"

# Output CSV file
outputFile="ip_report.csv"

# Initialize the CSV file with headers
echo "IP,Reachability" > "$outputFile"

# Read each line in the IP address file
while IFS= read -r ip
do
    # Ping the IP address with a timeout of 1 second
    if ping -c 1 -W 1 "$ip" &> /dev/null
    then
        # If ping is successful, mark as True
        echo "$ip,True" >> "$outputFile"
    else
        # If ping fails, mark as False
        echo "$ip,False" >> "$outputFile"
    fi
done < "$inputFile"

echo "Ping operation completed. Results are saved in $outputFile"
