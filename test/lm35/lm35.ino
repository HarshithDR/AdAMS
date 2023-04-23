// define the analog input pin for the LM35 sensor
const int lm35Pin = A0;

void setup() {
  // initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // read the voltage from the LM35 sensor
  float voltage = analogRead(lm35Pin) * 5.0 / 1023.0;

  // convert the voltage to temperature in Celsius
  float temperature = voltage * 100.0;

  // print the temperature to the serial monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");

  // wait for 1 second before reading again
  delay(1000);
}
