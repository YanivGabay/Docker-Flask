from flask import Flask, request, jsonify
import subprocess
import re
import os
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
        class_file_name = f'{class_name}.class'  # Name of the compiled Java class file
    else:
      return jsonify({'error': 'No public class found in the provided code'}), 400
    with open(java_file_name, 'w') as f:
            f.write(code)

    try:
        # Compile the Java program
        compile_result = subprocess.run(['javac', java_file_name], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'error': compile_result.stderr})

        # Run the compiled Java program
        run_result = subprocess.run(['java', class_name], capture_output=True, text=True)
        if run_result.returncode != 0:
            return jsonify({'error': run_result.stderr})
        
        output = run_result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    finally:
        # Cleanup: Remove the Java source and class files
        if os.path.exists(java_file_name):
            os.remove(java_file_name)
        if os.path.exists(class_file_name):
            os.remove(class_file_name)
        
    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)
