#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <Wire.h>
#include <Servo.h>
#include <math.h>

Servo pitch;
Servo roll;
Servo yaw;

//INTERFACE INFO:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
int buttonState = 0;         // variable for reading the pushbutton status

//COMS INFO:
//#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;
int print_count = 0;
int print_count_ = 200;
String out = "";
String fixdata = "";


//GPS INFO:
SoftwareSerial gpsSerial(9, 8);
Adafruit_GPS GPS(&gpsSerial);
boolean usingInterrupt = true;

//GYRO/ACCEL INFO:
double pitcho = 0.0;
double yawo = 0;
double rollo = 0;
double pos = 0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);


void receiveData(int byteCount) {

  while (Wire.available()) {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);

    if (number == 1) {

      if (state == 0) {
        digitalWrite(13, HIGH); // set the LED on
        state = 1;
      }
      else {
        digitalWrite(13, LOW); // set the LED off
        state = 0;
      }
    }
  }
}

void sendData() {
  Wire.write(build());
}

void setup() {
  pitcho.attach(3);
  rollo.attach(5);
  yawo.attach(6);
  // initialize serial coms
  Serial.begin(115200);   // initialize i2c as slave

  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);


  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  delay(1000);
  initSensors();
}

void initSensors()
{
  if (!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while (1);
  }
  if (!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while (1);
  }
}

uint32_t timer = millis();

void loop() {           //MAIN LOOP
  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
  if (timer > millis())  timer = millis();

  if (millis() - timer > 50) {
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
    Serial.println(build());
    pitcho.write((pitch+180)/2);
    rollo.write((roll+180)/2);
    yawo.write(yaw/2);
  }

}
