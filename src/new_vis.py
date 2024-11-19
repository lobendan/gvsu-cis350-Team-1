import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import pandas as pd
from matplotlib.animation import FuncAnimation
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.dates as mdates

# Define a class for monitoring file changes
class FileWatcher(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app
        
    def on_modified(self, event):
        if event.src_path.endswith(".csv"):
            self.app.update_data()

# Define the main application
class TradingApp:
    def __init__(self, root, csv_file):
        self.root = root
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        self.update_active = True  # Initially the update is active
        
        # Setup plot area in Tkinter window
        self.fig, self.ax = plt.subplots(2, 2, figsize=(10, 8))

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

        # Create buttons for Start/Pause and Flush History
        self.start_pause_button = tk.Button(self.root, text="Pause", command=self.toggle_update)
        self.start_pause_button.grid(row=4, column=0, padx=10, pady=10)

        self.flush_button = tk.Button(self.root, text="Flush History", command=self.flush_history)
        self.flush_button.grid(row=4, column=1, padx=10, pady=10)

        # Plot initial data
        self.plot_data()

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
        
        # Time-series plot of price
        self.ax[0, 0].plot(self.df['timestamp'], self.df['price'], label="Price", color="cyan")
        self.ax[0, 0].set_title("Price Over Time")
        self.ax[0, 0].set_xlabel('Time')
        self.ax[0, 0].set_ylabel('Price')

        # Highlight trades with markers
        long_trades = self.df[self.df['status'] == 'Open Long Trade']
        short_trades = self.df[self.df['status'] == 'Open Short Trade']
        
        # Mark long trades
        self.ax[0, 0].scatter(long_trades['timestamp'], long_trades['price'], color="green", label="Long Trade", zorder=5)
        for i, row in long_trades.iterrows():
            self.ax[0, 0].text(row['timestamp'], row['price'], "Long", color="white", fontsize=9, ha='right')

        # Mark short trades
        self.ax[0, 0].scatter(short_trades['timestamp'], short_trades['price'], color="red", label="Short Trade", zorder=5)
        for i, row in short_trades.iterrows():
            self.ax[0, 0].text(row['timestamp'], row['price']+40, "Short", color="white", fontsize=9, ha='center')

        # Rotate and format x-axis labels
        self.ax[0, 0].tick_params(axis='x', rotation=45)
        self.ax[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        # Short vs Long SMA plot
        self.ax[0, 1].plot(self.df['timestamp'], self.df['short sma'], label="Short SMA", color="red")
        self.ax[0, 1].plot(self.df['timestamp'], self.df['long sma'], label="Long SMA", color="green")
        self.ax[0, 1].set_title("Short SMA vs Long SMA")
        self.ax[0, 1].set_xlabel('Time')
        self.ax[0, 1].set_ylabel('SMA Values')

        # Rotate and format x-axis labels
        self.ax[0, 1].tick_params(axis='x', rotation=45)
        self.ax[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        # Profit since opening trade plot (rounded values)
        self.ax[1, 0].plot(self.df['timestamp'], self.df['profit since opening trade'], label="Profit Since Opening", color="purple")
        self.ax[1, 0].set_title("Profit Since Opening Trade")
        self.ax[1, 0].set_xlabel('Time')
        self.ax[1, 0].set_ylabel('Profit')

        # Rotate and format x-axis labels
        self.ax[1, 0].tick_params(axis='x', rotation=45)
        self.ax[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        # Total profit plot
        self.ax[1, 1].plot(self.df['timestamp'], self.df['total profit'], label="Total Profit", color="orange")
        self.ax[1, 1].set_title("Total Profit")
        self.ax[1, 1].set_xlabel('Time')
        self.ax[1, 1].set_ylabel('Total Profit')

        # Rotate and format x-axis labels
        self.ax[1, 1].tick_params(axis='x', rotation=45)
        self.ax[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        # Apply tight layout and redraw canvas
        self.fig.tight_layout()
        self.canvas.draw()


    def update_data(self):
        # Re-read CSV file to get new data
        self.df = pd.read_csv(self.csv_file)
        self.plot_data()

    def update_timer(self):
        if self.update_active:
            self.update_data()
            self.root.after(5000, self.update_timer)  # 5000ms = 5 seconds

    def toggle_update(self):
        # Toggle between start and pause
        self.update_active = not self.update_active
        if self.update_active:
            self.start_pause_button.config(text="Pause")
            self.update_timer()
        else:
            self.start_pause_button.config(text="Start")

    def flush_history(self):
        # Clear the data and reset the plots
        self.df = pd.DataFrame(columns=["timestamp", "price", "status", "short sma", "long sma", "profit since opening trade", "total profit"])
        self.plot_data()


# Main Tkinter GUI setup
def run_app():
    root = tk.Tk()
    root.title("Trading Data Visualizer")
    
    # File path to your CSV (updated path)
    csv_file = "src/trade_log.csv"
    
    app = TradingApp(root, csv_file)
    root.mainloop()

if __name__ == "__main__":
    run_app()
