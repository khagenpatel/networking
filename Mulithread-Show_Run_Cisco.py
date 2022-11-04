
import concurrent.futures
import csv
import sys, os
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetmikoAuthenticationException
from paramiko.ssh_exception import *
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

hosts_info = []


starting_time = time.perf_counter()
ipaddresses = []
platform = []
port = []

with open("Netmiko-Database.csv", encoding="cp1252") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        ipaddresses.append(row[0])
        platform.append(row[1])
        port.append(row[2])

    for (i, m, n) in zip(ipaddresses, platform, port):
        host = {
            'device_type': m,
            'ip': i,
            'username': 'patelk45',
            'password': 'Asd@0810',
            'port': n
        }

        hosts_info.append(host)


def open_connection(host):
    try:
        host1 = {
            'device_type': host['device_type'],
            'ip': host['ip'],
            'username': 'YOUR_USERNAME',
            'password': 'YOUR_PASSWORD',
            'port': host['port'], "conn_timeout": 2, "fast_cli": False
        }
        connection = ConnectHandler(**host1)
        print('Connection Established to Host:', host1['ip'])
        print(connection.host)
        print("*" * len(connection.host))

        connection.enable()
        find_hostname = connection.find_prompt()
        hostname = find_hostname.replace("#", "")

        print("\033[0;36;40mConnected to " + host[
            'ip'] + " " + "Hostname -" + hostname + " " + " Device Type -" + m + "\x1b[0m")

        output = connection.send_command("Show run", expect_string="#", delay_factor=100, max_loops=100000,
                                         read_timeout=1000)
        print("show running config - Saved")
        save_file = open(hostname + ".txt", "w")
        save_file.write(output)
        save_file.close()

        connection.disconnect()



    except (NetMikoTimeoutException, NetmikoAuthenticationException, AuthenticationException):
        print(f"Connection failed to " + host["ip"], file=sys.stderr)

        pass


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(open_connection, hosts_info)
        for result in results:
            print(result)

    finish = time.perf_counter()
    print('Time Elapsed:', finish - starting_time)
