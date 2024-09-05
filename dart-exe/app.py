from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    temp_file_name = 'temp.dart'
    
    # Save the code to a temporary Dart file
    with open(temp_file_name, 'w') as f:
        f.write(code)

    try:
        # Run the Dart code using subprocess
        result = subprocess.run(['dart', temp_file_name], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = {'error': e.stderr}
    except Exception as ex:
        output = {'error': str(ex)}
    finally:
        # Cleanup: Remove the temporary Dart file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5003)
