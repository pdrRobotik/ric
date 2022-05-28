#ifndef ACCESSNODE_H
#define ACCESSNODE_H

#include "Arduino.h"

extern char in_buffer[21];
extern bool i_c;

void setupNode(const char* stpStr) ;
void syncStream();
void setOutput(const char* target, const char* targetgroup, const char* message) ;

#endif
