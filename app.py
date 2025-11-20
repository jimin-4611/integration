import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Flask 앱 생성
app = Flask(__name__)

# 업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
# 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 업로드 크기 16MB 제한

# 허용된 파일 확장자 확인 함수
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected file'}), 400

    saved_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # 여기에 이미지 처리 로직 추가 예정 (OpenCV, EasyOCR 등)
            # 현재는 단순히 저장된 파일 경로만 반환
            
            # 파일 타입 확인 (간단한 로직)
            file_type = 'pdf' if filename.lower().endswith('.pdf') else 'image'
            
            saved_files.append({
                'name': filename,
                'path': filepath,
                'type': file_type
            })

    return jsonify({'message': 'Files uploaded successfully', 'files': saved_files}), 200

if __name__ == '__main__':
    app.run(debug=True)