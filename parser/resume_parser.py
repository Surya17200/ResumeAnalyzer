from pdfminer.high_level import extract_text as extract_pdf_text
import docx
import re

# -------------------- Extract Text from PDF --------------------
def extract_text_from_pdf(file_path):
    try:
        return extract_pdf_text(file_path)
    except Exception as e:
        return f"Error reading PDF: {e}"

# -------------------- Extract Text from DOCX --------------------
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"

# -------------------- Extract Raw Resume Text --------------------
def extract_resume_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format. Please upload a .pdf or .docx file."

# -------------------- Extract Features from Resume --------------------
def extract_resume_data(text):
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }
    return data

# -------------------- Helper Functions --------------------

def extract_name(text):
    # Simple heuristic: first line is often the name
    lines = text.strip().split('\n')
    if lines:
        return lines[0].strip()
    return "Name not found"

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group() if match else "Email not found"

def extract_phone(text):
    match = re.search(r'(\+91[-\s]?)?[6-9]\d{9}', text)
    return match.group() if match else "Phone number not found"

def extract_skills(text):
    # Sample skills list
    skill_keywords = [
        "Python", "Java", "SQL", "C++", "Machine Learning", "NLP", "Data Science",
"Flask", "Django", "TensorFlow", "Keras", "Pandas", "NumPy", "Git", "Linux"
    ]
    found_skills = [skill for skill in skill_keywords if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE)]
    return list(set(found_skills)) if found_skills else ["No skills found"]

def extract_education(text):
    education_keywords = ["B.Tech", "M.Tech", "B.E.", "M.E.", "B.Sc", "M.Sc", "Bachelor", "Master", "Ph.D", "High School"]
    matches = [edu for edu in education_keywords if edu.lower() in text.lower()]
    return list(set(matches)) if matches else ["Education details not found"]