//Motor 
int PWMA = 5; //Speed control
int DirA = 4; //Direction
int PWMB = 3; //Speed control
int DirB = 2; //Direction

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



      case 'g':                      
      getReady();
      break;

      case 'r':                      
      reset();
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



    

      case 's':                      // Stop first motor
      Stop();
      break;

    }
  }

}



void move(int motor, int speed, int direction) {  // Motor moves function

  boolean dirbool = HIGH;                         // High for clockwise movement
  if (direction == 0) { 
    dirbool = LOW;                                // Low for counterclockwise movement
  }

  if (motor == 1) {
    digitalWrite(DirA, dirbool);                  // Write first motor's direction and PWM
    analogWrite(PWMA, speed);
  }
  
  if (motor == 2) {                               // Write second motor's direction and PWM
  digitalWrite(DirB, dirbool);
  analogWrite(PWMB, speed);

  }
}

void getReady(){    
  minimumStepDownL();
  minimumStepDownM();
  minimumStepDownS();
  
}

void reset(){    
  minimumStepUpL();
  minimumStepUpM();
  minimumStepUpS();
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



//void doTick(){
//
//  move(1,testspeed2,0);
//  delay(delayTimeTick);
//  
//  move(1,testspeed2,1);
//  delay(delayTimeTick - 22);  // test
//  move(1,0,0);
//   
//}

//void doTick(){
//
//  move(1,testspeed2,0);
//  delay(delayTimeTick);
//  move(1,0,0);
//  delay(500);
//  
//  move(1,testspeed2,1);
//  delay(delayTimeTick -20);  // test
//  move(1,0,0);
//   
//  }

  

void Stop(){              // Stop

  move(1,0,0);
  
}



