import requests
import json
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import webbrowser

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
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Split the main frame into left and right frames
    left_frame = ttk.Frame(main_frame, padding="10")
    left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S))

    right_frame = ttk.Frame(main_frame, padding="10")
    right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S))

    # Labels to display the SMA values
    sma5_label = ttk.Label(left_frame, text="SMA (5): Loading...", font=("Helvetica", 20, "bold"))
    sma5_label.grid(row=0, column=0, pady=5)

    sma20_label = ttk.Label(left_frame, text="SMA (20): Loading...", font=("Helvetica", 20, "bold"))
    sma20_label.grid(row=1, column=0, pady=5)

    # Treeview for displaying live data table
    columns = ("Time", "SMA 5", "SMA 20")
    tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
    tree.heading("Time", text="Time"); tree.column("Time", width=100, anchor=tk.CENTER)
    tree.heading("SMA 5", text="SMA 5"); tree.column("SMA 5", width=100, anchor=tk.CENTER)
    tree.heading("SMA 20", text="SMA 20"); tree.column("SMA 20", width=100, anchor=tk.CENTER)
    tree.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.N, tk.E, tk.S))

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

            ax.cla()
            line1, = ax.plot(timestamps, sma5_values, label='SMA 5', color='blue', picker=5)
            line2, = ax.plot(timestamps, sma20_values, label='SMA 20', color='red', picker=5)
            ax.set_xlabel('Time')
            ax.set_ylabel('SMA Value')
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            fig.tight_layout()

            # Update SMA labels
            sma5_label.config(text=f"SMA (5): {sma5:.2f}")
            sma20_label.config(text=f"SMA (20): {sma20:.2f}")

            canvas.draw()

    # Set up the figure and animation
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.get_tk_widget().grid(row=0, column=0, pady=10)
    ani = FuncAnimation(fig, update, interval=15000, save_count=100)

    # Function to update the table with new data
    def update_table():
        tree.delete(*tree.get_children())
        for i in range(len(timestamps)):
            tree.insert("", "end", values=(timestamps[i], f"{sma5_values[i]:.2f}", f"{sma20_values[i]:.2f}"))
        left_frame.after(1000, update_table)

    update_table()
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

# Link to get API key
def open_link():
    webbrowser.open("https://taapi.io/")

link_text = "Don't have an API key? Get one "
link_label = tk.Label(key_frame, text=link_text, font=("Helvetica", 12))
link_label.grid(row=2, column=0, pady=5, sticky=tk.W)

here_link = tk.Label(key_frame, text="here", font=("Helvetica", 12), foreground="blue", cursor="hand2", underline=True)
here_link.grid(row=2, column=0, sticky=tk.W, padx=(len(link_text) * 7 + 6, 0))
here_link.bind("<Button-1>", lambda e: open_link())

# Function to proceed to the next screen after entering the key
def proceed():
    secret_key = key_entry.get()
    if secret_key:
        root.destroy()
        start_main_app(secret_key)

proceed_button = ttk.Button(key_frame, text="Proceed", command=proceed)
proceed_button.grid(row=3, column=0, pady=10)

root.mainloop()
