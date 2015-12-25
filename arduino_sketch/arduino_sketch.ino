#include <Servo.h>

#define SERVO_PIN 9
#define SERVO_ANGLE 130
#define LED_PIN 13

#define ACTIVATE_GATE "1"

#define RESET_SERVO "0"


Servo servo;


void toggleLED() {
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

void setup() {
  // Serial
  Serial.begin(9600);
  delay(500);
  Serial.setTimeout(500);

  //LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
  delay(1500);
  digitalWrite(LED_PIN, LOW);

  // Servo
  servo.attach(SERVO_PIN);
  servo.write(90);
  delay(500);
  //servo.write(0);

  delay(500);
}

void loop() {
  String s = Serial.readString();

  if (s == ACTIVATE_GATE) {
    toggleLED();
    
    if (servo.read() != 0) {
      servo.write(0);
      delay(1000);
    }

    servo.write(SERVO_ANGLE);
    delay(800);
    servo.write(0);

    Serial.println("portao ativado");

    toggleLED();
  }

  
  else if (s == RESET_SERVO) {
    toggleLED();
    
    int val = servo.read();

    if (val == 0) {
      Serial.println("servo: 0");
    }
    else {
      servo.write(0);
      Serial.print("servo reconfigurado para 0 (era ");
      Serial.print(val);
      Serial.println(")");
    }

    Serial.flush();

    delay(1000);
    toggleLED();
  }
}
