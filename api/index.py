from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from parser.resume_parser import extract_resume_text
from vercel_flask import Vercel

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'  # Vercel's temp folder
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        text = extract_resume_text(file_path)
        return render_template('success.html', filename=filename, extracted_text=text)
    return 'Invalid file type.'

@app.route('/view/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Adapt for Vercel
app = Vercel(app)
