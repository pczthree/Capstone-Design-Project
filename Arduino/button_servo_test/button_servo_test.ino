#include <Servo.h>

const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int out_elev = 3;

Servo elev;

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

void initServos()
{
  elev.attach(out_elev);
    
}

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  // initialize serial coms
  Serial.begin(115200);
  
  initServos();
  
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    Serial.print("\rHIGH");
    elev.write(60);
  }
  else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
    Serial.print("\rLOW ");
    elev.write(70);
  }
}
