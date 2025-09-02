int val;
bool wasPressed = false;  
const int threshold = 800; 

void setup()
{                
  Serial.begin(38400);
}

void loop()                     
{
  val = analogRead(9);
  Serial.print("analog 9 is: ");
  Serial.println(val);

  bool isPressed = val > threshold;

  if (isPressed && !wasPressed) {
    Serial.println("TOUCH"); 
  }

  wasPressed = isPressed; 

  delay(50); 
}
