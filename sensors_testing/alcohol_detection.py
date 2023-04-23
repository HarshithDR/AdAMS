import time
import Adafruit_ADS1x15  # Import the ADS1x15 module

# Define the ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115()

# Define the voltage divider ratio for the MQ-3 sensor
V_DIVIDER_RATIO = 4.2

# Define the load resistance for the MQ-3 sensor
LOAD_RESISTANCE = 1.0  # kOhm

# Define the calibration factor for the MQ-3 sensor
CAL_FACTOR = 5.0

# Main loop
while True:
    # Read the ADC value from channel 0 (A0)
    adc_val_0 = adc.read_adc(0, gain=1)

    # Convert the ADC value to voltage
    voltage_0 = adc_val_0 * 4.096 / 32767

    # Calculate the MQ-3 sensor resistance based on the voltage divider circuit
    mq_resistance = (V_DIVIDER_RATIO * LOAD_RESISTANCE / voltage_0) - LOAD_RESISTANCE

    # Calculate the gas concentration based on the MQ-3 sensor resistance
    gas_conc = CAL_FACTOR * mq_resistance / LOAD_RESISTANCE

    # Print the sensor readings to the console
    print('ADC0: {0:.3f}V, MQ-3 resistance: {1:.3f} kOhm'.format(voltage_0, mq_resistance))
    print('Gas concentration: {0:.3f} ppm'.format(gas_conc))

    # Wait for 1 second before taking the next reading
    time.sleep(1)
