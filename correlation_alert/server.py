import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from main import detect_correlation_change_alert as run_correlation_pipeline

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
origins = [value.strip() for value in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",") if value.strip()]
CORS(app, origins=origins)

@app.route("/service-status", methods=["GET"])
def service_status():
    return jsonify({"status": "running", "message": "Correlation Alert Service is running.", "service": "correlation-alert-api"})

@app.route("/detect-correlation-alert", methods=["POST"])
def detect_correlation_alert_api():
    try:
        if "file" in request.files:
            uploaded_file = request.files["file"]
            if not (uploaded_file.filename or "").lower().endswith(".csv"):
                return jsonify({"error": "A CSV file is required"}), 400
            df = pd.read_csv(uploaded_file)
            timestamp_col = request.form.get("timestamp_col")
            selected = request.form.get("selected_streams")
            selected_streams = [value.strip() for value in selected.split(",")] if selected else None
            window_size = int(request.form.get("window_size", 30)); step_size = int(request.form.get("step_size", 5))
            method = request.form.get("method", "pearson")
        else:
            body = request.get_json(silent=True) or {}
            if not isinstance(body.get("data"), list): return jsonify({"error": "Missing or invalid data"}), 400
            df = pd.DataFrame(body["data"]); timestamp_col = body.get("timestamp_col"); selected_streams = body.get("selected_streams")
            window_size = int(body.get("window_size", 30)); step_size = int(body.get("step_size", 5)); method = body.get("method", "pearson")
        df.columns = df.columns.str.strip()
        if not timestamp_col or not selected_streams or method not in {"pearson", "spearman", "kendall"}:
            return jsonify({"error": "Invalid analysis parameters"}), 400
        if not 2 <= window_size <= 10000 or not 1 <= step_size <= window_size:
            return jsonify({"error": "Invalid window or step size"}), 400
        result = run_correlation_pipeline(df, timestamp_col, selected_streams, window_size, step_size, method)
        correlations = [{"window_index": item["window_index"], "start_time": str(item["start_time"]), "end_time": str(item["end_time"]),
            "window_size": item["window_size"], "correlation_matrix": item["correlation_matrix"].round(4).to_dict()} for item in result["correlation_results"]]
        return jsonify({"status":"success","summary":{"processed_rows":len(result["processed_data"]),"windows":len(result["windows"]),
            "correlation_results":len(result["correlation_results"]),"changes":len(result["changes"]),"alerts":len(result["alerts"])},
            "correlations":correlations,"alerts":result["alerts"],"changes":result["changes"]}), 200
    except (ValueError, TypeError, KeyError):
        return jsonify({"status": "error", "message": "Invalid analysis request"}), 400
    except Exception:
        logging.exception("Correlation alert analysis failed")
        return jsonify({"status": "error", "message": "Analysis failed"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
