from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import requests
import base64

app = Flask(__name__)

# ---------------------------------credentials------------------------------
hostname = "9tf.h.filess.io"

database = "Adams_zebraherd"

port = "3307"

username = "Adams_zebraherd"

password = "ba2bdd0191f298555f884c5b21d437e60351fbd7"
# -------------------------------------------------------------------------------

# ----------------------------db connection-----------------------
mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password,
                                     port=port)

if mydb.is_connected():
    db_Info = mydb.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = mydb.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

# Function to get data from the MySQL database
def get_data():
    # Query to get the required data
    query = "SELECT * FROM AdamsEast LIMIT 30"
    # query = "SELECT * FROM adams_final WHERE current_time >= %s ORDER BY timestamp DESC LIMIT 30"
    # Execute the query and get the data
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    # Convert the data into a Pandas DataFrame
    df = pd.DataFrame(data, columns=['gyro_x', 'gyro_y', 'gyro_z','accelero_x','accelero_y','accelero_z', 'alcohol_detect', 'engine_temperature', 'coolant_temperature','ambient_temperature', 'latitude', 'longitude', 'impact_detect', 'humidity'])
    return df

# Function to get the map image from the map.io API
def get_map_image(lat, lon):
    url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s-l+9ed4bd({lon},{lat})/{lon},{lat},14.5,0,0/800x600?access_token=pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGd0NXBmbWMxMGUwM2dvMmhleHByazhyIn0.KYJ2IhAhKanhB-5eD3XwVQ"

    # Make a request to the API and get the image data
    response = requests.get(url)
    # image_data = response.content
    return response.content


# Route for the home page
@app.route('/')
def home():
    count = [i for i in range(1, 31)]
    # Get the data from the MySQL database
    df = get_data()
    # print(df['engine_temperature'][:-29])
    # Create line graphs for temperature vs time
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    axs[0, 0].plot(count, df['engine_temperature'])
    axs[0, 0].set_title('Engine temperature')
    axs[0, 1].plot(count, df['coolant_temperature'])
    axs[0, 1].set_title('Coolant temperature')
    axs[1, 0].plot(count, df['ambient_temperature'])
    axs[1, 0].set_title('Ambient temperature')
    axs[1, 1].plot(count, df['humidity'])
    axs[1, 1].set_title('Humidity')
    # Convert the Matplotlib figure to a base64-encoded string
    fig_base64 = fig_to_base64(fig)

    # Get the table data
    table_data = df[['alcohol_detect', 'impact_detect']].to_dict('records')
    # Get the map image
    latitude = df['latitude'][0]
    longitude = df['longitude'][0]
    map_image = get_map_image(latitude, longitude)
    # Render the template with the data
    return render_template('index.html', fig=fig_base64, table_data=table_data, map_image=map_image)

# Function to convert a Matplotlib figure to a base64-encoded string
def fig_to_base64(fig):
    import io
    from base64 import b64encode
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return b64encode(buf.read()).decode('utf-8')

@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True,host='192.168.136.208', port=5000)
