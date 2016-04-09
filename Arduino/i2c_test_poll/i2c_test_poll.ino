#include <Wire.h>

#define SLAVE_ADDRESS 0x05
int number = 0;
int state = 0;

int randNum = 0;
int randNum1 = 0;
int randNum2 = 0;
int index = 0;
String dataString = " ";
uint8_t nums[2];


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
  dataString = "Your number is: " + String(randNum);
  Serial.println(dataString.length());
  char *point = makeCharArray(dataString);
  for (int i = 0; i <= dataString.length(); i++) Serial.print(*(point + i));
  Serial.println("");
  //Serial.print("\r" + dataString);
  delay(1000);
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);
  
    if (number == 1){
    
      if (state == 0){
        digitalWrite(13, HIGH); // set the LED on
        state = 1;
      }
      else{
        digitalWrite(13, LOW); // set the LED off
        state = 0;
      }
    }
  }
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
  char *byte_nums = 0;
  int len = dataString.length() + 1;
  if (index == 0) char *byte_nums = makeCharArray(dataString);
  
  Wire.write(*(byte_nums + index));
  index++;
  
  if (index >= len)
  {
    index = 0;
    Wire.write(',');
  }
}

char * makeCharArray(String s)
{
  char n[32];
  s.toCharArray(n, s.length()+1);
  return n;
}

