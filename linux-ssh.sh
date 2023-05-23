#!/bin/bash

# Set your SSH username and password here
USERNAME="your-username"
PASSWORD="your-password"

# Name of the file containing the list of devices.
DEVICE_LIST_FILE="device_list.txt"

# Name of the output CSV file.
OUTPUT_FILE="device_output.csv"

# Write the headers to the CSV file.
echo "Device,Channel Group,Port,Protocol,Status,Interface,Status,VLAN,Duplex,Speed,Type" > $OUTPUT_FILE

# Read the device list file line by line.
while read -r device; do
    echo "Processing device: $device"

    # Run the command on the device and save the output.
    etherchannel_summary=$(sshpass -p $PASSWORD ssh -l $USERNAME $device "show etherchannel summary")
    interface_status=$(sshpass -p $PASSWORD ssh -l $USERNAME $device "show interface status | i connected")

    # Parse the output and write it to the CSV file.
    # This is a simple way of parsing the output that might not work with more complex output.
    # You might need to use a more powerful tool like awk or perl for this.
    IFS=$'\n'
    for line in $etherchannel_summary; do
        channel_group=$(echo $line | cut -d' ' -f1)
        port=$(echo $line | cut -d' ' -f2)
        protocol=$(echo $line | cut -d' ' -f3)
        status=$(echo $line | cut -d' ' -f4)

        for line_status in $interface_status; do
            interface=$(echo $line_status | cut -d' ' -f1)
            status=$(echo $line_status | cut -d' ' -f2)
            vlan=$(echo $line_status | cut -d' ' -f3)
            duplex=$(echo $line_status | cut -d' ' -f4)
            speed=$(echo $line_status | cut -d' ' -f5)
            type=$(echo $line_status | cut -d' ' -f6)
            
            # Write the data to the CSV file.
            echo "$device,$channel_group,$port,$protocol,$status,$interface,$status,$vlan,$duplex,$speed,$type" >> $OUTPUT_FILE
        done
    done
done < $DEVICE_LIST_FILE

echo "Finished processing all devices."
