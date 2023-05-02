#importing required modules

import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import os
import glob
import Adafruit_ADS1x15
from mpu6050 import mpu6050
import serial
import pynmea2

# ---------------------------------------------------------------------
#gyro and accelero setup
sensor = mpu6050(0x68) # Address of MPU-6050 on the I2C bus

#impact setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# mq3(alcohol sensor) config
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
MQ3_PIN = 0

#temperature sensors config
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

#gps config
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# --------------------------------------------------------------------------

def gyro():
    gyro = sensor.get_gyro_data()
    print(f"Gyro: x={gyro['x']}, y={gyro['y']}, z={gyro['z']}")
    acceleration = sensor.get_accel_data()
    print(f"Acceleration: x={acceleration['x']}, y={acceleration['y']}, z={acceleration['z']}")
    return gyro, acceleration

def impact():
    input_state = GPIO.input(17)
    if input_state == False:
        print('Button Pressed')
        return False
    return True

def alcohol():
    value = adc.read_adc(MQ3_PIN, gain=GAIN)
    voltage = value / 32767.0 * 3.3  # Convert to voltage (assuming ADS1115 is set to +/- 4.096V range)

    print(f"Analog value: {value}, Voltage: {voltage:.2f}V")
    return voltage

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

def gps():
    try:
        # Read the GPS data from the serial connection
        data = ser.readline().decode('ascii', errors='replace')

        # Parse the NMEA sentence
        if data[0:6] == '$GPGGA':
            msg = pynmea2.parse(data)

            # Extract the latitude and longitude values
            lat = msg.latitude
            lon = msg.longitude

            # Print the latitude and longitude values
            print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}")
            return lat, lon
    except:
        return 'not connected'

if __name__ == '__main__':
    gyro()
    alcohol()
    gps()
    temperature_ds18b20()
    impact()
    ambient_humidity_temperature()
