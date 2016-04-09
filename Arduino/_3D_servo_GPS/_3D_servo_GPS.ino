#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <Servo.h>
#include <Wire.h>
#include <math.h>

SoftwareSerial gpsSerial(9, 8);
Adafruit_GPS GPS(&gpsSerial);

const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int out_elev = 3;      //number of pwmout for elevator
const int out_ail = 5;
const int out_rudd  = 6;

int print_count = 0;
int print_count_ = 200;

double pitch = 0.0;
double pitch_ = 0.0;
double yaw = 0;
double yaw_ = 0;
double roll = 0;
double roll_ = 0;
double pos = 0;
double ptheta = 0;
double rtheta = 0;
double ytheta = 0;
float pdeadband = 3.0;
float rdeadband = 3.0;
float ydeadband = 3.0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);

Servo elev;
Servo rudd;
Servo ail;

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

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

void initServos()
{
  elev.attach(out_elev);
  ail.attach(out_ail);
  rudd.attach(out_rudd);
}

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  // initialize serial coms
  Serial.begin(115200);
  GPS.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  delay(1000);
  initServos();
  initSensors();

}


void loop() {

  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_vec_t   orientation;
  // read data from the GPS
  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }

  /* Calculate pitch and roll from the raw accelerometer data */
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    /* 'orientation' should have valid .pitch fields */

    pitch = orientation.pitch;
    roll = orientation.roll;

    if (abs(pitch - pitch_) > pdeadband)
      pitch_ = pitch;

    if (abs(roll - roll_) > rdeadband)
      roll_ = roll;

    ptheta = 0.5 * pitch_ + 90.0;
    rtheta = 0.5 * roll_ + 90;


    elev.write((int)ptheta); //acceptable degree range from 0 to 180
    ail.write((int)rtheta);

  }
  mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    /* 'orientation' should have valid .heading data now */
    yaw = orientation.heading;
    if (abs(yaw - yaw_) > ydeadband)
      yaw_ = yaw;

    ytheta = 0.5 * yaw_ + 90;
    rudd.write((int)ytheta);
  }
  if (print_count == print_count_)
  {
    
    Serial.print(F("\rPitch: "));
    Serial.print((int)pitch_);
    Serial.print(F(";  ptheta: "));
    Serial.print((int)ptheta);
    Serial.print("    ");
    Serial.print(F("Roll: "));
    Serial.print((int)roll_);
    Serial.print(F(";  rtheta: "));
    Serial.print((int)rtheta);
    Serial.print("    ");
    Serial.print(F("Yaw: "));
    Serial.print((int)yaw_);
    Serial.print(F(";  ytheta: "));
    Serial.print((int)ytheta);
    Serial.print("    ");
    Serial.print("Time: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.print(GPS.milliseconds);
    print_count = 0;

  }
  print_count++;

}
