#define LED_OK 10
#define LED_KO 8

String incoming = "";

unsigned long previousMillis = 0;
const long interval = 400;   // vitesse du clignotement (ms)
bool ledState = false;

void setup() {
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_KO, OUTPUT);

  digitalWrite(LED_OK, LOW);
  digitalWrite(LED_KO, LOW);

  Serial.begin(9600);
}

void loop() {
  //  Lecture série
  if (Serial.available()) {
    incoming = Serial.readStringUntil('\n');
    incoming.trim();
  }

  // Gestion clignotement
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    ledState = !ledState;

    if (incoming == "OK") {
      digitalWrite(LED_OK, ledState);
      digitalWrite(LED_KO, LOW);
    }
    else if (incoming == "KO") {
      digitalWrite(LED_OK, LOW);
      digitalWrite(LED_KO, ledState);
    }
  }
}

