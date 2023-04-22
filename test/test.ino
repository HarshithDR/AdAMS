int mq3_pin = A0; // Set up the analog input pin for the MQ-3 sensor
int threshold = 700; // Define the alcohol detection threshold

void setup() {
  Serial.begin(9600); // Set up serial communication for debugging
}

void loop() {
  // Read the sensor value
  int alcohol_value = analogRead(mq3_pin);
  Serial.println(alcohol_value);

  // Check if the alcohol level is above the threshold
  if (alcohol_value > threshold) {
    Serial.println("ALCOHOL DETECTED");
  } else {
    Serial.println("NO ALCOHOL DETECTED");
  }

  // Wait for 1 second before taking the next reading
  delay(1000);
}
