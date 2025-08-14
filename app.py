from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Dummy example values – replace with your analysis logic
        branch = "Computer Science"
        ats_score = 85
        skills = ["Python", "SQL", "Flask"]
        platforms = {
            "github": "github.com/example",
            "linkedin": "linkedin.com/in/example"
        }
        project_count = 3

        return render_template(
            'success.html',
            filename=filename,
            branch=branch,
            ats_score=ats_score,
            skills=skills,
            platforms=platforms,
            project_count=project_count
        )
    else:
        return 'Invalid file type. Please upload a PDF.'
@app.route('/view/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
