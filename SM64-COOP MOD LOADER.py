import ctypes
import tkinter as tk
from tkinter import ttk, messagebox, Menu, filedialog
import os
import shutil
import json
import subprocess

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def open_set_play_interface():
    """Ouvre une fenêtre modale pour configurer les exécutables pour les boutons de jeu."""
    def apply_changes():
        """Enregistre les chemins des exécutables sélectionnés."""
        ex_coop_path = ex_coop_entry.get()
        coop_deluxe_path = coop_deluxe_entry.get()

        if ex_coop_path and coop_deluxe_path:
            with open('play_executables.json', 'w') as f:
                json.dump({'EX_COOP': ex_coop_path, 'COOP_DELUXE': coop_deluxe_path}, f)
            messagebox.showinfo("Configuration", "Les chemins des exécutables ont été mis à jour.")
            set_play_window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner les chemins des exécutables pour les deux options.")

    def browse_file(entry_widget):
        """Ouvre une boîte de dialogue pour sélectionner un fichier exécutable."""
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    # Créer la fenêtre modale de configuration
    set_play_window = tk.Toplevel(root)
    set_play_window.title("Set Play")
    set_play_window.geometry("400x250")
    set_play_window.configure(bg=background_color)

    # Rendre la fenêtre modale
    set_play_window.grab_set()
    set_play_window.transient(root)

    # Configuration des chemins d'exécutables
    tk.Label(set_play_window, text="EX COOP Executable:", bg=background_color, fg='white').pack(pady=5, padx=10, anchor=tk.W)
    ex_coop_entry = tk.Entry(set_play_window, width=50)
    ex_coop_entry.pack(pady=5, padx=10)
    tk.Button(set_play_window, text="Browse", command=lambda: browse_file(ex_coop_entry)).pack(pady=5, padx=10)

    tk.Label(set_play_window, text="COOP DELUXE Executable:", bg=background_color, fg='white').pack(pady=5, padx=10, anchor=tk.W)
    coop_deluxe_entry = tk.Entry(set_play_window, width=50)
    coop_deluxe_entry.pack(pady=5, padx=10)
    tk.Button(set_play_window, text="Browse", command=lambda: browse_file(coop_deluxe_entry)).pack(pady=5, padx=10)

    tk.Button(set_play_window, text="Apply", command=apply_changes).pack(pady=20)



def periodic_update():
    """Refresh the mods and archive lists every 5 seconds."""
    update_mods_list()
    update_mods_archive_list()
    root.after(5000, periodic_update)  # Schedule this function to be called again in 5 seconds

def open_folder(folder):
    """Open the specified folder using the file explorer."""
    os.startfile(folder)

def get_main_lua_names(path):
    """Get a list of folder names containing main.lua files."""
    main_lua_names = []
    for root_dir, dirs, files in os.walk(path):
        if 'main.lua' in files and '.mods archive' not in root_dir.lower():
            main_lua_names.append(root_dir)
    return main_lua_names

def rename_lua_files(mods_path):
    """Rename .lua files to main.lua within their respective folders."""
    lua_files = [file for file in os.listdir(mods_path) if file.endswith('.lua') and os.path.isfile(os.path.join(mods_path, file))]
    
    for file in lua_files:
        source_path = os.path.join(mods_path, file)
        folder_name = os.path.splitext(file)[0]
        destination_folder = os.path.join(mods_path, folder_name)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        destination_path = os.path.join(destination_folder, 'main.lua')

        try:
            os.rename(source_path, destination_path)
        except Exception as e:
            print(f"Error renaming {file} to main.lua: {e}")

def update_mods_list():
    """Update the Mods tab list with folders containing main.lua."""
    mods_list = get_main_lua_names(mods_path)
    mods_listbox.delete(0, tk.END)
    for folder in mods_list:
        mods_listbox.insert(tk.END, os.path.basename(folder))

def update_mods_archive_list():
    """Update the Archive tab list with folders from .mods archive."""
    mods_archive_path = os.path.join(mods_path, '.mods archive')
    if not os.path.exists(mods_archive_path):
        os.makedirs(mods_archive_path)
    mods_archive_folders = [folder for folder in os.listdir(mods_archive_path) if os.path.isdir(os.path.join(mods_archive_path, folder))]
    archive_listbox.delete(0, tk.END)
    for folder in mods_archive_folders:
        archive_listbox.insert(tk.END, folder)

def move_to_archive():
    """Move selected items from Mods to .mods archive."""
    selected_indices = mods_listbox.curselection()
    if selected_indices:
        for index in selected_indices:
            selected_item = mods_listbox.get(index)
            source_path = os.path.join(mods_path, selected_item)
            destination_path = os.path.join(mods_path, '.mods archive', selected_item)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                print(f"Error moving {selected_item} to .mods archive: {e}")
        update_mods_list()
        update_mods_archive_list()

def move_to_loading():
    """Move selected items from .mods archive to Mods."""
    selected_indices = archive_listbox.curselection()
    if selected_indices:
        for index in selected_indices:
            selected_item = archive_listbox.get(index)
            source_path = os.path.join(mods_path, '.mods archive', selected_item)
            destination_path = os.path.join(mods_path, selected_item)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                print(f"Error moving {selected_item} to Mods: {e}")
        update_mods_list()
        update_mods_archive_list()

def delete_selected(listbox, archive=False):
    """Delete selected items from the listbox."""
    selected_indices = listbox.curselection()
    for index in selected_indices:
        selected_item = listbox.get(index)
        if archive:
            item_path = os.path.join(mods_path, '.mods archive', selected_item)
        else:
            item_path = os.path.join(mods_path, selected_item)
        try:
            shutil.rmtree(item_path)
        except Exception as e:
            print(f"Error deleting {selected_item}: {e}")
    update_mods_list()
    update_mods_archive_list()

def show_context_menu(event, listbox, archive=False):
    """Show context menu on right click."""
    menu = tk.Menu(root, tearoff=0)
    if archive:
        menu.add_command(label="Move to Loading", command=move_to_loading)
    else:
        menu.add_command(label="Move to Archive", command=move_to_archive)
    
    menu.add_separator()
    menu.add_command(label="Delete", command=lambda: confirm_delete(listbox, archive))
    menu.post(event.x_root, event.y_root)

def confirm_delete(listbox, archive=False):
    """Confirm deletion of selected items."""
    response = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected items?")
    if response:
        delete_selected(listbox, archive)

def open_save_script():
    """Open save.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    save_script = os.path.join(menu_folder, "save.py")
    os.startfile(save_script)

def open_add_mod_script():
    """Open add-mod.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    add_mod_script = os.path.join(menu_folder, "add-mod.py")
    os.startfile(add_mod_script)

def open_coopdx_script():
    """Open coopdx.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    coopdx_script = os.path.join(menu_folder, "coopdx.py")
    os.startfile(coopdx_script)

def open_gamebanana_script():
    """Open gamebanana.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    gamebanana_script = os.path.join(menu_folder, "gamebanana.py")
    os.startfile(gamebanana_script)

def open_essential_script():
    """Open essential.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    essential_script = os.path.join(menu_folder, "essential.py")
    os.startfile(essential_script)

def open_update_script():
    """Open update.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    update_script = os.path.join(menu_folder, "update.py")
    os.startfile(update_script)

def open_info_script():
    """Open info.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    info_script = os.path.join(menu_folder, "info.py")
    os.startfile(info_script)

def open_sm64_script():
    """Open SM64.py script from the 'Menu' folder."""
    menu_folder = os.path.join(os.path.dirname(__file__), "Menu")
    sm64_script = os.path.join(menu_folder, "SM64.py")
    os.startfile(sm64_script)

def load_play_executables():
    """Charge les chemins des exécutables depuis le fichier play_executables.json."""
    if os.path.exists('play_executables.json'):
        with open('play_executables.json', 'r') as f:
            data = json.load(f)
            return data.get('EX_COOP', None), data.get('COOP_DELUXE', None)
    return None, None

def play_executable(play_type):
    """Exécute l'exécutable correspondant à play_type ('EX_COOP' ou 'COOP_DELUXE')."""
    ex_coop_path, coop_deluxe_path = load_play_executables()
    if play_type == "EX_COOP":
        executable_path = ex_coop_path
    elif play_type == "COOP_DELUXE":
        executable_path = coop_deluxe_path
    else:
        executable_path = None

    if not executable_path or not os.path.exists(executable_path):
        response = messagebox.askyesno("Executable Not Set", "Executable not found or not set. Would you like to set it now?")
        if response:
            open_set_play_interface()
    else:
        subprocess.Popen(executable_path)


def setup_initial_mods():
    """Setup initial mods loading."""
    rename_lua_files(mods_path)
    update_mods_list()
    update_mods_archive_list()

def modify_transparency():
    """Open a dialog to modify the window transparency."""
    def apply_transparency():
        try:
            transparency = float(transparency_entry.get())
            if 0.0 <= transparency <= 1.0:
                root.attributes('-alpha', transparency)
                # Save transparency setting
                with open('settings.json', 'w') as f:
                    json.dump({'transparency': transparency}, f)
                transparency_window.destroy()
            else:
                messagebox.showerror("Invalid Input", "Transparency must be between 0.0 and 1.0.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    transparency_window = tk.Toplevel(root)
    transparency_window.title("Modify Transparency")
    transparency_window.geometry("300x150")
    
    tk.Label(transparency_window, text="Set Transparency (0.0 to 1.0):").pack(pady=10)
    transparency_entry = tk.Entry(transparency_window)
    transparency_entry.pack(pady=5)
    
    tk.Button(transparency_window, text="Apply", command=apply_transparency).pack(pady=10)

def load_settings():
    """Load settings from the settings.json file."""
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            transparency = settings.get('transparency', 0.7)
            root.attributes('-alpha', transparency)
    else:
        # Default transparency
        root.attributes('-alpha', 0.7)

# Path to the Mods folder
mods_path = os.path.join(os.getenv('APPDATA'), 'sm64ex-coop', 'mods')

# Create the mods folder if it doesn't exist
if not os.path.exists(mods_path):
    os.makedirs(mods_path)

# Create the .mods archive folder if it doesn't exist
mods_archive_path = os.path.join(mods_path, '.mods archive')
if not os.path.exists(mods_archive_path):
    os.makedirs(mods_archive_path)

# Create the main window
root = tk.Tk()
root.title("SM64-COOP MOD LOADER")
root.geometry("800x900")

# Apply the specified background color
background_color = '#850F8D'
root.config(bg=background_color)

# Load settings
load_settings()

# Create a Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# Mods tab
frame_mods = tk.Frame(notebook, bg=background_color)
notebook.add(frame_mods, text='Mods')

# List of folders containing main.lua in the Mods tab
mods_listbox = tk.Listbox(frame_mods, bg='#F0F0F0', fg='#000000', selectmode=tk.MULTIPLE)
mods_listbox.pack(expand=1, fill='both', padx=10, pady=10)

# List of archived items below the Mods list
archive_listbox = tk.Listbox(frame_mods, bg='#FFFFFF', fg='#000000', selectmode=tk.MULTIPLE)
archive_listbox.pack(expand=1, fill='both', padx=10, pady=10)

# Bind right-click to show the context menu
mods_listbox.bind('<Button-3>', lambda event: show_context_menu(event, mods_listbox))
archive_listbox.bind('<Button-3>', lambda event: show_context_menu(event, archive_listbox, archive=True))

# Menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Main menu
main_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Main", menu=main_menu)
main_menu.add_command(label="Add Mod", command=open_add_mod_script)
main_menu.add_command(label="Set Play", command=open_set_play_interface)
main_menu.add_command(label="Open File Mod", command=lambda: open_folder(mods_path))

# Index menu
index_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Index", menu=index_menu)
index_menu.add_command(label="Mod Coop", command=open_coopdx_script)
index_menu.add_command(label="Mod Gamebanana", command=open_gamebanana_script)
index_menu.add_command(label="Mod Essential", command=open_essential_script)

# Utility menu
utility_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Utility", menu=utility_menu)
utility_menu.add_command(label="Save 100%", command=open_save_script)

# Setting menu
setting_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Setting", menu=setting_menu)
setting_menu.add_command(label="Mod Loader", command=modify_transparency)
setting_menu.add_command(label="Super Mario 64", command=open_sm64_script)

# About menu
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Update", command=open_update_script)
about_menu.add_command(label="Info", command=open_info_script)

# Play buttons at the bottom of the interface
play_ex_coop_button = tk.Button(root, text="Play EX COOP", command=lambda: play_executable("EX_COOP"), bg='#850F8D', fg='white', font=('Helvetica', 14, 'bold'))
play_coop_deluxe_button = tk.Button(root, text="Play COOP DELUXE", command=lambda: play_executable("COOP_DELUXE"), bg='#850F8D', fg='white', font=('Helvetica', 14, 'bold'))

play_buttons_frame = tk.Frame(root, bg=background_color)
play_buttons_frame.pack(pady=20, side=tk.BOTTOM, fill=tk.X)

# Pack the buttons to center them
play_ex_coop_button.pack(side=tk.LEFT, padx=10, expand=True)
play_coop_deluxe_button.pack(side=tk.LEFT, padx=10, expand=True)


# Setup initial mods
setup_initial_mods()

# Start the periodic update
root.after(5000, periodic_update)  # Start periodic updates every 5 seconds

# Start the Tkinter main loop
root.mainloop()
