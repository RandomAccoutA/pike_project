from flask_app import app
from flask import render_template, jsonify

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")