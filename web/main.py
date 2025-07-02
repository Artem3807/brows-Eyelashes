from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, template_folder='./') # указывает на текущую директорию

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('media/'):
        return send_from_directory('media', path[6:])
    return send_from_directory('.', path)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False) 