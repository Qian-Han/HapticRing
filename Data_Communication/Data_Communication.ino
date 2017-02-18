void setup() {
  Serial.begin(115200);
}

void loop(){
  
  int a = analogRead(A0);
  int b = analogRead(A4);


   //Show raw picture
  Serial.print(a);  
  Serial.print(",");
  Serial.println(b);  

}





