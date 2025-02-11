from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = 'static/images/uploads'
RESULT_FOLDER = 'static/images/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(image_path):
    input_image = Image.open(image_path)
    
    max_size = 1500
    if input_image.size[0] > max_size or input_image.size[1] > max_size:
        ratio = min(max_size / input_image.size[0], max_size / input_image.size[1])
        new_size = (int(input_image.size[0] * ratio), int(input_image.size[1] * ratio))
        input_image = input_image.resize(new_size, Image.LANCZOS)
    output_image = remove(input_image)
    return output_image

def change_background(foreground_path, background_path):
    
    foreground = cv2.imread(foreground_path, cv2.IMREAD_UNCHANGED)
    
    background = cv2.imread(background_path)
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    
   
    alpha_channel = foreground[:, :, 3] / 255.0
    alpha_3_channel = np.stack([alpha_channel] * 3, axis=-1)
    
    foreground_rgb = foreground[:, :, :3]
    result = background * (1 - alpha_3_channel) + foreground_rgb * alpha_3_channel
    
    return result.astype(np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Dosya yüklenmedi', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'Dosya seçilmedi', 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_image = remove_background(filepath)
        result_path = os.path.join(RESULT_FOLDER, f'no_bg_{filename}')
        output_image.save(result_path, 'PNG')
        
        return {'result_path': result_path}
    
    return 'İzin verilmeyen dosya türü', 400

@app.route('/change-background', methods=['POST'])
def change_background_route():
    if 'background' not in request.files:
        return 'Arka plan dosyası yüklenmedi', 400
    
    if 'foreground_path' not in request.form:
        return 'Ön plan dosyası belirtilmedi', 400
    
    background_file = request.files['background']
    foreground_path = request.form['foreground_path']
    
    if background_file.filename == '':
        return 'Arka plan dosyası seçilmedi', 400
    
    if background_file and allowed_file(background_file.filename):
        bg_filename = secure_filename(background_file.filename)
        bg_filepath = os.path.join(app.config['UPLOAD_FOLDER'], bg_filename)
        background_file.save(bg_filepath)
        
      
        result = change_background(foreground_path, bg_filepath)
        result_filename = f'final_{os.path.basename(foreground_path)}'
        result_path = os.path.join(RESULT_FOLDER, result_filename)
        cv2.imwrite(result_path, result)
        
        return {'result_path': result_path}
    
    return 'İzin verilmeyen dosya türü', 400

if __name__ == '__main__':
    app.run(debug=True) 