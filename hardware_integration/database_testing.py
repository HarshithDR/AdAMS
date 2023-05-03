
import mysql.connector
from mysql.connector import Error


def insert_data(gyro_data,acceleration, alcohol_data, temp_data, lat,lon, impact_data,ambient_temp, humidity_data):
  mycursor = connection.cursor()
  sql = "INSERT INTO adams (gyro_x, gyro_y, gyro_z,accelero_x,accelero_y,accelero_z, alcohol_detect, engine_temperature, coolant_temperature,ambient_temperature, latitude, longitude, impact_detect, Humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"

  val = (gyro_data['x'], gyro_data['y'], gyro_data['z'], acceleration[0], acceleration[1], acceleration[2],
         str(alcohol_data), temp_data[0], temp_data[1], ambient_temp, lat, lon, str(impact_data), humidity_data)

  mycursor.execute(sql, val)
  connection.commit()

hostname = "1o7.h.filess.io"

database = "adams_wearforce"

port = "3307"

username = "adams_wearforce"

password = "086bb173a54213e78a9d31b06b0f32b70da0adc4"

try:
    connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        gyro, acceleration = {'x':6.546565956595659562,'y':0,'z':0},[651,541,654]
        alcohol = 'false'
        # lat, lon = gps1()
        temp = [0,0]
        crash = 'fasle'
        lat, lon = 0, 0
        ambient_temp, humidity = 123,123
        insert_data(gyro,acceleration, alcohol, temp,lat,lon , crash, ambient_temp,humidity)

except Error as e:

    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")





