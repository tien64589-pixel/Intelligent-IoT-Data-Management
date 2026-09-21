import sys
import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import json
import numpy as np

UPLOAD_FOLDER = os.path.join('data_science', 'storage')

# ensure the project root is on the import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data_science.development.choose_algorithm import choose_algorithm

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is up. POST JSON to /analyze"

@app.route('/analyze', methods=['POST'])
def analyze():
    streams = json.loads(request.form.get('streams')) if request.form.get('streams') else []
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    threshold = float(request.form.get('threshold'))
    algo_type = request.form.get('algo_type')

    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return 'No files were sent', 400

    if uploaded_file.filename == '':
        return 'No files selected', 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Security control: never use the client-supplied filename directly in a path.
    safe_filename = secure_filename(uploaded_file.filename)
    if not safe_filename or not safe_filename.lower().endswith('.csv'):
        return 'Only valid CSV files are accepted', 400

    upload_root = os.path.abspath(UPLOAD_FOLDER)
    save_path = os.path.abspath(os.path.join(upload_root, safe_filename))
    if os.path.commonpath([upload_root, save_path]) != upload_root:
        return 'Invalid upload path', 400

    uploaded_file.save(save_path)

    try:
        # Read CSV directly from file path
        df = pd.read_csv(save_path, parse_dates=['created_at'])
        df.sort_values(by='created_at', inplace=True)
        df.set_index('created_at', inplace=True)
        df = df.interpolate()

    except Exception as e:
        return f'Error in reading CSV: {e}', 400

    # run analysis
    try:
        result = choose_algorithm(df, streams, start_date, end_date, threshold, algo_type)
    except Exception as e:
        print('e', e)
        return jsonify({'error': str(e)}), 400

    print('result', result)

    clean_result = {}
    for stream, metrics in result.items():
        clean_metrics = {k: to_native(v) for k, v in metrics.items()}
        clean_result[stream] = clean_metrics

    return jsonify({"result": clean_result})

def to_native(val):
    if isinstance(val, np.generic):
        return val.item()
    return val

if __name__ == "__main__":
    # debug=True for auto-reload on edits
    app.run(host="0.0.0.0", port=5000, debug=True)