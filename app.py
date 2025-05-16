from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hardware')
def hardware():
    return render_template('hardware.html')

@app.route('/coming_soon')
def coming_soon():
    return render_template('soon.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)