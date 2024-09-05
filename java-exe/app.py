from flask import Flask, request, jsonify
import subprocess
import re
app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    class_match = re.search(r'public class (\w+)' , code)
    if class_match:
        class_name = class_match.group(1)
        java_file_name = f'{class_name}.java'
    else:
      return jsonify({'error': 'No public class found in the provided code'}), 400
    with open(java_file_name, 'w') as f:
            f.write(code)

    try:
       # Compile and run the Java program
        compile_result = subprocess.run(['javac', java_file_name], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'error': compile_result.stderr})

        run_result = subprocess.run(['java', class_name], capture_output=True, text=True)
        if run_result.returncode != 0:
            return jsonify({'error': run_result.stderr})
        
        return jsonify({'output': run_result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)
