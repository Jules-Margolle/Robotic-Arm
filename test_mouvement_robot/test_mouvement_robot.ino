#include <Servo.h>

/*

CHANGER EN FONCTION DU NOMBRE DE SERVOS

*/

const int maxSpeedDelay = 100;    // Vitesse maximale (délai minimal entre pas) !!!!!! vitesse max 35 ne pas mettre en dessous !!!!!!! c'est dangereux
const float accelerationStep = 0.000001;

const int NUM_SERVOS = 4;  
Servo servos[NUM_SERVOS];  


const int servoPins[NUM_SERVOS] = {3, 4, 5, 7};       
const int positionPins[NUM_SERVOS] = {A3, A4, A5, A7}; 

int centre = 90;
int recordedPositions[10][NUM_SERVOS];  
int numRecorded = 0;  


const int servoDelay = 500; 

int readServoFeedback(int feedbackPin) {
  return map(analogRead(feedbackPin), 51, 661, 0, 180);
}

void moveServosSyncWithAcceleration(Servo &servoA, Servo &servoB, int startAngle, int targetAngle, int maxSpeedDelay, int accelerationStep) {
  int step = (startAngle < targetAngle) ? 1 : -1;
  int stepDelay = maxSpeedDelay;
  int acceleration = accelerationStep;
  int angle1;
  int angle2;
  angle1  = 180-startAngle;
  angle2 = 0 + startAngle;

  Serial.println(angle1);
  Serial.println(angle2);


  servoA.write(angle1);
  servoB.write(angle2);

  for (int angle = startAngle; angle != targetAngle; angle += step) {
    servoA.write(angle1-step);
    servoB.write(angle2+step);
    delay(stepDelay);
    
    // if (stepDelay > maxSpeedDelay / 2) { 
    //   stepDelay -= acceleration; 
    // } else if (abs(targetAngle - angle) < 20) { 
    //   stepDelay += acceleration; 
    // }
    
    // stepDelay = constrain(stepDelay, 2, maxSpeedDelay);
  }
  
  servoA.write(targetAngle);
  servoB.write(targetAngle);
}

void moveServoWithAcceleration(Servo &servo, int startAngle, int targetAngle, int maxSpeedDelay, int accelerationStep) {
  int step = (startAngle < targetAngle) ? 1 : -1; // Détermine la direction du mouvement
  int stepDelay = maxSpeedDelay;                 // Délai actuel entre les pas (commence lentement)
  int acceleration = accelerationStep;           // Valeur pour ajuster l'accélération
  
  // Boucle pour déplacer progressivement le servo
  for (int angle = startAngle; angle != targetAngle; angle += step) {
    servo.write(angle);
    delay(stepDelay); // Contrôle la vitesse avec le délai
    
    // // Ajustement du délai pour simuler l'accélération/décélération
    // if (stepDelay > maxSpeedDelay / 2) { 
    //   stepDelay -= acceleration; // Accélération (réduction du délai)
    // } else if (abs(targetAngle - angle) < 20) { 
    //   stepDelay += acceleration; // Décélération à l'approche de la cible
    // }
    
    // stepDelay = constrain(stepDelay, 2, maxSpeedDelay); // Limite les valeurs de stepDelay
  }
  
  servo.write(targetAngle); // Assure d'arriver précisément à l'angle cible
}

void setup() {
  Serial.begin(9600);
  
/*
  for (int i = 0; i < NUM_SERVOS; i++) {
    
    
  }*/
  delay(2000);

  Serial.println("Prêt à enregistrer les positions. Appuyez sur le bouton ou entrez 's' pour sauvegarder.");
}



void saveServoPositions() {
  if (numRecorded < 10) {  
    Serial.print("Enregistrement de la position : ");
    for (int i = 0; i < NUM_SERVOS; i++) {

      int positionValue = analogRead(positionPins[i]);
      recordedPositions[numRecorded][i] = map(positionValue, 51, 661, 0, 180); 
      Serial.print(recordedPositions[numRecorded][i]);
      Serial.print(" ");
    }
    Serial.println();
    numRecorded++;
  } else {
    Serial.println("Mémoire pleine ! Supprimez des positions pour en ajouter.");
  }
}


void playRecordedPositions() {
  Serial.println("Relecture des positions enregistrées...");
  for (int i = 0; i < numRecorded; i++) {
    Serial.print("Position ");
    Serial.print(i + 1);
    Serial.print(": ");
    
    /*
    moveServosSyncWithAcceleration(servos[0], servos[1], readServoFeedback(A3), recordedPositions[i][0], maxSpeedDelay, accelerationStep);
    moveServosSyncWithAcceleration(servos[2], servos[3], readServoFeedback(A5), recordedPositions[i][2], maxSpeedDelay, accelerationStep);
    moveServoWithAcceleration(servos[4], readServoFeedback(A7),recordedPositions[i][4],maxSpeedDelay, accelerationStep);
    */
    moveServosSyncWithAcceleration(servos[0], servos[1], readServoFeedback(A3), recordedPositions[i][0], maxSpeedDelay, accelerationStep);
    moveServosSyncWithAcceleration(servos[2], servos[3], readServoFeedback(A5), recordedPositions[i][2], maxSpeedDelay, accelerationStep);
    moveServoWithAcceleration(servos[4], readServoFeedback(A7),recordedPositions[i][4],maxSpeedDelay, accelerationStep);
    //moveServoWithAcceleration(servos[5], readServoFeedback(A8),recordedPositions[i][5],maxSpeedDelay, accelerationStep);

    
    
    Serial.println();
    delay(servoDelay);  
  }
  Serial.println("Relecture terminée.");
}

void loop() {


  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 's') {
      saveServoPositions();
    } else if (command == 'p') {
      for(int i=0; i< NUM_SERVOS;i++)
      {
        servos[i].attach(servoPins[i]);
        servos[i].write(centre);
      }
      playRecordedPositions();
    }
  }
}
