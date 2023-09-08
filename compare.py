import tkinter as tk
from tkinter import filedialog
from collections import defaultdict, Counter
from tabulate import tabulate
import pandas as pd
import datetime


def parse_text_file(file_path):
    parsed_data = defaultdict(Counter)
    current_key = ""
    hostname = ""

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("hostname:"):
                hostname = line.split("hostname:")[1].strip()
            elif line.endswith("!!!!!!!!!!!!!!!!!!!!!!!!!!!"):
                current_key = ""
            elif line in ["arp table", "mac table", "powerinline table", "interface connected", "cdp table"]:
                current_key = line
            elif "Device ID:" in line:
                current_key = "cdp"
                device_id = line.split("Device ID:")[1].strip()
                parsed_data[current_key][device_id] += 1
            elif current_key:
                parsed_data[current_key][line] += 1

    return hostname, parsed_data


def compare_tables(parsed_data1, parsed_data2):
    result = defaultdict(lambda: defaultdict(list))

    for table in parsed_data1.keys():
        missing = parsed_data1[table] - parsed_data2[table]
        added = parsed_data2[table] - parsed_data1[table]

        result[table]["missing"] = sorted(missing.elements())
        result[table]["added"] = sorted(added.elements())

    return result


def print_and_save_to_excel(hostname, comparison_result):
    table_data = []
    headers = ["Table", "Change Type", "Count", "Items"]

    for table, changes in comparison_result.items():
        for change_type, items in changes.items():
            table_data.append([table, change_type.capitalize(), len(items), "\n".join(items)])

    print(tabulate(table_data, headers=headers))

    df = pd.DataFrame(table_data, columns=headers)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{hostname}_{timestamp}_comparison_result.xlsx"
    df.to_excel(output_file, index=False)


def browse_file():
    file_path = filedialog.askopenfilename(title="Select a text file")
    return file_path


def main():
    def on_submit():
        file_path1 = file_entry1.get()
        file_path2 = file_entry2.get()

        hostname1, parsed_data1 = parse_text_file(file_path1)
        hostname2, parsed_data2 = parse_text_file(file_path2)

        comparison_result = compare_tables(parsed_data1, parsed_data2)

        print_and_save_to_excel(hostname1, comparison_result)
        root.destroy()

    root = tk.Tk()
    root.title("File Comparison")

    file_entry1 = tk.StringVar()
    file_entry2 = tk.StringVar()

    tk.Label(root, text="File 1:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=file_entry1, width=50).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: file_entry1.set(browse_file())).grid(row=0, column=2)

    tk.Label(root, text="File 2:").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=file_entry2, width=50).grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: file_entry2.set(browse_file())).grid(row=1, column=2)

    tk.Button(root, text="Submit", command=on_submit).grid(row=2, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

