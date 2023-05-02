import serial
import pynmea2

# Open the serial connection to the NEO-6M module
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

while True:
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
    except KeyboardInterrupt:
        quit()
    except:
        pass