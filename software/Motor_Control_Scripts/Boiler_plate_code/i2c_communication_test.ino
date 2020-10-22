/*

  This code is run on Arduino.

  Boiler plate code that Connects Raspberry Pi via I2C to Arduino

  Resources: 
  DroneBot Workshop 2019
  https://dronebotworkshop.com

*/

// Include the Wire library for I2C
#include <Wire.h>

// LED on pin 13z
const int ledPin = 13; 

void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(9600);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    digitalWrite(ledPin, c);
    Serial.println("communication received");
  }
}
void loop() {
  delay(100);
}