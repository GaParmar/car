#include <Wire.h>
#include <Servo.h>

int motorPin = 9;
int steerPin = 10;
Servo motor;
Servo steer;

// throttle range 100 - 180
int throttle = 105;
// dir = 2(reverse) or 1(forward) or 0(neutral)
int dir = 1;
int angle = 90;

void init_motor(int d){
    motor.write(20);
    delay(d);
    motor.write(60);
    delay(d);
    motor.write(100);
    delay(d);
    motor.write(140);
    delay(d);
    motor.write(180);
    delay(d);
}

void setup() {
  Wire.begin(0x8);                
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
  motor.attach(motorPin);
  steer.attach(steerPin);
  steer.write(90);
  delay(3000);
  init_motor(400);
  Serial.setTimeout(4);
}

void loop() {
  if(dir==1 || dir==2){motor.write(throttle);}
  else{motor.write(105);}
  steer.write(angle);
  Serial.println(throttle);
  delay(100);
}

void receiveEvent(int howMany) {
  while (Wire.available()){
    byte buff = Wire.read();
    if(buff == 0){/*Serial.println("buff is 0");*/}
    else{/*Serial.println("invalid buff value");*/}
    char type = Wire.read();
    byte val = Wire.read();
    if(type=='t'){throttle = val;}
    else if(type=='d'){dir = val;}
    else if(type=='s'){angle = val;}
  }
}
