from flask import Flask, request
import os

app = Flask(__name__)
upload_dir = "server_uploads"
os.makedirs(upload_dir, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        request.files['image'].save(os.path.join(upload_dir, request.files['image'].filename))
    if 'label' in request.files:
        request.files['label'].save(os.path.join(upload_dir, request.files['label'].filename))
    if 'data_yaml' in request.files:
        request.files['data_yaml'].save(os.path.join(upload_dir, request.files['data_yaml'].filename))
    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)