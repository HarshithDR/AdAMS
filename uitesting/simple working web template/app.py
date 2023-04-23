from flask import Flask, render_template

app = Flask(__name__)

# dictionary containing sensor names and values
sensors = {
    "ambient temperature": "20 C",
    "oil temperature": "80 C",
    "coolant temperature": "60 C",
    "camera": "on",
    "alcohol": "off",
    "crash": "none",
    "coordinates": "(0, 0)"
}

@app.route('/')
def index():
    return render_template('index.html', sensors=sensors)

if __name__ == '__main__':
    app.run(debug=True)
