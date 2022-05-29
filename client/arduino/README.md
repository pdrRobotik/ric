# Arduino AccessNode Bibliothek


## Verwendung
Mit der Bibliothek kann *ein* Verbindung zu dem Serial Interface vom **Robotik InterConnect / MDSN** aufgebaut werden. Und Nachricht ausgetauscht werden.\
  \
Das erste Beispiel initialisiert die Verbindung zum SerialInterface mit dem Namen **"ExampleName"**.\
Und verschickt die Nachricht **"Hallo Welt!"** and die Ziel Node **"test"** in der Ziel Gruppe **"testGruppe"**.
```cpp
#include <AccessNode.h>

RobotikInterConnect* ric;

void setup() {
    ric = new RobotikInterConnect("ExampleName");
}

void loop() {
    ric->send("test","testGruppe","Hallo Welt!"); 
}
```