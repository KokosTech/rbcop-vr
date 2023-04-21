#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <SoftwareSerial.h>

#define SAMPLE_SIZE 25

const int xpin = A0; // x-axis of the accelerometer
const int ypin = A1; // y-axis
const int zpin = A2; // z-axis

const int rx = 2;
const int tx = 3;

DynamicJsonDocument doc(1024);

// add bluetooth communication
SoftwareSerial hc05(rx, tx);

void setup(void) {
  Serial.begin(9600);
  hc05.begin(9600);
}

void loop(void) {
  int x = analogRead(xpin); //read from xpin
  delay(1); //
  int y = analogRead(ypin); //read from ypin
  delay(1); 
  int z = analogRead(zpin); //read from zpin
  
  float zero_G = 512.0; //ADC is 0~1023 the zero g output equal to Vs/2
  float scale = 102.3; //ADXL335330 Sensitivity is 330mv/g
  
  float x1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    x1 +=(((float)x - 331.5)/65*9.8);
  }
  x1 = x1 / SAMPLE_SIZE;

  float y1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    y1 += (((float)y - 329.5)/68.5*9.8);
  }
  y1 = y1 / SAMPLE_SIZE;

  float z1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    z1 += (((float)z - 340)/68*9.8);
  }
  z1 = z1 / SAMPLE_SIZE;

  doc["sensor"] = "adxl335";
  doc["angle_data"][0] = x1;
  doc["angle_data"][1] = y1;
  doc["angle_data"][2] = z1;

  String sx = String(x1);
  String sy = String(y1);
  String sz = String(z1);


  hc05.println("{\"sensor\":\"adxl335\",\"angle_data\":[" + sx + ", " + sy + "," + sz + "]}"); 
  // serializeJson(doc, Serial);
  // Serial.print("\n");
  delay(700);
}