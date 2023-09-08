import tkinter as tk
from tkinter import filedialog, Scrollbar, messagebox
import csv
from netmiko import ConnectHandler
from collections import defaultdict
import datetime


timestamp1 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_device_info(device, username, password):
    connection = ConnectHandler(device_type="cisco_ios", ip=device["ip"], username=username, password=password,port=22, fast_cli=False, global_delay_factor=5,timeout=60, session_log=f'con-{timestamp1}.txt')

    hostname = connection.base_prompt
    print(f'Connected to {hostname}')

    commands = [
        "show ip arp",
        "show mac address-table",
        "show cdp nei detail",
        "show power inline | i on",
        "show interface status | inc connected",
    ]

    output = defaultdict(list)
    for cmd in commands:
        output[cmd] = connection.send_command(cmd,read_timeout=100,expect_string="#").splitlines()

    return hostname, output


def save_output():
    if not devices_listbox.curselection():
        tk.messagebox.showerror("Error", "Please select a device from the list.")
        return
    username = username_entry.get()
    password = password_entry.get()
    selected_device = devices_listbox.get(devices_listbox.curselection())

    device = next(d for d in devices if d["hostname"] == selected_device)

    hostname, output = get_device_info(device, username, password)

    sections = [
        ("arp table", "show ip arp"),
        ("mac table", "show mac address-table"),
        ("cdp table", "show cdp nei detail"),
        ("powerinline table", "show power inline | i on"),
        ("interface connected", "show interface status | inc connected"),
    ]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{hostname}-{timestamp}.txt", "w") as file:
        file.write(f"hostname:{hostname}\n")
        for section_name, cmd in sections:
            file.write(f"{section_name}\n")
            for line in output[cmd]:
                if section_name == "cdp table":
                    if "Device ID" in line:
                        line1=line.replace("Device ID: ","")
                        file.write(f"{line1}\n")
                elif section_name == "arp table":
                    if "Internet" in line:
                        file.write(line.split()[3] + "\n")
                elif section_name == "mac table":
                    if "DYNAMIC" in line:
                        file.write(line.split()[1] + "\n")
                    elif "dynamic" in line.lower():
                        file.write(line.split()[1] + "\n")

                elif section_name in ["powerinline table", "interface connected"]:
                    file.write(line.split()[0] + "\n")
            file.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")


def load_devices_from_csv(file_path):
    devices = []
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            devices.append({"hostname": row["hostname"], "ip": row["ip"]})
    return devices


def update_device_list(*args):
    search_text = search_var.get().lower()
    devices_listbox.delete(0, tk.END)
    for device in devices:
        if search_text in device["hostname"].lower():
            devices_listbox.insert(tk.END, device["hostname"])


# Load devices from a CSV file
devices = load_devices_from_csv("devices.csv")

root = tk.Tk()
root.title("Network Device Info")

search_label = tk.Label(root, text="Search:")
search_label.grid(row=0, column=0, sticky='w')

search_var = tk.StringVar()
search_var.trace("w", update_device_list)

search_entry = tk.Entry(root, textvariable=search_var)
search_entry.grid(row=0, column=1, columnspan=2, sticky='ew')

devices_listbox_frame = tk.Frame(root)
devices_listbox_frame.grid(row=1, column=0, rowspan=2)


box_frame = tk.Frame(root)
devices_listbox_frame.grid(row=1, column=0, rowspan=4, sticky='ns')

scrollbar = Scrollbar(devices_listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

devices_listbox = tk.Listbox(devices_listbox_frame, yscrollcommand=scrollbar.set, width=30)
devices_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=devices_listbox.yview)

update_device_list()

username_label = tk.Label(root, text="Username:")
username_label.grid(row=2, column=1, sticky='e')

username_entry = tk.Entry(root)
username_entry.grid(row=2, column=2, sticky='w')

password_label = tk.Label(root, text="Password:")
password_label.grid(row=3, column=1, sticky='e')

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=3, column=2, sticky='w')

save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.grid(row=4, column=1, columnspan=2, sticky='ew')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()