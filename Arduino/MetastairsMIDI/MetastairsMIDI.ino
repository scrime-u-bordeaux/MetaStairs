// #include <usbMIDI.h>
#include <Bounce.h>

const int threshold = 700;

const int capteurs[4] = {9, 7, 3, 1};
bool wasPressed[4] = {false, false, false, false};

// Canal MIDI utilisé
const int channel = 1;
const int cable = 0;

// Notes MIDI à jouer pour chaque capteur
const int notes[4] = {60, 62, 64, 65};  // C4, D4, E4, F4

void setup() {
  Serial.begin(38400);
  // Rien de spécial ici
}

void loop() {
  for (int i = 0; i < 4; i++) {
    int val = analogRead(capteurs[i]);
    Serial.print("analog ");
    Serial.print(capteurs[i]);
    Serial.print(" is: ");
    Serial.println(val);

    bool isPressed = val > threshold;

    // Nouvelle pression détectée
    if (isPressed && !wasPressed[i]) {
      Serial.print("TOUCH_");
      Serial.println(i + 1);  // TOUCH_1 à TOUCH_4
      usbMIDI.sendNoteOn(notes[i], 100, channel, cable);  // vélocité 100
      wasPressed[i] = true;
    }

    // Relâchement détecté
    if (!isPressed && wasPressed[i]) {
      usbMIDI.sendNoteOff(notes[i], 0, channel, cable);
      wasPressed[i] = false;
    }
  }

  // Ignore les messages MIDI entrants
  while (usbMIDI.read()) {}

  delay(1);
}
