import os
import requests
import zipfile
import tkinter as tk
from tkinter import messagebox

# URL du fichier ZIP
url = "https://archive.org/download/mods-sm64-coop/tough_boss-by%20EmilyEmmi.zip"

# Chemins
appdata_path = os.getenv('APPDATA')
if not appdata_path:
    raise EnvironmentError("La variable d'environnement APPDATA n'est pas définie.")

mods_path = os.path.join(appdata_path, 'sm64ex-coop', 'mods')
download_path = os.path.join(mods_path, 'tough_boss-by EmilyEmmi.zip')

def telecharger_zip():
    try:
        # Téléchargement du fichier ZIP
        print(f"Téléchargement de {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Vérifie si la requête a réussi
        
        # Crée le répertoire de destination s'il n'existe pas
        os.makedirs(mods_path, exist_ok=True)
        
        # Téléchargement en morceaux
        with open(download_path, 'wb') as f:
            total_size = int(response.headers.get('content-length', 0))
            print(f"Taille estimée du fichier : {total_size} octets")
            downloaded_size = 0
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    print(f"Téléchargé {downloaded_size} / {total_size} octets")
        
        if os.path.getsize(download_path) == total_size:
            print(f"Fichier ZIP téléchargé à {download_path}")
            return True
        else:
            print("Le fichier ZIP téléchargé semble incomplet.")
            os.remove(download_path)
            return False
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False

def extraire_zip():
    try:
        if os.path.exists(download_path):
            print(f"Décompression du fichier ZIP {download_path}...")
            with zipfile.ZipFile(download_path, 'r') as z:
                z.extractall(mods_path)
            print(f"Fichiers extraits dans {mods_path}")
            
            # Suppression du fichier ZIP après extraction
            os.remove(download_path)
            print(f"Fichier ZIP supprimé : {download_path}")
            return True
        else:
            print(f"Le fichier ZIP {download_path} n'existe pas pour l'extraction.")
            return False
    except zipfile.BadZipFile:
        print("Le fichier téléchargé n'est pas un fichier ZIP valide.")
        return False
    except Exception as e:
        print(f"Erreur lors de l'extraction ou de la suppression du fichier ZIP : {e}")
        return False

def afficher_notification():
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    messagebox.showinfo("Installation Terminée", "Mod is installed!")
    root.destroy()

def verifier_et_executer():
    if not os.path.exists(download_path):
        print(f"Le fichier ZIP {download_path} n'existe pas.")
        if telecharger_zip():
            if extraire_zip():
                afficher_notification()
            else:
                print("Impossible de décompresser le fichier ZIP.")
    else:
        print(f"Le fichier ZIP existe déjà à {download_path}.")
        if extraire_zip():
            afficher_notification()
        else:
            print("Erreur lors de la décompression du fichier ZIP.")

if __name__ == "__main__":
    verifier_et_executer()
