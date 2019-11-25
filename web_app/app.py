from flask import Flask, flash, redirect, render_template, request, abort, url_for, jsonify, send_file
import json
from main import main
import os
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/results")
def results():
    return render_template('results.html')

@app.route("/api/custom_chart", methods=['POST'])
def custom_chart():
    data = request.form
    print("POST /api/custom_chart recieved")
    main(dict(data))
    return redirect(url_for('results'))

if __name__ == "__main__":
    app.run(debug=True)
