#include <ESP8266WiFi.h>
#include <WebSocketsServer.h>
#include <LittleFS.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "TELEVA-703";
const char* password = "12345678";

WebSocketsServer webSocket = WebSocketsServer(81);
AsyncWebServer server(80);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
    if (type == WStype_TEXT) {
        String message = String((char *)payload);
        Serial.printf("Message received: %s\n", message.c_str());
        
        float freq = message.toFloat();
        uint32_t frequency = freq*1000;

        if ((frequency <= 166700) && (frequency >= 160325))
        {
            // Send divider to radio
            uint8_t div = (frequency - 160325)/25;
            //String value = String(div, DEC);
            //String response = String("Received frequency: " + value);
            //webSocket.sendTXT(num, response);

        }
        else
        {
            String message = String("Taajuus taajuusalueen ulkopuolella\n Tuettu taajuusalue: 160.325 - 166.700 MHz");
            webSocket.sendTXT(num, message);

        }

        // Check frequency limits and send note if out of range
        //String response = "Received frequency: " + message;
        //webSocket.sendTXT(num, response);

        // if frequency in range then send divider to the radio
    }
}

void setup() {
    Serial.begin(115200);
    
    // Initialize LittleFS
    if (!LittleFS.begin()) {
        Serial.println("An Error has occurred while mounting LittleFS");
        return;
    }

    // Set up the access point
    WiFi.softAP(ssid, password);
    Serial.println("Access Point started");

    // Start WebSocket server
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);

    // Serve the HTML file from LittleFS
    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
        request->send(LittleFS, "/index.html", "text/html");
    });

    server.begin();
}

void loop() {
    webSocket.loop();
}
