void setup() {

  Serial.begin(9600);

  for (int i=2; i < 6; i++){
    pinMode(i, OUTPUT); 
  }
  for (int i=2; i < 6; i++){
    digitalWrite(i, LOW); 
  }
}

void setUp_leds(char num);

void loop() {
 


  char data1 = Serial.read();
  char data2 = Serial.read();
   setUp_leds(data1);
 
}
  


void setUp_leds(char num){

  switch (num){

    case '1':
        digitalWrite(2, HIGH);
        break;
    case '2':
          for (int i=2; i < 4; i++)
          {
            digitalWrite(i, HIGH); 
          }
        break;
    case '3':
          for (int i=2; i < 5; i++)
          {
            digitalWrite(i,HIGH); 
          }
        break;
    case '4':
          for (int i=2; i < 5; i++)
          {
            digitalWrite(i, LOW); 
          }
          delay(100);
          digitalWrite(5, HIGH);
        break;

    case '5':
          for (int i=2; i < 6; i++)
          {
            digitalWrite(i, LOW); 
          }
        break;
  }   
}






