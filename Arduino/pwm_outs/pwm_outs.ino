#include <SoftwareSerial.h>
#include <Adafruit_GPS.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <Servo.h>
#include <math.h>

Servo pitcho;
Servo rollo;
Servo yawo;


//COMS INFO:
//#define SLAVE_ADDRESS 0x04
String out = "";
String fixdata = "";


//GPS INFO:
SoftwareSerial gpsSerial(9, 8);
Adafruit_GPS GPS(&gpsSerial);
boolean usingInterrupt = true;

//GYRO/ACCEL INFO:
double pitch = 0.0;
double yaw = 0;
double roll = 0;
double pos = 0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);

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
void setup() {
  pitcho.attach(3);
  rollo.attach(5);
  yawo.attach(6);

  
  // initialize serial coms
  Serial.begin(115200);   // initialize i2c as slave


  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  delay(1000);
  initSensors();
}



uint32_t timer = millis();

void loop() {           //MAIN LOOP
  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
  if (timer > millis())  timer = millis();

  if (millis() - timer > 500) {
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
    pitcho.write((pitch+180)/2);
    rollo.write((roll+180)/2);
    yawo.write(yaw/2);
  }

}
