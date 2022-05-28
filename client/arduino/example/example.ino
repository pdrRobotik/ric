#include <AccessNode.h>

RobotikInterConnectNA* ric;
int counter = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  digitalWrite(LED_BUILTIN, HIGH);
  
  ric = new RobotikInterConnectNA("test");
  
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  
  //ric->send("longTestPackageTarget","longTestPackageTargetGroup","longTestPackageMessageMessage"+String(counter));

  //counter++;
  
  //if (ric->hasData())
  //  ric->send("t","g",ric->read());
  
  ric->send("t","g",ric->read_wait());
  

  
  delay(1);
}
