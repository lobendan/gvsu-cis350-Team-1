import requests
import json
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

TAurl = "https://api.taapi.io/bulk"

priceurl = "https://api.taapi.io/price"

# Main application function
def start_main_app(secret_key):
    # Parameters for getting live price data
    params = {
        "secret": secret_key,
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1m"
    }

    # Payload for getting live indicator data
    payload = {
        "secret": secret_key,
        "construct": {
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "1m",
            "indicators": [
                {
                    "indicator": "sma",
                    "period": 5
                },
                {
                    "indicator": "sma",
                    "period": 20
                }
            ]
        }
    }
    headers = {"Content-Type": "application/json"}

    # GUI setup
    root = tk.Tk()
    root.title("BTC/USDT Live Indicators")

    # Define the frame for displaying data
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Labels to display the SMA values
    sma5_label = ttk.Label(frame, text="SMA (5): Loading...", font=("Helvetica", 20, "bold"))
    sma5_label.grid(row=0, column=0, pady=5)

    sma20_label = ttk.Label(frame, text="SMA (20): Loading...", font=("Helvetica", 20, "bold"))
    sma20_label.grid(row=1, column=0, pady=5)

    # Lists to hold live data
    timestamps = []
    sma5_values = []
    sma20_values = []

    # Function to get SMA data
    def get_sma_data():
        response = requests.request("POST", TAurl, json=payload, headers=headers)
        if response.status_code == 200:
            json_str = response.content.decode("utf-8")
            data_dict = json.loads(json_str)
            sma5 = None
            sma20 = None
            for item in data_dict['data']:
                if item['indicator'].upper() == "SMA" and item["id"] == "binance_BTC/USDT_1m_sma_5_0":
                    sma5 = item['result']['value']
                elif item['indicator'].upper() == "SMA" and item["id"] == "binance_BTC/USDT_1m_sma_20_0":
                    sma20 = item['result']['value']
            return sma5, sma20
        else:
            print(f"Failed to retrieve SMA data: {response.status_code}")
            return None, None

    # Function to update the graph and labels
    def update(frame):
        sma5, sma20 = get_sma_data()
        if sma5 is not None and sma20 is not None:
            current_time = time.strftime('%H:%M:%S')
            timestamps.append(current_time)
            sma5_values.append(sma5)
            sma20_values.append(sma20)

            plt.cla()
            plt.plot(timestamps, sma5_values, label='SMA 5', color='blue')
            plt.plot(timestamps, sma20_values, label='SMA 20', color='red')
            plt.xlabel('Time')
            plt.ylabel('SMA Value')
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()

            # Update SMA labels
            sma5_label.config(text=f"SMA (5): {sma5:.2f}")
            sma20_label.config(text=f"SMA (20): {sma20:.2f}")

    # Set up the figure and animation
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, interval=15000, save_count=100)

    # Start the GUI main loop in a separate thread
    def start_plot():
        plt.show()

    # Function to display the live table
    def start_table():
        table_window = tk.Toplevel(root)
        table_window.title("Live Data Table")
        table_frame = ttk.Frame(table_window, padding="10")
        table_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Treeview for displaying data
        columns = ("Time", "SMA 5", "SMA 20")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        tree.heading("Time", text="Time"); tree.column("Time", width=100, anchor=tk.CENTER)
        tree.heading("SMA 5", text="SMA 5"); tree.column("SMA 5", width=100, anchor=tk.CENTER)
        tree.heading("SMA 20", text="SMA 20"); tree.column("SMA 20", width=100, anchor=tk.CENTER)
        tree.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.E, tk.S))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Function to update the table with new data
        def update_table():
            tree.delete(*tree.get_children())
            for i in range(len(timestamps)):
                tree.insert("", "end", values=(timestamps[i], f"{sma5_values[i]:.2f}", f"{sma20_values[i]:.2f}"))
            table_window.after(1, update_table)

        update_table()

    tk.Button(root, text="Show Graph", command=start_plot).grid(row=2, column=0, pady=10)
    tk.Button(root, text="Show Table", command=start_table).grid(row=3, column=0, pady=10)

    update(0)  # Initial update
    root.mainloop()

# GUI setup for key input
root = tk.Tk()
root.title("API Key Input")

# Frame for key input
key_frame = ttk.Frame(root, padding="10")
key_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label and entry for API key
key_label = ttk.Label(key_frame, text="Enter your API Key:", font=("Helvetica", 14))
key_label.grid(row=0, column=0, pady=5)

key_entry = ttk.Entry(key_frame, width=50)
key_entry.grid(row=1, column=0, pady=5)

# Function to proceed to the next screen after entering the key
def proceed():
    secret_key = key_entry.get()
    if secret_key:
        root.destroy()
        start_main_app(secret_key)

proceed_button = ttk.Button(key_frame, text="Proceed", command=proceed)
proceed_button.grid(row=2, column=0, pady=10)

root.mainloop()
