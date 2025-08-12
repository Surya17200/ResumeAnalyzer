from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from parser.resume_parser import extract_resume_text, parse_resume, calculate_ats_score

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

        # Extract & Parse
        resume_text = extract_resume_text(filepath)
        parsed_data = parse_resume(resume_text)

        # ATS Score
        total_possible_skills = set(parsed_data["skills"])
        ats_score = calculate_ats_score(
            parsed_data["skills"],
            total_possible_skills,
            parsed_data["platforms"],
            parsed_data["project_count"]
        )

        return render_template(
            'success.html',
            filename=filename,
            branch=parsed_data["branch"],
            skills=parsed_data["skills"],
            platforms=parsed_data["platforms"],
            project_count=parsed_data["project_count"],
            ats_score=ats_score
        )
    else:
        return 'Invalid file type. Please upload a PDF or DOCX.'

@app.route('/view/<filename>')
def view_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
