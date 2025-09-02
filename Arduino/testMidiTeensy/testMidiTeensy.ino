// const int fsrPin = A0;
const int threshold = 50;
bool wasPressed = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int fsrValue = analogRead(9);
  bool isPressed = fsrValue > threshold;

  if (isPressed && !wasPressed) {
    Serial.println("TOUCH");
  }

  wasPressed = isPressed;
  delay(10); // anti-rebond
}

