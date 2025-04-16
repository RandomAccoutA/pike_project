from flask_app import app
from flask import render_template, jsonify, request

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/button-press', methods=["POST"])
def button_press():
    data = request.get_json()

    button_name = data.get("button_name")

    return jsonify({"resp": "Test Response :)"})