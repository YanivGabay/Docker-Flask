from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Directory to store uploaded code files temporarily
UPLOAD_FOLDER = 'temp_codes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

# Handle POST requests to upload code files
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file to the temporary directory
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return jsonify({'message': f'File {file.filename} uploaded successfully'})

# Handle GET requests to execute code files
@app.route('/execute', methods=['GET'])
def execute():
    # List files in the temporary directory
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return jsonify({'error': 'No code files available for execution'})

    # For simplicity, let's execute the first file in the directory
    filename = files[0]
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Read the code file
    with open(filepath, 'r') as f:
        code = f.read()
    print(f"before the try block of post to the other container")
    
    # Forward the code to the Python executor
    executor_url = 'http://service2:5001/execute'

    try:
        print(f"trying to post request to: {executor_url}")
        response = requests.post(executor_url, json={'code': code})
        response.raise_for_status()  # Raise HTTPError for bad responses
        return jsonify(response.json())  # Ensure to jsonify the response correctly
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
