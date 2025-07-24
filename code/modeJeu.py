import time
import subprocess
from datetime import datetime

# Dictionnaire des scripts
modes = {
    1: "pianoNormal.py",
    2: "metastairsAccordAvecVolume.py",
    3: "finalShepard.py"
}

tempsMode = 30  # secondes
idx = 1

print("Heure de démarrage :", datetime.now().strftime("%H:%M:%S"))

process = None  # pour stocker le processus actif

try:
    while True:
        script = modes.get(idx)
        if script:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] → Lancement de : {script}")
            try:
                # Lance le script en arrière-plan
                process = subprocess.Popen(["python3", script])
            except Exception as e:
                print(f"Erreur au lancement de {script} : {e}")
        else:
            print(f"Script {idx} non trouve.")

        # Attend le temps imparti
        for i in range(tempsMode):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Mode actif : {script} | Temps restant : {tempsMode - i}s", end='\r')
            time.sleep(1)

        # Termine le processus s'il est encore en cours
        if process and process.poll() is None:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] → Interruption de : {script}")
            process.terminate()
            try:
                process.wait(timeout=5)  # attend sa fin proprement
            except subprocess.TimeoutExpired:
                print("Forçage de l'arrêt...")
                process.kill()

        # Passage au script suivant (circulaire)
        idx += 1
        if idx > len(modes):
            idx = 1
except KeyboardInterrupt:
    print("\nArret manuel.")
finally:
    print("Fin de l'interaction")