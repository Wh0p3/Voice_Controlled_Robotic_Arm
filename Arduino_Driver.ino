#include <Servo.h>

Servo servo_base;
Servo servo_shoulder;
Servo servo_elbow;

void setup() {
  // Attach servos to pins
  servo_base.attach(9);
  servo_shoulder.attach(10);
  servo_elbow.attach(11);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the serial input (base, shoulder, elbow angles)
    String input = Serial.readStringUntil('\n');
    int base_angle, shoulder_angle, elbow_angle;

    // Parse the angles from the input string
    sscanf(input.c_str(), "%d %d %d", &base_angle, &shoulder_angle, &elbow_angle);

    // Move the servos to the received angles
    servo_base.write(base_angle);
    servo_shoulder.write(shoulder_angle);
    servo_elbow.write(elbow_angle);

    // Print the angles to the Serial Monitor for debugging
    Serial.print("Base: "); Serial.print(base_angle);
    Serial.print(" | Shoulder: "); Serial.print(shoulder_angle);
    Serial.print(" | Elbow: "); Serial.println(elbow_angle);
  }
}
