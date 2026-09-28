import os
import sys
import io
import re
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2
import docx

# Ensure UTF-8 stdout encoding on Windows so emojis never crash logging
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Ensure backend directory is in sys.path so it runs seamlessly from root or backend folder
_backend_dir = os.path.dirname(os.path.abspath(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Import the advanced dynamic resume engine
from resume_engine import (
    analyze_resume_comprehensively,
    extract_skills_robust,
    calculate_experience_timeline,
    calculate_ats_score_breakdown
)

app = Flask(__name__)
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'])

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file with error handling"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.is_encrypted:
                print("PDF is encrypted/password protected")
                return None
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += page_text + "\n"
                except Exception as page_error:
                    print(f"Error extracting page {page_num + 1}: {page_error}")
                    continue
            
            if not text.strip():
                print("No text extracted from PDF - might be image-based or corrupted")
                return None
            
            return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text.strip()
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return None

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read().strip()
    except Exception as e:
        print(f"TXT extraction error: {e}")
        return None

def extract_skills_from_text(text):
    """Bridge for backward compatibility - returns list of skill names"""
    skills, _ = extract_skills_robust(text)
    return [s["name"] for s in skills]

def analyze_resume_with_mock_ai(text):
    """Bridge for backward compatibility - runs comprehensive dynamic analysis"""
    return analyze_resume_comprehensively(text)

@app.route('/')
def home():
    """Serve the advanced UI as homepage"""
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(frontend_dir, 'advanced-index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume from uploaded file or raw text"""
    try:
        resume_text = None
        
        # 1. Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                file_ext = filename.rsplit('.', 1)[1].lower()
                if file_ext == 'pdf':
                    resume_text = extract_text_from_pdf(file_path)
                elif file_ext in ['docx', 'doc']:
                    resume_text = extract_text_from_docx(file_path)
                elif file_ext == 'txt':
                    resume_text = extract_text_from_txt(file_path)
                
                # Cleanup temporary file
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception:
                    pass
                
                if not resume_text:
                    return jsonify({"error": "Could not extract readable text from the document. Please ensure it is not scanned/password-protected."}), 400
            else:
                return jsonify({"error": "Unsupported file format. Please upload PDF, DOCX, or TXT."}), 400

        # 2. Check if text was sent directly via JSON or form data
        elif request.is_json:
            data = request.get_json(silent=True)
            if data and 'resume_text' in data:
                resume_text = data['resume_text']
            else:
                try:
                    import json as _json
                    raw_str = request.get_data().decode('utf-8', errors='replace')
                    data = _json.loads(raw_str)
                    resume_text = data.get('resume_text')
                except Exception:
                    pass
        elif 'resume_text' in request.form:
            resume_text = request.form['resume_text']
        
        if not resume_text:
            return jsonify({"error": "No resume file or text provided."}), 400

        # 3. Perform dynamic, multi-dimensional analysis
        analysis_result = analyze_resume_comprehensively(resume_text)
        
        if "error" in analysis_result and len(analysis_result) == 1:
            return jsonify(analysis_result), 400
        
        # Attach preview snippet
        analysis_result['extracted_text'] = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        
        domain = analysis_result.get('primary_domain', 'Professional')
        score = analysis_result.get('score', 0)
        exp = analysis_result.get('career_intelligence', {}).get('experience_level', 'N/A')
        print(f"[Engine] Analyzed {domain} resume - ATS Score: {score} - Experience: {exp} - Skills: {len(analysis_result.get('skills', []))}")
        
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"Error in analyze_resume: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "engine": "Dynamic ATS Assessment & Career Intelligence Engine v2.0",
        "features": ["Multi-Domain Skill Taxonomy", "5-Pillar ATS Scoring", "Accurate Timeline Experience", "Radar Competency Profiling"]
    })

@app.route('/<path:filename>')
def static_files(filename):
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(frontend_dir, filename)

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    print("🚀 Starting AI Resume Analyzer (Dynamic Assessment Engine v2.0)...")
    print("🎯 Multi-domain evaluation active: Mechanical, Software, Cloud/DevOps, Data/AI, Civil, Electrical")
    print("🌐 Backend server running on: http://localhost:5000")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)