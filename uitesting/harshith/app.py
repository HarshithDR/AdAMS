import time
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

# Initialize list with 60 zeroes
data_list = [0] * 60

# Function to update data_list with user input
def update_data_list(value):
    data_list.pop(0)
    data_list.append(value)

# Route for the main web page
@app.route('/')
def index():
    # Get current time
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Render three graph panels with data_list
    graph1 = generate_graph_panel(data_list, 'Graph Panel 1')
    graph2 = generate_graph_panel(data_list, 'Graph Panel 2')
    graph3 = generate_graph_panel(data_list, 'Graph Panel 3')

    # Render map panel with Mapbox API
    map_panel = generate_map_panel()

    # Render event panel
    sleep_status = False
    crash_status = False
    alcohol_status = False
    event_panel = generate_event_panel(sleep_status, crash_status, alcohol_status)

    # Render main page with all components
    return render_template('index.html', current_time=current_time, graph1=graph1, graph2=graph2, graph3=graph3, map_panel=map_panel, event_panel=event_panel)

# Function to generate a graph panel with data_list
def generate_graph_panel(data, title):
    plt.figure(figsize=(6, 4))
    plt.plot(data)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)
    plt.savefig('static/images/{}.png'.format(title.replace(" ", "_")))
    plt.close()
    return title.replace(" ", "_")

# Function to generate a map panel with Mapbox API
def generate_map_panel():
    # Use your own Mapbox API key and coordinates
    api_key = 'pk.eyJ1Ijoiam9obi1kZW82NTQ2NjQ2NCIsImEiOiJjbGd0NXBmbWMxMGUwM2dvMmhleHByazhyIn0.KYJ2IhAhKanhB-5eD3XwVQ'
    latitude = '12.9724'
    longitude = '77.5806'
    map_url = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{},{},15,0,0/600x400?access_token={}'.format(longitude, latitude, api_key)
    return map_url

# Function to generate an event panel
def generate_event_panel(sleep_status, crash_status, alcohol_status):
    sleep_alert = ''
    crash_alert = ''
    alcohol_alert = ''
    if sleep_status:
        sleep_alert = 'Sleep status: True'
    if crash_status:
        crash_alert = 'Crash status: True'
    if alcohol_status:
        alcohol_alert = 'Alcohol status: True'
    return '{}<br>{}<br>{}'.format(sleep_alert, crash_alert, alcohol_alert)

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')