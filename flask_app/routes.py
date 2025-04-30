from flask_app import app
from flask import render_template, jsonify, request

from . import ml

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/button-press', methods=["POST"])
def button_press():
    nonml_words = ""

    data = request.get_json()

    button_name = data.get("button_name")

    if data.get("is_category"):
        file = open("flask_app/words/"+button_name+".txt", "r")
        nonml_words = file.read()
        file.close()

    ml_words = ml.generate(data.get("word_history"), data.get("readout_state"))

    return jsonify({"nonml": nonml_words, "ml": ml_words})