#include <Servo.h>

Servo indexFingerServo;
Servo thumbServo;

void setup() {
  indexFingerServo.attach(9);
  thumbServo.attach(10);
}

void loop() {
  // Read values from Serial and control servos
  if (Serial.available() > 0) {
    int indexFingerPos = Serial.parseInt();
    int thumbPos = Serial.parseInt();

    indexFingerServo.write(indexFingerPos);
    thumbServo.write(thumbPos);
  }
}
