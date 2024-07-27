import ctypes
import tkinter as tk

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Créer la fenêtre principale
root = tk.Tk()
root.title("SM64 Tool Loader")
root.geometry("400x200")

# Ajouter des labels pour la version et l'auteur
version_label = tk.Label(root, text="Version", font=("Arial", 18))
version_label.pack(pady=(20, 0))

version_value = tk.Label(root, text="1.6", font=("Arial", 16), fg="red")
version_value.pack()

author_label = tk.Label(root, text="Creator", font=("Arial", 18))
author_label.pack(pady=(20, 0))

author_value = tk.Label(root, text="Soniceurs", font=("Arial", 16), fg="red")
author_value.pack()

# Lancer l'application
root.mainloop()

