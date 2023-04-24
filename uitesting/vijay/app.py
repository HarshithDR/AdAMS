# from flask import Flask, render_template
import requests
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, request
import time

app = Flask(__name__)

#creating empty list for graphs
data1 = [0] * 60
data2 = [0] * 60
data3 = [0] * 60
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')

@app.route('/')
def index():

    # -------map---------------------------------------------
    # Set up the longitude and latitude coordinates for the location
    lat = 12.9724
    lon = 77.5806

    # Construct the URL for the OpenMapTiles API call
    url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s-l+9ed4bd({lon},{lat})/{lon},{lat},14.5,0,0/800x600?access_token=pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGd0NXBmbWMxMGUwM2dvMmhleHByazhyIn0.KYJ2IhAhKanhB-5eD3XwVQ"

    # Make a request to the API and get the image data
    response = requests.get(url)
    image_data = response.content


    # -------------------------------------------------------------------
    # ------notification---------------------------------------------------------------




    # -------------------------------------------------------------------
        # Render the template with the image data
    return render_template('index.html', image_data=image_data)

@app.route('/submit', methods=['POST'])
def submit():
    value = request.form['inputValue']
    if value == 'RED':
        return render_template('collision.html')
    else:
        return 'Value submitted: {}'.format(value)

if __name__ == '__main__':
    app.run(debug=True)
