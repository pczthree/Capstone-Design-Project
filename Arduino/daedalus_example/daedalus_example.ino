#include <Wire.h>
#include <L3G.h>
#include <PWM.h>

int32_t frequency = 50; //Hz

byte radio_in_rudder = 53;
byte radio_in_elevator = 49;
byte radio_in_aileron = 45;
byte out_rudder = 3;
byte out_elevator = 5;
byte out_aileron = 2;

double rudder;
double elevator;
double aileron;
double value_rudder;
double value_elevator;
double value_aileron;

const float alpha1 = 0.0875;
const float alpha = 0.0875;

double fXg = 0;
double fYg = 0;
double fZg = 0;

double pitch, roll, Xg, Yg, Zg;

int count;

L3G gyro;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(100);
  
  if (!gyro.init())
  {
    Serial.println("Failed to autodetect gyro type!");
    while (1);
  }
InitTimersSafe();
  bool success = SetPinFrequencySafe(3,frequency);
  if(success){
    pinMode(13,OUTPUT);
    digitalWrite(13,HIGH);
  }
  
  pinMode(radio_in_rudder, INPUT);
  
  gyro.enableDefault();
}

void loop() {
  
  //Start Gyro
  

  //Low Pass Filter
  //fXg = (int)gyro.g.x * alpha + (fXg * (1.0 - alpha));
  //fYg = (int)gyro.g.y * alpha + (fYg * (1.0 - alpha));
 

  for (count = 0; count < 10000; count++)
  {
      gyro.read();
      fZg = (int)gyro.g.z * alpha + (fZg * (1.0 - alpha1));
      Serial.println(fZg);

      value_rudder = pulseIn(radio_in_rudder, HIGH);
      value_elevator = pulseIn(radio_in_elevator, HIGH);
      //value_aileron = pulseIn(radio_in_aileron, HIGH);
  
      rudder = (value_rudder/2000)*255;
      elevator = (value_elevator/2000)*255;
      //aileron = (value_aileron/2000)*255;
  
      if (fZg < 0){
      analogWrite(out_rudder, 135);
      analogWrite(out_elevator, 135);
      //analogWrite(out_aileron, 155);
      }

      else {
      analogWrite(out_rudder, 215);
      analogWrite(out_elevator, 215);
            }
      
      if(count == 9999)
      { 
          count = 0;
          fZg= 0; 
      }
  }
  
  //fZg = (int)gyro.g.z;
  //Roll & Pitch Equations
  //roll  = (atan2(-fYg, fZg)*180.0)/M_PI;
  //pitch = (atan2(fXg, sqrt(fYg*fYg + fZg*fZg))*180.0)/M_PI;

 
////////////////////////////////////////////////////////////////////
  
  //PWM Out
  //value_rudder = pulseIn(radio_in_rudder, HIGH);
  //value_elevator = pulseIn(radio_in_elevator, HIGH);
  //value_aileron = pulseIn(radio_in_aileron, HIGH);
  
  //rudder = (value_rudder/2000)*255;
  //elevator = (value_elevator/2000)*255;
  //aileron = (value_aileron/2000)*255;
  
  //if (fZg < 0){
    //analogWrite(out_rudder, 135);
    //analogWrite(out_elevator, 135);
    //analogWrite(out_aileron, 155);
 //}

 //else {
    //analogWrite(out_rudder, 215);
    //analogWrite(out_elevator, 215);
 //}
 //if (-1 < fZg < 1){
    //analogWrite(out_rudder, 215);
    //analogWrite(out_elevator, 215);
    //analogWrite(out_aileron, 215);
 //}

  ///if (fZg > 1){
    //analogWrite(out_rudder, 290);
    //analogWrite(out_elevator, 290);
    //analogWrite(out_aileron, 290);
  //}
 
}
