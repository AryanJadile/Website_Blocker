import time
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import json
import os

# Global variables
host_file_path = r"C://Windows//System32//drivers//etc//hosts"
redirect = "127.0.0.1"
site_block = []
scheduled_blocks = []
browsing_data = {}


# Function to add a website to the block list
def add_website():
    website = website_entry.get()
    if website:
        site_block.append(website)
        messagebox.showinfo("Added", f"{website} added to block list")
        website_entry.delete(0, tk.END)
        update_block_list()
    else:
        messagebox.showwarning("Input Error", "Please enter a website URL")


# Function to block websites
def block_website():
    with open(host_file_path, "r+") as host_file:
        content = host_file.read()
        for website in site_block:
            if website not in content:
                # Add website to hosts file
                host_file.write(redirect + " " + website + "\n")
                messagebox.showinfo("Blocked", f"{website} BLOCKED")
            else:
                messagebox.showwarning("Already Blocked", f"{website} is ALREADY BLOCKED")
    update_browsing_data("blocked")


# Function to unblock websites
def unblock_website():
    with open(host_file_path, "r+") as host_file:
        content = host_file.readlines()
        host_file.seek(0)
        for line in content:
            # Rewrite file excluding blocked websites
            if not any(website in line for website in site_block):
                host_file.write(line)
        host_file.truncate()
        messagebox.showinfo("Unblocked", f"Selected websites UNBLOCKED")
    update_browsing_data("unblocked")


# Function to schedule website blocking
def schedule_block():
    website = website_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()

    if website and start_time and end_time:
        scheduled_blocks.append({
            "website": website,
            "start_time": start_time,
            "end_time": end_time
        })
        messagebox.showinfo("Scheduled", f"Blocking of {website} scheduled")
        update_schedule_list()
    else:
        messagebox.showwarning("Input Error", "Please enter all required information")


# Function to update the block list display
def update_block_list():
    block_list.delete(0, tk.END)
    for site in site_block:
        block_list.insert(tk.END, site)


# Function to update the schedule list display
def update_schedule_list():
    schedule_list.delete(0, tk.END)
    for block in scheduled_blocks:
        schedule_list.insert(tk.END, f"{block['website']} - {block['start_time']} to {block['end_time']}")


# Function to update browsing data
def update_browsing_data(action):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if current_date not in browsing_data:
        browsing_data[current_date] = {"blocked": 0, "unblocked": 0}
    browsing_data[current_date][action] += 1
    save_browsing_data()


# Function to save browsing data
def save_browsing_data():
    with open("browsing_data.json", "w") as f:
        json.dump(browsing_data, f)


# Function to load browsing data
def load_browsing_data():
    global browsing_data
    if os.path.exists("browsing_data.json"):
        with open("browsing_data.json", "r") as f:
            browsing_data = json.load(f)


# Function to display browsing analytics
def show_analytics():
    analytics_window = tk.Toplevel(root)
    analytics_window.title("Browsing Analytics")
    analytics_window.geometry("300x200")

    for date, data in browsing_data.items():
        tk.Label(analytics_window, text=f"Date: {date}").pack()
        tk.Label(analytics_window, text=f"Blocked: {data['blocked']}").pack()
        tk.Label(analytics_window, text=f"Unblocked: {data['unblocked']}").pack()
        tk.Label(analytics_window, text="---").pack()


# Function to exit the program
def exit_program():
    root.destroy()


# Creating the main GUI window
root = tk.Tk()
root.title("Advanced Website Blocker")
root.geometry("600x500")
root.configure(bg="#2C3E50")

# Labels and Entries for user input
tk.Label(root, text="Enter Website to Block:", fg="#ECF0F1", bg="#2C3E50", font=("Arial", 12, "bold")).pack(pady=5)
website_entry = tk.Entry(root, width=50, fg="#2C3E50", bg="#ECF0F1", font=("Arial", 10))
website_entry.pack(pady=5)

tk.Label(root, text="Schedule Block:", fg="#ECF0F1", bg="#2C3E50", font=("Arial", 12, "bold")).pack(pady=5)
tk.Label(root, text="Start Time (HH:MM):", fg="#ECF0F1", bg="#2C3E50").pack()
start_time_entry = tk.Entry(root, width=20, fg="#2C3E50", bg="#ECF0F1")
start_time_entry.pack()

tk.Label(root, text="End Time (HH:MM):", fg="#ECF0F1", bg="#2C3E50").pack()
end_time_entry = tk.Entry(root, width=20, fg="#2C3E50", bg="#ECF0F1")
end_time_entry.pack()

# Buttons for various actions
tk.Button(root, text="Add Website", command=add_website, fg="#2C3E50", bg="#3498DB", font=("Arial", 10, "bold")).pack(
    pady=5)
tk.Button(root, text="Block Websites", command=block_website, fg="#2C3E50", bg="#E74C3C",
          font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="Unblock Websites", command=unblock_website, fg="#2C3E50", bg="#F1C40F",
          font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="Schedule Block", command=schedule_block, fg="#2C3E50", bg="#27AE60",
          font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="Show Analytics", command=show_analytics, fg="#2C3E50", bg="#9B59B6",
          font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(root, text="Exit", command=exit_program, fg="#ECF0F1", bg="#34495E", font=("Arial", 10, "bold")).pack(pady=5)

# Frame and Listbox for blocked websites
block_list_frame = tk.Frame(root, bg="#2C3E50")
block_list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

tk.Label(block_list_frame, text="Blocked Websites:", fg="#ECF0F1", bg="#2C3E50", font=("Arial", 10, "bold")).pack()
block_list = tk.Listbox(block_list_frame, fg="#2C3E50", bg="#ECF0F1", width=50)
block_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame and Listbox for scheduled blocks
schedule_list_frame = tk.Frame(root, bg="#2C3E50")
schedule_list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

tk.Label(schedule_list_frame, text="Scheduled Blocks:", fg="#ECF0F1", bg="#2C3E50", font=("Arial", 10, "bold")).pack()
schedule_list = tk.Listbox(schedule_list_frame, fg="#2C3E50", bg="#ECF0F1", width=50)
schedule_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Load existing data
load_browsing_data()

# Start the GUI main loop
root.mainloop()
