#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <Servo.h>
#include <Wire.h>
#include <math.h>

const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int out_elev = 3;

int print_count = 0;
int print_count_ = 200;

double pitch = 0.0;
double pitch_ = 0.0;
double pos = 0;
double theta = 0;

float deadband = 3.0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);

Servo elev;

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
}

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
  initSensors();
  
}

void loop() {
  
  sensors_event_t accel_event;
  sensors_vec_t   orientation;
  
  /* Calculate pitch and roll from the raw accelerometer data */
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    /* 'orientation' should have valid .pitch fields */
    
    pitch = orientation.pitch;
    if (abs(pitch - pitch_) > deadband)
      pitch_ = pitch;

    theta = 0.5*pitch_ + 90.0;
      
    elev.write((int)theta);
    
  }
  
  if (print_count == print_count_)
  {
    Serial.print(F("\rPitch: "));
    Serial.print((int)pitch_);
    Serial.print(F(";  theta: "));
    Serial.print((int)theta);
    Serial.print("    ");
    print_count = 0;
    
  }
  print_count++;
  
}
