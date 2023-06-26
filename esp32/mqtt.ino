#include <Ethernet.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <ESP32Ping.h>


byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};  // MAC address
IPAddress ip(10, 9, 0, 36);  // IP address que o esp32 irá assumir
EthernetClient ethClient;


////////////MQTT RELATED
const char* mqtt_server = "10.9.0.35"; // MQTT broker/server IP address
const char* mqttTopic = "pi2"; //topico do mqtt
const int mqttPort = 1883; //porta do mqtt
 
PubSubClient client(ethClient);

void setup() {
  Serial.begin(115200);
  pinMode(15, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(21, OUTPUT); //rele 
 
  setup_ethernet();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_ethernet() {
  Serial.println("Begin Ethernet");

  Ethernet.init(5); 
  if (Ethernet.begin(mac)) { // Dynamic IP setup
    Serial.println("DHCP OK!");
  } else {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
    }
  }
  delay(5000);


  Serial.print("Local IP : ");
  Serial.println(Ethernet.localIP());
  Serial.print("Subnet Mask : ");
  Serial.println(Ethernet.subnetMask());
  Serial.print("Gateway IP : ");
  Serial.println(Ethernet.gatewayIP());
  Serial.print("DNS Server : ");
  Serial.println(Ethernet.dnsServerIP());

  Serial.println("Ethernet Successfully Initialized");

}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

//  int opMode = messageTemp[// mudar o indice].toInt();
  int opMode = (int)messageTemp[7]-48;
  Serial.print(opMode);
  sinalDefinition(opMode);
  
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("pi2");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void sinalDefinition(int valor){
  if(valor == 0){ //off
    digitalWrite(15, LOW);
    digitalWrite(2, LOW);
    digitalWrite(4, HIGH);
    digitalWrite(21, LOW);
  } else if(valor == 1){ //on
    digitalWrite(15, HIGH);
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    digitalWrite(21, LOW);
    
  } else if(valor == 2){ //standby
    digitalWrite(15, LOW);
    digitalWrite(2, LOW);
    digitalWrite(4, HIGH);
    digitalWrite(21, LOW);
    
  } else if(valor == 3){ //emergencia
    digitalWrite(15, LOW);
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    digitalWrite(21, HIGH);
  }

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();



}
