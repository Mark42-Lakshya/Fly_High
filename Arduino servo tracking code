// final
#include <Servo.h>
Servo servoX;
Servo servoY;
int posX = 90;
int posY = 90;
void setup() {
  Serial.begin(115200);
  servoX.attach(9);
  servoY.attach(10);
  servoX.write(posX);
  servoY.write(posY);
}
void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int comma = data.indexOf(',');
    if (comma > 0) {
      String xStr = data.substring(0, comma);
      String yStr = data.substring(comma + 1);
      posX = xStr.toInt();
      posY = yStr.toInt();
      posX = constrain(posX, 0, 180);
      posY = constrain(posY, 0, 180);
      servoX.write(posX);
      servoY.write(posY);

    }
  }
  Serial.println(posX,posY);
  
}
