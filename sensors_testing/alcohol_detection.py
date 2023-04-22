import time
import Adafruit_ADS1x15  # Import the ADS1x15 module
import RPi.GPIO as GPIO

# Define the ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Define the GPIO pin connected to the MQ-3 sensor digital output
MQ_PIN = 18

# Set up the GPIO pin for the MQ-3 sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(MQ_PIN, GPIO.IN)

# Define the calibration factor for the MQ-3 sensor
CAL_FACTOR = 5.0

# Main loop
while True:
    # Read the ADC values from channel 0 (A0) and channel 1 (A1)
    adc_val_0 = adc.read_adc(0, gain=1)
    adc_val_1 = adc.read_adc(1, gain=1)

    # Convert the ADC values to voltage
    voltage_0 = adc_val_0 * 4.096 / 32767
    voltage_1 = adc_val_1 * 4.096 / 32767

    # Read the digital output from the MQ-3 sensor
    mq_val = GPIO.input(MQ_PIN)

    # Calculate the alcohol concentration based on the MQ-3 sensor reading
    alcohol_conc = mq_val * CAL_FACTOR

    # Print the sensor readings to the console
    print('ADC0: {0:.3f}V, ADC1: {1:.3f}V, MQ-3: {2}'.format(voltage_0, voltage_1, mq_val))
    print('Alcohol concentration: {0:.3f} ppm'.format(alcohol_conc))

    # Wait for 1 second before taking the next reading
    time.sleep(1)
