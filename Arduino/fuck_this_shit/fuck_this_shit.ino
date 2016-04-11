#include <Adafruit_GPS.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_9DOF.h>
#include <math.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x05
int randNum = 0;
int index = 0;

byte n[32];

String fixdata = "";

uint32_t timer = millis();

//GPS INFO:
Adafruit_GPS GPS(&Serial);
//boolean usingInterrupt = true;

//GYRO/ACCEL INFO:
double pitch = 0.0;
double yaw = 0;
double roll = 0;
double pos = 0;

Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);

void setup()
{
  pinMode(13, OUTPUT);
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate

  initSensors();
}

void initSensors(){}

void loop() {           //MAIN LOOP
  char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
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
  }
  
  
  randNum = random(10);
  //String s = build();
  //Serial.println(strlen(buildString().c_str()));
  //Serial.println(sizeof(s));
  delay(100);
}

void receiveData(int byteCount)
{
  bool shouldReset = Wire.read();
  if (shouldReset == 1) index = 0;
}

void sendData2()
{
  //if (index == 0) buildByteArray(buildString());
  //Wire.write(n[index]);
  Wire.write(buildString().c_str());
  //index++;
}

void buildByteArray2(String s)
{
  //memset(n, 0, sizeof(n));
  //s.toCharArray(n, 1000);
}

String buildString()
{
  return String(pitch);
}

void buildString2()
{
  //memset(n, 0, sizeof(n));
  //String s = build();
  //strncpy(n, "hello ", sizeof(n));
}

String build()
{
  if (GPS.fix)
  {
    fixdata = String(GPS.latitudeDegrees), +',' + String(GPS.longitudeDegrees) + ',' + String(GPS.speed) + ',' + String(GPS.altitude);
  }
  else
  {
    fixdata = ("0,0,0,0");
  }
  return String(pitch) + ',' + String(roll) + ',' + String(yaw) + ',' + String(GPS.hour) + ',' + String(GPS.minute) + ',' + String(GPS.seconds) + ',' + fixdata;

}

//=======================================================
void sendData()
{
  if (index == 0) buildByteArray(buildString());
  Wire.write(n[index]);
  index++;
}

void buildByteArray(String s)
{
  s.getBytes(n, 32);
}

