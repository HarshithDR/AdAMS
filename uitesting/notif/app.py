from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    value = request.form['inputValue']
    if value == 'RED':
        return render_template('collision.html')
    else:
        return 'Value submitted: {}'.format(value)

if __name__ == '__main__':
    app.run(debug=True)
