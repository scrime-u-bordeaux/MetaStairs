import time
import subprocess
from datetime import datetime
import keyboard  # pip install keyboard

# Dictionnaire des scripts
modes = {
    1: "pianoNormal.py",
    2: "metastairsAccordAvecVolume.py",
    3: "finalShepard.py"
}

idx = 1
print("Appuie sur une touche pour changer de mode.")
print("Heure de demarrage :", datetime.now().strftime("%H:%M:%S"))

process = None  # pour stocker le processus actif

try:
    while True:
        script = modes.get(idx)
        if script:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] → Lancement de : {script}")
            try:
                process = subprocess.Popen(["python3", script])
            except Exception as e:
                print(f"Erreur au lancement de {script} : {e}")
        else:
            print(f"Script {idx} non trouve.")

        print("En cours : appuie sur une touche pour passer au mode suivant...")

        # Attente d'une touche clavier
        keyboard.read_event()

        # Termine le processus courant
        if process and process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] → Interruption de : {script}")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Forçage de l'arret...")
                process.kill()

        # Passage au script suivant
        idx = idx + 1 if idx < len(modes) else 1

except KeyboardInterrupt:
    print("\nArret manuel.")
finally:
    print("Fin de l’interaction.")
