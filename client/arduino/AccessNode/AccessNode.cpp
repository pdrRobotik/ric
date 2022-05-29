#include "Arduino.h"
#include "AccessNode.h"

/**
 * @brief Initialisiert die Kommunikation zum SerialInterface.
 * 
 * @param name der Node Name mit dem sich beim SerialInterface registriert wird.
 */
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

/**
 * @brief Empfängt eine Nachricht. Wartet bis es eine Nachricht gibt.
 * 
 * @return String mit der gelesen Nachricht.
 */
String RobotikInterConnect::read_wait() {
  Serial.print(">@"); //Request Message with Wait

  while (Serial.available() == 0) delay(2);

  return Serial.readStringUntil('\n');
}

/**
 * @brief Empfängt eine Nachricht ohne zu wärten. -> wenn keine Nachricht bereit steht, wird "" gegeben.
 * 
 * @return String mit der gelesen Nachricht. Leer wenn es keine Nachricht gab.
 */
String RobotikInterConnect::read() { //Empty String if no message is waiting
  Serial.print(":@"); //Request Message

  return Serial.readStringUntil('\n');
}

/**
 * @brief Überprüft ob es eine Nachricht zum lesen gibt.
 * 
 * @return true, wenn es mindestens eine Nachricht zum lesen gibt, sonst false.
 */
bool RobotikInterConnect::hasData() {
  Serial.print("@@");
  bool result = Serial.parseInt() > 0;
  Serial.readStringUntil('\n');
  return result;
}

/**
 * @brief Schickt eine Nachricht an ein Empfänger.
 * 
 * @param target Die Ziel-Node an die, die Nachricht geschickt werden soll.
 * @param targetgroup Die Gruppe in der die Zeil-Node ist.
 * @param msg Die Nachricht die an die Ziel-Node geschickt werden soll.
 */
void RobotikInterConnect::send(String target,String targetgroup,String msg) {
  Serial.print("@:"); //Send Message

  Serial.print(target);
  Serial.print("@");
  Serial.print(targetgroup);
  Serial.print(":");
  Serial.print(msg);
  Serial.print("\n");
}