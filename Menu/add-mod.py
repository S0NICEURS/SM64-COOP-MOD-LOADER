import os
import zipfile
import rarfile
import shutil
import ctypes
from tkinter import Tk
from tkinter.filedialog import askopenfilename

if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Fonction pour décompresser un fichier zip
def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Décompressé {zip_path} dans {extract_to}")
    except Exception as e:
        print(f"Erreur lors de la décompression du fichier zip : {e}")

# Fonction pour décompresser un fichier rar
def unrar_file(rar_path, extract_to):
    try:
        with rarfile.RarFile(rar_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
        print(f"Décompressé {rar_path} dans {extract_to}")
    except Exception as e:
        print(f"Erreur lors de la décompression du fichier rar : {e}")

# Fonction pour copier un fichier lua
def copy_lua_file(lua_path, destination_folder):
    try:
        shutil.copy(lua_path, destination_folder)
        print(f"Copié {lua_path} dans {destination_folder}")
    except Exception as e:
        print(f"Erreur lors de la copie du fichier lua : {e}")

# Fonction principale
def main():
    # Répertoire de destination
    destination_folder = os.path.join(os.getenv('APPDATA'), 'sm64ex-coop', 'mods')

    # Assurez-vous que le répertoire de destination existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Ouvrir la boîte de dialogue pour sélectionner un fichier
    Tk().withdraw()  # Cacher la fenêtre principale de Tkinter
    file_path = askopenfilename(filetypes=[("Fichiers zip, rar ou lua", "*.zip;*.rar;*.lua")])

    if not file_path:
        print("Aucun fichier sélectionné.")
        return

    # Vérifier l'extension du fichier et appeler la fonction appropriée
    if file_path.lower().endswith('.zip'):
        unzip_file(file_path, destination_folder)
    elif file_path.lower().endswith('.rar'):
        unrar_file(file_path, destination_folder)
    elif file_path.lower().endswith('.lua'):
        copy_lua_file(file_path, destination_folder)
    else:
        print("Type de fichier non supporté. Veuillez sélectionner un fichier .zip, .rar ou .lua.")

if __name__ == "__main__":
    main()

