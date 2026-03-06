from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from steganography import SecureSteganography

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

stego = SecureSteganography()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hide', methods=['GET', 'POST'])
def hide_data():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image file selected')
            return redirect(request.url)
        
        file = request.files['image']
        secret_data = request.form['secret_data']
        password = request.form['password']
        
        if file.filename == '' or not secret_data or not password:
            flash('Please provide all required fields')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)
            
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_stego.png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            success, message = stego.hide_data(input_path, secret_data, password, output_path)
            
            if success:
                flash('Data hidden successfully!')
                return render_template('hide.html', success=True, output_file=output_filename)
            else:
                flash(f'Error: {message}')
        else:
            flash('Invalid file type. Please use PNG, JPG, JPEG, or BMP.')
    
    return render_template('hide.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract_data():
    if request.method == 'POST':
        if 'stego_image' not in request.files:
            flash('No stego image file selected')
            return redirect(request.url)
        
        file = request.files['stego_image']
        password = request.form['password']
        
        if file.filename == '' or not password:
            flash('Please provide all required fields')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stego_path = os.path.join(UPLOAD_FOLDER, f"extract_{filename}")
            file.save(stego_path)
            
            success, result = stego.extract_data(stego_path, password)
            
            if success:
                return render_template('extract.html', success=True, extracted_data=result)
            else:
                flash(f'Error: {result}')
        else:
            flash('Invalid file type. Please use PNG, JPG, JPEG, or BMP.')
    
    return render_template('extract.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

@app.route('/capacity', methods=['GET', 'POST'])
def check_capacity():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image file selected')
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '' or not allowed_file(file.filename):
            flash('Please select a valid image file')
            return redirect(request.url)
        
        tmp_path = os.path.join(UPLOAD_FOLDER, f"temp_{secure_filename(file.filename)}")
        file.save(tmp_path)
        capacity = stego.get_image_capacity(tmp_path)
        try:
            os.remove(tmp_path)
        except:
            pass
        
        return render_template('capacity.html', capacity=capacity, filename=file.filename)
    
    return render_template('capacity.html')

if __name__ == '__main__':
    app.run(debug=True)
