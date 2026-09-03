import json
import os
import sys
import logging
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath(os.path.join("data_science", "storage"))
ALLOWED_EXTENSIONS = {"csv"}
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from data_science.development.choose_algorithm import choose_algorithm

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))

def safe_upload(uploaded_file):
    filename = secure_filename(uploaded_file.filename or "")
    if not filename or "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("A CSV file is required")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    destination = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))
    if os.path.commonpath([UPLOAD_FOLDER, destination]) != UPLOAD_FOLDER:
        raise ValueError("Invalid upload path")
    uploaded_file.save(destination)
    return destination

@app.route("/")
def home():
    return "Server is up. POST multipart form data to /analyze"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return jsonify({"error": "CSV file is required"}), 400
        save_path = safe_upload(uploaded_file)
        streams = json.loads(request.form.get("streams", "[]"))
        threshold = float(request.form.get("threshold"))
        df = pd.read_csv(save_path, parse_dates=["created_at"])
        df.sort_values(by="created_at", inplace=True)
        df.set_index("created_at", inplace=True)
        df = df.interpolate()
        result = choose_algorithm(df, streams, request.form.get("start_date"), request.form.get("end_date"), threshold, request.form.get("algo_type"))
        clean = {stream: {key: to_native(value) for key, value in metrics.items()} for stream, metrics in result.items()}
        return jsonify({"result": clean})
    except (ValueError, KeyError, json.JSONDecodeError):
        return jsonify({"error": "Invalid analysis request"}), 400
    except Exception:
        logging.exception("Analysis failed")
        return jsonify({"error": "Analysis failed"}), 500

def to_native(value):
    return value.item() if isinstance(value, np.generic) else value

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
