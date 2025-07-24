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
process = None

print("Heure de démarrage :", datetime.now().strftime("%H:%M:%S"))

def lancer_script(idx):
    script = modes.get(idx)
    if not script:
        print(f"Script {idx} non trouvé.")
        return None
    print(f"[{datetime.now().strftime('%H:%M:%S')}] → Lancement de : {script}")
    try:
        return subprocess.Popen(["python3", script])
    except Exception as e:
        print(f"Erreur au lancement de {script} : {e}")
        return None

try:
    process = lancer_script(idx)

    while True:
        time.sleep(0.1)

        for key in ['1', '2', '3']:
            if keyboard.is_pressed(key):
                new_idx = int(key)
                if new_idx != idx:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] → Changement de mode demandé : {key}")

                    # Stop le processus actuel
                    if process and process.poll() is None:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] → Interruption de : {modes[idx]}")
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            print("Forçage de l'arrêt...")
                            process.kill()

                    # Démarre le nouveau mode
                    idx = new_idx
                    process = lancer_script(idx)

                break  # évite de capter plusieurs touches à la fois

except KeyboardInterrupt:
    print("\nArrêt manuel.")
finally:
    if process and process.poll() is None:
        process.terminate()
    print("Fin de l'interaction")
