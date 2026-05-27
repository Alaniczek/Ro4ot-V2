#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* WIFI_SSID = "AkuKu";
const char* WIFI_PASS = "12345678";
const int LOCAL_PORT  = 4210;
const int SERVER_PORT = 17145; // Port changed to 17145 (one up from 17144)

WiFiUDP udp;
char packetBuffer[255];

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n[WIFI] Connected!");
  Serial.print("[IP] Robot IP: ");
  Serial.println(WiFi.localIP());
  
  udp.begin(LOCAL_PORT);
}

void loop() {
  int packetSize = udp.parsePacket();
  
  if (packetSize) {
    int len = udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len] = 0;
    
    Serial.print("[UDP] Cmd received: ");
    Serial.println(packetBuffer);

    // Get the sender's IP
    IPAddress remoteIp = udp.remoteIP();
    Serial.print("[UDP] Replying to: ");
    Serial.print(remoteIp);
    Serial.print(" on port: ");
    Serial.println(SERVER_PORT);

    // Prepare response
    udp.beginPacket(remoteIp, SERVER_PORT);
    if (strcmp(packetBuffer, "ping") == 0) {
      udp.write("pong");
    } else {
      udp.write("ACK: ");
      udp.write(packetBuffer);
    }
    
    if (udp.endPacket()) {
      Serial.println("[UDP] Packet sent successfully");
    } else {
      Serial.println("[UDP] Failed to send packet");
    }
  }
}
