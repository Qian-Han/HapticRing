int state = -1;

void setup() {
  Serial.begin(115200);
}

void loop(){
  
  int a = analogRead(A0);

   //Show raw picture
  Serial.println(a);  

  delay(1);

/*
  if (Serial.available()>0)
  {
    state = Serial.read();

    switch(state){
      case 'g':
      int a = analogRead(A0);
      Serial.println(a);
    }
  }
  */
}








