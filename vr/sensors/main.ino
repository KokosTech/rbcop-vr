#include <usb.h>

USBDevice usbDevice;

const uint8_t REPORT_ID = 1;
const uint8_t REPORT_SIZE = 9;

struct Report {
    uint8_t reportId;
    int16_t gyroX;
    int16_t gyroY;
    int16_t gyroZ;
    uint8_t distance1;
    uint8_t distance2;
    uint8_t button;
};

Report report;

void setup() {
    Serial.begin(9600);
    while (!Serial)
        ;

    usbDevice.setManufacturer("RbCop");
    usbDevice.setProduct("RbCop Sensor");
    usbDevice.setSerialNumber("123456");
    usbDevice.setVendorId(0x1234);
    usbDevice.setProductId(0x5678);
    usbDevice.begin();
}

void loop() {
    // Read sensor values
    int16_t gyroX = analogRead(A0);
    int16_t gyroY = analogRead(A1);
    int16_t gyroZ = analogRead(A2);
    uint8_t distance1 = analogRead(A3) >> 2;
    uint8_t distance2 = analogRead(A4) >> 2;
    bool button = digitalRead(2);

    // Populate report
    report.reportId = REPORT_ID;
    report.gyroX = gyroX;
    report.gyroY = gyroY;
    report.gyroZ = gyroZ;
    report.distance1 = distance1;
    report.distance2 = distance2;
    report.button = button;

    // Send report
    usbDevice.send((uint8_t*)&report, REPORT_SIZE);

    delay(10);
}