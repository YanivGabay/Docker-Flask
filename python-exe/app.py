from flask import Flask, request, jsonify
import subprocess
import os
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    temp_file_name = 'temp.py'
    # Save the code to a temporary Python file
    with open('temp.py', 'w') as f:
        f.write(code)

    try:
        # Run the Python code using subprocess
        result = subprocess.run(['python', temp_file_name], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr})  # Also jsonify here
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500  # Also jsonify here
    finally:
        #clean up the temp file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
