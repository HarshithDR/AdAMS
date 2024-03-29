from flask import Flask, render_template, redirect, url_for
import time
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)
data1 = [0] * 60
data2 = [0] * 60
data3 = [0] * 60
count = 0

@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')

@app.route('/')
def index():
    global data1, data2, data3

    value1 = 10  # example value for graph 1
    value2 = 20  # example value for graph 2
    value3 = 30  # example value for graph 3

    data1.pop(0)
    data1.append(value1)

    data2.pop(0)
    data2.append(value2)

    data3.pop(0)
    data3.append(value3)

    buffer1 = generate_graph(data1)
    buffer2 = generate_graph(data2)
    buffer3 = generate_graph(data3)

    buffer1.seek(0)
    buffer2.seek(0)
    buffer3.seek(0)

    # Set up the longitude and latitude coordinates for the location
    lat = 12.9724
    lon = 77.5806

    # Construct the URL for the OpenMapTiles API call
    url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s-l+9ed4bd({lon},{lat})/{lon},{lat},14.5,0,0/800x600?access_token=pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGd0NXBmbWMxMGUwM2dvMmhleHByazhyIn0.KYJ2IhAhKanhB-5eD3XwVQ"

    # Make a request to the API and get the image data
    response = requests.get(url)
    image_data = response.content

    # Render the template with the image data and graph buffers
    return render_template('index.html', image_data=image_data, buffer1=buffer1.read(), buffer2=buffer2.read(), buffer3=buffer3.read())

@app.route("/update/<int:graph>/<int:value>")
def update(graph, value):
    global data1, data2, data3

    if graph == 1:
        data = data1
    elif graph == 2:
        data = data2
    elif graph == 3:
        data = data3

    data.pop(0)
    data.append(value)

    buffer = generate_graph(data)
    buffer.seek(0)

    return redirect(url_for("index"))

def generate_graph(data):
    plt.plot(range(len(data)), data)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Data vs Time')
    buffer = BytesIO()
    global count
    count = count+1
    plt.savefig("static/images/graph"+ str(count)+".png", format='png')
    buffer.seek(0)
    plt.close()
    return buffer

if __name__ == '__main__':
    app.run(debug=True)
