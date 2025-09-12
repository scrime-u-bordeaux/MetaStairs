#pragma once

// OnePole filter (thanks to EarLevel Engineering !)
class OnePole {
private:
  double cutoffFrequency;
  double samplingRate;
  float a0, b1, z1;

public:
  OnePole(double fc = 20, double sr = 100) :
  cutoffFrequency(fc), samplingRate(sr), z1(0) {
    updateCoefficients();
  }

  ~OnePole() {}

  void setSamplingRate(double sr) {
    samplingRate = sr;
    updateCoefficients();
  }

  void setCutoffFrequency(double fc) {
    cutoffFrequency = fc;
    updateCoefficients();
  }

  float process(float in) {
    z1 = in * a0 + z1 * b1;
    return z1;
  }

private:
  void updateCoefficients() {
    b1 = exp(-2.0 * M_PI * cutoffFrequency / samplingRate);
    a0 = 1.0 - b1;    
  }
};