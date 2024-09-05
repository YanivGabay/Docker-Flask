from flask import Flask,request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/upload",methods=["POST"])
def upload():
    return "code uploaded successfully"

@app.route('/execute',methods=['GET'])
def execute():
    return "code executed successfully"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)