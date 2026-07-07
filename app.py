from flask import Flask, request, jsonify, send_from_directory
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='public')

# Trỏ đường dẫn lưu trữ ra thư mục /share của Home Assistant
DATA_DIR = '/share/kiosk_media'
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

# Tự động tạo thư mục nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tạo file config mặc định nếu chưa có
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"playlist": [], "duration": 5, "transition": "fade"}, f)

# ... (GIỮ NGUYÊN TOÀN BỘ CÁC ROUTE BÊN DƯỚI NHƯ CŨ) ...

@app.route('/')
def admin():
    return app.send_static_file('index.html')

# ... (Giữ nguyên các route /viewer, /uploads, /upload, /files, /config) ...
@app.route('/viewer')
def viewer():
    return app.send_static_file('viewer.html')

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file", 400
    file = request.files['file']
    if file.filename == '':
        return "No filename", 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return "Uploaded successfully", 200

@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = request.json
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)
        return jsonify({"status": "success"})
    else:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)