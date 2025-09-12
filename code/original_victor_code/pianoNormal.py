import serial
import pygame
import time
import sys
import os
import csv
from datetime import datetime

# Configuration
threshold = 650 #seuil minimum
capteurs = ["TOUCH_1", "TOUCH_2", "TOUCH_3", "TOUCH_4", "TOUCH_5", "TOUCH_6", "TOUCH_7", "TOUCH_8", "TOUCH_9"]


note_assignment = {
    "TOUCH_1": 60,  # C4
    "TOUCH_2": 61,  # C#4 / Db4
    "TOUCH_3": 62,  # D4
    "TOUCH_4": 63,  # D#4 / Eb4
    "TOUCH_5": 64,  # E4
    "TOUCH_6": 65,  # F4
    "TOUCH_7": 66,  # F#4 / Gb4
    "TOUCH_8": 67,  # G4
    "TOUCH_9": 68   # G#4 / Ab4
}

# Fichier de log CSV
LOG_DIR = "logs"

if len(sys.argv) > 1:
    LOG_FILE = os.path.join(LOG_DIR, sys.argv[1])
else:
    LOG_FILE = os.path.join(LOG_DIR, "sensorLog_defaultName.csv")  # nom par défaut


was_pressed = {key: False for key in capteurs}
last_velocity = {key: 0 for key in capteurs}

# CSV helpers
def ensure_logfile():
    os.makedirs(LOG_DIR, exist_ok=True)
    need_header = not os.path.exists(LOG_FILE)
    if need_header:
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # En-tete : tu peux ajouter/retirer des colonnes si besoin
            writer.writerow(["timestamp", "event", "touche", "note", "volume", "sensor value"])

def log_event(event: str, touche: str, note: int | None, volume: float | None, raw_value: int | None):

    # event: "PRESS", "UPDATE", "RELEASE"
    # note/volume peuvent etre None sur certains evenements, mais ici on les remplit autant que possible.

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # millisecondes
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([ts, event, touche, "" if note is None else note, "" if volume is None else f"{volume:.4f}", "" if raw_value is None else raw_value])


# Init pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# Chargement des sons
note_wav_map = {
    60: pygame.mixer.Sound("./../../sons/samplespianowav/C4.wav"),   # C4
    61: pygame.mixer.Sound("./../../sons/samplespianowav/Db4.wav"),  # C#4 / Db4
    62: pygame.mixer.Sound("./../../sons/samplespianowav/D4.wav"),   # D4
    63: pygame.mixer.Sound("./../../sons/samplespianowav/Eb4.wav"),  # D#4 / Eb4
    64: pygame.mixer.Sound("./../../sons/samplespianowav/E4.wav"),   # E4
    65: pygame.mixer.Sound("./../../sons/samplespianowav/F4.wav"),   # F4
    66: pygame.mixer.Sound("./../../sons/samplespianowav/Gb4.wav"),  # F#4 / Gb4
    67: pygame.mixer.Sound("./../../sons/samplespianowav/G4.wav"),   # G4
    68: pygame.mixer.Sound("./../../sons/samplespianowav/Ab4.wav")   # G#4 / Ab4
}


ensure_logfile()

# Connexion serie
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
    print("Pret a detecter les pressions...")

    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if line.startswith("TOUCH_") and ":" in line:
                touche, val_str = line.split(":")
                val = int(val_str)
                
                if touche not in capteurs:
                    continue

                is_pressed = val > threshold
                velocity = int((val - threshold) / (850 - threshold) * 126) + 1
                velocity = min(max(velocity, 1), 127)
                volume = velocity / 127.0

                if is_pressed and not was_pressed[touche]:
                    note = note_assignment[touche]
                    if note in note_wav_map:
                        note_wav_map[note].stop()
                        note_wav_map[note].set_volume(volume)
                        note_wav_map[note].play()
                        print(f"[{touche}] Note {note} | Volume {volume:.2f}")
                        log_event("PRESS", touche, note, volume, val) ###
                        was_pressed[touche] = True
                        last_velocity[touche] = velocity

                elif is_pressed and was_pressed[touche] and velocity != last_velocity[touche]:
                    note = note_assignment[touche]
                    if note in note_wav_map:
                        note_wav_map[note].stop()
                        note_wav_map[note].set_volume(volume)
                        note_wav_map[note].play()
                        # print(f"[UPDATE] {touche} | Volume {volume:.2f}")
                        print(f"[{touche}] Note {note} | Volume {volume:.2f}")
                        log_event("UPDATE", touche, note, volume, val) ###
                        last_velocity[touche] = velocity

                elif not is_pressed and was_pressed[touche]:
                    print(f"[RELEASE] {touche}")
                    log_event("RELEASE", touche, note, 0.0, val) ###
                    was_pressed[touche] = False
                    last_velocity[touche] = 0

        except KeyboardInterrupt:
            print("\nArret manuel.")
            break
        except Exception as e:
            print("Erreur dans la boucle principale :", e)

except serial.SerialException as e:
    print(f"Erreur serie : {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Port serie ferme.")
