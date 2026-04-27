unsigned long lastMicros = 0;
const long interval = 200; // 200 microseconds = 5000 Hz

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (micros() - lastMicros >= interval) {
    lastMicros = micros();
    
    int sensorValue = analogRead(A0);
    int scaledValue = sensorValue - 512;

    Serial.println(scaledValue);
  }
}