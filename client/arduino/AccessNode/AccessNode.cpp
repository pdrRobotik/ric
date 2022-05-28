#include "Arduino.h"
#include "AccessNode.h"

RobotikInterConnectNA::RobotikInterConnectNA(String name) {
  Serial.setTimeout(1000); //Set Timeout to 1 Seconds

  Serial.begin(9600);

  bool hello_not_Ok = true;
  while (hello_not_Ok) {
    delay(500); //Try Handshake every 5 Seconds
    Serial.print("hello\n");
    hello_not_Ok = Serial.readStringUntil('\n') != "hello";
  }
  
  Serial.print(name);
  Serial.print(":n\n");//NARROW ACCESSNODE
}

String RobotikInterConnectNA::read_wait() {
  while (Serial.available() == 0) delay(1); //Wait Until Data is avaliable

  return Serial.readStringUntil('\n');
}

String RobotikInterConnectNA::read() {
  return Serial.readStringUntil('\n');
}

bool RobotikInterConnectNA::hasData() {
  return Serial.available() > 0;
}

void RobotikInterConnectNA::send(String target,String targetgroup,String msg) {
  Serial.print(target);
  Serial.print("@");
  Serial.print(targetgroup);
  Serial.print(":");
  Serial.print(msg);
  Serial.print("\n");
}