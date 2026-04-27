unsigned long lastMicros = 0;
const long interval = 200; // 200 microseconds = 5000 Hz

void setup() {
  Serial.begin(115200);
}

void loop() {
  // Use a timer instead of a simple delay for precision
  if (micros() - lastMicros >= interval) {
    lastMicros = micros();
    
    int sensorValue = analogRead(A0);
    // Scale here OR in Python. Let's do it here as you started.
    int scaledValue = sensorValue - 512;

    Serial.println(scaledValue);
  }
}