import ctypes
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Création de la fenêtre principale cachée
root = tk.Tk()
root.withdraw()

# Affichage de la boîte de dialogue d'erreur
messagebox.showerror("Error", "Currently not available")
