from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/example_image')
def example_image():
    image_path = 'static/images/image.png'
    return render_template('example_image.html', image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
