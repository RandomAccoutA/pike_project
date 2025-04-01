from flask_app import app
from flask import render_template, jsonify

button_text = "A"

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", button_text=button_text)

@app.route('/call-function', methods=['POST'])
def call_function():
    global button_text
    if button_text == "A":
        button_text = "B"
    else:
        button_text = "A"
    print(button_text)
    return jsonify({"button_text": button_text})