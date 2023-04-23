from flask import Flask, render_template
import time
import random
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

data = [0] * 60

@app.route("/")
def index():
    return render_template("index.html")

def generate_graph():
    plt.plot(range(len(data)), data)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Data vs Time')
    buffer = BytesIO()
    plt.savefig("image.png", format='png')
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
    return buffer.read()

if __name__ == "__main__":
    app.run(debug=True)
