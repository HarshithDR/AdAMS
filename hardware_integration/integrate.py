#importing required modules

import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import glob
import Adafruit_ADS1x15
from mpu6050 import mpu6050

# ---------------------------------------------------------------------
#gyro and accelero setup
sensor = mpu6050(0x68) # Address of MPU-6050 on the I2C bus

#impact setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# mq3(alcohol sensor) config
adc = Adafruit_ADS1x15.ADS1115()   # Define the ADS1115 ADC object
# Define the voltage divider ratio for the MQ-3 sensor
V_DIVIDER_RATIO = 4.2
# Define the load resistance for the MQ-3 sensor
LOAD_RESISTANCE = 1.0  # kOhm
# Define the calibration factor for the MQ-3 sensor
CAL_FACTOR = 5.0

#temperature sensors config
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

# --------------------------------------------------------------------------

def gyro():
    gyro = sensor.get_gyro_data()
    print(f"Gyro: x={gyro['x']}, y={gyro['y']}, z={gyro['z']}")
    return gyro

def acceleration():
    acceleration = sensor.get_accel_data()
    print(f"Acceleration: x={acceleration['x']}, y={acceleration['y']}, z={acceleration['z']}")
    return acceleration

def impact():
    input_state = GPIO.input(17)
    if input_state == False:
        print('Button Pressed')
        return False
    return True

def alcohol():
    # Read the ADC value from channel 0 (A0)
    adc_val_0 = adc.read_adc(0, gain=1)

    # Convert the ADC value to voltage
    voltage_0 = adc_val_0 * 4.096 / 32767

    # Calculate the MQ-3 sensor resistance based on the voltage divider circuit
    mq_resistance = (V_DIVIDER_RATIO * LOAD_RESISTANCE / voltage_0) - LOAD_RESISTANCE

    # Calculate the gas concentration based on the MQ-3 sensor resistance
    gas_conc = CAL_FACTOR * mq_resistance / LOAD_RESISTANCE

    # Print the sensor readings to the console
    # print('ADC0: {0:.3f}V, MQ-3 resistance: {1:.3f} kOhm'.format(voltage_0, mq_resistance))
    print('Gas concentration: {0:.3f} ppm'.format(gas_conc))

    return gas_conc

def ambient_humidity_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    return temperature, humidity


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
def temperature_ds18b20():
    temp= []
    for device_folder in device_folders:
        device_file = device_folder + '/w1_slave'
        print("Temperature sensor", device_folder[-15:], ":", read_temp(device_file), "C")
        temp.append(read_temp(device_file))
    return temp


