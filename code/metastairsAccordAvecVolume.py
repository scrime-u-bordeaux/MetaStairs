import serial
import time
import pygame
import mido

# Configuration initiale
threshold = 650
capteurs = ["TOUCH_1", "TOUCH_2", "TOUCH_3", "TOUCH_4"]
was_pressed = [False] * 4
last_velocity = [0] * 4

# Initialisation de pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(128)

# Mapping note MIDI
note_wav_map = {
    21: pygame.mixer.Sound("./../sons/samplespianowav/A0.wav"),
    22: pygame.mixer.Sound("./../sons/samplespianowav/Bb0.wav"),
    23: pygame.mixer.Sound("./../sons/samplespianowav/B0.wav"),
    24: pygame.mixer.Sound("./../sons/samplespianowav/C1.wav"),
    25: pygame.mixer.Sound("./../sons/samplespianowav/Db1.wav"),
    26: pygame.mixer.Sound("./../sons/samplespianowav/D1.wav"),
    27: pygame.mixer.Sound("./../sons/samplespianowav/Eb1.wav"),
    28: pygame.mixer.Sound("./../sons/samplespianowav/E1.wav"),
    29: pygame.mixer.Sound("./../sons/samplespianowav/F1.wav"),
    30: pygame.mixer.Sound("./../sons/samplespianowav/Gb1.wav"),
    31: pygame.mixer.Sound("./../sons/samplespianowav/G1.wav"),
    32: pygame.mixer.Sound("./../sons/samplespianowav/Ab1.wav"),
    33: pygame.mixer.Sound("./../sons/samplespianowav/A1.wav"),
    34: pygame.mixer.Sound("./../sons/samplespianowav/Bb1.wav"),
    35: pygame.mixer.Sound("./../sons/samplespianowav/B1.wav"),
    36: pygame.mixer.Sound("./../sons/samplespianowav/C2.wav"),
    37: pygame.mixer.Sound("./../sons/samplespianowav/Db2.wav"),
    38: pygame.mixer.Sound("./../sons/samplespianowav/D2.wav"),
    39: pygame.mixer.Sound("./../sons/samplespianowav/Eb2.wav"),
    40: pygame.mixer.Sound("./../sons/samplespianowav/E2.wav"),
    41: pygame.mixer.Sound("./../sons/samplespianowav/F2.wav"),
    42: pygame.mixer.Sound("./../sons/samplespianowav/Gb2.wav"),
    43: pygame.mixer.Sound("./../sons/samplespianowav/G2.wav"),
    44: pygame.mixer.Sound("./../sons/samplespianowav/Ab2.wav"),
    45: pygame.mixer.Sound("./../sons/samplespianowav/A2.wav"),
    46: pygame.mixer.Sound("./../sons/samplespianowav/Bb2.wav"),
    47: pygame.mixer.Sound("./../sons/samplespianowav/B2.wav"),
    48: pygame.mixer.Sound("./../sons/samplespianowav/C3.wav"),
    49: pygame.mixer.Sound("./../sons/samplespianowav/Db3.wav"),
    50: pygame.mixer.Sound("./../sons/samplespianowav/D3.wav"),
    51: pygame.mixer.Sound("./../sons/samplespianowav/Eb3.wav"),
    52: pygame.mixer.Sound("./../sons/samplespianowav/E3.wav"),
    53: pygame.mixer.Sound("./../sons/samplespianowav/F3.wav"),
    54: pygame.mixer.Sound("./../sons/samplespianowav/Gb3.wav"),
    55: pygame.mixer.Sound("./../sons/samplespianowav/G3.wav"),
    56: pygame.mixer.Sound("./../sons/samplespianowav/Ab3.wav"),
    57: pygame.mixer.Sound("./../sons/samplespianowav/A3.wav"),
    58: pygame.mixer.Sound("./../sons/samplespianowav/Bb3.wav"),
    59: pygame.mixer.Sound("./../sons/samplespianowav/B3.wav"),
    60: pygame.mixer.Sound("./../sons/samplespianowav/C4.wav"),  # Do central
    61: pygame.mixer.Sound("./../sons/samplespianowav/Db4.wav"),
    62: pygame.mixer.Sound("./../sons/samplespianowav/D4.wav"),
    63: pygame.mixer.Sound("./../sons/samplespianowav/Eb4.wav"),
    64: pygame.mixer.Sound("./../sons/samplespianowav/E4.wav"),
    65: pygame.mixer.Sound("./../sons/samplespianowav/F4.wav"),
    66: pygame.mixer.Sound("./../sons/samplespianowav/Gb4.wav"),
    67: pygame.mixer.Sound("./../sons/samplespianowav/G4.wav"),
    68: pygame.mixer.Sound("./../sons/samplespianowav/Ab4.wav"),
    69: pygame.mixer.Sound("./../sons/samplespianowav/A4.wav"),
    70: pygame.mixer.Sound("./../sons/samplespianowav/Bb4.wav"),
    71: pygame.mixer.Sound("./../sons/samplespianowav/B4.wav"),
    72: pygame.mixer.Sound("./../sons/samplespianowav/C5.wav"),
    73: pygame.mixer.Sound("./../sons/samplespianowav/Db5.wav"),
    74: pygame.mixer.Sound("./../sons/samplespianowav/D5.wav"),
    75: pygame.mixer.Sound("./../sons/samplespianowav/Eb5.wav"),
    76: pygame.mixer.Sound("./../sons/samplespianowav/E5.wav"),
    77: pygame.mixer.Sound("./../sons/samplespianowav/F5.wav"),
    78: pygame.mixer.Sound("./../sons/samplespianowav/Gb5.wav"),
    79: pygame.mixer.Sound("./../sons/samplespianowav/G5.wav"),
    80: pygame.mixer.Sound("./../sons/samplespianowav/Ab5.wav"),
    81: pygame.mixer.Sound("./../sons/samplespianowav/A5.wav"),
    82: pygame.mixer.Sound("./../sons/samplespianowav/Bb5.wav"),
    83: pygame.mixer.Sound("./../sons/samplespianowav/B5.wav"),
    84: pygame.mixer.Sound("./../sons/samplespianowav/C6.wav"),
    85: pygame.mixer.Sound("./../sons/samplespianowav/Db6.wav"),
    86: pygame.mixer.Sound("./../sons/samplespianowav/D6.wav"),
    87: pygame.mixer.Sound("./../sons/samplespianowav/Eb6.wav"),
    88: pygame.mixer.Sound("./../sons/samplespianowav/E6.wav"),
    89: pygame.mixer.Sound("./../sons/samplespianowav/F6.wav"),
    90: pygame.mixer.Sound("./../sons/samplespianowav/Gb6.wav"),
    91: pygame.mixer.Sound("./../sons/samplespianowav/G6.wav"),
    92: pygame.mixer.Sound("./../sons/samplespianowav/Ab6.wav"),
    93: pygame.mixer.Sound("./../sons/samplespianowav/A6.wav"),
    94: pygame.mixer.Sound("./../sons/samplespianowav/Bb6.wav"),
    95: pygame.mixer.Sound("./../sons/samplespianowav/B6.wav"),
    96: pygame.mixer.Sound("./../sons/samplespianowav/C7.wav"),
    97: pygame.mixer.Sound("./../sons/samplespianowav/Db7.wav"),
    98: pygame.mixer.Sound("./../sons/samplespianowav/D7.wav"),
    99: pygame.mixer.Sound("./../sons/samplespianowav/Eb7.wav"),
    100: pygame.mixer.Sound("./../sons/samplespianowav/E7.wav"),
    101: pygame.mixer.Sound("./../sons/samplespianowav/F7.wav"),
    102: pygame.mixer.Sound("./../sons/samplespianowav/Gb7.wav"),
    103: pygame.mixer.Sound("./../sons/samplespianowav/G7.wav"),
    104: pygame.mixer.Sound("./../sons/samplespianowav/Ab7.wav"),
    105: pygame.mixer.Sound("./../sons/samplespianowav/A7.wav"),
    106: pygame.mixer.Sound("./../sons/samplespianowav/Bb7.wav"),
    107: pygame.mixer.Sound("./../sons/samplespianowav/B7.wav"),
    108: pygame.mixer.Sound("./../sons/samplespianowav/C8.wav")
}

# Chargement du fichier MIDI
# midi = mido.MidiFile("./../fichiers_midi/John Newman Love me again.mid.mid")
# midi = mido.MidiFile("./../fichiers_midi/Bad Bunny - Efecto.mid")
midi = mido.MidiFile("./../fichiers_midi/Bad Bunny - Efecto_no_drums.mid")


# Extraction des groupes de notes simultanees
events = []
absolute_time = 0.0
for msg in midi:
    absolute_time += msg.time
    if msg.type == "note_on" and msg.velocity > 0:
        events.append((absolute_time, msg.note))

note_groups = []
group = []
last_time = None
group_threshold = 0.02  # tolerance pour regroupement en secondes

for t, note in events:
    if last_time is None or abs(t - last_time) <= group_threshold:
        group.append(note)
    else:
        if group:
            note_groups.append(group)
        group = [note]
    last_time = t
if group:
    note_groups.append(group)

print("Groupes de notes MIDI charges :", note_groups)

# Connexion serie
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # 38400
time.sleep(2)
print("Pret. Touchez un capteur pour jouer un groupe de notes.")

index = 0  # index de groupe MIDI

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line.startswith("TOUCH_"):
            try:
                label, val_str = line.split(":")
                val = int(val_str)
                idx = capteurs.index(label)

                is_pressed = val > threshold
                velocity = int((val - threshold) / (850 - threshold) * 126) + 1
                velocity = min(max(velocity, 1), 127)
                volume = velocity / 127.0

                if is_pressed and not was_pressed[idx]:
                    group = note_groups[index]
                    print(f"[{label}] → Groupe {index+1}: {group} | Volume: {volume:.2f}")
                    print("valeur capteur :", val)
                    for note in group:
                        if note in note_wav_map:
                            note_wav_map[note].stop()
                            note_wav_map[note].set_volume(volume)
                            note_wav_map[note].play()
                        else:
                            print(f"Note {note} non trouvee.")
                    index += 1
                    if index >= len(note_groups):
                        print("Recommencer au debut.")
                        index = 0
                    was_pressed[idx] = True
                    last_velocity[idx] = velocity

                elif is_pressed and was_pressed[idx] and velocity != last_velocity[idx]:
                    group = note_groups[index - 1]  # rejoue le dernier groupe joue
                    print(f"[UPDATE & REPLAY] {label} | Volume: {volume:.2f}")
                    print("valeur capteur :", val)
                    for note in group:
                        if note in note_wav_map:
                            note_wav_map[note].stop()
                            note_wav_map[note].set_volume(volume)
                            note_wav_map[note].play()
                        else:
                            print(f"Note {note} non trouvee.")
                    index += 1
                    if index >= len(note_groups):
                        print("Recommencer au debut.")
                        index = 0
                    was_pressed[idx] = True
                    last_velocity[idx] = velocity

                elif not is_pressed and was_pressed[idx]:
                    was_pressed[idx] = False
                    last_velocity[idx] = 0
                    print(f"[RELEASE] {label}")

            except Exception as e:
                print("Erreur:", e)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("Arret manuel.")
finally:
    ser.close()
    print("Connexion serie fermee.")
