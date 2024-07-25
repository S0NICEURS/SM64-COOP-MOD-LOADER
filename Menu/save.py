import os
import requests
import ctypes
from zipfile import ZipFile
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Path where the file will be downloaded and extracted
base_path = Path.home() / "AppData" / "Roaming" / "sm64ex-coop"
zip_filename = "126_sm64_save_file.zip"
bin_filename = "sm64_save_file.bin"
zip_url = "https://gamebanana.com/dl/1239226"

# Function to download the file
def download_file(url, local_filename, progress_callback):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded_size += len(chunk)
            progress_callback(downloaded_size / total_size * 100)
    print(f"Download complete: {local_filename}")

# Function to unzip the file
def unzip_file(zip_path, extract_to_folder, progress_callback):
    with ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        for i, file in enumerate(zip_ref.namelist()):
            zip_ref.extract(file, extract_to_folder)
            progress_callback((i + 1) / total_files * 100)
    print(f"Unzipping complete: {zip_path}")

# Function to display a confirmation pop-up before starting
def ask_confirmation():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askokcancel(
        "Confirmation",
        "You can find your old save on backup_sm64_save_file.bin\nAre you sure you want to continue?",
        icon='warning'
    )
    root.destroy()  # Ensure the main window is destroyed after the confirmation dialog
    return response

# Function to display a completion message
def show_completion_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(
        "Operation Complete",
        message,
        icon='info'
    )
    root.destroy()  # Destroy the main window to close the program

# Function to display a cancellation message
def show_cancellation_message():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(
        "Warning",
        "The operation was canceled.",
        icon='info'
    )
    root.destroy()  # Destroy the main window to close the program

# Function to update the progress bar
def update_progress(value):
    progress_var.set(value)
    root.update_idletasks()

# Function to animate the progress bar (loading animation)
def animate_progress_bar():
    if progress_var.get() < 100:
        progress_var.set((progress_var.get() + 0.5) % 100)  # Increment and wrap around
        root.after(50, animate_progress_bar)  # Repeat the animation

# Function to set up and show the progress window
def setup_progress_window():
    global root, progress_var
    
    # Create a new window for the progress bar
    root = tk.Tk()
    root.title("Operation in Progress")
    
    # Create the message label
    message_label = tk.Label(root, text="Please wait!\nIf the operation takes too long, try again")
    message_label.pack(pady=(10, 0))
    
    # Create the progress bar
    progress_var = tk.DoubleVar()
    progress = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress.pack(padx=20, pady=20)
    
    # Start the animation
    root.after(0, animate_progress_bar)
    
    return root

# Function to run the process with a progress bar
def run_with_progress():
    global root

    # Ask for confirmation before proceeding
    if not ask_confirmation():
        print("Operation canceled.")
        show_cancellation_message()
        return

    # Set up and show the progress window
    root = setup_progress_window()
    
    def background_task():
        try:
            # Create the full path for the zip file and the bin file
            zip_path = base_path / zip_filename
            bin_path = base_path / bin_filename
            
            # Download the zip file even if it already exists
            print("Downloading...")
            download_file(zip_url, zip_path, update_progress)
            
            # If the bin file exists, move it
            if bin_path.exists():
                backup_bin_path = base_path / f"backup_{bin_filename}"
                shutil.move(bin_path, backup_bin_path)
                print(f"{bin_filename} moved to {backup_bin_path}")
            
            # Unzip the file after downloading
            if zip_path.exists():
                print("Unzipping...")
                unzip_file(zip_path, base_path, update_progress)
                # Clean up the zip file after extraction
                os.remove(zip_path)
                print(f"{zip_filename} deleted.")
            
            # Display a completion message
            root.after(0, lambda: show_completion_message("Congratulations! The operation was completed successfully."))
        
        except Exception as e:
            print(f"Error: {e}")
            root.after(0, show_cancellation_message)
        
        finally:
            root.after(0, root.destroy)  # Ensure the window is closed in case of error or success

    # Run the background task in a separate thread
    threading.Thread(target=background_task, daemon=True).start()
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    run_with_progress()
