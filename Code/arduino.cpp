#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>

#define I2C_ADDRESS 0x08
#define MAX_BUFFER_SIZE 32

// Définir les pins des servos

#define servo0 2
#define servo1 3
#define servo2 4
#define servo3 5
#define servo4 6
#define servo5 7
#define servo6 8
#define servo7 9
#define servo8 10

#define FDservo0 A2
#define FDservo1 A3
#define FDservo2 A4
#define FDservo3 A5
#define FDservo4 A6
#define FDservo5 A7
#define FDservo6 A8
#define FDservo7 A9

Servo servo[9];
short int fd[8];
int step = 1;
short int speedDelay = 50;


short int receivedArray[100]; // Tableau pour stocker les données reçues
short int target[8];
short int targetMoinUn[8];
short int recordedPositions[100][8];
int indexRecordedPositions = 0;
int receivedInt = 0;
int index = 0;
int positionIndex = 0;
int positions[10][2]; // Un tableau pour stocker jusqu'à 10 positions (2 axes)

void feedback(){ // enregistre les feedback et creer leur correspondance sur l'echelle d'écriture des servos
  fd[0] =  analogRead(FDservo0);
  fd[1] =  analogRead(FDservo1);
  fd[2] =  analogRead(FDservo2);
  fd[3] =  analogRead(FDservo3);
  fd[4] =  analogRead(FDservo4);
  fd[5] =  analogRead(FDservo5);
  fd[6] =  analogRead(FDservo6);
  fd[7] =  analogRead(FDservo7);
  for(unsigned short int i =0;i<7;i++){
    fd[i] = map(fd[i], 661, 51, 0, 180);
  }
}


void receiveEvent(int numBytes) {
  while (Wire.available() && index < 100) {
    receivedArray[index++] = Wire.read(); // Lire chaque octet
  }

  for(int i=1 ; i< 9; i++)
  {
    target[i-1] = receivedArray[i];
  }
}

void requestEvent() {

    feedback();
    Wire.write(fd[0]); // Renvoyer la position actuelle du servo 1
    Wire.write(fd[1]); // Renvoyer la position actuelle du servo 2
    Wire.write(fd[2]);
    Wire.write(fd[3]);
    Wire.write(fd[4]);
    Wire.write(fd[5]); // servo 5 probleme feedback
    Wire.write(fd[6]);
    Wire.write(fd[7]);
  
}

int stepMove(short int position, short int TargetAngle, Servo &servo){ // fonction qui envoie le signal pwm correspondant
  if(position > TargetAngle){
    position = position - step;
    servo.write(position);
  }else if(position<TargetAngle){
    position = position + step;
    servo.write(position);
    }
  return position;
}

void recordPositions(){
  int tab[8];
  feedback();
  for(int i=0; i<8; i++)
  {
    recordedPositions[indexRecordedPositions][i] = fd[i];
  }
  
  indexRecordedPositions++;
  for(int i =0; i< 8; i++)
  {
    Serial.print(recordedPositions[indexRecordedPositions-1][i]);
    Serial.print(" ");
  }
  Serial.println("");
}

void move(short int TargetAngle[], short int actualPosition[]){


  short int positionServo[8];
  unsigned short int j = 0;
  unsigned short int cpt = 0;
  feedback();
  for(j = 0; j<8;j++){
    positionServo[j] = actualPosition[j];
  }
  // positionServo = recordPosition();
  while(cpt <= 6){ // creer une boucle qui incremante un step à la position des servos jusqu'à ce qu'ils soient à leur position final
    cpt=0;
    for(j=0; j<7; j++){    
        positionServo[j] = stepMove(positionServo[j],TargetAngle[j], servo[j]);
        if(positionServo[j] == TargetAngle[j]){
          cpt++;
        }
    }
    delay(speedDelay); // delai permettant de regler la vitesse
    Serial.println(cpt);
  }
  feedback(); // surement à supprimer
 
}


void attachServo(){ //active les broches avec les servos correspondants
  servo[0].attach(servo0);
  servo[1].attach(servo1);
  servo[2].attach(servo2);
  servo[3].attach(servo3);
  servo[4].attach(servo4);
  servo[5].attach(servo5);
  servo[6].attach(servo6);
  servo[7].attach(servo7);
  servo[8].attach(servo8);
}

void detachServo(){//desactive les broches avec les servos correspondants
  servo[0].detach();
  servo[1].detach();
  servo[2].detach();
  servo[3].detach();
  servo[4].detach();
  servo[5].detach();
  servo[6].detach();
  servo[7].detach();
  servo[8].detach();
}

void ouverturePince()
{
  servo[8].write(0);
}

void fermeturePince()
{
  servo[8].write(150);
}

void setup() {
  Wire.begin(I2C_ADDRESS); // Initialiser I2C en tant qu'esclave
  Wire.onReceive(receiveEvent); // Définir la fonction de réception
  Wire.onRequest(requestEvent);
  Serial.begin(9600); // Pour debug via le port série
  attachServo();
  for(int i=0; i<9; i++)
  {
    servo[i].write(90);
  }


  
  for(int i=0; i<8; i++)
  {
    targetMoinUn[i] = fd[i];
  }

  pinMode(FDservo0, INPUT);
  pinMode(FDservo1, INPUT);
  pinMode(FDservo2, INPUT);
  pinMode(FDservo3, INPUT);
  pinMode(FDservo4, INPUT);
  pinMode(FDservo5, INPUT);  
  pinMode(FDservo6, INPUT);
  pinMode(FDservo7, INPUT);

  fermeturePince();
  
}

void addOneAxe()
{

}



void loop() {
  // Afficher les données reçues (pour débogage)
  if (index > 0) {
    Serial.print("Tableau reçu : ");
    for (int i = 0; i < index; i++) {
      Serial.print(receivedArray[i]);
      Serial.print(" ");
    }
    Serial.println();
    index = 0; // Réinitialiser l'index pour recevoir de nouvelles données

    if (receivedArray[0] == 0) {
      detachServo();
    }
    else if(receivedArray[0] == 1)
    {
        attachServo();
        
    }
    else if (receivedArray[0] == 2) {
      recordPositions();
    }
    else if(receivedArray[0] == 3)
    {
      indexRecordedPositions = 0;
    }
    else if(receivedArray[0] == 4)
    {
      //attachServo(); a verifier parce que je passe la commande dans le client java
      short int temp[indexRecordedPositions];

      for(int i=0 ; i<indexRecordedPositions; i++)
      {
        move(recordedPositions[i]);
        delay(1000);
      }
      indexRecordedPositions = 0;
    
    }
    else if(receivedArray[0] == 5)
    {
      move(target, targetMoinUn);
      targetMoinUn = target;
    }
    else if(receivedArray[0] == 7)
    {
      ouverturePince();
    }
    else if(receivedArray[0] == 8)
    {
      fermeturePince();
    }
   
  }
  delay(100);
}
