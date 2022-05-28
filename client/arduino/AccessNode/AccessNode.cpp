#include "Arduino.h"
#include "AccessNode.h"

/*char in_buffer[201] = {};
bool i_c = false;
byte ib_c = 0;
char out_buffer[401] = "";
char o_c = 'n';

void setupNode(const char* stpStr)  {
  Serial.begin(9600);
  while (Serial.available() == 0) delay(1);
  Serial.readBytes(in_buffer, 2);
  in_buffer[2] = '\0';
  
  Serial.print(stpStr);
  Serial.print('\n');
  
  in_buffer[200] = '\0';
}

void syncStream() {
    i_c = false;
    Serial.print(o_c);
    
    if (Serial.read() == 'y') { 
        ib_c = Serial.readBytesUntil('\n', in_buffer, 200);  i_c = true;
    }
    
    if (o_c == 'y') { 
      Serial.print(out_buffer);Serial.print('\n'); o_c = 'n'; 
    }
    
    if (ib_c < 200) in_buffer[ib_c] = '\0';
}

void setOutput(const char* target, const char* targetgroup, const char* message) {
    o_c = 'y';
    out_buffer[0] = '\0';
    strcat (out_buffer, target);
    strcat (out_buffer, "@");
    strcat (out_buffer, targetgroup);
    strcat (out_buffer, ":");
    strcat (out_buffer, message);
}*/



RobotikInterConnectNA::RobotikInterConnectNA(String name) {
  //Serial.setTimeout(1000); //Set Timeout to 1 Seconds

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