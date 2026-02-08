#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Raviii";
const char* password = "11080505";

// Laptop IP (important!)
const char* serverURL = "http://10.233.22.234:5001/ingest";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    // Simulated network metrics
    int latency = random(20, 100);
    float packet_loss = random(0, 30) / 10.0;
    int congestion = random(1, 5);
    int users = random(50, 200);

    String payload = "{";
    payload += "\"latency_ms\":" + String(latency) + ",";
    payload += "\"packet_loss\":" + String(packet_loss) + ",";
    payload += "\"congestion_level\":" + String(congestion) + ",";
    payload += "\"active_users\":" + String(users) + ",";
    payload += "\"traffic_type\":\"NORMAL\"";
    payload += "}";

    int httpResponseCode = http.POST(payload);

    Serial.println("Sent payload:");
    Serial.println(payload);
    Serial.print("Response code: ");
    Serial.println(httpResponseCode);

    http.end();
  }

  delay(5000);
}
