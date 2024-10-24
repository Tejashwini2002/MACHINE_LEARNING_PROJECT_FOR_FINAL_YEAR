'''
from flask import Flask, request, render_template, jsonify
import os
from data_processing import process_file
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed_files/'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Process the file
    processed_data = process_file(file_path)
    
    # Save processed data as JSON
    json_filename = f"{os.path.splitext(file.filename)[0]}.json"
    json_path = os.path.join(PROCESSED_FOLDER, json_filename)
    with open(json_path, 'w') as json_file:
        json.dump(processed_data, json_file, indent=4)
    
    return jsonify({"status": "success", "processed_file": json_filename})

if __name__ == "__main__":
    app.run(debug=True)
'''
from flask import Flask, request, render_template, jsonify
import os
import json
from data_processing import process_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed_files/'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Process the file
    processed_data = process_file(file_path)
    
    # Save processed data as JSON
    json_filename = f"{os.path.splitext(file.filename)[0]}.json"
    json_path = os.path.join(PROCESSED_FOLDER, json_filename)
    with open(json_path, 'w') as json_file:
        json.dump(processed_data, json_file, indent=4)
    
    return jsonify({"status": "success", "processed_file": json_filename})

# Route for searching through JSON files
@app.route('/search', methods=['POST'])
def search_files():
    keyword = request.form['keyword'].lower()
    result_files = []

    # Loop through all JSON files in the processed_files folder
    for json_filename in os.listdir(PROCESSED_FOLDER):
        json_path = os.path.join(PROCESSED_FOLDER, json_filename)
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
            # Search for the keyword in the content of the JSON file
            if 'content' in data and keyword in data['content'].lower():
                result_files.append({
                    'file_name': json_filename,
                    'content': data['content']
                })

    # If no files match the keyword
    if not result_files:
        return jsonify({"status": "no_results", "message": "No files matched the keyword"}), 404

    return jsonify({"status": "success", "files": result_files})

if __name__ == "__main__":
    app.run(debug=True)
