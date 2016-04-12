//#include <Adafruit_GPS.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <math.h>
//#include <SoftwareSerial.h>
//#include <Wire.h>

//INTERFACE INFO:
//const int buttonPin = 2;     // the number of the pushbutton pin
//const int ledPin =  13;      // the number of the LED pin
//int buttonState = 0;         // variable for reading the pushbutton status

//COMS INFO:
//#define SLAVE_ADDRESS 0x05
int number = 0;
int state = 0;
int print_count = 0;
int print_count_ = 200;
String out = "";
//String fixdata = "";


//GPS INFO:
//SoftwareSerial gpsSerial(9, 8);
//Adafruit_GPS GPS(&gpsSerial);
//boolean usingInterrupt = true;

//GYRO/ACCEL INFO:
double pitch = 0.0;
double yaw = 0;
double roll = 0;
double pos = 0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);


String build()
{
//  if (GPS.fix)
//  {
//    fixdata = String(GPS.latitudeDegrees), +',' + String(GPS.longitudeDegrees) + ',' + String(GPS.speed) + ',' + String(GPS.altitude);
//  }
//  else
//  {
//    fixdata = ("0,0,0,0");
//  }
  out = String(pitch) + ',' + String(roll) + ',' + String(yaw);// + ',' + String(GPS.hour) + ',' + String(GPS.minute) + ',' + String(GPS.seconds) + ',' + fixdata;

  return out;
}

//void receiveData(int byteCount) {
//
//  while (Wire.available()) {
//    number = Wire.read();
//    Serial.print("data received: ");
//    Serial.println(number);
//
//    if (number == 1) {
//
//      if (state == 0) {
//        digitalWrite(13, HIGH); // set the LED on
//        state = 1;
//      }
//      else {
//        digitalWrite(13, LOW); // set the LED off
//        state = 0;
//      }
//    }
//  }
//}
//
//void sendData() {
//  //Wire.write(build());
//}

void setup() {
//  // initialize the LED pin as an output:
//  pinMode(ledPin, OUTPUT);
//  // initialize the pushbutton pin as an input:
//  pinMode(buttonPin, INPUT);
//  // initialize serial coms
Serial.begin(9600);   
//
//  Wire.begin(SLAVE_ADDRESS);
//  // define callbacks for i2c communication
//  Wire.onReceive(receiveData);
//  Wire.onRequest(sendData);


//  GPS.begin(9600);
//  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
//  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  delay(1000);
  initSensors();
}

void initSensors()
{
  if (!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    //Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while (1);
  }
  if (!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    //Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while (1);
  }
}

uint32_t timer = millis();

void loop() {           //MAIN LOOP
//  char c = GPS.read();
//  if (GPS.newNMEAreceived()) {
//    if (!GPS.parse(GPS.lastNMEA()))
//      return;
//  }
  if (timer > millis())  timer = millis();

  if (millis() - timer > 100) {
    timer = millis(); // reset the timer
    sensors_event_t accel_event;
    sensors_event_t mag_event;
    sensors_vec_t   orientation;

    /* Calculate pitch and roll from the raw accelerometer data */
    accel.getEvent(&accel_event);
    if (dof.accelGetOrientation(&accel_event, &orientation))
    {
      pitch = orientation.pitch;
      roll = orientation.roll;
    }
    mag.getEvent(&mag_event);
    if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
    {
      yaw = orientation.heading;
    }
    Serial.print("\n" + build());
  }

}
