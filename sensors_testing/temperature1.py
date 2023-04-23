import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create the ADC object
ads = ADS.ADS1115(i2c)

# set the gain and data rate
ads.gain = 2/3
ads.data_rate = 128

# create an analog input channel on the ADS1115
chan = AnalogIn(ads, ADS.P0)

# convert the analog reading to temperature in Celsius
while True:
    temp = chan.voltage * 100
    print('Temperature: {} C'.format(temp))
    time.sleep(1)
