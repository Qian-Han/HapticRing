//Motor 
int PWMA = 5; //Speed control
int DirA = 4; //Direction
int PWMB = 3; //Speed control
int DirB = 2; //Direction

int state = -1;
int count = 0;

int angle = 0;
float lastStateA = 0.0;
float lastStateB = 0.0;


float lastStateA_raw = 0.0;
float lastStateB_raw = 0.0;


// Threshold of hall sensor
//const int Threshold_positive = 750;
//const int Threshold_negative = 350; 

const int ThresholdA_900 = 900;
const int ThresholdA_820 = 820;
const int ThresholdA_740 = 740;
const int ThresholdA_660 = 660;
const int ThresholdA_580 = 580;
const int ThresholdA_500 = 500;
const int ThresholdA_420 = 420;
const int ThresholdA_340 = 340;
const int ThresholdA_260 = 260;
const int ThresholdA_180 = 180; 


const int ThresholdB_750 = 750;
const int ThresholdB_700 = 700;
const int ThresholdB_650 = 650;
const int ThresholdB_600 = 600;
const int ThresholdB_550 = 550;
const int ThresholdB_500 = 500;
const int ThresholdB_450 = 450;
const int ThresholdB_400 = 400;
const int ThresholdB_350 = 350;
const int ThresholdB_300 = 300;







//const int Threshold = 500;

const int delayTime = 30;

int testspeed = 100;         // change to different motor speed, according to PWM
int testspeed2 = 255;
int hhcount = 1;


void setup() {
  Serial.begin(9600);
  pinMode(PWMA, OUTPUT);
  pinMode(DirA, OUTPUT); 
}

void loop(){
  
  float a = analogRead(A0);
  float b = analogRead(A4);
//  float a_raw = a;
//  float b_raw = b;

  // Show raw picture
//  Serial.print(a);
////  long t = millis();
//  Serial.print("           ");
////  Serial.print(t);
////  Serial.print("           ");
////  Serial.println(hhcount++);
// 
////  Serial.print("           ");
//  Serial.println(b);
//  Serial.print("           ");

/*
  if(a >= ThresholdA_900){
    a = 10;}
    else if(a >= ThresholdA_820 && a < ThresholdA_900)
    {a = 9;}
    else if(a >= ThresholdA_740 && a < ThresholdA_820)
    {a = 8;}
    else if(a >= ThresholdA_660 && a < ThresholdA_740)
    {a = 7;}
    else if(a >= ThresholdA_580 && a < ThresholdA_660)
    {a = 6;}
    else if(a >= ThresholdA_500 && a < ThresholdA_580)
    {a = 5;}
    else if(a >= ThresholdA_420 && a < ThresholdA_500)
    {a = 4;}
    else if(a >= ThresholdA_340 && a < ThresholdA_420)
    {a = 3;}
    else if(a >= ThresholdA_260 && a < ThresholdA_340)
    {a = 2;}
    else if(a >= ThresholdA_180 && a < ThresholdA_260)
    {a = 1;}
    else if(a < ThresholdA_180)
    {a = 0;}*/
//  Serial.print(a);  

/*
  if(b >= ThresholdB_750){
    b = 10;}
    else if(b >= ThresholdB_700 && b < ThresholdB_750)
    {b = 9;}
    else if(b >= ThresholdB_650 && b < ThresholdB_700)
    {b = 8;}
    else if(b >= ThresholdB_600 && b < ThresholdB_650)
    {b = 7;}
    else if(b >= ThresholdB_550 && b < ThresholdB_600)
    {b = 6;}
    else if(b >= ThresholdB_500 && b < ThresholdB_550)
    {b = 5;}
    else if(b >= ThresholdB_450 && b < ThresholdB_500)
    {b = 4;}
    else if(b >= ThresholdB_400 && b < ThresholdB_450)
    {b = 3;}
    else if(b >= ThresholdB_350 && b < ThresholdB_400)
    {b = 2;}
    else if(b >= ThresholdB_300 && b < ThresholdB_350)
    {b = 1;}
    else if(b < ThresholdB_300)
    {b = 0;}
  */  
//  Serial.print(a);
//  Serial.print("         ");
//  Serial.println(b);


// LOOKUP TABLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//  if ((lastStateB == 10) && (b == 9)) {
////    Serial.print(lastStateB_raw);
////    Serial.print("      ");
////    
////    Serial.print(lastStateB);
////    Serial.print("      ");
////    
////    Serial.print(b_raw);
////    Serial.print("      ");
////    
////    Serial.print(b);
////    Serial.print("      ");
////    
////    Serial.print(a_raw);
////    Serial.print("      ");
////    Serial.println(a);
//    
// 
//    
//    if (a == 0) { // a == 0
//       angle += 2;
//     } 
//     else if(a > 0){ // a == 3|| a == 2
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 9) && (b == 8)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//
//
////    Serial.print(lastStateB_raw);
////    Serial.print("      ");
////    
////    Serial.print(lastStateB);
////    Serial.print("      ");
////    
////    Serial.print(b_raw);
////    Serial.print("      ");
////    
////    Serial.print(b);
////    Serial.print("      ");
////    
////    Serial.print(a_raw);
////    Serial.print("      ");
////    Serial.println(a);
////    
// 
//    if (a == 0) { // a == 0
//       angle += 2;
//     } 
//     else if(a > 0){ // a == 2|| a == 3 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//
//  if ((lastStateB == 8) && (b == 7)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);  
//
//
////
////    Serial.print(lastStateB_raw);
////    Serial.print("      ");
////    
////    Serial.print(lastStateB);
////    Serial.print("      ");
////    
////    Serial.print(b_raw);
////    Serial.print("      ");
////    
////    Serial.print(b);
////    Serial.print("      ");
////    
////    Serial.print(a_raw);
////    Serial.print("      ");
////    Serial.println(a);
//    
//   
//    if (a < 2) { //a == 0|| a == 1
//       angle += 2;
//     } 
//     else if(a > 2){ //a == 3|| a == 4
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 7) && (b == 6)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//
////
////    Serial.print(lastStateB_raw);
////    Serial.print("      ");
////    
////    Serial.print(lastStateB);
////    Serial.print("      ");
////    
////    Serial.print(b_raw);
////    Serial.print("      ");
////    
////    Serial.print(b);
////    Serial.print("      ");
////    
////    Serial.print(a_raw);
////    Serial.print("      ");
////    Serial.println(a);
//    
//   
//    if (a <= 2) { // a == 1|| a == 0
//       angle += 2;
//     } 
//     else if(a > 2){ // a == 4 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//
//  if ((lastStateB == 6) && (b == 5)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a < 4) {  // a == 2 || a == 1
//       angle += 2;
//     } 
//     else if(a >= 4){ // a == 4 || a == 5 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 5) && (b == 4)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a <= 4) { // a == 2 || a == 3
//       angle += 2;
//     } 
//     else if(a > 4){ // a == 5 || a == 6
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 4) && (b == 3)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a <= 5) {  // a == 3 ||　a == 4 
//       angle += 2;
//     } 
//     else if(a >= 6){ // a  == 7 || a == 8 || a == 6
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 3) && (b == 2)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a <= 7) {  // a == 4
//       angle += 2;
//     } 
//     else if(a >= 7){ // a == 9 || a == 8 || a == 7
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 2) && (b == 1)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a <= 7) {  // a == 4 || a == 5
//       angle += 2;
//     } 
//     else if(a >= 8){ // a == 10 || a == 9 || a == 8
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  
//  if ((lastStateB == 1) && (b == 0)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);    
//    if (a < 10) {  // a == 5 || a == 6
//       angle += 2;
//     } 
//     else if(a == 10){  // a == 10
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
/////////////////////////////////////////////////////////////////////// finished today!!!!
//  
//  if ((lastStateB == 0) && (b == 1)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a == 10) { // a == 10
//       angle += 2;
//     } 
//     else if(a < 10){ // a == 5 || a == 6
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 1) && (b == 2)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a >= 7) { // a == 10 || a == 9 || a == 8
//       angle += 2;
//     } 
//     else if(a < 7){   // a == 4 || a == 5
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 2) && (b == 3)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a >= 7) {  // a == 9 || a == 8 || a == 7
//       angle += 2;
//     } 
//     else if(a < 7){ // a == 4
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//  
//  if ((lastStateB == 3) && (b == 4)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a >= 6) { // a == 7 || a == 6
//       angle += 2;
//     } 
//     else if(a < 6){ // a == 4 || a == 3
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//  
//  if ((lastStateB == 4) && (b == 5)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 4) { // a == 6 || a == 5
//       angle += 2;
//     } 
//     else if(a <= 4){ // a == 3 || a == 2
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 5) && (b == 6)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 3) { // a == 4 || a == 5
//       angle += 2;
//     } 
//     else if(a <= 3){ // a == 1 || a == 2 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 6) && (b == 7)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 2) { // a == 3 || a == 4 
//       angle += 2;
//     } 
//     else if(a <= 2){ // a == 0 || a == 1 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  } 
//
//  if ((lastStateB == 7) && (b == 8)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 1) { //  a == 3 || a == 4
//       angle += 2;
//     } 
//     else if(a <= 1){ // a == 0 || a == 1 
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 8) && (b == 9)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 0) { // a == 2 || a == 3
//       angle += 2;
//     } 
//     else if(a == 0){ // a == 0
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
//  if ((lastStateB == 9) && (b == 10)) {
////    Serial.print(lastStateB);
////    Serial.print(",");
////    Serial.print(b);
////    Serial.print("                   ");
////    Serial.println(a);
//    if (a > 0) {  // a == 3 || a == 2 
//     } 
//     else if(a == 0){ // a == 0
//       angle -= 2;
//     }
//     else{
//      //do nothing
//     }
//  }
//
// 
//    




if ((lastStateB == 10) && (b == 9)) {
//    Serial.print(lastStateB_raw);
//    Serial.print("      ");
//    
//    Serial.print(lastStateB);
//    Serial.print("      ");
//    
//    Serial.print(b_raw);
//    Serial.print("      ");
//    
//    Serial.print(b);
//    Serial.print("      ");
//    
//    Serial.print(a_raw);
//    Serial.print("      ");
//    Serial.println(a);
    
 
    
    if (a == 0) { // a == 0
       angle += 2;
     } 
     else if(a > 0){ // a == 3|| a == 2
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 9) && (b == 8)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);


//    Serial.print(lastStateB_raw);
//    Serial.print("      ");
//    
//    Serial.print(lastStateB);
//    Serial.print("      ");
//    
//    Serial.print(b_raw);
//    Serial.print("      ");
//    
//    Serial.print(b);
//    Serial.print("      ");
//    
//    Serial.print(a_raw);
//    Serial.print("      ");
//    Serial.println(a);
//    
 
    if (a == 0) { // a == 0
       angle += 2;
     } 
     else if(a > 0){ // a == 2|| a == 3 
       angle -= 2;
     }
     else{
      //do nothing
     }
  }


  if ((lastStateB == 8) && (b == 7)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);  


//
//    Serial.print(lastStateB_raw);
//    Serial.print("      ");
//    
//    Serial.print(lastStateB);
//    Serial.print("      ");
//    
//    Serial.print(b_raw);
//    Serial.print("      ");
//    
//    Serial.print(b);
//    Serial.print("      ");
//    
//    Serial.print(a_raw);
//    Serial.print("      ");
//    Serial.println(a);
    
   
    if (a < 2) { //a == 0|| a == 1
       angle += 2;
     } 
     else if(a > 2){ //a == 3|| a == 4
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 7) && (b == 6)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);

//
//    Serial.print(lastStateB_raw);
//    Serial.print("      ");
//    
//    Serial.print(lastStateB);
//    Serial.print("      ");
//    
//    Serial.print(b_raw);
//    Serial.print("      ");
//    
//    Serial.print(b);
//    Serial.print("      ");
//    
//    Serial.print(a_raw);
//    Serial.print("      ");
//    Serial.println(a);
    
   
    if (a <= 2) { // a == 1|| a == 0
       angle += 2;
     } 
     else if(a > 2){ // a == 4 
       angle -= 2;
     }
     else{
      //do nothing
     }
  }


  if ((lastStateB == 6) && (b == 5)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a < 4) {  // a == 2 || a == 1
       angle += 2;
     } 
     else if(a >= 4){ // a == 4 || a == 5 
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 5) && (b == 4)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a <= 4) { // a == 2 || a == 3
       angle += 2;
     } 
     else if(a > 4){ // a == 5 || a == 6
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 4) && (b == 3)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a <= 5) {  // a == 3 ||　a == 4 
       angle += 2;
     } 
     else if(a >= 6){ // a  == 7 || a == 8 || a == 6
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 3) && (b == 2)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a <= 7) {  // a == 4
       angle += 2;
     } 
     else if(a >= 7){ // a == 9 || a == 8 || a == 7
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 2) && (b == 1)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a <= 7) {  // a == 4 || a == 5
       angle += 2;
     } 
     else if(a >= 8){ // a == 10 || a == 9 || a == 8
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  
  if ((lastStateB == 1) && (b == 0)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);    
    if (a < 10) {  // a == 5 || a == 6
       angle += 2;
     } 
     else if(a == 10){  // a == 10
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

///////////////////////////////////////////////////////////////////// finished today!!!!
  
  if ((lastStateB == 0) && (b == 1)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a == 10) { // a == 10
       angle += 2;
     } 
     else if(a < 10){ // a == 5 || a == 6
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 1) && (b == 2)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a >= 7) { // a == 10 || a == 9 || a == 8
       angle += 2;
     } 
     else if(a < 7){   // a == 4 || a == 5
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 2) && (b == 3)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a >= 7) {  // a == 9 || a == 8 || a == 7
       angle += 2;
     } 
     else if(a < 7){ // a == 4
       angle -= 2;
     }
     else{
      //do nothing
     }
  }
  
  if ((lastStateB == 3) && (b == 4)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a >= 6) { // a == 7 || a == 6
       angle += 2;
     } 
     else if(a < 6){ // a == 4 || a == 3
       angle -= 2;
     }
     else{
      //do nothing
     }
  }
  
  if ((lastStateB == 4) && (b == 5)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 4) { // a == 6 || a == 5
       angle += 2;
     } 
     else if(a <= 4){ // a == 3 || a == 2
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 5) && (b == 6)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 3) { // a == 4 || a == 5
       angle += 2;
     } 
     else if(a <= 3){ // a == 1 || a == 2 
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 6) && (b == 7)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 2) { // a == 3 || a == 4 
       angle += 2;
     } 
     else if(a <= 2){ // a == 0 || a == 1 
       angle -= 2;
     }
     else{
      //do nothing
     }
  } 

  if ((lastStateB == 7) && (b == 8)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 1) { //  a == 3 || a == 4
       angle += 2;
     } 
     else if(a <= 1){ // a == 0 || a == 1 
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 8) && (b == 9)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 0) { // a == 2 || a == 3
       angle += 2;
     } 
     else if(a == 0){ // a == 0
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

  if ((lastStateB == 9) && (b == 10)) {
//    Serial.print(lastStateB);
//    Serial.print(",");
//    Serial.print(b);
//    Serial.print("                   ");
//    Serial.println(a);
    if (a > 0) {  // a == 3 || a == 2 
     } 
     else if(a == 0){ // a == 0
       angle -= 2;
     }
     else{
      //do nothing
     }
  }

 
   




































// LOOKUP TABLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  if(angle == 360){
      angle = 0;}

  if(angle == -2){
      angle = 358;}
      
  lastStateA = a;
  lastStateB = b;  

//  lastStateA_raw = a_raw;
//  lastStateB_raw = b_raw;
//
//
//  
//  Serial.println(angle); 
  //fps(1);
  
  if(Serial.available()>0){
    
    state = Serial.read(); }         // Serial read from monitor
    
    switch(state){                   // different state to switch  
      
      case 'u':                      // First motor makes the brake move up
      minimumStepUp();
      break;

      case 'd':                      // First motor makes the brake move down
      minimumStepDown();
      break;

      case 'e':                      // First motor makes the brake move down slowly
      slowMinimumStepDown();
      break;

      case 'i':                      // First motor makes the brake move up slowly
      slowMinimumStepUp();
      break;

      case 's':                      // Stop first motor
      Stop();
      break;

      case 'c':                      // clear data
      angle = 0;
      break;
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

void minimumStepUp(){    // minimumStepUp

  move(1,testspeed2,1);
  delay(delayTime);
  move(1,0,0);
  
  }

void minimumStepDown(){   // minimumStepDown

  move(1,testspeed2,0);
  delay(delayTime);
  move(1,0,0);
  
  }

void slowMinimumStepDown(){   // minimumStepDown

  move(1,testspeed,0);
  delay(delayTime);
  move(1,0,0);
  
  }

void slowMinimumStepUp(){    // minimumStepUp

  move(1,testspeed,1);
  delay(delayTime);
  move(1,0,0);
  
  }
  

void Stop(){              // Stop

  move(1,0,0);
  
  }

static inline void fps(const int seconds){
  // Create static variables so that the code and variables can
  // all be declared inside a function
  static unsigned long lastMillis;
  static unsigned long frameCount;
  static unsigned int framesPerSecond;
  
  // It is best if we declare millis() only once
  unsigned long now = millis();
  frameCount ++;
  if (now - lastMillis >= seconds * 1000) {
    framesPerSecond = frameCount / seconds;
    Serial.print("#fps: ");
    Serial.println(framesPerSecond);
    frameCount = 0;
    lastMillis = now;
  }
}

