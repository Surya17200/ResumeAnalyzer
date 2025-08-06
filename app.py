from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from parser.resume_parser import extract_resume_text, extract_resume_data

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Handle file upload
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

        # Extract text and structured data
        resume_text = extract_resume_text(file_path)
        parsed_data = extract_resume_data(resume_text)

        return render_template(
            'success.html',
            filename=filename,
            resume_text=resume_text,
            parsed_data=parsed_data
        )
    else:
        return 'Invalid file type. Please upload a PDF or DOCX.'

# View uploaded resume (optional)
@app.route('/view/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run app
if __name__ == '__main__':
    print("🚀 Flask app starting...")
    app.run(debug=True)
