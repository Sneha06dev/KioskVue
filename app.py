import os
import subprocess
import webbrowser
from flask import Flask, json, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Load index.html

@app.route("/get_products")
def get_products():
    file_path = "output.json"

    if not os.path.exists(file_path):
        return jsonify({"error": "output.json not found"}), 404

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return jsonify(data)  # Return JSON response
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500

if __name__ == "__main__":  
    # Run air_write.py and wait for it to close
    subprocess.run(["python", "air_write.py"])  

    # After air_write.py is closed, run read_text.py
    subprocess.run(["python", "read_text.py"])  

    # Open browser only after read_text.py finishes
    webbrowser.open("http://127.0.0.1:5000")  

    # Start Flask server
    app.run(debug=True, use_reloader=False)
