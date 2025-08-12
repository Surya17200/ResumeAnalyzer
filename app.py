from flask import Flask, render_template, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename
from parser.resume_parser import extract_resume_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return 'No file part'

    file = request.files['resume']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        resume_text = extract_resume_text(filepath)
        return render_template('success.html', filename=filename, resume_text=resume_text)
    else:
        return 'Invalid file type. Please upload PDF/DOCX.'

@app.route('/view/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
