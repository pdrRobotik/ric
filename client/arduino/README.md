# Arduino AccessNode Bibliothek


## Verwendung
Mit der Bibliothek kann *ein* Verbindung zu dem Serial Interface vom **Robotik InterConnect / MDSN** aufgebaut werden. Und Nachricht ausgetauscht werden.\
  \
Das Beispiel initialisiert die Verbindung zum SerialInterface mit dem Namen **"ExampleName"**\
und verschickt die Nachricht **"Hallo Welt!"** an die Ziel-Node **"test"** in der Ziel-Gruppe **"testGruppe"** alle 0,1 Sekunden.
```cpp
#include <AccessNode.h>

RobotikInterConnect* ric;

void setup() {
    ric = new RobotikInterConnect("ExampleName");
}

void loop() {
    ric->send("test","testGruppe","Hallo Welt!"); 

    delay(100);
}
```
  \
Dieses Beispiel wartet auf eine Nachricht.\
Sobald diese erhalten wurde wird diese an die Ziel-Node **"test"** in der Ziel-Gruppe **"testGruppe"** gesendet.\
Danach wird eine Millisekunde pausiert und wieder von neu angefangen.
```cpp
#include <AccessNode.h>

RobotikInterConnect* ric;

void setup() {
    ric = new RobotikInterConnect("ExampleName");
}

void loop() {
    ric->send("test","testGruppe",ric->read_wait());  

    delay(1);
}
```
  \
Dieses Beispiel überprüft ob es eine neue Nachricht gibt, wenn ja wird diese gelesen und an die Ziel-Node **"test"** in der Ziel-Gruppe **"testGruppe"** gesendet.\
Nach dem überprüfen (egal ob es eine Nachricht gab oder nicht) werden 10 Millisekunde pausiert und dann wieder überprüft.\
**Der gesamt Effekt ist ähnlich dem 2. Beispiel. Wenn möglich sollte so etwas aber wie oben umgesetzt werden**
```cpp
#include <AccessNode.h>

RobotikInterConnect* ric;

void setup() {
    ric = new RobotikInterConnect("ExampleName");
}

void loop() {
    if (ric->hasData()) {
        ric->send("test","testGruppe",ric->read());
    }

    delay(1);
}
```

## Referenz

### **RobotikInterConnect**  \
  \
Initialisiert die Kommunikation zum SerialInterface.\
**Parameter**\
`name` - der Node Name mit dem sich beim SerialInterface registriert wird.\
```cpp
RobotikInterConnect(String name)
```  
  
### **send**  
Schickt eine Nachricht an ein Empfänger.\
**Parameter**\
`target` - Die Ziel-Node an die, die Nachricht geschickt werden soll.\
`targetgroup` - Die Gruppe in der die Zeil-Node ist.\
`msg` - Die Nachricht die an die Ziel-Node geschickt werden soll.\
```cpp
void send(String target,String targetgroup,String msg)
```

```cpp
String read_wait()
```

```cpp
String read()
```

```cpp
bool hasData()
```