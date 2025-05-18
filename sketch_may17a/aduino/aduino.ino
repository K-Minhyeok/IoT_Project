#include <WiFi.h>
#include <WiFiClientSecure.h> 
#include <PubSubClient.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// const char* ssid = "hailers217";
// const char* password = "SailTheHail";
const char* ssid = "NTH413";
const char* password = "cseenth413";

const char* mqtt_server = "e94e4245a7a44cf9a744f49b1072c3f2.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "node2";
const char* mqtt_pass = "node2NODE@";

// OLED Configuration
#define SCREEN_WIDTH    128
#define SCREEN_HEIGHT   64
#define OLED_RESET      -1
#define OLED_ADDR       0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Valve configuration 
#define VALVE_PIN1    25  // LEFT
#define VALVE_PIN2    21  // R

WiFiClientSecure espClient;
PubSubClient client(espClient);


const char* root_ca = \
"-----BEGIN CERTIFICATE-----\n" \
"MIIFBjCCAu6gAwIBAgIRAIp9PhPWLzDvI4a9KQdrNPgwDQYJKoZIhvcNAQELBQAw\n" \
"TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh\n" \
"cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMjQwMzEzMDAwMDAw\n" \
"WhcNMjcwMzEyMjM1OTU5WjAzMQswCQYDVQQGEwJVUzEWMBQGA1UEChMNTGV0J3Mg\n" \
"RW5jcnlwdDEMMAoGA1UEAxMDUjExMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\n" \
"CgKCAQEAuoe8XBsAOcvKCs3UZxD5ATylTqVhyybKUvsVAbe5KPUoHu0nsyQYOWcJ\n" \
"DAjs4DqwO3cOvfPlOVRBDE6uQdaZdN5R2+97/1i9qLcT9t4x1fJyyXJqC4N0lZxG\n" \
"AGQUmfOx2SLZzaiSqhwmej/+71gFewiVgdtxD4774zEJuwm+UE1fj5F2PVqdnoPy\n" \
"6cRms+EGZkNIGIBloDcYmpuEMpexsr3E+BUAnSeI++JjF5ZsmydnS8TbKF5pwnnw\n" \
"SVzgJFDhxLyhBax7QG0AtMJBP6dYuC/FXJuluwme8f7rsIU5/agK70XEeOtlKsLP\n" \
"Xzze41xNG/cLJyuqC0J3U095ah2H2QIDAQABo4H4MIH1MA4GA1UdDwEB/wQEAwIB\n" \
"hjAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUHAwEwEgYDVR0TAQH/BAgwBgEB\n" \
"/wIBADAdBgNVHQ4EFgQUxc9GpOr0w8B6bJXELbBeki8m47kwHwYDVR0jBBgwFoAU\n" \
"ebRZ5nu25eQBc4AIiMgaWPbpm24wMgYIKwYBBQUHAQEEJjAkMCIGCCsGAQUFBzAC\n" \
"hhZodHRwOi8veDEuaS5sZW5jci5vcmcvMBMGA1UdIAQMMAowCAYGZ4EMAQIBMCcG\n" \
"A1UdHwQgMB4wHKAaoBiGFmh0dHA6Ly94MS5jLmxlbmNyLm9yZy8wDQYJKoZIhvcN\n" \
"AQELBQADggIBAE7iiV0KAxyQOND1H/lxXPjDj7I3iHpvsCUf7b632IYGjukJhM1y\n" \
"v4Hz/MrPU0jtvfZpQtSlET41yBOykh0FX+ou1Nj4ScOt9ZmWnO8m2OG0JAtIIE38\n" \
"01S0qcYhyOE2G/93ZCkXufBL713qzXnQv5C/viOykNpKqUgxdKlEC+Hi9i2DcaR1\n" \
"e9KUwQUZRhy5j/PEdEglKg3l9dtD4tuTm7kZtB8v32oOjzHTYw+7KdzdZiw/sBtn\n" \
"UfhBPORNuay4pJxmY/WrhSMdzFO2q3Gu3MUBcdo27goYKjL9CTF8j/Zz55yctUoV\n" \
"aneCWs/ajUX+HypkBTA+c8LGDLnWO2NKq0YD/pnARkAnYGPfUDoHR9gVSp/qRx+Z\n" \
"WghiDLZsMwhN1zjtSC0uBWiugF3vTNzYIEFfaPG7Ws3jDrAMMYebQ95JQ+HIBD/R\n" \
"PBuHRTBpqKlyDnkSHDHYPiNX3adPoPAcgdF3H2/W0rmoswMWgTlLn1Wu0mrks7/q\n" \
"pdWfS6PJ1jty80r2VKsM/Dj3YIDfbjXKdaFU5C+8bhfJGqU3taKauuz0wHVGT3eo\n" \
"6FlWkWYtbt4pgdamlwVeZEW+LM7qZEJEsMNPrfC03APKmZsJgpWCDWOKZvkZcvjV\n" \
"uYkQ4omYCTX5ohy+knMjdOmdH9c7SpqEWBDC86fiNex+O0XOMEZSa8DA\n" \
"-----END CERTIFICATE-----\n";



void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void showMessage(const String& line1, const String& line2 = "") {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.println(line1);
  if (line2 != "") display.println(line2);
  display.display();
}

// void reconnect() {
//   while (!client.connected()) {
//     if (client.connect("LilyGOClient", mqtt_user, mqtt_pass)) {
//       client.subscribe("handong/temperature");
//     } else {
//       delay(2000);
//     }
//   }
// }

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("LilyGOCliEnt2", mqtt_user, mqtt_pass)) {
      Serial.println("connected");
      client.subscribe("handong/node2");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state()); 
      Serial.println(" try again in 2 seconds");
      delay(2000);
    }
  }
}


void setup() {
  Serial.begin(115200);
  // valve 초기 설정 
  pinMode(VALVE_PIN1, OUTPUT);
  pinMode(VALVE_PIN2, OUTPUT);
  digitalWrite(VALVE_PIN1, LOW);
  digitalWrite(VALVE_PIN2, LOW);
  
  setup_wifi();
 

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("SSD1306 OLED init failed");
    while (true);
  }

  showMessage("Connecting to","wilson");

  // espClient.setInsecure(); // TLS 인증서 검증 생략
  espClient.setCACert(root_ca);

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback([](char* topic, byte* payload, unsigned int length) {
    Serial.print("Message received: ");
    Serial.write(payload, length);
    Serial.println();

    String message;
    for (int i = 0; i < length; i++) {
      message += (char)payload[i];
    }

    
    // OLED에 표시
    showMessage("Received:", message);
    if(message=="valve 1 on"){
      digitalWrite(VALVE_PIN1, HIGH);
    }
    else if(message=="valve 1 off"){
      digitalWrite(VALVE_PIN1,LOW); 
    }
    else if(message=="valve 2 on"){
      digitalWrite(VALVE_PIN2, HIGH);
    }
    else if(message=="valve 2 off"){
      digitalWrite(VALVE_PIN2,LOW); 
    }

  });
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  client.publish("test/topic", "Hello from LilyGO!2222");
  delay(5000);
}
