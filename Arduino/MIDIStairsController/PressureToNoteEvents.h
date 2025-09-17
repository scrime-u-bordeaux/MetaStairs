#pragma once

#include "OnePole.h"

class PressureToNoteEvents {
public:
  /////////////////////////////////////////////////////////////////////////////
  // our variables                                                           //
  /////////////////////////////////////////////////////////////////////////////
  uint8_t note;
  OnePole filter;
  float prevValue;
  float prevDeltaValue;
  float peakDeltaValue;
  // absolute thresholds
  float lowThresh;
  float highThresh;
  // state 
  bool aboveLowThresh;
  bool on;

  /// for calibration :
  bool calibrating;
  float minValue;

public:
  /////////////////////////////////////////////////////////////////////////////
  // Listener class that should be passed to each instance                   //
  /////////////////////////////////////////////////////////////////////////////
  class Listener {
  public:
    Listener() {}
    ~Listener() {}
    virtual void onNoteEvent(uint8_t note, uint8_t velocity) = 0;
  };
  /////////////////////////////////////////////////////////////////////////////

private:
  Listener* listener;

public:
  PressureToNoteEvents(uint8_t n = 0) :
    note(n), prevValue(0), prevDeltaValue(0), peakDeltaValue(0),
    lowThresh(0.4), highThresh(0.6), on(false),
    calibrating(false), minValue(0)
  {
    filter.setCutoffFrequency(50);
    filter.setSamplingRate(1000); // read all analog inputs every 1 ms
  }
  ~PressureToNoteEvents() {}

  void setNote(uint8_t n) { note = n; }
  void setLowThresh(float t) { lowThresh = t; }
  void setHighThresh(float t) { highThresh = t; }

  void setCalibrating(bool c) {
    if (c && !calibrating) { minValue = 0; }
    calibrating = c;
  }

  void setListener(PressureToNoteEvents::Listener* l) {
    listener = l;
  }
  
  // we process a normalized pressure value ///////////////////////////////////
  float process(float v) {
    if (calibrating) {
      if (v > minValue) minValue = v;
    } else {
      v = (v - minValue) / (1 - minValue);
      v = v < 0 ? 0 : v;
    }

    float value = filter.process(v);

    float deltaValue = value - prevValue;

    // check if we are above lowThresh and eventually trig NOTE OFF ///////////
    if (prevValue < lowThresh && value >= lowThresh) {
      prevDeltaValue = 0;
      peakDeltaValue = 0;
      aboveLowThresh = true;
    } else if (prevValue >= lowThresh && value < lowThresh) {
      aboveLowThresh = false;
      if (on) {
        on = false;
        listener->onNoteEvent(note, 0);
      }
    }

    // if we are above lowThresh, update peakDeltaValue ///////////////////////
    if (aboveLowThresh && deltaValue > peakDeltaValue) {
      peakDeltaValue = deltaValue;
    }

    // if we meet conditions to trig NOTE ON, trig it and set "on" flag to ////
    // avoid repetitions //////////////////////////////////////////////////////
    // if all sensors work as expected :
    if (deltaValue < prevDeltaValue && value > highThresh) {
    // else
    // if (value > highThresh) {
      // we are decelerating so we can trig a note on
      if (!on) {
        // if all sensors work as expected :
        // here we compute the velocity from peakDeltaValue
        // we might want to configure this with sysex message ... (TBD)
        uint8_t velocity = map(peakDeltaValue * 1000, 0, 100, 64, 127);
        listener->onNoteEvent(note, constrain(velocity, 1, 127));
        // else
        // listener->onNoteEvent(note, 127);
        on = true;
      }
    }

    // update prevX vars //////////////////////////////////////////////////////
    prevValue = value;
    prevDeltaValue = deltaValue;
    return value;
  }
};