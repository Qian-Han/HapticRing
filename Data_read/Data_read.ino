int t;
int count;

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
//  t = millis();
//  count ++ ;
//  Serial.print(",");
//  Serial.print(t);
//  Serial.print(",");
//  Serial.println(count);
  
  //delay(1);

}

