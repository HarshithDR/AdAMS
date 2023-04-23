from flask import Flask, render_template
from mapbox import Geocoder, Static
from urllib import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
geocoder = Geocoder(access_token='pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGdyd295aGQxY2NnM3JsaG1renk4bmtvIn0.G-0NFXogdDoZcwOaf3QpQg')

def get_location(address):
    response = geocoder.forward(address)
    location = response.geojson()['features'][0]['geometry']['coordinates']
    return location

static = Static(access_token='pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGdyd295aGQxY2NnM3JsaG1renk4bmtvIn0.G-0NFXogdDoZcwOaf3QpQg')

def get_map(location):
    image = static.image('mapbox/streets-v11', lonlat=location, width=800, height=600, zoom=12)
    return image.url
@app.route('/map', methods=['POST'])
def map():
    address = request.form['address']
    location = get_location(address)
    map_url = get_map(location)
    return render_template('map.html', map_url=map_url)


if __name__ == "__main__":
    app.run(debug=True)
