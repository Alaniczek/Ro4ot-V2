#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* WIFI_SSID = "AkuKu";
const char* WIFI_PASS = "12345678";
const int LOCAL_PORT  = 4210;

WiFiUDP udp;
char packetBuffer[255];

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.println("");
  Serial.println(WiFi.localIP());
  
  udp.begin(LOCAL_PORT);
}

void loop() {
  int packetSize = udp.parsePacket();
  
  if (packetSize) {
    memset(packetBuffer, 0, 255);
    udp.read(packetBuffer, 255);
    
    Serial.println(packetBuffer);
  }
}