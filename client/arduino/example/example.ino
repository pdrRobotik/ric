#include <AccessNode.h>

RobotikInterConnect* ric;
int counter = 0;
bool isClicked = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(5,INPUT);

  digitalWrite(LED_BUILTIN, HIGH);
  
  ric = new RobotikInterConnect("test");
  
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  
  //ric->send("longTestPackageTarget","longTestPackageTargetGroup","longTestPackageMessageMessage"+String(counter));

  //counter++;
  
  //if (ric->hasData())
  //  ric->send("t","g",ric->read());
  
  ric->send("t","g",ric->read_wait());  

  /*if (HIGH == digitalRead(5)) {
    if (!isClicked) {
      ric->send("t","g","J");
      isClicked = true;
    }
  }
  else {
    isClicked = false;
  }*/
  
  delay(1);
}
