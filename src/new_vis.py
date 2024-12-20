import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import pandas as pd
from matplotlib.animation import FuncAnimation
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.dates as mdates
import threading
import time
from strat import run_Trader
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Label, ttk

# Pre-launch popup window
class PreLaunchWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Launch Settings")
        self.master.geometry("325x150")
        
        # Set up labels and text entries
        self.label1 = tk.Label(self.master, text="API Key 1:")
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.entry1 = tk.Entry(self.master, width=30)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)
        
        self.label2 = tk.Label(self.master, text="API Key 2:")
        self.label2.grid(row=1, column=0, padx=10, pady=10)
        self.entry2 = tk.Entry(self.master, width=30)
        self.entry2.grid(row=1, column=1, padx=10, pady=10)
        
        # Launch button
        self.launch_button = tk.Button(self.master, text="Launch App", command=self.on_launch)
        self.launch_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.api_keys = None
    
    def on_launch(self):
        key1 = self.entry1.get()
        key2 = self.entry2.get()
        if key1 and key2:
            self.api_keys = (key1, key2)
            self.master.destroy()

# Define a class for monitoring file changes
class FileWatcher(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app
        
    def on_modified(self, event):
        if event.src_path.endswith(".csv"):
            self.app.update_data()

# Define the main application
class TradingApp:
    def __init__(self, root, csv_file, trader):
        self.root = root
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        self.update_active = True  # Initially, the update is active
        self.trader = trader

        self.validate_numeric = self.root.register(self.only_positive_numbers)
        
        # Setup plot area in Tkinter window
        self.fig, self.ax = plt.subplots(2, 2, figsize=(10, 8))
        plt.style.use('grayscale')

        # Set dark mode theme for the plot
        self.fig.patch.set_facecolor('#2e2e2e')  # Dark background for the figure
        for ax_row in self.ax.flatten():
            ax_row.set_facecolor('#2e2e2e')  # Dark background for each subplot
            ax_row.tick_params(axis='x', colors='white')  # White tick marks for x-axis
            ax_row.tick_params(axis='y', colors='white')  # White tick marks for y-axis
            ax_row.set_xlabel(ax_row.get_xlabel(), color='white')
            ax_row.set_ylabel(ax_row.get_ylabel(), color='white')

        # Setup canvas for the plots
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=4)
        
        # Set up dark mode for Tkinter window
        self.root.configure(bg='#2e2e2e')  # Dark background for the window
        self.root.option_add('*foreground', 'white')  # White text for labels

        # Buttons
        self.open_long = tk.Button(self.root, text="Open Long", fg="black", bg='lightgreen',command=self.open_long)
        self.open_long.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.open_long.config(font=("Helvetica", 13, "bold"), fg="black", bg="lightgreen")

        self.open_short = tk.Button(self.root, text="Open Short", fg="black", bg='crimson', command=self.open_short)
        self.open_short.grid(row=3, column=1, padx=10, pady=10, sticky = 'w')
        self.open_short.config(font=("Helvetica", 13, "bold"), fg="black", bg="crimson")

        self.close_trade = tk.Button(self.root, text="Close Trade", fg="black", bg='coral', command=self.close_trade)
        self.close_trade.grid(row=4, column=1, padx=10, pady=10, sticky = 'w')
        self.close_trade.config(font=("Helvetica", 13, "bold"), fg="black", bg="coral")

        self.flush_button = tk.Button(self.root, text="Flush History", fg="black", command=self.flush_history)
        self.flush_button.grid(row=4, column=0, padx=10, pady=10)

        self.flush_profit_button = tk.Button(self.root, text="Flush Total Profit Session", fg="black", command=self.flush_profit)
        self.flush_profit_button.grid(row=5, column=0, padx=10, pady=10)

        self.start_pause_button = tk.Button(self.root, text="Pause Autotrader", fg="black", bg='lightgray', command=self.toggle_update)
        self.start_pause_button.grid(row=6, column=0, padx=10, pady=10)

        self.deposit_label = tk.Label(self.root, text="Deposit Money:", fg="black")
        self.deposit_label.grid(row=5, column=2, padx=10, pady=10, sticky = 'e')

        self.deposit_input = tk.Entry(self.root, validate="key", validatecommand=(self.validate_numeric, '%P'), fg='black')
        self.deposit_input.grid(row=5, column=3, padx=10, pady=10, sticky = 'e')

        self.deposit_button = tk.Button(self.root, text="Deposit", fg="black", bg='lightblue', command=self.deposit_money)
        self.deposit_button.grid(row=5, column=4, padx=10, pady=10, sticky = 'w')

        self.withdraw_label = tk.Label(self.root, text="Withdraw Money:", fg="black")
        self.withdraw_label.grid(row=6, column=2, padx=10, pady=10, sticky = 'e')

        self.withdraw_input = tk.Entry(self.root, validate="key", validatecommand=(self.validate_numeric, '%P'), fg='black')
        self.withdraw_input.grid(row=6, column=3, padx=10, pady=10, sticky = 'e')

        self.withdraw_button = tk.Button(self.root, text="Withdraw", fg="black", bg='lightblue', command=self.withdraw_money)
        self.withdraw_button.grid(row=6, column=4, padx=10, pady=10, sticky = 'w')

        self.info_box_label = tk.Label(self.root, text="Active Profit: $0.00\nCurrent Networth: $0.00\nCurrent Position: $0.00", bg='#2e2e2e')
        self.info_box_label.grid(row=1, column=2, padx=10, pady=10, sticky='n')
        self.info_box_label.config(font=("Helvetica", 13))

        self.action_box = tk.Label(self.root, text="AutoTrader has been started successfully...", bg='#2e2e2e')
        self.action_box.grid(row=7, column=0, padx=10, pady=10, sticky='e')
        self.action_box.config(font=("Helvetica", 13))

        # Stop Loss Margin
        self.stop_loss_label = tk.Label(root, text="Stop Loss:", fg="black")
        self.stop_loss_label.grid(row=3, column=2, padx=10, pady=10, sticky = 'e')

        self.stop_loss_entry = tk.Entry(root, fg="black", validate="key", validatecommand=(self.validate_numeric, '%P'))
        self.stop_loss_entry.insert(0, f"{self.trader.strat.stop_loss}")  # Replace with actual current value
        self.stop_loss_entry.grid(row=3, column=3, padx=10, pady=10, sticky = 'w')

        self.submit_stop_loss = tk.Button(root, text="Update", fg="black", command=self.update_stop_loss)
        self.submit_stop_loss.grid(row=3, column=4, padx=10, pady=10, sticky = 'w')

        # Take Profit Margin
        self.take_profit_label = tk.Label(root, text="Take Profit:", fg="black")
        self.take_profit_label.grid(row=2, column=2, padx=10, pady=10, sticky = 'e')

        self.take_profit_entry = tk.Entry(root, fg="black", validate="key", validatecommand=(self.validate_numeric, '%P'))
        self.take_profit_entry.insert(0, f"{self.trader.strat.take_profit}")  # Replace with actual current value
        self.take_profit_entry.grid(row=2, column=3, padx=10, pady=10, sticky = 'w')

        self.submit_take_profit = tk.Button(root, text="Update", fg="black", command=self.update_take_profit)
        self.submit_take_profit.grid(row=2, column=4, padx=10, pady=10, sticky = 'w')

        # Leverage
        self.leverage_label = tk.Label(root, text="Leverage:", fg="black")
        self.leverage_label.grid(row=4, column=2, padx=10, pady=10, sticky = 'e')

        self.leverage_entry = tk.Entry(root, fg="black", validate="key", validatecommand=(self.validate_numeric, '%P'))
        self.leverage_entry.insert(0, f"{self.trader.strat.leverage}")  # Replace with actual current value
        self.leverage_entry.grid(row=4, column=3, padx=10, pady=10, sticky = 'w')

        self.submit_leverage = tk.Button(root, text="Update", fg="black", command=self.update_leverage)
        self.submit_leverage.grid(row=4, column=4, padx=10, pady=10, sticky = 'w')

        # Plot initial data
        self.plot_data()

        self.add_logo()

        # Set up file watcher for live updates
        self.observer = Observer()
        self.handler = FileWatcher(self)
        self.observer.schedule(self.handler, path=os.path.dirname(self.csv_file), recursive=False)
        self.observer.start()
        
        # Update every 5 seconds
        self.update_timer()

    def plot_data(self):
        # Clear previous plots
        for ax_row in self.ax.flatten():
            ax_row.clear()

        # Convert 'timestamp' to datetime and handle time format
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], format='%Y-%m-%d %H:%M:%S')

        # Time-series plot of price with SMA overlays
        self.ax[0, 0].plot(self.df['timestamp'], self.df['price'], label="Price", color="cyan")
        self.ax[0, 0].plot(self.df['timestamp'], self.df['short sma'], label="Short SMA", color="red", linestyle='--')
        self.ax[0, 0].plot(self.df['timestamp'], self.df['long sma'], label="Long SMA", color="green", linestyle='--')
        self.ax[0, 0].set_title("Price and SMAs Over Time", color= 'white')
        self.ax[0, 0].set_xlabel('Time', color= 'white')
        self.ax[0, 0].set_ylabel('Price/SMA Values', color= 'white')

        # Highlight trades with markers
        long_trades = self.df[self.df['status'] == 'Open Long Trade']
        short_trades = self.df[self.df['status'] == 'Open Short Trade']

        self.ax[0, 0].scatter(long_trades['timestamp'], long_trades['price'], color="green", label="Long Trade", zorder=5)
        for i, row in long_trades.iterrows():
            self.ax[0, 0].text(row['timestamp'], row['price'], "Long", color="white", fontsize=9, ha='right')

        self.ax[0, 0].scatter(short_trades['timestamp'], short_trades['price'], color="red", label="Short Trade", zorder=5)
        for i, row in short_trades.iterrows():
            self.ax[0, 0].text(row['timestamp'], row['price'] + 40, "Short", color="white", fontsize=9, ha='center')

        # Rotate and format x-axis labels
        self.ax[0, 0].tick_params(axis='x', rotation=45)
        self.ax[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Add a legend
        self.ax[0, 0].legend(loc='upper left', fontsize='small')

        # Autoscale for the first subplot
        self.ax[0, 0].relim()  # Recalculate limits
        self.ax[0, 0].autoscale_view()  # Apply new limits

        # Rolling average of total profit
        self.ax[0, 1].plot(self.df['timestamp'], self.df['networth'],color="blue")
        self.ax[0, 1].set_title("Networth", color= 'white')
        self.ax[0, 1].set_xlabel('Time', color= 'white')
        self.ax[0, 1].set_ylabel('Networth', color= 'white')

        # Rotate and format x-axis labels
        self.ax[0, 1].tick_params(axis='x', rotation=45)
        self.ax[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        
        # Autoscale for the second subplot
        self.ax[0, 1].relim()
        self.ax[0, 1].autoscale_view()

        # Profit since opening trade plot
        self.ax[1, 0].plot(self.df['timestamp'], self.df['profit since opening trade'], label="Profit Since Opening", color="purple")
        self.ax[1, 0].set_title("Profit Since Opening Trade", color= 'white')
        self.ax[1, 0].set_xlabel('Time', color= 'white')
        self.ax[1, 0].set_ylabel('Profit', color= 'white')

        # Rotate and format x-axis labels
        self.ax[1, 0].tick_params(axis='x', rotation=45)
        self.ax[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Autoscale for the third subplot
        self.ax[1, 0].relim()
        self.ax[1, 0].autoscale_view()

        # Total profit plot
        self.ax[1, 1].plot(self.df['timestamp'], self.df['total profit'], label="Total Profit", color="orange")
        self.ax[1, 1].set_title("Total Profit", color= 'white')
        self.ax[1, 1].set_xlabel('Time', color= 'white')
        self.ax[1, 1].set_ylabel('Total Profit', color= 'white')

        # Rotate and format x-axis labels
        self.ax[1, 1].tick_params(axis='x', rotation=45)
        self.ax[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Autoscale for the fourth subplot
        self.ax[1, 1].relim()
        self.ax[1, 1].autoscale_view()

        # Apply tight layout and redraw canvas
        #self.fig.tight_layout()
        if self.canvas is None:
            pass #wait until it's initialized

        else:
            self.canvas.draw()    
            self.fig.subplots_adjust(hspace=.4)  # Adjust vertical spacing (increase the value for more space)

    def update_data(self):
        # Re-read CSV file to get new data
        self.df = pd.read_csv(self.csv_file)

        #get data from backend for text output
        active_profit = self.trader.strat.total_profit
        current_networth = self.trader.strat.networth
        current_position = self.trader.strat.profit
        
        # Update the info box label with both active profit and current networth
        self.info_box_label.config(text=f"Active Profit: ${active_profit:.2f}\nCurrent Networth: ${current_networth:.2f}\nCurrent Position: ${current_position:.2f}")
        self.plot_data()
        
    def update_timer(self):
        if self.update_active:
            self.update_data()
            self.root.after(15000, self.update_timer)  # 15000ms = 15 seconds

    def toggle_update(self):
        # Toggle between start and pause
        self.update_active = not self.update_active
        if self.update_active:
            self.start_pause_button.config(text="Pause AutoTrader")
            self.update_timer()
            self.trader.active = True
        else:
            self.start_pause_button.config(text="Start AutoTrader")
            self.trader.active = False

    def add_logo(self):
        # Load the logo image (replace with the path to your logo image)
        logo_path = Path(__file__).parent / 'logo.png' 
        logo = Image.open(logo_path)
        logo_resized = logo.resize((522, 326))
        logo_tk = ImageTk.PhotoImage(logo_resized)
        # Create a Label widget and set the image as the label's image
        logo_label = tk.Label(self.root, image=logo_tk, bg='#2e2e2e')  # Set background color to match the window
        logo_label.image = logo_tk  # Keep a reference to avoid garbage collection
        
        # Position the logo (you can change row and column based on your layout)
        logo_label.grid(row=0, column=2, padx=7, pady=7)  # Adjust position as needed

    def open_long(self):
        if self.trader.strat.active_trades_amnt < self.trader.strat.parallel_trades_amnt:
            self.action_box.config(text=f"A long trade is trying to be been opened!")
            self.trader.strat.manual_trade = 'open long'
        
        else:
            self.action_box.config(text=f"The maximum amount of open trades has been reached!")

    def open_short(self):
        if self.trader.strat.active_trades_amnt < self.trader.strat.parallel_trades_amnt:
            self.action_box.config(text=f"A short trade is trying to be been opened!")
            self.trader.strat.manual_trade = 'open short'
        
        else:
            self.action_box.config(text=f"The maximum amount of open trades has been reached!")

    def close_trade(self):
        
        if self.trader.strat.active_trades_amnt > 0:
            self.action_box.config(text=f"A trade is trying to be closed!")
            self.trader.strat.manual_trade = 'close trade'
        
        else:
            self.action_box.config(text=f"There are no active trades that can be closed...")

    def withdraw_money(self):
        try:
            amount = float(self.withdraw_input.get())
            self.trader.strat.networth = self.trader.strat.networth - amount
            self.action_box.config(text=f"${amount} have been withdrawn...")
        except:
            print('invalid input (withdrawing)')
            self.action_box.config(text=f"invalid input (withdrawing)")
    
    def deposit_money(self):
        try:
            amount = float(self.deposit_input.get())
            self.trader.strat.networth = self.trader.strat.networth + amount
            self.action_box.config(text=f"${amount} have been deposited...")
        except:
            print('invalid input (depositing)')
            self.action_box.config(text=f"invalid input (depositing)")

    def update_take_profit(self):
        try:
            amount = float(self.take_profit_entry.get())
            self.trader.strat.take_profit = amount
            self.action_box.config(text=f"The take profit margin has been updated to ${amount}!")
        except:
            print('invalid input (take profit)')
            self.action_box.config(text=f"invalid input (take profit)")

    def update_stop_loss(self):
        try:
            amount = float(self.stop_loss_entry.get())
            self.trader.strat.stop_loss = amount
            self.action_box.config(text=f"The stop loss margin has been updated to ${amount}!")
        except:
            print('invalid input (stop loss)')
            self.action_box.config(text=f"invalid input (stop loss)")

    def update_leverage(self):
        try:
            amount = float(self.leverage_entry.get())
            
            if self.trader.strat.active_trades_amnt > 0:
                print("leverage can't be changed while trades are open")
                self.action_box.config(text=f"leverage can't be changed while trades are open...")

            else:
                self.trader.strat.leverage = amount
                self.action_box.config(text=f"The leverage has been updated to {amount}!")
        except:
            print('invalid input (leverage)')
            self.action_box.config(text=f"invalid input (leverage)")
    

    def flush_history(self):
        # Clear the data and reset the plots
        df = pd.read_csv(self.csv_file)
    
        # Check if the dataframe has enough rows
        if len(df) < 2:
            print("Error - Can't flush an empty log file.")
            self.action_box.config(text=f"Error - Can't flush an empty log file.")
            return
        
        last_row = df.iloc[[-1]]  # Retain only the last row of data

        # Keep only the first and last rows
        filtered_df = pd.DataFrame(last_row)
        
        # Save the updated dataframe back to the CSV file
        filtered_df.to_csv(self.csv_file, index=False)
        self.action_box.config(text=f"The history has been flushed!")

    def flush_profit(self):
        self.trader.strat.total_profit = 0
        self.action_box.config(text=f"The profit session has been reset!")
    
    def only_positive_numbers(self, input_value):
        """
        Validation function to allow only positive numeric values.
        """
        if input_value == "" or input_value.isdigit():
            return True  # Allow empty input (e.g., for clearing the field) or numbers
        elif input_value.replace(".", "", 1).isdigit() and input_value.count('.') < 2:
            return True  # Allow floating-point numbers
        return False  # Reject other inputs

# Background function for the trading backend
def run_backend(trader):
    while True:
        trader.run()
        time.sleep(15)  # Adjust the update frequency as needed

# Main Tkinter GUI setup
def run_app():
    # Show the pre-launch window to collect API keys
    pre_launch_root = tk.Tk()
    pre_launch_window = PreLaunchWindow(pre_launch_root)
    pre_launch_root.mainloop()

    if pre_launch_window.api_keys is None:
        return  # Exit if the launch is cancelled

    # File path to your CSV
    csv_file = "src/trade_log.csv"
    icon_path = Path(__file__).parent / 'logo.png'
    
    # Retrieve API keys from pre-launch window
    price_key, ti_key = pre_launch_window.api_keys

    # Start the backend in a separate thread
    trader = run_Trader(price_key, ti_key)
    backend_thread = threading.Thread(target=run_backend, args=(trader,), daemon=True)
    backend_thread.start()

    # Start the frontend
    root = tk.Tk()
    root.title("AutoTrader")
    icon_image = tk.PhotoImage(file=icon_path)  # Replace with your image file path
    root.iconphoto(True, icon_image)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size to the full screen size
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    app = TradingApp(root, csv_file, trader)
    root.mainloop()

if __name__ == "__main__":
    run_app()
