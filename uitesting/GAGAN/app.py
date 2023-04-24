from flask import Flask, render_template
import time
import random
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, redirect, url_for
import time
import requests
import base64

app = Flask(__name__)
data = [0] * 60
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')
# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route('/')
def index():
    global data
    value= 10
    data.pop(0)
    data.append(value)
    buffer = generate_graph()
    buffer.seek(0)
    # return render_template("index.html")
    # return buffer.read()
    # Set up the longitude and latitude coordinates for the location
    lat = 12.9724
    lon = 77.5806

    # Construct the URL for the OpenMapTiles API call
    url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s-l+9ed4bd({lon},{lat})/{lon},{lat},14.5,0,0/800x600?access_token=pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGd0NXBmbWMxMGUwM2dvMmhleHByazhyIn0.KYJ2IhAhKanhB-5eD3XwVQ"

    # Make a request to the API and get the image data
    response = requests.get(url)
    image_data = response.content

    # Render the template with the image data
    return render_template('index.html', image_data=image_data)
def generate_graph():
    plt.plot(range(len(data)), data)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Data vs Time')
    buffer = BytesIO()
    plt.savefig("static/images/image.png", format='png')
    buffer.seek(0)
    plt.close()
    return buffer
@app.route("/update/<int:value>")
def update(value):
    global data
    data.pop(0)
    data.append(value)
    buffer = generate_graph()
    buffer.seek(0)
    # return render_template("index.html")
    # return buffer.read()
    return redirect(url_for("index"))
if __name__ == '__main__':
    app.run(debug=True)