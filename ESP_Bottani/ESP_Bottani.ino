//HALLOOO
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define PUBLISH_TOPIC "test/publish"
#define T_TOPIC "sensor/Temperature"
#define H_TOPIC "sensor/pH"
#define M_TOPIC "sensor/Moisture"

#define ts_sensor 5000
#define ts_button 100
