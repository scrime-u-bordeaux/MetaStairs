const int threshold = 700;

const int capteurs[4] = {9, 7, 3, 1};  // Pins analogiques A2 à A5
bool wasPressed[4] = {false, false, false, false};  // états précédents

void setup() {
  Serial.begin(38400);
}

void loop() {
  for (int i = 0; i < 4; i++) {
    int val = analogRead(capteurs[i]);
    Serial.print("analog ");
    Serial.print(capteurs[i]);
    Serial.print(" is: ");
    Serial.println(val);

    bool isPressed = val > threshold;

    if (isPressed && !wasPressed[i]) {
      Serial.print("TOUCH_");
      Serial.println(i + 1);  // TOUCH_1 à TOUCH_4
    }

    wasPressed[i] = isPressed;
  }

  delay(1);  // pause globale
}
