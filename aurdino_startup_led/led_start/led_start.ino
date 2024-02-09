void setup() {

  Serial.begin(9600);

  for (int i=2; i < 6; i++){
    pinMode(i, OUTPUT); 
  }
  for (int i=2; i < 6; i++){
    digitalWrite(i, HIGH); 
  }
}

void setUp_leds(char num);

void loop() {
  if (Serial.available() > 0) {
    char data1 = Serial.read(); 
    char data2 = Serial.read();
    
    setUp_leds(data1); // invoke fnc 
  }
}

void setUp_leds(char num){

  switch (num){

    case '1':
        digitalWrite(2, LOW);
        break;
    case '2':
          for (int i=2; i < 4; i++)
          {
            digitalWrite(i, LOW); 
          }
        break;
    case '3':
          for (int i=2; i < 5; i++)
          {
            digitalWrite(i,LOW); 
          }
        break;
    case '4':
          for (int i=2; i < 6; i++)
          {
            digitalWrite(i, LOW); 
          }
        break;
    case '5':
          for (int i=2; i < 6; i++)
          {
            digitalWrite(i, HIGH); 
          }
        break;
  }   
}






