from flask import Flask, render_template, request, redirect, url_for
from main import create_graph
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/results")
def results():
    return render_template('results.html')

@app.route("/api/custom_chart", methods=['POST'])
def custom_chart():
    data = request.form
    create_graph(dict(data))
    return redirect(url_for('results'))

if __name__ == "__main__":
    app.run(debug=True)
