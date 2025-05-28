from flask_app import app
from flask import render_template, jsonify, request
import pickle

from . import ml

@app.route('/')
@app.route('/index')
def index():
    #clear datasets (for debug purposes)
    with open("flask_app/ml_data.pkl", "wb") as f:
        pickle.dump({}, f)
    with open("flask_app/fw_data.pkl", "wb") as f:
        pickle.dump({}, f)

    return render_template("index.html")

@app.route('/button-press', methods=["POST"])
def button_press():
    nonml_words = ""
    ml_words = ""

    data = request.get_json()

    button_name = data.get("button_name")
    readout_words = data.get("readout_words")

    if data.get("is_run"):
        ml.process(readout_words)
        return jsonify({})

    if data.get("is_category"):
        file = open("flask_app/words/"+button_name+".txt", "r")
        nonml_words = file.read()
        file.close()

    ml_words = ml.generate(readout_words)

    return jsonify({"nonml": nonml_words, "ml": ml_words})