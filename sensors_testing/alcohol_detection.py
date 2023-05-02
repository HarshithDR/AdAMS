import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
MQ3_PIN = 0

while True:
    value = adc.read_adc(MQ3_PIN, gain=GAIN)
    voltage = value / 32767.0 * 3.3 # Convert to voltage (assuming ADS1115 is set to +/- 4.096V range)

    print(f"Analog value: {value}, Voltage: {voltage:.2f}V")

    time.sleep(0.1) # Sleep for 100ms before taking the next measurement
