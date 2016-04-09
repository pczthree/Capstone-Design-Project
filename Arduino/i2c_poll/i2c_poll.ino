#include <Wire.h>

#define SLAVE_ADDRESS 0x05
int randNum = 0;
int index = 0;

byte n[1000];

void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  Serial.println("Ready!");
}

void loop()
{
  randNum = random(256);
  delay(1000);
}

void receiveData(int byteCount)
{
  bool shouldReset = Wire.read();
  if (shouldReset == 1) index = 0;
}

void sendData()
{
  if (index == 0) buildByteArray(buildString());
  Wire.write(n[index]);
  index++;
}

void buildByteArray(String s)
{
  s.getBytes(n, 1000);
}

String buildString()
{
  return "Your number is: " + String(randNum);
}

