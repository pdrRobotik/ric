#include "Arduino.h"
#include "AccessNode.h"

RobotikInterConnect::RobotikInterConnect(String name) {
  Serial.setTimeout(1000); //Set Timeout to 1 Seconds

  Serial.begin(57600); //9600 - Safe Speed //115200 - Almost Fastest

  bool hello_not_Ok = true;
  while (hello_not_Ok) {
    delay(500); //Try Handshake every 5 Seconds
    Serial.print("hello\n");
    hello_not_Ok = Serial.readStringUntil('\n') != "hello";
  }
  
  Serial.print(name);
  Serial.print(":n\n");//NARROW ACCESSNODE
}

String RobotikInterConnect::read_wait() {
  Serial.print(">@"); //Request Message with Wait

  while (Serial.available() == 0) delay(2);

  return Serial.readStringUntil('\n');
}

String RobotikInterConnect::read() { //Empty String if no message is waiting
  Serial.print(":@"); //Request Message

  return Serial.readStringUntil('\n');
}

bool RobotikInterConnect::hasData() {
  Serial.print("@@");
  bool result = Serial.parseInt() > 0;
  Serial.readStringUntil('\n');
  return result;
}

void RobotikInterConnect::send(String target,String targetgroup,String msg) {
  Serial.print("@:"); //Send Message

  Serial.print(target);
  Serial.print("@");
  Serial.print(targetgroup);
  Serial.print(":");
  Serial.print(msg);
  Serial.print("\n");
}