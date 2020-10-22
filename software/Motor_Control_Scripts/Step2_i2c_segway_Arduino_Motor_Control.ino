/*
  This code is run on Arduino.
  
  This code has been built with code logic from
  3 motor control code & i2c_test.ino code.

  How to run:
  This when run in conjuction with PyCamera code, keyboard inputs of 
  1 and 0 will enable the 3 motors to turn on and turn off. 
  
*/

// Include the Wire library for I2C
#include <Wire.h>

// LED on pin 13z
const int ledPin = 13; 
int enA = 9;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 3;
int in3 = 5;
int in4 = 4;
// Motor C connections
int enC = 10; //ena on 2nd driver - connected to PWM #6 on Arduino
int in5 = 11; //in1 on 2nd driver
int in6 = 12; //in2 on 2nd driver
int pwm = 255 ;
int delay_param1 = 1000;
int delay_param2 = 1000;

void setup() {

  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(enC, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(in5, OUTPUT);
  pinMode(in6, OUTPUT);
  
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Turn off motors - Initial state
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  digitalWrite(in5, LOW);
  digitalWrite(in6, LOW);

  Serial.begin(9600);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    Serial.println("communication received");
    char c = Wire.read(); // receive byte as a character
    if (c == 1) {
      three_motor_direction_control_func();
      digitalWrite(ledPin, c);

    }
    else if (c == 0){
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
        digitalWrite(in5, LOW);
        digitalWrite(in6, LOW);
        digitalWrite(ledPin, c);

    }

  }
}
void loop() {
  delay(100);
}

// This function lets you control spinning direction of motors
void three_motor_direction_control_func() {
  // Set motors to maximum speed
  // For PWM maximum possible values are 0 to 51: pwm
  digitalWrite(enA, pwm);
  digitalWrite(enB, pwm);
  digitalWrite(enC, pwm);

  // Turn on motor A & B & C
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  digitalWrite(in5, HIGH);
  digitalWrite(in6, LOW);
  delay(delay_param2);
  
  // Now change motor directions
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(in5, LOW);
  digitalWrite(in6, HIGH);
  delay(delay_param2);
  
}