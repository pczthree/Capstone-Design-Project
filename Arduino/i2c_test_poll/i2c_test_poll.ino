#include <Wire.h>

#define SLAVE_ADDRESS 0x05
int state = 0;

int randNum = 0;
int randNum1 = 0;
int randNum2 = 0;
int index = 0;
String dataString = " ";
uint8_t nums[2];

byte n[1000];

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData2);
  
  Serial.println("Ready!");
}

void loop() {
  nums[0] = random(256);
  nums[1] = random(256);
  randNum = random(256);
  //Serial.println(dataString.length());
  //byte *point = makeByteArray(dataString);
  //for (int i = 0; i <= dataString.length(); i++) Serial.println(*(point + i));
  //Serial.println();
  //Serial.println("");
  //Serial.print("\r" + dataString);
  delay(1000);
}

// callback for received data
void receiveData(int byteCount){
  bool shouldReset = Wire.read();
  if (shouldReset == 1) index = 0;
}
  
// callback for sending data
void sendData(){
  //Serial.println("Request recieved. Sending:");
  int len = dataString.length() + 1;     /* obtain length of string w/ terminator */
  char ascii_num[len];               /* create character array */

  dataString.toCharArray(ascii_num, len); /* copy string to character array */

  for (int i=0; i < len; ++i){
    Wire.write(ascii_num[i]);
    //Serial.println(ascii_num[i]);
  }
  Wire.write(',');
}

void sendData1(){
  Wire.write(nums[index]);
  index++;
  if (index >= 2) index = 0;
  
}

void sendData2()
{
  String outString = buildString();
  //int len = outString.length() + 1;
  //if (index == 0) *byte_nums = makeByteArray(dataString);
  if (index == 0) buildByteArray(outString);
  //byte toWrite = *byte_nums;
  byte toWrite = n[index];
  //Serial.println(toWrite);
  Wire.write(toWrite);
  index++;
  /*
  if (index >= len)
  {
    index = 0;
    Wire.write(',');
  }
  */
}

byte * makeByteArray(String s)
{
  byte n[1000];
  s.getBytes(n, 1000);
  return n;
}

void buildByteArray(String s)
{
  s.getBytes(n, 1000);
}

String buildString()
{
  return "Your number is: " + String(randNum);
}

