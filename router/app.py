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

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return jsonify({'message': f'File {file.filename} uploaded successfully'})

@app.route('/execute', methods=['GET'])
def execute():
    results = []
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return jsonify({'error': 'No code files available for execution'})

    for filename in files:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, 'r') as f:
            code = f.read()

        executor_url = determine_executor_url(filename)
        try:
            response = requests.post(executor_url, json={'code': code})
            response.raise_for_status()
            results.append({'file': filename, 'output': response.json()})
        except requests.exceptions.RequestException as e:
            results.append({'file': filename, 'error': str(e)})

    return jsonify(results)

def determine_executor_url(filename):
    if filename.endswith('.py'):
        return 'http://service2:5001/execute'
    elif filename.endswith('.java'):
        return 'http://service3:5002/execute'
  ##  elif filename.endswith('.dart'):
    #    return 'http://dart-executor:5003/execute'
    else:
        return None  # or a default executor if you have one

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
