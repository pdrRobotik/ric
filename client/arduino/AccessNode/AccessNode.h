#ifndef ACCESSNODE_H
#define ACCESSNODE_H

#include "Arduino.h"

class RobotikInterConnectNA {
  public:
    RobotikInterConnectNA(String name);
    void send(String target,String targetgroup,String msg);

    String read_wait();
    String read(); //Read what is already available. Empty if nothing.
    bool hasData();
};

#endif
