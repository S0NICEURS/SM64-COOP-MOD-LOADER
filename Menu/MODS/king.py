import ctypes
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import subprocess
import os

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# URL de l'image
image_url = "https://i.ibb.co/mcLNs6y/kingg.png"

def create_main_window():
    root = tk.Tk()
    root.title("Add Mods")
    root.configure(bg="black")
    
    try:
        # Récupérer l'image depuis l'URL
        print("Récupération de l'image...")
        response = requests.get(image_url)
        response.raise_for_status()  # Vérifier si la requête a réussi
        img_data = response.content
        print("Image récupérée avec succès.")

        # Charger l'image avec Pillow
        print("Chargement de l'image avec Pillow...")
        img = Image.open(BytesIO(img_data))
        img = img.resize((500, 250), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        print("Image chargée et redimensionnée avec succès.")

        # Ajouter l'image en haut
        label_img = tk.Label(root, image=img, bg="black")
        label_img.image = img  # garder une référence à l'image
        label_img.pack(pady=10)
        print("Image ajoutée à l'interface.")

        # Ajouter le texte "Nom du Mod"
        title = tk.Label(root, text="King", font=("Helvetica", 20, "bold"), fg="white", bg="black")
        title.pack(pady=5)

        # Ajouter le texte "Nom de l'auteur"
        author = tk.Label(root, text="By king the memer", font=("Helvetica", 16), fg="white", bg="black")
        author.pack(pady=5)

        # Ajouter le texte "Description du mod"
        description = tk.Label(root, text="embody yourself as a king", font=("Helvetica", 12), fg="white", bg="black", wraplength=400)
        description.pack(pady=10)

        # Ajouter le bouton "Add in Mods" en bas
        button_add = ttk.Button(root, text="Add in Mods", command=run_minecraftDL)
        button_add.pack(pady=20)
        print("Tous les éléments ont été ajoutés à l'interface.")
        
    except Exception as e:
        print(f"Erreur : {e}")
    
    root.mainloop()

def run_minecraftDL():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'kingDL.py')
        subprocess.run(['python', script_path], check=True)
        print("Le script kingDL.py a été exécuté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de kingDL.py : {e}")

# Appeler la fonction pour créer la fenêtre principale
create_main_window()
