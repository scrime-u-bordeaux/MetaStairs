#include "PressureToNoteEvents.h"

#define NB_OF_KEYS 9
#define MIDI_OUT_CHANNEL 1

struct noteGenData {
  uint8_t analogInput;
  uint8_t note;
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

void setup() {
  Serial.begin(115200);
  for (auto i = 0; i < NB_OF_KEYS; ++i) {
    noteGenerators[i] = new PressureToNoteEvents(noteGeneratorsData[i].note);
    noteGenerators[i]->setListener(&midiNotesSender);
  }

  digitalWrite(13, HIGH); // set the LED on
}

void loop() {
  // fix display bounds to [0,1]
  // Serial.print(",0,1");
  // Serial.println();

  float value;
  for (auto i = 0; i < NB_OF_KEYS; ++i) {
    value = analogRead(noteGeneratorsData[i].analogInput) / 1024.f;
    // if (i == 0) {
    //   Serial.println(value);
    // }
    noteGenerators[i]->process(value);
  }

  while (usbMIDI.read()) {
    // manage modes here according to MIDI input,
    // e.g enter thresh calibration mode on some NOTE ON event
  }

  delay(1);
}
