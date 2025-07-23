import serial
import pygame
import time

# Configuration
threshold = 650
capteurs = ["TOUCH_1", "TOUCH_2", "TOUCH_3", "TOUCH_4"]
note_assignment = {
    "TOUCH_1": 60,  # C4
    "TOUCH_2": 62,  # D4
    "TOUCH_3": 64,  # E4
    "TOUCH_4": 65   # F4
}
was_pressed = {key: False for key in capteurs}
last_velocity = {key: 0 for key in capteurs}

# Init pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

# Chargement des sons
note_wav_map = {
    60: pygame.mixer.Sound("./../sons/samplespianowav/C4.wav"),
    62: pygame.mixer.Sound("./../sons/samplespianowav/D4.wav"),
    64: pygame.mixer.Sound("./../sons/samplespianowav/E4.wav"),
    65: pygame.mixer.Sound("./../sons/samplespianowav/F4.wav")
}

# Connexion serie
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
    print("Pret à detecter les pressions...")

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
                        last_velocity[touche] = velocity

                elif not is_pressed and was_pressed[touche]:
                    print(f"[RELEASE] {touche}")
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
