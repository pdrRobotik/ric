#ifndef ACCESSNODE_H
#define ACCESSNODE_H

#include "Arduino.h"

/*extern char in_buffer[21];
extern bool i_c;

void setupNode(const char* stpStr) ;
void syncStream();
void setOutput(const char* target, const char* targetgroup, const char* message);*/

class RobotikInterConnectNA {
  public:
    RobotikInterConnectNA(String name);
    void send(String target,String targetgroup,String msg);

    String read_wait();
    String read(); //What is already available. Empty if nothing.
    bool hasData();
};

#endif
