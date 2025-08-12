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

# -------------------- Generic Extractor --------------------
def extract_resume_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format. Please upload a .pdf or .docx file."

# -------------------- Keywords --------------------
GENERIC_KEYWORDS = [
    "python", "java", "c++", "sql", "html", "css", "javascript", "excel", "power bi",
    "machine learning", "deep learning", "data analysis", "data science"
]

BRANCH_KEYWORDS = {
    "cse": ["dbms", "operating system", "computer networks", "software engineering", "ai", "ml"],
    "ece": ["vlsi", "embedded systems", "signal processing", "microcontrollers"],
    "mech": ["cad", "cam", "thermodynamics", "manufacturing"]
}

PLATFORM_LINKS = {
    "github": r"github\.com/[A-Za-z0-9_-]+",
    "leetcode": r"leetcode\.com/[A-Za-z0-9_-]+",
    "hackerrank": r"hackerrank\.com/[A-Za-z0-9_-]+",
    "codeforces": r"codeforces\.com/[A-Za-z0-9_-]+",
    "kaggle": r"kaggle\.com/[A-Za-z0-9_-]+"
}

PROJECT_KEYWORDS = ["project", "developed", "built", "created", "designed", "implemented"]

# -------------------- Detect Branch --------------------
def detect_branch(text):
    for branch, keywords in BRANCH_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            return branch
    return None

# -------------------- Parse Resume --------------------
def parse_resume(resume_text):
    resume_lower = resume_text.lower()
    branch = detect_branch(resume_lower)

    skill_set = set(GENERIC_KEYWORDS)
    if branch and branch in BRANCH_KEYWORDS:
        skill_set.update(BRANCH_KEYWORDS[branch])
    else:
        for skills in BRANCH_KEYWORDS.values():
            skill_set.update(skills)

    found_skills = [skill for skill in skill_set if skill.lower() in resume_lower]

    # Platforms
    found_links = {}
    for platform, pattern in PLATFORM_LINKS.items():
        match = re.search(pattern, resume_text, re.IGNORECASE)
        if match:
            found_links[platform] = match.group()

    # Projects count
    project_count = sum(1 for word in PROJECT_KEYWORDS if word in resume_lower)

    return {
        "branch": branch if branch else "Not detected",
        "skills": found_skills,
        "platforms": found_links,
        "project_count": project_count
    }

# -------------------- ATS Score --------------------
def calculate_ats_score(found_skills, total_skills, platforms, project_count):
    score = 0

    # Skills (70%)
    if total_skills:
        score += (len(found_skills) / len(total_skills)) * 70

    # Platforms (15%)
    score += len(platforms) * 3  # each worth 3 points

    # Projects (15%)
    score += min(project_count * 5, 15)  # cap at 15%

    return round(min(score, 100), 2)
