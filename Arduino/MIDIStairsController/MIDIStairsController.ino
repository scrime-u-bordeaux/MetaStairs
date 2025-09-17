#define NB_OF_KEYS 9
#define MIDI_OUT_CHANNEL 1
// #define DEBUG 1

#include "PressureToNoteEvents.h"

struct noteGenData {
  uint8_t analogInput;
  uint8_t note;
  float processed = 0.f;
};

noteGenData noteGeneratorsData[NB_OF_KEYS] = {
  // { A0, 0 },
  { A1, 1 },
  { A2, 2 },
  { A3, 3 },
  { A4, 4 },
  { A5, 5 },
  { A6, 6 },
  { A7, 7 },
  { A8, 8 },
  { A9, 9 }
};

class MidiNotesSender : public PressureToNoteEvents::Listener {
  virtual void onNoteEvent(uint8_t note, uint8_t velocity) {
    if (velocity > 0) {
      usbMIDI.sendNoteOn(note, velocity, MIDI_OUT_CHANNEL);
    } else {
      usbMIDI.sendNoteOff(note, 0, MIDI_OUT_CHANNEL);
    }
  }
};

MidiNotesSender midiNotesSender;
PressureToNoteEvents* noteGenerators[NB_OF_KEYS];
bool calibrating = true;
uint64_t startDate = millis();

void setup() {
#ifdef DEBUG
  Serial.begin(115200);
#endif

  for (auto i = 0; i < NB_OF_KEYS; ++i) {
    noteGenerators[i] = new PressureToNoteEvents(noteGeneratorsData[i].note);
    noteGenerators[i]->setCalibrating(true);
    noteGenerators[i]->setListener(&midiNotesSender);
  }

  digitalWrite(13, HIGH); // set the LED on

  startDate = millis();
}

void loop() {
  if (calibrating && startDate - millis() > 3000) {
    calibrating = false;
    for (auto gen : noteGenerators) {
      gen->setCalibrating(false);
      Serial.println(gen->minValue);
    }
    Serial.println("stop calibrating");
  }

  float value;
  for (auto i = 0; i < NB_OF_KEYS; ++i) {
    value = analogRead(noteGeneratorsData[i].analogInput) / 1024.f;
    noteGeneratorsData[i].processed = noteGenerators[i]->process(value);
  }
  
#ifdef DEBUG
  for (const auto data& : noteGeneratorsData) {
    Serial.print(data.processed);
    Serial.print(",");
  }
  Serial.println("0,1");
#endif

  while (usbMIDI.read()) {
    // manage modes here according to MIDI input,
    // e.g enter thresh calibration mode on some NOTE ON event
  }

  delay(1);
}
