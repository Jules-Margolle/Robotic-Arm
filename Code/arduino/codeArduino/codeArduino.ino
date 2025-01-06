#include <Arduino.h>
#include <Wire.h>

#define I2C_ADDRESS 0x08
#define MAX_BUFFER_SIZE 32

int receivedArray[100]; // Tableau pour stocker les données reçues
int index = 0;

void setup() {
  Wire.begin(I2C_ADDRESS); // Initialiser I2C en tant qu'esclave
  Wire.onReceive(receiveEvent); // Définir la fonction de réception
  Serial.begin(9600); // Pour debug via le port série
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

    
  }
  delay(100);
}

void receiveEvent(int numBytes) {
  while (Wire.available() && index < 100) {
    receivedArray[index++] = Wire.read(); // Lire chaque octet
  }
}