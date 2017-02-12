//Motor 
int PWMA = 5; //Speed control
int DirA = 4; //Direction
int PWMB = 3; //Speed control
int DirB = 2; //Direction

int state = -1;
int count = 0;


const int delayTime = 30;
const int delayTimeTick = 150;
const int preTickStep = 4;



int testspeed = 100;         // change to different motor speed, according to PWM
int testspeed2 = 255;
int hhcount = 1;


void setup() {
  Serial.begin(115200);
}

void loop(){
  
  int a = analogRead(A0);
  int b = analogRead(A4);


   //Show raw picture
  Serial.print(a);  // 30 or 980
  Serial.print(",");
  Serial.println(b);  // 210 or 820 

}





