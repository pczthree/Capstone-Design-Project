#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_9DOF.h>

/* Assign a unique ID to the sensors */
Adafruit_9DOF                 dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

float deadband = 1.0;

double roll = 0.0;
double pitch = 0.0;
double yaw = 0.0;

double roll_ = 0.0;
double pitch_ = 0.0;
double yaw_ = 0.0;

/**************************************************************************/
/*!
    @brief  Initialises all the sensors used by this example
*/
/**************************************************************************/
void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
}

/**************************************************************************/
/*!

*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  //Serial.println(F("Adafruit 9 DOF Pitch/Roll/Heading Example")); Serial.println("");
  
  /* Initialise the sensors */
  initSensors();
}

/**************************************************************************/
/*!
    @brief  Constantly check the roll/pitch/heading/altitude/temperature
*/
/**************************************************************************/
void loop(void)
{
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_vec_t   orientation;
  

  /* Calculate pitch and roll from the raw accelerometer data */
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    /* 'orientation' should have valid .roll and .pitch fields */
    roll = orientation.roll;
    pitch = orientation.pitch;
    
    if (abs(roll - roll_) > deadband)
    {
      Serial.print(F("Roll: "));
      Serial.print(roll);
      Serial.print(F("; "));

      roll_ = roll;
    }
    else
    {
      Serial.print(F("Roll: "));
      Serial.print(roll_);
      Serial.print(F("; "));
    }

    if (abs(pitch - pitch_) > deadband)
    {
      Serial.print(F("Pitch: "));
      Serial.print(pitch);
      Serial.print(F("; "));

      pitch_ = pitch;
    }
    else
    {
      Serial.print(F("Pitch: "));
      Serial.print(pitch_);
      Serial.print(F("; "));
    }
  }
  
  /* Calculate the heading using the magnetometer */
  mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    /* 'orientation' should have valid .heading data now */
    
    yaw = orientation.heading;
    if (abs(yaw - yaw_) > deadband)
    {
      Serial.print(F("Heading: "));
      Serial.print(yaw);
      Serial.print(F("; "));

      yaw_ = yaw;
    }
    else
    {
      Serial.print(F("Heading: "));
      Serial.print(yaw);
      Serial.print(F("; "));
    }
  }

  Serial.print(F("\r"));
  Serial.flush();
  //delay(1000);
}
