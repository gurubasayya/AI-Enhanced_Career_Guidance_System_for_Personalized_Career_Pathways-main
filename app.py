from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import json
import re
from werkzeug.utils import secure_filename
from markupsafe import Markup
from openapi import generate_career_guidance
import pdfplumber
from forms import PersonalInformationForm
from docx import Document
from PIL import Image
import pytesseract
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Add escapejs filter
def escapejs_filter(s):
    if s is None:
        return ''
    s = str(s)
    s = s.replace('\\', '\\\\')
    s = s.replace('\"', '\\"')
    s = s.replace("\'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    s = s.replace('</', '<\/')
    return Markup(s)

app.jinja_env.filters['escapejs'] = escapejs_filter
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for resume upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # For now, just store email in session (implement proper auth later)
        session['user_email'] = email
        return redirect(url_for('upload_resume'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Implement registration logic here
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload-resume', methods=['GET', 'POST'])
def upload_resume():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            session['resume_filename'] = filename
            
            # Extract information from resume
            try:
                text = extract_text_from_file(file_path)
                extracted_info = parse_resume_info(text)
                session['extracted_info'] = extracted_info
                flash('Resume uploaded successfully! Information extracted and pre-filled below.', 'success')
            except Exception as e:
                flash('Resume uploaded but information extraction failed. Please fill the form manually.', 'warning')
                session['extracted_info'] = {}
            
            return redirect(url_for('personal_info'))
        else:
            flash('Invalid file type. Please upload PDF, DOC, DOCX, or image files.', 'error')
    
    return render_template('upload_resume.html')

def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    text = ""
    file_ext = file_path.lower().split('.')[-1]
    
    try:
        if file_ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        elif file_ext in ['doc', 'docx']:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        
        elif file_ext in ['png', 'jpg', 'jpeg', 'gif']:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        
        elif file_ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
    
    return text

def parse_resume_info(text):
    """Parse personal information from resume text"""
    info = {
        'name': '',
        'phone': '',
        'linkedin': '',
        'college': '',
        'degree': '',
        'age': ''
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        info['email'] = email_match.group()
    
    # Phone pattern (various formats)
    phone_patterns = [
        r'\+?\d{1,3}[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}',
        r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}',
        r'\d{10}'
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            info['phone'] = phone_match.group()
            break
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/[\w-]+|linkedin\.com/pub/[\w-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        info['linkedin'] = 'https://' + linkedin_match.group()
    
    # Name extraction (first few lines, excluding email/phone)
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and not re.search(r'@|\d{10}|linkedin|resume|cv', line, re.IGNORECASE):
            if len(line.split()) >= 2 and len(line) < 50:
                info['name'] = line
                break
    
    # Education extraction
    education_keywords = ['university', 'college', 'institute', 'school']
    degree_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'bca', 'mca', 'be', 'me']
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in education_keywords):
            info['college'] = line.strip()
            break
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in degree_keywords):
            # Extract degree information
            if 'computer' in line_lower or 'cs' in line_lower:
                info['degree'] = 'Computer Science'
            elif 'engineering' in line_lower or 'engineer' in line_lower:
                info['degree'] = 'Engineering'
            elif 'business' in line_lower or 'mba' in line_lower:
                info['degree'] = 'Business Administration'
            elif 'data' in line_lower:
                info['degree'] = 'Data Science'
            elif 'information' in line_lower and 'technology' in line_lower:
                info['degree'] = 'Information Technology'
            break
    
    return info



@app.route('/personal-info', methods=['GET', 'POST'])
def personal_info():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Store personal information in session
        session['personal_info'] = {
            'name': request.form['name'],
            'age': request.form['age'],
            'college': request.form['college'],
            'country': request.form['country'],
            'degree': request.form['degree'],
            'year_of_study': request.form['year_of_study'],
            'phone': request.form['phone'],
            'linkedin': request.form['linkedin']
        }
        return redirect(url_for('skills_assessment'))
    
    # Get extracted information from session
    extracted_info = session.get('extracted_info', {})
    return render_template('personal_info.html', extracted_info=extracted_info)

@app.route('/skills-assessment', methods=['GET', 'POST'])
def skills_assessment():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get and clean skills lists
        technical_skills = [skill.strip() for skill in request.form.getlist('technical_skills') if skill.strip()]
        soft_skills = [skill.strip() for skill in request.form.getlist('soft_skills') if skill.strip()]
        
        # Store skills information
        session['skills'] = {
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'experience_level': request.form['experience_level'],
            'certifications': request.form['certifications']
        }
        return redirect(url_for('exam_choice'))
    
    return render_template('skills_assessment.html')

@app.route('/exam-choice', methods=['GET', 'POST'])
def exam_choice():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        take_exam = request.form.get('take_exam')
        if take_exam == 'yes':
            return redirect(url_for('aptitude_test'))
        else:
            return redirect(url_for('career_analysis'))
    
    return render_template('exam_choice.html')

@app.route('/aptitude-test', methods=['GET', 'POST'])
def aptitude_test():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Store test results
        session['test_results'] = {
            'logical_reasoning': request.form['q1'],
            'analytical_thinking': request.form['q2'],
            'problem_solving': request.form['q3'],
            'creativity': request.form['q4'],
            'leadership': request.form['q5']
        }
        return redirect(url_for('career_analysis'))
    
    return render_template('aptitude_test.html')

# Store analysis results in memory (in production, use a proper cache or database)
analysis_store = {}

def generate_analysis_id():
    """Generate a unique ID for storing analysis results."""
    import uuid
    return str(uuid.uuid4())

# Job skills mapping based on the notebook
JOB_SKILLS_MAPPING = {
    'Cloud Engineer': ['cloud computing', 'devops', 'networking', 'linux', 'python', 'security'],
    'Web Developer': ['javascript', 'html', 'css', 'web development', 'api', 'database'],
    'Network Engineer': ['networking', 'linux', 'security'],
    'Database Administrator': ['sql', 'nosql', 'database', 'security'],
    'Cybersecurity Analyst': ['cybersecurity', 'networking', 'linux', 'security'],
    'Software Engineer': ['java', 'python', 'c++', 'data structures', 'algorithms', 'devops'],
    'AI Engineer': ['machine learning', 'python', 'data analysis', 'tensorflow', 'pytorch'],
    'Embedded Systems Engineer': ['c++', 'c', 'embedded systems', 'hardware'],
    'Business Analyst': ['business analysis', 'communication', 'sql', 'data analysis', 'project management'],
    'Data Analyst': ['data analysis', 'sql', 'python', 'data visualization'],
    'DevOps Engineer': ['devops', 'cloud computing', 'linux', 'automation'],
    'Mobile App Developer': ['java', 'kotlin', 'swift', 'mobile development', 'ui/ux design'],
    'UI/UX Designer': ['ui/ux design', 'user research', 'graphic design'],
    'Project Manager': ['project management', 'leadership', 'communication', 'risk management'],
    'Data Scientist': ['data analysis', 'machine learning', 'python', 'statistics']
}

def normalize_skill(skill):
    """Normalize skill names to match the job requirements"""
    if not skill:
        return ''
    
    skill = skill.strip().lower()
    
    # Skill mapping for normalization
    skill_mapping = {
        'js': 'javascript', 'nodejs': 'javascript', 'node.js': 'javascript',
        'reactjs': 'javascript', 'react.js': 'javascript',
        'py': 'python', 'django': 'python', 'flask': 'python',
        'cpp': 'c++', 'cplusplus': 'c++',
        'csharp': 'c#', 'dotnet': 'c#', '.net': 'c#',
        'ml': 'machine learning', 'ai': 'machine learning',
        'artificial intelligence': 'machine learning',
        'dl': 'deep learning', 'neural networks': 'deep learning',
        'aws': 'cloud computing', 'azure': 'cloud computing', 'gcp': 'cloud computing',
        'mysql': 'sql', 'postgresql': 'sql', 'postgres': 'sql',
        'mongodb': 'nosql', 'cassandra': 'nosql', 'redis': 'nosql',
        'html5': 'html', 'css3': 'css',
        'communication skills': 'communication',
        'project planning': 'project management',
        'user interface': 'ui/ux design', 'user experience': 'ui/ux design'
    }
    
    return skill_mapping.get(skill, skill)

def calculate_job_eligibility(user_skills, job_skills_map):
    """Calculate eligibility scores for each job based on user skills"""
    eligibility_scores = {}
    
    # Normalize user skills
    normalized_user_skills = [normalize_skill(skill) for skill in user_skills]
    
    for job, required_skills in job_skills_map.items():
        if not required_skills:
            eligibility_scores[job] = 0.0
            continue
        
        # Calculate skill match percentage
        matched_skills = [skill for skill in normalized_user_skills if skill in required_skills]
        skill_match_percentage = (len(matched_skills) / len(required_skills)) * 100
        
        # Add bonus for having more skills
        bonus_points = min(20, len(normalized_user_skills) * 0.5)
        
        # Final score
        final_score = min(100, skill_match_percentage + bonus_points)
        eligibility_scores[job] = final_score
    
    return eligibility_scores

def analyze_skill_gaps(user_skills, job_skills_map):
    """Analyze skill gaps for each job"""
    normalized_user_skills = [normalize_skill(skill) for skill in user_skills]
    skill_gaps = {}
    
    for job, required_skills in job_skills_map.items():
        missing_skills = [skill for skill in required_skills if skill not in normalized_user_skills]
        skill_gaps[job] = {
            'missing_skills': missing_skills,
            'match_percentage': ((len(required_skills) - len(missing_skills)) / len(required_skills)) * 100 if required_skills else 0
        }
    
    return skill_gaps

@app.route('/career-analysis')
def career_analysis():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    # Get user data from session
    user_skills = session.get('skills', {})
    personal_info = session.get('personal_info', {})
    test_results = session.get('test_results', {})
    
    # Combine all user skills
    all_user_skills = []
    if 'technical_skills' in user_skills:
        all_user_skills.extend(user_skills['technical_skills'])
    if 'soft_skills' in user_skills:
        all_user_skills.extend(user_skills['soft_skills'])
    
    # Calculate job eligibility scores
    job_eligibility = calculate_job_eligibility(all_user_skills, JOB_SKILLS_MAPPING)
    
    # Sort jobs by eligibility score
    sorted_jobs = sorted(job_eligibility.items(), key=lambda x: x[1], reverse=True)
    
    # Get top 5 recommendations
    recommended_careers = []
    for job, score in sorted_jobs[:5]:
        growth_mapping = {
            'AI Engineer': 'Very High',
            'Data Scientist': 'Very High', 
            'Cloud Engineer': 'High',
            'Cybersecurity Analyst': 'High',
            'DevOps Engineer': 'High'
        }
        recommended_careers.append({
            'title': job,
            'match': round(score, 1),
            'growth': growth_mapping.get(job, 'Medium')
        })
    
    # Analyze skill gaps
    skill_gap_analysis = analyze_skill_gaps(all_user_skills, JOB_SKILLS_MAPPING)
    
    # Generate skill gaps for top jobs
    skill_gaps = []
    for job, score in sorted_jobs[:3]:
        gaps = skill_gap_analysis[job]
        if gaps['missing_skills']:
            skill_gaps.append({
                'skill': ', '.join(gaps['missing_skills'][:3]),  # Top 3 missing skills
                'importance': 'High' if score < 70 else 'Medium',
                'current_level': 'None'
            })
    
    # Calculate trending jobs suitability based on top job match
    trending_jobs_suitability = sorted_jobs[0][1] if sorted_jobs else 50
    
    # Generate course recommendations based on skill gaps
    course_mapping = {
        'machine learning': 'Machine Learning Fundamentals',
        'cloud computing': 'AWS Cloud Practitioner',
        'python': 'Python for Data Science',
        'javascript': 'Modern JavaScript Development',
        'cybersecurity': 'Cybersecurity Fundamentals',
        'data analysis': 'Data Analysis with Python',
        'project management': 'PMP Certification'
    }
    
    recommended_courses = []
    for job, score in sorted_jobs[:3]:
        gaps = skill_gap_analysis[job]
        for skill in gaps['missing_skills'][:2]:  # Top 2 missing skills per job
            if skill in course_mapping:
                recommended_courses.append({
                    'title': course_mapping[skill],
                    'provider': 'Coursera',
                    'duration': '6 weeks'
                })
    
    # Remove duplicates
    seen_courses = set()
    unique_courses = []
    for course in recommended_courses:
        if course['title'] not in seen_courses:
            unique_courses.append(course)
            seen_courses.add(course['title'])
    
    # Prepare the analysis results
    analysis_id = generate_analysis_id()
    analysis_results = {
        'recommended_careers': recommended_careers,
        'user_skills': user_skills,
        'skill_gaps': skill_gaps,
        'trending_jobs_suitability': round(trending_jobs_suitability),
        'recommended_courses': unique_courses[:5]  # Top 5 courses
    }
    
    # Store results in memory with the analysis_id
    analysis_store[analysis_id] = analysis_results
    
    # Store only the analysis_id in the session
    session['current_analysis_id'] = analysis_id
    
    return render_template('career_analysis.html', results=analysis_results)

def get_career_key(input_title):
    """Find the correct career key from CAREER_GUIDANCE regardless of case or spaces."""
    input_title_clean = input_title.replace('%20', ' ').strip().lower()
    from openapi import CAREER_GUIDANCE  # Import here to avoid circular import
    for key in CAREER_GUIDANCE.keys():
        if key.lower() == input_title_clean:
            return key
    return 'default'

@app.route('/career-guidance/<career_title>')
def career_guidance(career_title):
    """Render the career guidance page with detailed information."""
    try:
        # Use helper to get correct key for any job role
        career_key = get_career_key(career_title)
        match_percentage = request.args.get('match', 85, type=int)
        growth = request.args.get('growth', 'High')
        user_skills = session.get('skills', {
            'programming': 'Beginner',
            'problem_solving': 'Intermediate',
            'communication': 'Intermediate'
        })
        guidance = generate_career_guidance(
            career_title=career_key,
            match_percentage=match_percentage,
            growth=growth,
            user_skills=user_skills
        )
        return render_template('career_guidance.html', guidance=guidance)
    except Exception as e:
        flash(f'Error loading career guidance: {str(e)}', 'error')
        return redirect(url_for('career_analysis'))

@app.route('/api/career-guidance/<career_title>')
def get_career_guidance(career_title):
    """API endpoint to get guidance for a specific career."""
    try:
        # Get match percentage and growth from query parameters if available
        match_percentage = request.args.get('match', 85, type=int)
        growth = request.args.get('growth', 'High')
        
        # Return JSON response with redirect URL
        return jsonify({
            'redirect': url_for('career_guidance', 
                              career_title=career_title,
                              match=match_percentage,
                              growth=growth)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Technologies used in this project:

# - **Python**: Main programming language for backend logic.
# - **Flask**: Web framework for building the server, routing, and rendering templates.
# - **Jinja2**: Templating engine used by Flask for HTML rendering.
# - **Werkzeug**: Utility library for secure file uploads.
# - **Flask session**: For storing user data between requests.
# - **Flask flash**: For displaying messages to users.
# - **OpenAPI module**: Custom Python module for career guidance logic.
# - **dotenv**: For loading environment variables from `.env` files.
# - **Azure AI Inference SDK**: (Imported, but not actively used in current logic) For connecting to Azure AI models.
# - **HTML/CSS/JavaScript**: Used in frontend templates (not shown in code, but implied by `render_template`).
# - **Bootstrap** (optional, if used in templates): For frontend styling.
# - **UUID**: For generating unique analysis IDs.
# - **JSON**: For API responses and data interchange.

# Optional/Planned:
# - **Database**: Not yet implemented, but recommended for production.
# - **Cloud deployment**: Possible future deployment to Azure or other cloud platforms.

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
