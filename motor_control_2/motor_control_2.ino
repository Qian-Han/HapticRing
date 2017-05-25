int STBY = 10; //standby

//Motor A
int PWMA = 3; //Speed control 
int AIN1 = 9; //Direction
int AIN2 = 8; //Direction


int state = -1;
int count = 0;

const int delayTimeXS = 3;
const int delayTimeS = 10;
const int delayTimeM = 20;
const int delayTimeL = 30;

const int getReadyTime = 130;

const int delayTimeTick = 150;




int testspeed = 255;


void setup() {
  Serial.begin(115200);
  pinMode(STBY, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
}

void loop(){
  
  if(Serial.available()>0){
  
    
    state = Serial.read();          
    
    switch(state){                   // different state to switch  

      case 'p':                      
      minimumStepUpXS();
      break;
      
      case 'q':                      
      minimumStepUpS();
      break;

      case 'w':                      
      minimumStepUpM();
      break;

      case 'e':                      
      minimumStepUpL();
      break;


      case 'm':                      
      minimumStepDownXS();
      break;


      case 'z':                      
      minimumStepDownS();
      break;

      case 'x':                      
      minimumStepDownM();
      break;

      case 'c':                      
      minimumStepDownL();
      break;

      case '/':
      slowup();
      break;

      case '.':
      slowdown();
      break;

      case 's':                      // Stop first motor
      Stop();
      break;

      case 'b':                      // Stop first motor
      Bump();
      break;

    }
  }

}


void move(int motor, int speed, int direction){
//Move specific motor at speed and direction
//motor: 0 for B 1 for A
//speed: 0 is off, and 255 is full speed
//direction: 0 clockwise, 1 counter-clockwise

  digitalWrite(STBY, HIGH); //disable standby

  boolean inPin1 = HIGH;
  boolean inPin2 = LOW;

  if(direction == 1){
    inPin1 = LOW;
    inPin2 = HIGH;
  } 

  if(motor == 1){
    digitalWrite(AIN1, inPin1);
    digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  }
}

void slowup()
{
  move(1, 150, 1);
}

void slowdown()
{
  move(1, 150, 0);
}


void minimumStepUpXS(){    
  move(1,testspeed,1);
  delay(delayTimeXS);
  move(1,0,0);
  
}


void minimumStepUpS(){    
  move(1,testspeed,1);
  delay(delayTimeS);
  move(1,0,0);
  
}

void minimumStepUpM(){    
  move(1,testspeed,1);
  delay(delayTimeM);
  move(1,0,0);
  
}


void minimumStepUpL(){    
  move(1,testspeed,1);
  delay(delayTimeL);
  move(1,0,0);
  
}


void minimumStepDownXS(){    
  move(1,testspeed,0);
  delay(delayTimeXS);
  move(1,0,0);
  
}


void minimumStepDownS(){   
  
  move(1,testspeed,0);
  delay(delayTimeS);
  move(1,0,0);
  
}

void minimumStepDownM(){   
  
  move(1,testspeed,0);
  delay(delayTimeM);
  move(1,0,0);
  
}


void minimumStepDownL(){   
  
  move(1,testspeed,0);
  delay(delayTimeL);
  move(1,0,0);
  
}


void Stop(){              // Stop

   digitalWrite(STBY, LOW); 
  
}

void Bump(){   

  for(int i = 0;i < 150; i++){
    move(1,testspeed,0);
    delay(4.5*delayTimeL);
    move(1,0,0);
    delay(300);
    move(1,testspeed,1);
    delay(3*delayTimeL);
    move(1,0,0);
    delay(2000);
  }
  
}







