int t;
int count;

void setup() {
  Serial.begin(115200);
}

void loop(){
  
  int a = analogRead(A0);
  int b = analogRead(A4);


  // Show raw picture
  Serial.println(a);
  Serial.print(",");
  Serial.print(b);
//  t = millis();
//  count ++ ;
//  Serial.print(",");
//  Serial.print(t);
//  Serial.print(",");
//  Serial.println(count);
  
  //delay(1);

}

