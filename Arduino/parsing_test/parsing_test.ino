#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(9, 8);


Adafruit_GPS GPS(&mySerial);

void setup()
{
  Serial.begin(115200);

  GPS.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);  //Turns on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  delay(1000);
}





uint32_t timer = millis();
void loop()              
{


  // read data from the GPS in the 'main loop'
 char c = GPS.read();
  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;  
  }

  if (timer > millis())  timer = millis();

  if (millis() - timer > 500) {
    timer = millis(); // reset the timer

    Serial.print("\n\rTime: ");
//    Serial.print(c);
  Serial.print(String(GPS.hour)+','+String(GPS.minute)+','+String(GPS.seconds));
//    Serial.print(GPS.hour, DEC); Serial.print(':');
//    Serial.print(GPS.minute, DEC); Serial.print(':');
//    Serial.print(GPS.seconds, DEC); Serial.print('.');
  }
}

