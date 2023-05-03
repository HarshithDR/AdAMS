
import mysql.connector
from mysql.connector import Error


def insert_data(gyro_data, alcohol_data, temp_data, gps_data, impact_data, humidity_data):
  mycursor = connection.cursor()
  sql = "INSERT INTO adams (gyro_x, gyro_y, gyro_z, alcohol_detect, engine_temperature, coolant_temperature, ambient_temperature, latitude, longitute, impact_detect, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (gyro_data['x'], gyro_data['y'], gyro_data['z'], alcohol_data, temp_data[0], temp_data[1], temp_data[2], gps_data[0], gps_data[1], impact_data, humidity_data)
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

        gyro_data = {"x": 123, "y": 23, "z": 123}
        alcohol_data = True
        temp_data = [213, 324, 213]
        gps_data = [21341, 1234]
        impact_data = False
        humidity_data = 234.23

        insert_data(gyro_data, alcohol_data, temp_data, gps_data, impact_data, humidity_data)

except Error as e:

    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")





