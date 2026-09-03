import json
import logging
import os
import sys
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

from test import get_dataset, get_corr

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "storage"))
project_root = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from data_science.development.choose_algorithm import choose_algorithm

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))

def safe_upload(uploaded_file):
    filename = secure_filename(uploaded_file.filename or "")
    if not filename.lower().endswith(".csv"):
        raise ValueError("A CSV file is required")
    os.makedirs(STORAGE_DIR, exist_ok=True)
    destination = os.path.abspath(os.path.join(STORAGE_DIR, filename))
    if os.path.commonpath([STORAGE_DIR, destination]) != STORAGE_DIR:
        raise ValueError("Invalid upload path")
    uploaded_file.save(destination)
    return destination

@app.route("/health")
def health(): return jsonify({"status": "ok"})

@app.route("/analyze-csv", methods=["POST"])
def analyze_csv():
    try:
        file_path = get_dataset(request.files.get("file"), "data_point", int(request.form.get("window_size", 15)))
        csv_path = os.path.abspath(os.path.join(project_root, file_path))
        if os.path.commonpath([project_root, csv_path]) != project_root:
            raise ValueError("Invalid result path")
        return send_file(csv_path, mimetype="text/csv", as_attachment=True, download_name="report.csv")
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid analysis request"}), 400
    except Exception:
        logging.exception("CSV analysis failed")
        return jsonify({"success": False, "message": "Analysis failed"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        save_path = safe_upload(request.files.get("file"))
        streams = json.loads(request.form.get("streams", "[]"))
        threshold = float(request.form["threshold"]) if request.form.get("threshold") else None
        df = pd.read_csv(save_path, parse_dates=["created_at"]).sort_values("created_at").set_index("created_at").interpolate()
        result = choose_algorithm(df, streams, request.form.get("start_date"), request.form.get("end_date"), threshold, request.form.get("algo_type"))
        clean = {stream: {key: to_native(value) for key, value in metrics.items()} for stream, metrics in result.items()}
        return jsonify({"result": clean})
    except (ValueError, KeyError, json.JSONDecodeError, AttributeError):
        return jsonify({"error": "Invalid analysis request"}), 400
    except Exception:
        logging.exception("Analysis failed")
        return jsonify({"error": "Analysis failed"}), 500

@app.route("/analyze-corr", methods=["POST"])
def analyze_corr():
    try:
        values = {name: int(request.form.get(name, default)) for name, default in {
            "window_size":15,"start_year":2025,"start_month":1,"start_day":1,"start_hour":0,"start_minute":0,"start_second":0,
            "end_year":2025,"end_month":1,"end_day":6,"end_hour":0,"end_minute":10,"end_second":0}.items()}
        corrs = get_corr(request.files.get("file"), request.form.get("time_col", "data_point"), values["window_size"], STORAGE_DIR,
            values["start_year"], values["start_month"], values["start_day"], values["start_hour"], values["start_minute"], values["start_second"],
            values["end_year"], values["end_month"], values["end_day"], values["end_hour"], values["end_minute"], values["end_second"])
        return jsonify({"success": True, "corrs": corrs})
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid correlation request"}), 400
    except Exception:
        logging.exception("Correlation analysis failed")
        return jsonify({"success": False, "message": "Correlation analysis failed"}), 500

def to_native(value): return value.item() if isinstance(value, np.generic) else value

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
