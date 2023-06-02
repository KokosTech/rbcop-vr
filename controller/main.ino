#include <SoftwareSerial.h>

#define SAMPLE_SIZE 25

const int xpin = A0; // x-axis of the accelerometer
const int ypin = A1; // y-axis
const int zpin = A2; // z-axis

const int rx = 2;
const int tx = 3;

// add bluetooth communication
SoftwareSerial hc05(rx, tx);

void setup(void) {
  hc05.begin(9600);
}

void loop(void) {
  int x = analogRead(xpin); //read from xpin
  delay(1); //
  int y = analogRead(ypin); //read from ypin
  delay(1); 
  int z = analogRead(zpin); //read from zpin
  
  float x1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    x1 += x;
  }
  x1 = x1 / SAMPLE_SIZE;

  float y1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    y1 += y;
  }
  y1 = y1 / SAMPLE_SIZE;

  float z1 = 0;
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    z1 += z;
  }
  z1 = z1 / SAMPLE_SIZE;
  
  String sx = String(x1);
  String sy = String(y1);
  String sz = String(z1);

  hc05.println("{\"sensor\":\"adxl335\",\"angle_data\":[" + sx + ", " + sy + "," + sz + "]}"); 

  delay(700);
}
