String inputString = "";         
boolean stringComplete = false;
int iki = 2;
int dort = 4;
int alti = 6;
int sekiz = 8;
void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  pinMode(iki, OUTPUT);
  pinMode(dort, OUTPUT);
  pinMode(alti, OUTPUT);
  pinMode(sekiz, OUTPUT);
}

void loop() {
  if (stringComplete) {
    Serial.println(inputString); 
    inputString = "";
    stringComplete = false;
    digitalWrite(iki, LOW);
    digitalWrite(dort, LOW);
    digitalWrite(alti, LOW);
    digitalWrite(sekiz, LOW);
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    inputString += inChar;
    if (inChar == '2') {
      stringComplete = true;
      digitalWrite(iki, LOW);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, HIGH);
      digitalWrite(alti, HIGH);
      digitalWrite(sekiz, HIGH);
      delay(30);               // wait for a second
    }
    if (inChar == '4')
    {
      stringComplete = true;
      digitalWrite(iki, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, LOW);
      digitalWrite(alti, HIGH);
      digitalWrite(sekiz, HIGH);
      delay(30);               // wait for a second
    }
   if (inChar == '6')
    {
      stringComplete = true;
      digitalWrite(iki, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, HIGH);
      digitalWrite(alti, LOW);
      digitalWrite(sekiz, HIGH);
      delay(30);               // wait for a second
    } 
    if (inChar == '8')
    {
      stringComplete = true;
      digitalWrite(iki, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, HIGH);
      digitalWrite(alti, HIGH);
      digitalWrite(sekiz, LOW);      
      delay(30);               // wait for a second
    }
    
    if (inChar == 'q')
    {
      stringComplete = true;
      digitalWrite(iki, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(alti, HIGH);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(sekiz, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100);               // wait for a second
    }
    if (inChar == 'w')
    {
      stringComplete = true;
      digitalWrite(iki, LOW);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(dort, LOW);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(alti, LOW);   // turn the LED on (HIGH is the voltage level)
      digitalWrite(sekiz, LOW);   // turn the LED on (HIGH is the voltage level)
      delay(100);               // wait for a second
    }
  }
}


