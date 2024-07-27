import ctypes
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import subprocess  # Pour exécuter des fichiers Python

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        img = Image.open(BytesIO(response.content))
        return img
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None
    except IOError as e:
        print(f"Erreur lors de l'ouverture de l'image : {e}")
        return None

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mod Essential")

        # Configurer le fond noir pour la fenêtre principale
        self.root.configure(bg="black")

        # Background de l'apps
        url = "https://i.ibb.co/1bPZbrJ/wp1995120.png"
        self.original_image = download_image(url)
        
        if self.original_image is None:
            print("Impossible de charger l'image.")
            return
        
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        
        # Créer un canevas pour l'image
        self.canvas = tk.Canvas(root, width=self.original_image.width, height=self.original_image.height, bg="black", bd=0, highlightthickness=0)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.image = self.tk_image
        
        # Créer un cadre pour les boutons centré
        self.button_frame = tk.Frame(root, bg="black")
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        # Création des cadres pour les boutons afin de simuler la bordure
        self.create_button_frame(self.button_frame, "API", self.show_home)
        self.create_button_frame(self.button_frame, "MODS", self.show_mods)
        self.create_button_frame(self.button_frame, "ROM HACK", self.show_rom_hack)
        
        # Centrer les boutons horizontalement
        self.button_frame.update_idletasks()
        self.button_frame_width = self.button_frame.winfo_width()
        self.button_frame.place(relx=0.5, anchor=tk.N, x=self.button_frame_width // 0.1)
        
        # Créer les frames pour les différentes pages
        self.home_frame = tk.Frame(root, bg="black")
        self.mods_frame = tk.Frame(root, bg="black")
        self.rom_hack_frame = tk.Frame(root, bg="black")
        
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        self.mods_frame.pack(fill=tk.BOTH, expand=True)
        self.rom_hack_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ajouter un label pour afficher la page actuelle
        self.page_label = tk.Label(root, text="API", bg="black", fg="red", font=("Helvetica", 10))
        self.page_label.pack(side=tk.BOTTOM, pady=23)
        
        # Définir la police pour les textes
        self.text_font = ("Helvetica", 10, "bold")  # Réduit la taille de la police

        # Variables pour stocker les IDs des textes
        self.minecraft_text_id = None
        self.character_select_text_id = None
        self.smash_bros_text_id = None
        self.mods_text_ids = []  # Nouvelle liste pour stocker les IDs des nouveaux textes
        
        self.show_home()  # Affiche la page d'accueil par défaut

    def create_button_frame(self, parent_frame, text, command):
        # Cadre qui simulera la bordure du bouton
        button_frame = tk.Frame(parent_frame, bg="black", height=2)
        button_frame.pack(side=tk.LEFT, padx=5)
        
        # Bouton à l'intérieur du cadre
        button = tk.Button(button_frame, text=text, command=command, 
                           bg="black", fg="white", bd=0, relief="flat")
        button.pack(pady=(2, 0))
        
    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        self.page_label.config(text="API")

        # Ajouter les textes "Character Select" et "Super Smash Bros" à gauche
        if not self.character_select_text_id:
            self.character_select_text_id = self.canvas.create_text(20, 20,  # Positionné à gauche
                                                                    text="Character Select", fill="white", font=self.text_font, anchor=tk.W)
            # Lier un clic sur le texte "Character Select" à une fonction (vide pour l'instant)
            self.canvas.tag_bind(self.character_select_text_id, '<Button-1>', self.character_select_clicked)
        
        if not self.smash_bros_text_id:
            self.smash_bros_text_id = self.canvas.create_text(20, 40,  # Positionné à gauche et juste en dessous de "Character Select"
                                                              text="Super Smash Bros", fill="white", font=self.text_font, anchor=tk.W)
            # Lier un clic sur le texte "Super Smash Bros" à une fonction (vide pour l'instant)
            self.canvas.tag_bind(self.smash_bros_text_id, '<Button-1>', self.smash_bros_clicked)
        
        # Effacer le texte "Minecraft" et les autres textes de mods s'ils sont affichés
        if self.minecraft_text_id:
            self.canvas.delete(self.minecraft_text_id)
            self.minecraft_text_id = None
        for text_id in self.mods_text_ids:
            self.canvas.delete(text_id)
        self.mods_text_ids.clear()

    def show_mods(self):
        self.hide_all_frames()
        self.mods_frame.pack(fill=tk.BOTH, expand=True)
        self.page_label.config(text="MODS")

        # Ajouter le texte "Minecraft" sur le côté gauche du canvas
        if not self.minecraft_text_id:
            self.minecraft_text_id = self.canvas.create_text(20, 20,  # Positionné à gauche
                                                             text="Minecraft +", fill="white", font=self.text_font, anchor=tk.W)
            # Lier un clic sur le texte "Minecraft" à une fonction
            self.canvas.tag_bind(self.minecraft_text_id, '<Button-1>', self.open_minecraft_file)

        # Ajouter les autres textes en dessous de "Minecraft"
        mods_texts = [
            ("Sonic Character Rebooted", "Menu/MODS/sonic_rebooted.py"),
            ("Speedrun Timer Reworked", "Menu/MODS/speedrun_time.py"),
            ("AI Hunter (Single Player)", "Menu/MODS/ai_hunter.py"),
            ("Random Objects", "Menu/MODS/random_obj.py"),
            ("Mario Hunt", "Menu/MODS/mario_hunt.py"),
            ("Super Mario Kart", "Menu/MODS/smk.py"),
            ("Proximity Chat", "Menu/MODS/proxi_chat.py"),
            ("Brutal Bosses", "Menu/MODS/boss.py"),
            ("King", "Menu/MODS/king.py"),
            ("NoClip", "Menu/MODS/noclip.py"),
        ]
        
        y_position = 40
        for mod_text, mod_file in mods_texts:
            text_id = self.canvas.create_text(20, y_position, text=mod_text, fill="white", font=self.text_font, anchor=tk.W)
            self.mods_text_ids.append(text_id)
            self.canvas.tag_bind(text_id, '<Button-1>', lambda e, file=mod_file: self.open_mod_file(file))
            y_position += 20  # Réduit l'espacement entre les textes

        # Effacer les textes "Character Select" et "Super Smash Bros" s'ils sont affichés
        if self.character_select_text_id:
            self.canvas.delete(self.character_select_text_id)
            self.character_select_text_id = None
        if self.smash_bros_text_id:
            self.canvas.delete(self.smash_bros_text_id)
            self.smash_bros_text_id = None

    def show_rom_hack(self):
        self.hide_all_frames()
        self.rom_hack_frame.pack(fill=tk.BOTH, expand=True)
        self.page_label.config(text="ROM HACK")

        # Effacer les textes s'ils sont affichés
        if self.character_select_text_id:
            self.canvas.delete(self.character_select_text_id)
            self.character_select_text_id = None
        if self.smash_bros_text_id:
            self.canvas.delete(self.smash_bros_text_id)
            self.smash_bros_text_id = None
        if self.minecraft_text_id:
            self.canvas.delete(self.minecraft_text_id)
            self.minecraft_text_id = None
        for text_id in self.mods_text_ids:
            self.canvas.delete(text_id)
        self.mods_text_ids.clear()

    def hide_all_frames(self):
        self.home_frame.pack_forget()
        self.mods_frame.pack_forget()
        self.rom_hack_frame.pack_forget()

    def open_minecraft_file(self, event):
        # Exécuter le fichier Python dans le dossier MODS
        subprocess.Popen(["python", "Menu/MODS/minecraft.py"], shell=True)
    
    def open_mod_file(self, file):
        # Exécuter le fichier Python spécifié
        subprocess.Popen(["python", file], shell=True)

    def character_select_clicked(self, event):
        # Fonction à appeler lors du clic sur "Character Select"
        subprocess.Popen(["python", "Menu/API/cs.py"], shell=True)
    
    def smash_bros_clicked(self, event):
        # Fonction à appeler lors du clic sur "Super Smash Bros"
        subprocess.Popen(["python", "Menu/API/ssb.py"], shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
