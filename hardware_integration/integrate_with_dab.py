# importing required modules

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
import mysql.connector
from mysql.connector import Error

# ---------------------------------------------------------------------
# gyro and accelero setup
sensor = mpu6050(0x68)  # Address of MPU-6050 on the I2C bus

# impact setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# mq3(alcohol sensor) config
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
MQ3_PIN = 0

# temperature sensors config
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

# gps config
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
# --------------------------------------------------------------------------

#---------------------------------credentials------------------------------
hostname = "1o7.h.filess.io"
database = "adams_wearforce"
port = "3307"
username = "adams_wearforce"
password = "086bb173a54213e78a9d31b06b0f32b70da0adc4"
#-------------------------------------------------------------------------------

#----------------------------db connection-----------------------
connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password,
                                             port=port)
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

def gyro():
    gyro = sensor.get_gyro_data()
    print(f"Gyro: x={gyro['x']}, y={gyro['y']}, z={gyro['z']}")
    acceleration = sensor.get_accel_data()
    print(f"Acceleration: x={acceleration['x']}, y={acceleration['y']}, z={acceleration['z']}")
    return gyro, acceleration


def impact():
    input_state = GPIO.input(26)
    if input_state == False:
        print('crash detected')
        return 'true'
    else:
        print('no crash detected')
        return 'false'


def alcohol():
    value = adc.read_adc(MQ3_PIN, gain=GAIN)
    voltage = value / 32767.0 * 3.3  # Convert to voltage (assuming ADS1115 is set to +/- 4.096V range)
    print(f"Analog value: {value}, Voltage: {voltage:.2f}V")
    if voltage >= 0.9:
        print('alcohol detected')
        return 'true'
    else:
        return 'false'


def ambient_humidity_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)
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
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def temperature_ds18b20():
    temp = []
    for device_folder in device_folders:
        device_file = device_folder + '/w1_slave'
        print("Temperature sensor", device_folder[-15:], ":", read_temp(device_file), "C")
        temp.append(read_temp(device_file))
    return temp


def gps1():
    temp = True
    while temp:
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
                temp = False

        except:
            return 'not connected'
    return lat, lon

def insert_data(gyro_data,acceleration, alcohol_data, temp_data, lat,lon, impact_data,ambient_temp, humidity_data):
  mycursor = connection.cursor()
  sql = "INSERT INTO adams (gyro_x, gyro_y, gyro_z,accelero_x,accelero_y,accelero_z, alcohol_detect, engine_temperature, coolant_temperature," \
        " ambient_temperature, latitude, longitute, impact_detect, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

  val = (gyro_data['x'], gyro_data['y'], gyro_data['z'],acceleration['x'],acceleration['y'],acceleration['z'],
         alcohol_data, temp_data[0], temp_data[1], lat, lon, impact_data,ambient_temp, humidity_data)

  mycursor.execute(sql, val)
  connection.commit()

def database(gyro_data,acceleration,alcohol_data,lat,lon,temp_data,impact_data,ambient_temp,humidity):
    insert_data(gyro_data,acceleration, alcohol_data, temp_data,lat,lon , impact_data, ambient_temp,humidity)

    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")

if __name__ == '__main__':
    gyro, acceleration = gyro()
    alcohol = alcohol()
    lat, lon = gps1()
    temp = temperature_ds18b20()
    crash = impact()
    ambient_temp, humidity = ambient_humidity_temperature()
    try:
        database(gyro,acceleration,alcohol,lat,lon,temp,crash,ambient_temp,humidity)
    except Error as e:
        print("Error while connecting to MySQL", e)