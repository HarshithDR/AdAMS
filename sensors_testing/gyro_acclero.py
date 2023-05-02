from mpu6050 import mpu6050

sensor = mpu6050(0x68) # Address of MPU-6050 on the I2C bus

acceleration = sensor.get_accel_data()
print(f"Acceleration: x={acceleration['x']}, y={acceleration['y']}, z={acceleration['z']}")

gyro = sensor.get_gyro_data()
print(f"Gyro: x={gyro['x']}, y={gyro['y']}, z={gyro['z']}")
