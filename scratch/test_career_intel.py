import re

def extract_candidate_profile(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = None
    role = None
    company = None
    
    # 1. Candidate Name detection from top lines
    blacklist_words = {'resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary', 'contact', 'email', 'phone', 'portfolio', 'page', 'objective'}
    for line in lines[:5]:
        clean = re.sub(r'[^a-zA-Z\s\.\-]', '', line).strip()
        words = clean.split()
        if 2 <= len(words) <= 4:
            if not any(w.lower() in blacklist_words for w in words):
                if '@' not in line and 'http' not in line and not re.search(r'\d', line):
                    name = clean.title()
                    break
    
    # 2. Current / Recent Role and Company detection
    # Look for patterns like "Title | Company | 2022 - Present" or "Title at Company"
    role_pattern = re.compile(
        r'^(?P<title>[A-Za-z\s/,\-&]+?)\s*(?:\||–|-|@|at)\s*(?P<company>[A-Za-z0-9\s,\.\-&]+?)\s*(?:\||–|-|\(|\d{4}|$)',
        re.IGNORECASE
    )
    
    for line in lines:
        if any(h in line.lower() for h in ['present', 'current', '2023', '2024', '2022']):
            m = role_pattern.match(line)
            if m:
                t = m.group('title').strip()
                c = m.group('company').strip()
                if 3 <= len(t) <= 40 and not any(k in t.lower() for k in ['university', 'college', 'bachelor', 'master', 'education', 'project']):
                    role = t.title()
                    company = c.title()
                    break

    # Fallback role from line 2 if title-like
    if not role and len(lines) > 1:
        cand_line = lines[1].strip()
        if len(cand_line) < 40 and not any(c in cand_line for c in ['@', '|', 'http', '(', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            role = cand_line.title()

    return {
        "name": name or "Professional Candidate",
        "role": role or "Engineering Specialist",
        "company": company or "Current Organization"
    }

with open('backend/software_engineer_resume.txt', 'r', encoding='utf-8') as f:
    sw = f.read()

with open('backend/mechanical_engineer_resume.txt', 'r', encoding='utf-8') as f:
    me = f.read()

print("SW Profile:", extract_candidate_profile(sw))
print("ME Profile:", extract_candidate_profile(me))
