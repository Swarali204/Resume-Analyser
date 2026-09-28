"""
Advanced Dynamic Resume Assessment & Intelligence Engine
Provides true multi-dimensional ATS scoring, word-boundary skill extraction across multiple engineering and business domains,
accurate timeline-based experience calculation, candidate-specific strengths/weaknesses, and market intelligence.
"""

import re
import os
import sys
import math
from datetime import datetime

# Ensure UTF-8 stdout encoding on Windows so rupee and special characters never crash logging
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

CURRENT_YEAR = 2024  # Standard baseline year

# ============================================================================
# 1. COMPREHENSIVE MULTI-DOMAIN SKILL TAXONOMY (WORD BOUNDARY PROTECTED)
# ============================================================================
SKILL_TAXONOMY = [
    # --- MECHANICAL, AEROSPACE & MANUFACTURING ---
    ("SolidWorks", r"\bsolidworks\b", "CAD & 3D Modeling", "Mechanical"),
    ("AutoCAD", r"\bautocad\b", "CAD & Drafting", "Mechanical"),
    ("CATIA", r"\bcatia\b", "CAD & Aerospace Design", "Mechanical"),
    ("Fusion 360", r"\bfusion\s*360\b", "CAD/CAM", "Mechanical"),
    ("Inventor", r"\bautodesk\s+inventor\b|\binventor\b", "CAD", "Mechanical"),
    ("ANSYS", r"\bansys\b", "FEA & Simulation", "Mechanical"),
    ("FEA / Stress Analysis", r"\b(fea|finite\s+element\s+analysis|stress\s+analysis)\b", "Simulation", "Mechanical"),
    ("CFD / Fluid Dynamics", r"\b(cfd|computational\s+fluid\s+dynamics|fluid\s+flow)\b", "Simulation", "Mechanical"),
    ("Thermal Analysis", r"\bthermal\s+(?:analysis|management|optimization)\b", "Simulation", "Mechanical"),
    ("Fatigue & Durability Testing", r"\b(fatigue\s+(?:testing|analysis)|durability\s+testing)\b", "Testing", "Mechanical"),
    ("Simulink", r"\bsimulink\b", "Modeling & Simulation", "Engineering"),
    ("MATLAB", r"\bmatlab\b", "Numerical Computing", "Engineering"),
    ("CNC Machining & Milling", r"\b(cnc|cnc\s+machining|milling|lathe)\b", "Manufacturing", "Mechanical"),
    ("3D Printing / Additive Mfg", r"\b(3d\s+printing|additive\s+manufacturing|fdm|sla)\b", "Manufacturing", "Mechanical"),
    ("Injection Molding", r"\binjection\s+molding\b", "Manufacturing", "Mechanical"),
    ("GD&T (Geometric Dimensioning)", r"\b(gd&t|geometric\s+dimensioning(?:\s+and\s+tolerancing)?)\b", "Standards & Quality", "Mechanical"),
    ("Composite Materials", r"\b(composite\s+materials?|composites?|carbon\s+fiber)\b", "Materials", "Mechanical"),
    ("ISO / ASME / ASTM Standards", r"\b(iso(?:\s+\d{3,5})?|asme|astm|faa\s+regulations?)\b", "Standards & Compliance", "Mechanical"),
    ("DFM / DFA", r"\b(dfm|dfa|design\s+for\s+manufactur(?:ability|ing))\b", "Manufacturing", "Mechanical"),
    ("Product Design", r"\bproduct\s+design\b|\bmechanical\s+design\b", "Design", "Mechanical"),
    ("Mechatronics & Robotics", r"\b(mechatronics?|robotics?|kinematics)\b", "Hardware & Systems", "Mechanical"),
    ("Hydraulics & Pneumatics", r"\b(hydraulics?|pneumatics?)\b", "Mechanical Systems", "Mechanical"),

    # --- SOFTWARE ENGINEERING & WEB DEVELOPMENT ---
    ("JavaScript", r"\b(javascript|es6|es20\d\d)\b", "Programming Languages", "Software"),
    ("TypeScript", r"\btypescript\b", "Programming Languages", "Software"),
    ("Python", r"\bpython\b", "Programming Languages", "Software"),
    ("Java", r"\bjava\b(?!\s*script)", "Programming Languages", "Software"),
    ("C++", r"\bc\+\+\b", "Programming Languages", "Software"),
    ("C#", r"\bc#\b|\bcsharp\b", "Programming Languages", "Software"),
    ("PHP", r"\bphp\b", "Programming Languages", "Software"),
    ("Go / Golang", r"\b(golang|go\s+language)\b", "Programming Languages", "Software"),
    ("Rust", r"\brust\s+(?:lang|programming)\b", "Programming Languages", "Software"),
    ("Ruby / Rails", r"\b(ruby|ruby\s+on\s+rails)\b", "Programming Languages", "Software"),
    ("Swift", r"\bswift\s+(?:programming|development|ios)\b", "Mobile", "Software"),
    ("Kotlin", r"\bkotlin\b", "Mobile", "Software"),
    ("React", r"\breact(?:\.js|js)?\b", "Frontend Development", "Software"),
    ("Angular", r"\bangular(?:\.js|js)?\b", "Frontend Development", "Software"),
    ("Vue.js", r"\bvue(?:\.js|js)?\b", "Frontend Development", "Software"),
    ("Next.js", r"\bnext(?:\.js|js)?\b", "Frontend Development", "Software"),
    ("Node.js", r"\bnode(?:\.js|js)?\b", "Backend Development", "Software"),
    ("Express.js", r"\bexpress(?:\.js|js)?\b", "Backend Development", "Software"),
    ("Django", r"\bdjango\b", "Backend Development", "Software"),
    ("Flask", r"\bflask\b", "Backend Development", "Software"),
    ("Spring Boot", r"\bspring\s*boot\b|\bspring\s+framework\b", "Backend Development", "Software"),
    ("HTML5", r"\bhtml(?:5)?\b", "Frontend Development", "Software"),
    ("CSS3 / Modern CSS", r"\b(css3?|sass|scss|tailwind(?:css)?|bootstrap)\b", "Frontend Development", "Software"),
    ("RESTful APIs", r"\b(restful\s+apis?|rest\s+apis?|restful\s+web\s+services)\b", "Architecture", "Software"),
    ("Microservices", r"\bmicroservices?\b", "Architecture", "Software"),
    ("GraphQL", r"\bgraphql\b", "API Design", "Software"),
    ("WebSockets", r"\bwebsockets?\b", "Networking", "Software"),

    # --- CLOUD, DATABASES & DEVOPS ---
    ("AWS", r"\b(aws|amazon\s+web\s+services|ec2|s3|lambda|dynamodb|ecs|eks)\b", "Cloud & Infrastructure", "Cloud/DevOps"),
    ("Azure", r"\b(azure|microsoft\s+azure)\b", "Cloud & Infrastructure", "Cloud/DevOps"),
    ("Google Cloud (GCP)", r"\b(gcp|google\s+cloud(?:\s+platform)?)\b", "Cloud & Infrastructure", "Cloud/DevOps"),
    ("Docker", r"\bdocker\b|\bcontainerization\b", "DevOps & Containers", "Cloud/DevOps"),
    ("Kubernetes", r"\b(kubernetes|k8s)\b", "DevOps & Orchestration", "Cloud/DevOps"),
    ("CI/CD Automation", r"\b(ci[/-]cd|continuous\s+integration|jenkins|github\s+actions)\b", "DevOps", "Cloud/DevOps"),
    ("Git / Version Control", r"\b(git|github|gitlab|bitbucket)\b", "DevOps", "Software"),
    ("MongoDB", r"\bmongodb\b|\bmongo\b", "Databases", "Cloud/DevOps"),
    ("PostgreSQL", r"\b(postgresql|postgres)\b", "Databases", "Cloud/DevOps"),
    ("MySQL", r"\bmysql\b", "Databases", "Cloud/DevOps"),
    ("Redis", r"\bredis\b", "Databases", "Cloud/DevOps"),
    ("SQL", r"\bsql\b(?!\s*server)", "Databases", "Cloud/DevOps"),
    ("Linux / Bash", r"\b(linux|ubuntu|centos|debian|bash\s+scripting)\b", "Systems & OS", "Cloud/DevOps"),

    # --- DATA SCIENCE & AI / ML ---
    ("Machine Learning", r"\bmachine\s+learning\b", "AI & Data Science", "Data/AI"),
    ("Deep Learning", r"\bdeep\s+learning\b|\bneural\s+networks?\b", "AI & Data Science", "Data/AI"),
    ("Artificial Intelligence", r"\bartificial\s+intelligence\b", "AI & Data Science", "Data/AI"),
    ("Natural Language Processing (NLP)", r"\b(nlp|natural\s+language\s+processing)\b", "AI & Data Science", "Data/AI"),
    ("Computer Vision", r"\bcomputer\s+vision\b", "AI & Data Science", "Data/AI"),
    ("PyTorch", r"\bpytorch\b", "AI Frameworks", "Data/AI"),
    ("TensorFlow", r"\btensorflow\b", "AI Frameworks", "Data/AI"),
    ("Scikit-Learn", r"\b(scikit-learn|sklearn)\b", "AI Frameworks", "Data/AI"),
    ("Pandas / NumPy", r"\b(pandas|numpy)\b", "Data Manipulation", "Data/AI"),
    ("Power BI", r"\bpower\s*bi\b", "Business Intelligence", "Business/Data"),
    ("Tableau", r"\btableau\b", "Data Visualization", "Business/Data"),
    ("Advanced Excel", r"\b(advanced\s+excel|microsoft\s+excel|spreadsheets)\b", "Data Analysis", "Business/Data"),

    # --- CIVIL & ELECTRICAL ---
    ("Embedded Systems", r"\bembedded\s+systems?\b|\bmicrocontrollers?\b", "Hardware & Firmware", "Electrical"),
    ("PCB Design", r"\b(pcb\s+design|altium|kicad|eagle)\b", "Hardware & Circuits", "Electrical"),
    ("PLC Programming", r"\b(plc\s+programming|scada|ladder\s+logic)\b", "Industrial Automation", "Electrical"),
    ("Revit / BIM", r"\b(revit|bim|building\s+information\s+modeling)\b", "Design & Modeling", "Civil"),
    ("Structural Analysis", r"\b(structural\s+analysis|staad\s*pro|etabs)\b", "Engineering", "Civil"),

    # --- MANAGEMENT, QUALITY & SOFT SKILLS ---
    ("Agile & Scrum Methodologies", r"\b(agile|scrum|kanban|sprint\s+planning)\b", "Project Management", "Management"),
    ("Jira", r"\bjira\b", "Project Tracking", "Management"),
    ("Technical Leadership & Mentoring", r"\b(technical\s+lead|team\s+lead|managed\s+team|mentored|coached\s+engineers|led\s+cross-functional)\b", "Leadership", "Soft Skills"),
    ("Six Sigma & Lean", r"\b(six\s+sigma|lean\s+manufacturing|kaizen|5s)\b", "Process Excellence", "Management"),
    ("Quality Assurance & Testing", r"\b(quality\s+assurance|quality\s+control|\bqa/qc\b)\b", "Quality", "Operations"),
    ("Cross-Functional Collaboration", r"\b(cross-functional|stakeholder\s+management|collaboration)\b", "Collaboration", "Soft Skills"),
    ("Problem Solving & RCA", r"\b(problem[- ]solving|root\s+cause\s+analysis|\brca\b)\b", "Core Competency", "Soft Skills")
]

# Month string to number mapping
MONTH_MAP = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
}

# ============================================================================
# 2. ACCURATE SKILL EXTRACTION & DOMAIN IDENTIFICATION
# ============================================================================
def extract_skills_robust(text):
    """
    Extracts skills using word-boundary regular expressions and captures
    skills explicitly listed under TECHNICAL SKILLS headings without false positives.
    """
    detected_skills = []
    seen_names = set()
    domain_votes = {"Mechanical": 0, "Software": 0, "Cloud/DevOps": 0, "Data/AI": 0, "Electrical": 0, "Civil": 0}

    # 1. Word boundary regex search against defined taxonomy
    for canonical_name, pattern, category, domain in SKILL_TAXONOMY:
        if re.search(pattern, text, re.IGNORECASE):
            if canonical_name not in seen_names:
                detected_skills.append({
                    "name": canonical_name,
                    "category": category,
                    "domain": domain
                })
                seen_names.add(canonical_name)
                if domain in domain_votes:
                    domain_votes[domain] += 2

    # 2. Targeted section parser for "TECHNICAL SKILLS"
    skills_sec_regex = re.compile(
        r'(?:TECHNICAL\s+SKILLS|SKILLS|CORE\s+COMPETENCIES|AREAS\s+OF\s+EXPERTISE)[\s:]*\n([\s\S]*?)(?=\n[A-Z\s]{4,}|\Z)',
        re.IGNORECASE
    )
    sec_match = skills_sec_regex.search(text)
    if sec_match:
        section_content = sec_match.group(1)
        for line in section_content.split('\n'):
            line_str = line.strip()
            if not line_str:
                continue
            # Strip section prefixes like "CAD Software:" or "Frontend:"
            if ":" in line_str:
                line_str = line_str.split(":", 1)[1]
            tokens = re.split(r'[,;|•/]\s*', line_str)
            for tok in tokens:
                clean_tok = tok.strip()
                # Validate length and filter common noise words
                if 2 <= len(clean_tok) <= 30:
                    clean_lower = clean_tok.lower()
                    if clean_lower in ["etc", "and", "or", "years", "experience", "strong", "proficient", "basic", "knowledge"]:
                        continue
                    if not any(clean_lower == s.lower() for s in seen_names):
                        # Determine category heuristically
                        cat = "Industry Tool"
                        detected_skills.append({
                            "name": clean_tok,
                            "category": cat,
                            "domain": "Domain Specific"
                        })
                        seen_names.add(clean_tok)

    # Determine primary domain
    primary_domain = max(domain_votes, key=domain_votes.get) if any(domain_votes.values()) else "General Professional"
    if domain_votes.get(primary_domain, 0) == 0:
        # Fallback to headline / title analysis
        t_lower = text.lower()
        if "mechanical" in t_lower or "solidworks" in t_lower:
            primary_domain = "Mechanical"
        elif "software" in t_lower or "react" in t_lower or "developer" in t_lower:
            primary_domain = "Software"
        elif "data" in t_lower or "machine learning" in t_lower:
            primary_domain = "Data/AI"

    return detected_skills, primary_domain

# ============================================================================
# 3. ACCURATE EXPERIENCE & TIMELINE CALCULATOR
# ============================================================================
def calculate_experience_timeline(text):
    """
    Parses dates across all lines, accurately separates work experience from education,
    resolves overlapping dates, and identifies explicit years claims.
    """
    lines = text.split('\n')
    edu_headers = ["education", "academic", "university", "college", "degree"]
    exp_headers = ["experience", "work history", "employment", "professional background"]
    
    in_education = False
    in_experience = False
    
    work_spans = []
    edu_spans = []
    
    # Matches: "2021 - Present", "Jan 2020 - Dec 2021", "2019 to 2020", "05/2018 - 09/2021"
    date_pattern = re.compile(
        r'(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+)?(\d{4})\s*(?:-|–|—|to)\s*(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+)?(Present|Current|\d{4})',
        re.IGNORECASE
    )
    
    # Explicit statements like "3+ years of experience" or "5 years experience"
    explicit_match = re.search(r'(\d+)\+?\s*years?\s*(?:of)?\s*(?:experience|expertise|in\s+[a-z]+)', text, re.IGNORECASE)
    explicit_years = float(explicit_match.group(1)) if explicit_match else None
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        # Track section boundaries
        if any(line_lower.startswith(h) for h in edu_headers):
            in_education = True
            in_experience = False
            continue
        elif any(line_lower.startswith(h) for h in exp_headers):
            in_experience = True
            in_education = False
            continue
        elif re.match(r'^[A-Z\s]{4,}$', line_clean) and len(line_clean) > 3:
            # Uppercase header like PROJECTS or ACHIEVEMENTS
            in_education = False
            if any(h in line_lower for h in ['project', 'certif', 'award', 'skill']):
                in_experience = False
        
        # Check for dates
        matches = date_pattern.findall(line_clean)
        for m in matches:
            s_mon, s_yr, e_mon, e_yr = m
            sy = int(s_yr)
            sm = MONTH_MAP.get(s_mon.lower(), 1) if s_mon else 1
            
            if e_yr.lower() in ['present', 'current']:
                ey = CURRENT_YEAR
                em = 12
                is_current = True
            else:
                ey = int(e_yr)
                em = MONTH_MAP.get(e_mon.lower(), 12) if e_mon else 12
                is_current = False
            
            # Sanity check
            if 1970 <= sy <= CURRENT_YEAR + 1 and 1970 <= ey <= CURRENT_YEAR + 5 and sy <= ey:
                span = {
                    "start": sy + (sm - 1) / 12.0,
                    "end": ey + em / 12.0,
                    "line": line_clean,
                    "sy": sy,
                    "ey": ey,
                    "is_current": is_current
                }
                # Classify into education vs work
                if in_education or any(k in line_lower for k in ['university', 'college', 'bachelor', 'master', 'phd', 'gpa', 'b.s.', 'm.s.']):
                    edu_spans.append(span)
                else:
                    work_spans.append(span)

    # Merge overlapping work intervals to prevent double counting
    if work_spans:
        sorted_spans = sorted(work_spans, key=lambda x: x['start'])
        merged = []
        curr_start = sorted_spans[0]['start']
        curr_end = sorted_spans[0]['end']
        
        for s in sorted_spans[1:]:
            if s['start'] <= curr_end:
                curr_end = max(curr_end, s['end'])
            else:
                merged.append((curr_start, curr_end))
                curr_start = s['start']
                curr_end = s['end']
        merged.append((curr_start, curr_end))
        calculated_years = sum(end - start for start, end in merged)
    else:
        calculated_years = 0.0

    # Determine final years representation
    if explicit_years:
        if calculated_years > 0:
            final_years = max(explicit_years, round(calculated_years, 1))
        else:
            final_years = explicit_years
    else:
        final_years = round(calculated_years, 1) if calculated_years > 0 else 1.0

    # Determine seniority badge
    if final_years >= 8:
        seniority = "Senior / Lead Specialist"
    elif final_years >= 4:
        seniority = "Mid-Senior Level"
    elif final_years >= 2:
        seniority = "Mid-Level Professional"
    else:
        seniority = "Entry-Level / Associate"

    return {
        "final_years": final_years,
        "explicit_years": explicit_years,
        "calculated_years": round(calculated_years, 1),
        "seniority": seniority,
        "work_roles_detected": len(work_spans),
        "display_text": f"{final_years} Years ({seniority})"
    }

# ============================================================================
# 4. MULTI-DIMENSIONAL ATS SCORING ENGINE
# ============================================================================
def calculate_ats_score_breakdown(text, skills, exp_info):
    """
    Computes an objective, multi-pillar ATS score (0-100) assessing:
    1. Structure & Essential Sections (20)
    2. Quantifiable Impact & Metrics (25)
    3. Action Verbs & Leadership Phrasing (20)
    4. Domain Skill Depth & Tooling (20)
    5. ATS Format, Readability & Word Count (15)
    """
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 1. Section Structure (Max 20)
    structure_score = 0
    has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text))
    has_phone = bool(re.search(r'(\+?\d[\d\s\-()]{8,}\d)', text))
    has_linkedin_or_gh = bool(re.search(r'linkedin\.com|github\.com|portfolio', text_lower))

    if has_email: structure_score += 2
    if has_phone: structure_score += 1
    if has_linkedin_or_gh: structure_score += 2

    has_summary = bool(re.search(r'\b(summary|objective|profile|professional\s+summary)\b', text_lower))
    if has_summary: structure_score += 4

    has_experience = bool(re.search(r'\b(experience|work\s+history|employment)\b', text_lower))
    if has_experience and exp_info['work_roles_detected'] >= 2:
        structure_score += 5
    elif has_experience:
        structure_score += 3

    has_education = bool(re.search(r'\b(education|academic|university|degree)\b', text_lower))
    if has_education: structure_score += 3

    has_skills_section = bool(re.search(r'\b(skills|competencies|technologies)\b', text_lower))
    if has_skills_section: structure_score += 3

    # 2. Quantifiable Impact (Max 25)
    # Filter lines to genuine accomplishment / duty bullets, skipping section headers and summaries
    header_blacklist = {
        'summary', 'professional summary', 'executive summary', 'profile', 'objective', 'overview',
        'technical skills', 'skills', 'education', 'certifications', 'projects', 'professional experience',
        'experience', 'work history', 'contact', 'references', 'achievements'
    }
    extracted_bullets = []
    for l in lines:
        l_str = l.strip()
        l_lower = l_str.lower()
        if not l_str or len(l_str) < 15:
            continue
        if any(h == l_lower or l_lower.startswith(h + ':') for h in header_blacklist):
            continue
        if any(skip in l_lower for skip in ['@', 'phone:', 'linkedin.com', 'github.com', 'gpa:', 'bachelor of', 'master of', 'university', 'curriculum vitae']):
            continue
        if l_str.startswith(('•', '-', '*', '–')):
            clean_b = re.sub(r'^[•\-\*\–\s]+', '', l_str).strip()
            if len(clean_b) > 15:
                extracted_bullets.append(clean_b)
        elif len(l_str) > 30 and l_str[0].isupper() and l_str.endswith('.') and not any(kw in l_lower for kw in ['years of experience', 'experienced', 'dedicated', 'seeking', 'enthusiastic']):
            extracted_bullets.append(l_str)

    bullets = extracted_bullets if extracted_bullets else [l for l in lines if l.startswith(('•', '-', '*', '–')) or len(l) > 25]
    metric_regex = re.compile(
        r'(\d+%\s*|[₹$]\s*[\d,]+(?:\.\d+)?\s*(?:k|m|lakhs?|crores?|million|billion)?|\b(?:rs\.?|inr)\s*[\d,]+(?:\.\d+)?|\b\d+\s*(?:k|m|lakhs?|crores?|million|thousand|users|clients|engineers|developers|projects|hours|months|years|parts|tons|seconds|ms)\b|\b\d{2,}\b)',
        re.IGNORECASE
    )
    bullets_with_metrics = [b for b in bullets if metric_regex.search(b)]
    unquantified_bullets = [b for b in bullets if not metric_regex.search(b)]
    metric_ratio = len(bullets_with_metrics) / max(1, len(bullets))

    if metric_ratio >= 0.45:
        metrics_score = 25
    elif metric_ratio >= 0.30:
        metrics_score = 21
    elif metric_ratio >= 0.18:
        metrics_score = 16
    elif metric_ratio > 0.05:
        metrics_score = 11
    else:
        metrics_score = 5

    # 3. Action Verbs (Max 20)
    strong_action_verbs = {
        'designed', 'developed', 'led', 'implemented', 'spearheaded', 'orchestrated', 'built',
        'optimized', 'engineered', 'reduced', 'increased', 'managed', 'created', 'conducted',
        'automated', 'deployed', 'collaborated', 'architected', 'streamlined', 'analyzed',
        'delivered', 'mentored', 'established', 'formulated', 'executed', 'published', 'awarded',
        'solved', 'monitored', 'tested', 'audited', 'synthesized', 'pioneered', 'directed'
    }
    action_verb_count = 0
    for b in bullets:
        first_words = re.findall(r'\b[A-Za-z]+\b', b.lower())[:3]
        if any(w in strong_action_verbs for w in first_words):
            action_verb_count += 1

    verb_ratio = action_verb_count / max(1, len(bullets))
    if verb_ratio >= 0.60:
        action_verb_score = 20
    elif verb_ratio >= 0.40:
        action_verb_score = 16
    elif verb_ratio >= 0.20:
        action_verb_score = 12
    else:
        action_verb_score = 6

    # 4. Skill Relevance and Depth (Max 20)
    num_skills = len(skills)
    if num_skills >= 15:
        skills_score = 20
    elif num_skills >= 10:
        skills_score = 17
    elif num_skills >= 6:
        skills_score = 14
    elif num_skills >= 3:
        skills_score = 9
    else:
        skills_score = 4

    # 5. Readability & Formatting (Max 15)
    formatting_score = 0
    if 300 <= word_count <= 850:
        formatting_score += 8
    elif 200 <= word_count <= 1100:
        formatting_score += 5
    else:
        formatting_score += 2

    if len(bullets) >= 6:
        formatting_score += 4
    elif len(bullets) >= 3:
        formatting_score += 2

    has_cert_or_achieve = bool(re.search(r'\b(certifications?|certified|achievements?|awards?|honors?)\b', text_lower))
    if has_cert_or_achieve:
        formatting_score += 3

    total_score = structure_score + metrics_score + action_verb_score + skills_score + formatting_score
    total_score = max(15, min(97, total_score))

    return {
        "score": total_score,
        "breakdown": {
            "structure": {"score": structure_score, "max": 20},
            "metrics": {"score": metrics_score, "max": 25},
            "action_verbs": {"score": action_verb_score, "max": 20},
            "verbs": {"score": action_verb_score, "max": 20},
            "skills": {"score": skills_score, "max": 20},
            "formatting": {"score": formatting_score, "max": 15},
            "format": {"score": formatting_score, "max": 15}
        },
        "stats": {
            "word_count": word_count,
            "total_bullets": len(bullets),
            "quantified_bullets": len(bullets_with_metrics),
            "metric_percentage": round(metric_ratio * 100, 1),
            "action_verb_percentage": round(verb_ratio * 100, 1)
        },
        "bullets_with_metrics_samples": bullets_with_metrics[:3],
        "bullets_unquantified_samples": unquantified_bullets[:3]
    }

# ============================================================================
# 5. DYNAMIC STRENGTHS, WEAKNESSES & RECOMMENDATIONS ENGINE
# ============================================================================
def generate_candidate_insights(text, skills, exp_info, score_info, domain):
    """
    Produces customized, non-generic strengths and actionable weaknesses
    grounded in candidate's real profile, metrics, and domain.
    """
    strengths = []
    improvements = []
    recommendations = []
    
    skill_names = [s["name"] for s in skills]
    text_lower = text.lower()
    
    # ---------------- STRENGTHS ----------------
    # 1. Quantifiable metrics strength
    if score_info["stats"]["quantified_bullets"] > 0:
        sample = score_info["bullets_with_metrics_samples"][0]
        # Clean sample bullet
        sample_clean = re.sub(r'^[•\-\*\s]+', '', sample).strip()
        if len(sample_clean) > 80:
            sample_clean = sample_clean[:77] + "..."
        strengths.append(f"Demonstrated Measurable Impact: Quantified achievements present (e.g. \"{sample_clean}\").")
    
    # 2. Domain toolset depth
    domain_skills = [s["name"] for s in skills if s.get("domain") in [domain, "Mechanical", "Software", "Cloud/DevOps", "Data/AI"]]
    if len(domain_skills) >= 4:
        top_tools = ", ".join(domain_skills[:4])
        strengths.append(f"Deep {domain} Toolset: Proficient with core industry technologies ({top_tools}).")
    
    # 3. Leadership & Collaboration
    if any(k in text_lower for k in ['led', 'mentored', 'supervised', 'cross-functional', 'lead engineer', 'team lead']):
        strengths.append("Technical Leadership & Mentorship: Documented ownership of teams, junior engineer mentoring, or cross-functional delivery.")
    
    # 4. Standards & Compliance
    if any(k in text_lower for k in ['iso', 'asme', 'astm', 'gd&t', 'hipaa', 'ci/cd', 'agile', 'soc2', 'standards']):
        strengths.append("Engineering Rigor & Industry Standards: Adheres to standardized workflows, quality standards, and formal methodologies.")
    
    # 5. Certifications & Honors
    if bool(re.search(r'\b(certified|certification|award|honors?|published)\b', text_lower)):
        strengths.append("Validated Credentials & Recognition: Highlights professional certifications and formal industry accolades.")
    elif exp_info["final_years"] >= 3:
        strengths.append(f"Solid Career Trajectory: {exp_info['display_text']} showing steady career progression.")

    # ---------------- WEAKNESSES & IMPROVEMENTS ----------------
    # 1. Unquantified bullets
    unquantified = score_info["stats"]["total_bullets"] - score_info["stats"]["quantified_bullets"]
    if unquantified > 0:
        pct = 100 - int(score_info["stats"]["metric_percentage"])
        improvements.append(f"Unquantified Bullet Points: {pct}% of your bullet points describe duties without quantifiable metrics (%, $, time, or scale saved).")
    
    # 2. Domain-specific skill gaps
    if domain == "Mechanical":
        missing_mech = []
        if not any(k in text_lower for k in ['dfm', 'dfa']): missing_mech.append("DFM/DFA")
        if not any(k in text_lower for k in ['plm', 'pdm', 'windchill', 'teamcenter']): missing_mech.append("PDM/PLM Systems")
        if not any(k in text_lower for k in ['tolerance analysis', 'stack-up']): missing_mech.append("Tolerance Stack-up Analysis")
        if missing_mech:
            improvements.append(f"Adjacent Manufacturing Skills: Consider adding experience with {', '.join(missing_mech)} to stand out.")
    elif domain == "Software":
        missing_swe = []
        if not any(k in text_lower for k in ['jest', 'cypress', 'testing', 'unit test', 'pytest']): missing_swe.append("Automated Testing (Jest/Cypress)")
        if not any(k in text_lower for k in ['system design', 'architecture']): missing_swe.append("System Design & Architecture")
        if not any(k in text_lower for k in ['kubernetes', 'k8s']): missing_swe.append("Kubernetes Orchestration")
        if missing_swe:
            improvements.append(f"Modern Engineering Gaps: Highlight {', '.join(missing_swe)} for senior recruiter appeal.")

    # 3. Professional Links
    if not re.search(r'github\.com|portfolio|linkedin\.com/in/', text_lower):
        improvements.append("Portfolio / Profile Links Missing: Lack of clickable LinkedIn, GitHub, or live portfolio links impairs recruiter verification.")

    # 4. Summary Tailoring
    if not re.search(r'\b(seeking|target|focused on)\b', text_lower):
        improvements.append("Target Role Alignment: The summary section should clearly articulate the exact target seniority and niche role sought.")

    # ---------------- RECOMMENDATIONS (DYNAMIC, HIGHLY PERSONALIZED & ACTIONABLE) ----------------
    profile = extract_candidate_profile(text) if text else {"role": f"{domain} Specialist", "company": ""}
    cand_role = profile.get("role", f"{domain} Specialist")
    cand_company = profile.get("company", "")
    years = float(exp_info.get("final_years") or exp_info.get("years") or 2.0)
    skill_names_lower = {s.lower() for s in skill_names}
    top_domain_skills = [s["name"] for s in skills[:3]]

    # 1. Action Bullet Transformation (Google XYZ Metric Formula) with candidate's REAL unquantified bullet
    unquantified_samples = score_info.get("bullets_unquantified_samples", [])
    if unquantified_samples:
        clean_sample = re.sub(r'^[•\-\*\–\s]+', '', unquantified_samples[0]).strip()
        if len(clean_sample) > 85:
            clean_sample = clean_sample[:82] + "..."
        
        sample_low = clean_sample.lower()
        if domain == "Software":
            if any(k in sample_low for k in ['api', 'backend', 'rest', 'server', 'node', 'django', 'spring', 'endpoint']):
                rewrite_ex = "Architected 12+ RESTful API endpoints in Node.js, achieving <120ms p95 latency and supporting 50,000+ daily requests"
            elif any(k in sample_low for k in ['frontend', 'react', 'ui', 'web', 'app', 'interface', 'responsive']):
                rewrite_ex = "Developed responsive modular UI in React, accelerating page load speeds by 35% and improving conversion by 14%"
            elif any(k in sample_low for k in ['database', 'query', 'sql', 'mongo', 'postgres', 'data']):
                rewrite_ex = "Optimized database schema and query indexes, reducing query execution times by 40% under peak load"
            elif any(k in sample_low for k in ['deploy', 'cloud', 'docker', 'pipeline', 'ci/cd', 'aws']):
                rewrite_ex = "Automated containerized deployment via Docker/AWS, reducing deployment cycle times by 50%"
            else:
                rewrite_ex = "Delivered core full-stack features end-to-end, reducing sprint backlog by 30% and eliminating 15+ high-priority bugs"
            recommendations.append(f"Action Bullet Transformation: For your bullet \"{clean_sample}\", replace passive duty phrasing with Google's XYZ metric formula (\"Accomplished [X], as measured by [Y], by doing [Z]\"). Example: \"{rewrite_ex}\".")
        
        elif domain == "Mechanical":
            if any(k in sample_low for k in ['automotive', 'chassis', 'vehicle', 'car', 'powertrain']):
                rewrite_ex = "Engineered 8+ automotive sub-assemblies in SolidWorks and validated via ANSYS FEA, reducing component mass by 22% while maintaining a 2.0x safety factor"
            elif any(k in sample_low for k in ['aircraft', 'aerospace', 'landing', 'flight', 'wing']):
                rewrite_ex = "Developed precision aerospace structures meeting FAA/ISO standards, passing 100% of static stress tests with zero re-machining cycles"
            elif any(k in sample_low for k in ['machinery', 'equipment', 'industrial', 'tooling', 'machine']):
                rewrite_ex = "Designed automated tooling fixtures in SolidWorks/AutoCAD, cutting cycle time by 20% and saving ₹3,50,000 in manufacturing scrap annually"
            elif any(k in sample_low for k in ['thermal', 'battery', 'cooling', 'fluid', 'heat', 'flow']):
                rewrite_ex = "Conducted CFD/thermal simulations on cooling enclosures, lowering peak operating temperatures by 8°C"
            else:
                rewrite_ex = "Engineered production CAD models in SolidWorks with GD&T datum tolerance callouts, cutting vendor tooling turnaround by 3 weeks"
            recommendations.append(f"Action Bullet Transformation: For your bullet \"{clean_sample}\", replace passive duty phrasing with Google's XYZ metric formula (\"Accomplished [X], as measured by [Y], by doing [Z]\"). Example: \"{rewrite_ex}\".")
        
        elif domain in ["Data/AI", "Machine Learning"]:
            rewrite_ex = "Trained and deployed predictive ML models with 92% validation accuracy, reducing operational forecasting error by 25%"
            recommendations.append(f"Action Bullet Transformation: In your bullet \"{clean_sample}\", replace passive duty descriptions with validation metrics and business outcomes. Example: \"{rewrite_ex}\".")
        else:
            rewrite_ex = "Spearheaded operational process optimization, cutting project delivery cycle times by 25% and saving 15 staff hours weekly"
            recommendations.append(f"Action Bullet Transformation: For your bullet \"{clean_sample}\", quantify commercial outcomes using Google's XYZ formula. Example: \"{rewrite_ex}\".")

    # 2. Context-Aware Technical Gap Recommendations (Checked against candidate's ACTUAL skills)
    if domain == "Software":
        if not any(k in skill_names_lower for k in ['jest', 'cypress', 'testing', 'unit test', 'pytest', 'junit']):
            recommendations.append("Automated Test Coverage & TDD: While your full-stack proficiencies are strong, your resume lacks automated testing frameworks (Jest, Cypress, or PyTest). Adding bullet points with code coverage metrics (e.g. 'implemented Jest test suites achieving 85%+ code coverage') signals production-grade engineering rigor.")
        elif not any(k in skill_names_lower for k in ['typescript', 'ts']):
            recommendations.append("TypeScript Strict Typing: Adopting TypeScript over standard JavaScript eliminates runtime exceptions and is required by 85%+ of Tier-1 software engineering teams.")
        elif not any(k in skill_names_lower for k in ['redis', 'memcached', 'cache']):
            recommendations.append("In-Memory Caching (Redis): Highlight distributed caching layers (Redis) to demonstrate performance optimization for high-concurrency API backends.")
        elif not any(k in skill_names_lower for k in ['system design', 'architecture', 'distributed systems']):
            recommendations.append("Architectural Trade-Off Documentation: Highlight system design decisions (e.g., event streaming, database indexing strategies, microservices decoupling) to qualify for Senior/Staff roles.")
        else:
            recommendations.append("Cloud Native CI/CD Velocity: Quantify zero-downtime deployment pipelines, rollback automation, and cloud cost optimizations across your infrastructure.")

    elif domain == "Mechanical":
        if not any(k in skill_names_lower for k in ['dfm', 'dfa', 'dfm / dfa']):
            recommendations.append("DFM / DFA Tooling Optimization: Highlight specific Design for Manufacturing (DFM) and Design for Assembly (DFA) optimizations for machined or molded components to quantify tooling and scrap savings.")
        elif not any(k in skill_names_lower for k in ['plm', 'pdm', 'windchill', 'teamcenter']):
            recommendations.append("Enterprise PLM Workflow Integration: Explicitly cite experience with enterprise PDM/PLM systems (e.g., PTC Windchill or Siemens Teamcenter) to prove turnkey production handoff to vendor machine shops.")
        elif not any(k in skill_names_lower for k in ['tolerance analysis', 'stack-up', 'stackup']):
            recommendations.append("Tolerance Stack-Up Analysis: Document 1D/3D worst-case and RSS statistical tolerance stack-up analyses to demonstrate precision manufacturing quality control.")
        elif not any(k in skill_names_lower for k in ['fea / stress analysis', 'cfd / fluid dynamics', 'ansys']):
            recommendations.append("Computational Simulation Validation: Correlate FEA/CFD stress and thermal simulations with physical laboratory strain-gauge or dynamometer tests to validate virtual models.")
        else:
            recommendations.append("Advanced Additive & Lightweighting: Showcase topology optimization and additive manufacturing (DMLS/SLS) for high-performance structural components.")

    elif domain in ["Data/AI", "Machine Learning"]:
        if not any(k in skill_names_lower for k in ['mlops', 'fastapi', 'docker', 'mlflow']):
            recommendations.append("MLOps & Production Model Serving: Package your models with FastAPI and Docker to demonstrate end-to-end production serving readiness rather than isolated Jupyter notebooks.")
        else:
            recommendations.append("LLM & Generative AI Systems: Incorporate retrieval-augmented generation (RAG), vector databases, and AI agent architectures to command market premiums.")

    elif domain in ["DevOps", "Cloud"]:
        if not any(k in skill_names_lower for k in ['terraform', 'iac', 'ansible']):
            recommendations.append("Infrastructure-as-Code (Terraform): Formalize cloud environments using Terraform or Ansible to demonstrate automated, repeatable multi-region infrastructure provisioning.")
        else:
            recommendations.append("Observability & SLO Monitoring: Specify Prometheus, Grafana, and distributed tracing implementation with SLA/SLO uptime metrics.")
    else:
        recommendations.append("Measurable Business Impact: Feature at least 2 quantified business wins per position (budget managed, revenue growth, or process turnaround time cut).")

    # 3. Dual-Channel ATS Keyword Placement tailored to top skills
    if top_domain_skills:
        recommendations.append(f"Dual-Channel ATS Keyword Optimization: Ensure your top proficiencies ({', '.join(top_domain_skills)}) appear both in your Technical Skills section and directly within accomplishment bullets with quantified business outcomes, boosting recruiter keyword relevance.")
    else:
        recommendations.append("ATS Keyword Alignment: Align bullet headers and technical proficiencies directly with target job descriptions for high recruiter relevance.")

    # 4. Next-Tier Career Elevation Milestone (Tailored to seniority & title)
    comp_ref = f" at {cand_company}" if cand_company else ""
    if years < 2.5:
        recommendations.append(f"Autonomous Proof-of-Work: As an emerging {cand_role}, feature 2-3 comprehensive end-to-end projects with demonstrable links/repositories to prove autonomous delivery and minimize onboarding oversight.")
    elif years < 6.0:
        recommendations.append(f"Senior Elevation Milestone: Leverage your {years:.1f} years as {cand_role}{comp_ref} to demonstrate end-to-end subsystem ownership, architectural decision-making, and mentorship of junior engineers.")
    else:
        recommendations.append(f"Staff & Leadership Trajectory: As a senior professional with {years:.1f} years experience, pivot bullet focus from implementation tasks to organizational velocity: authoring RFCs, reducing cross-service bottlenecks, and delivering business ROI.")

    # 5. Professional Verification & Portfolio Links
    has_github = bool(re.search(r'github\.com', text_lower))
    has_linkedin = bool(re.search(r'linkedin\.com/in/', text_lower))
    has_portfolio = bool(re.search(r'portfolio|behance|dribbble', text_lower))

    if not has_linkedin:
        recommendations.append("Professional Recruiter Verification: Add a customized, clickable LinkedIn profile link (e.g. linkedin.com/in/yourname) in your contact header to facilitate instant recruiter vetting.")
    elif domain == "Software" and not has_github:
        recommendations.append("Technical Proof-of-Work: Adding a clickable GitHub profile link showcasing your repositories and clean commit history provides tangible code proof to technical hiring managers.")
    elif domain == "Mechanical" and not has_portfolio:
        recommendations.append("Hardware Portfolio Visibility: Provide a link to a digital portfolio showcasing 3D CAD renders, exploded assembly schematics, and FEA stress contour plots for your key design projects.")

    return strengths[:5], improvements[:5], recommendations[:5]

# ============================================================================
# 6. DYNAMIC CAREER INTELLIGENCE & MARKET DATA
# ============================================================================
def extract_candidate_profile(text):
    """
    Robustly extracts candidate name, most recent job title, and company from resume text.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = None
    role = None
    company = None
    
    # 1. Candidate Name detection from top lines
    blacklist_words = {'resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary', 'contact', 'email', 'phone', 'portfolio', 'page', 'objective', 'overview'}
    for line in lines[:6]:
        clean = re.sub(r'[^a-zA-Z\s\.\-]', '', line).strip()
        words = clean.split()
        if 2 <= len(words) <= 4:
            if not any(w.lower() in blacklist_words for w in words):
                if '@' not in line and 'http' not in line and not re.search(r'\d', line):
                    name = clean.title()
                    break
    
    # 2. Current / Recent Role and Company detection
    role_pattern = re.compile(
        r'^(?P<title>[A-Za-z\s/,\-&]+?)\s*(?:\||–|-|@|at)\s*(?P<company>[A-Za-z0-9\s,\.\-&]+?)\s*(?:\||–|-|\(|\d{4}|$)',
        re.IGNORECASE
    )
    
    for line in lines:
        if any(h in line.lower() for h in ['present', 'current', '2023', '2024', '2025', '2026', '2022']):
            m = role_pattern.match(line)
            if m:
                t = m.group('title').strip()
                c = m.group('company').strip()
                if 3 <= len(t) <= 45 and not any(k in t.lower() for k in ['university', 'college', 'bachelor', 'master', 'education', 'project']):
                    role = t.title()
                    company = c.title()
                    break

    # Fallback role from line 2 if title-like
    if not role and len(lines) > 1:
        cand_line = lines[1].strip()
        if len(cand_line) < 45 and not any(c in cand_line for c in ['@', '|', 'http', '(', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            role = cand_line.title()

    return {
        "name": name or "Professional Candidate",
        "role": role or "Engineering Specialist",
        "company": company or ""
    }

def format_inr(val) -> str:
    """Format numeric salary values into standard Indian Rupee notation (₹X,XX,XXX)"""
    val_int = int(round(float(val) / 10000.0) * 10000)
    s = str(abs(val_int))
    if len(s) <= 3:
        formatted = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
    return f"₹{formatted}"

def generate_career_intelligence_data(domain, exp_info, score_info, skills, text=""):
    """
    Builds hyper-personalized, candidate-specific career intelligence, salary insights,
    market positioning, and 3-phase career trajectory derived from the candidate's actual
    extracted skills, calculated experience timeline, ATS score, and resume details.
    """
    years = float(exp_info.get("final_years", 1.0))
    score = int(score_info.get("score", 75))
    seniority = exp_info.get("seniority", "Professional")
    skill_names = [s["name"] for s in skills]
    skill_names_lower = {s.lower() for s in skill_names}
    
    profile = extract_candidate_profile(text) if text else {
        "name": "Professional Candidate",
        "role": f"{seniority} {domain} Specialist",
        "company": ""
    }
    candidate_name = profile["name"]
    current_role = profile["role"]
    company = profile["company"]
    company_suffix = f" at {company}" if company else ""

    # 1. Detect candidate's dominant technical focus & sub-specialty
    sub_specialties = []
    if any(k in skill_names_lower for k in ['react', 'vue.js', 'angular', 'next.js', 'html5', 'css3 / modern css']):
        sub_specialties.append("Modern Frontend & Web UI")
    if any(k in skill_names_lower for k in ['node.js', 'express.js', 'django', 'spring boot', 'python', 'java', 'php', 'c#', 'c++']):
        sub_specialties.append("Backend APIs & Microservices")
    if any(k in skill_names_lower for k in ['aws', 'docker', 'kubernetes', 'ci/cd automation', 'git / version control']):
        sub_specialties.append("Cloud Infrastructure & DevOps")
    if any(k in skill_names_lower for k in ['mongodb', 'postgresql', 'mysql', 'redis']):
        sub_specialties.append("Database & Data Persistence")
    if any(k in skill_names_lower for k in ['solidworks', 'autocad', 'catia', 'fusion 360', 'inventor', 'product design']):
        sub_specialties.append("3D CAD & Product Design")
    if any(k in skill_names_lower for k in ['ansys', 'fea / stress analysis', 'cfd / fluid dynamics', 'thermal analysis', 'fatigue & durability testing']):
        sub_specialties.append("FEA & Computational Simulation")
    if any(k in skill_names_lower for k in ['cnc machining & milling', '3d printing / additive mfg', 'injection molding', 'dfm / dfa']):
        sub_specialties.append("Precision Tooling & Manufacturing")
    if any(k in skill_names_lower for k in ['gd&t (geometric dimensioning)', 'iso / asme / astm standards', 'six sigma & lean', 'quality assurance & testing']):
        sub_specialties.append("Quality Standards & GD&T Compliance")
    if any(k in skill_names_lower for k in ['machine learning', 'deep learning', 'pytorch', 'tensorflow', 'pandas', 'nlp']):
        sub_specialties.append("AI / Machine Learning Systems")
    
    primary_focus = sub_specialties[0] if sub_specialties else f"{domain} Engineering"
    top_tool = skill_names[0] if skill_names else f"{domain} Core"
    second_tool = skill_names[1] if len(skill_names) > 1 else "Modern Tooling"
    third_tool = skill_names[2] if len(skill_names) > 2 else "System Architecture"

    # 2. Dynamic Compensation Calculation in Indian Rupees (INR / ₹)
    if domain == "Software":
        base_salary = int(550000 + (years * 180000) + (score * 3500))
        next_salary = int(base_salary * 1.25)
    elif domain == "Mechanical":
        base_salary = int(450000 + (years * 135000) + (score * 3000))
        next_salary = int(base_salary * 1.20)
    elif domain == "Data/AI":
        base_salary = int(600000 + (years * 200000) + (score * 4000))
        next_salary = int(base_salary * 1.28)
    elif domain == "Cloud/DevOps":
        base_salary = int(550000 + (years * 180000) + (score * 3500))
        next_salary = int(base_salary * 1.24)
    else:
        base_salary = int(420000 + (years * 120000) + (score * 2500))
        next_salary = int(base_salary * 1.20)

    min_base = max(300000, int(base_salary * 0.88))
    max_base = int(base_salary * 1.15)
    salary_display = f"{format_inr(min_base)} - {format_inr(max_base)}"

    min_next = int(next_salary * 0.90)
    max_next = int(next_salary * 1.18)
    next_salary_display = f"{format_inr(min_next)} - {format_inr(max_next)}"

    # 3. Market standing & percentile
    if score >= 85:
        percentile = "Top 8%"
        market_standing = "Highly Competitive Candidate"
    elif score >= 75:
        percentile = "Top 18%"
        market_standing = "Strong Market Fit"
    elif score >= 65:
        percentile = "Top 35%"
        market_standing = "Competitive Baseline"
    else:
        percentile = "Developing"
        market_standing = "Growth Opportunity Profile"

    # 4. Dynamic 3-Phase Progression Roadmap (Directly addressing candidate's exact level and roles)
    if years < 2.5:
        career_roadmap = [
            {
                "phase": "Phase 1: Immediate Milestone",
                "timeline": "Next 6 - 12 Months",
                "target_role": f"Mid-Level {domain} Engineer",
                "focus": f"Transition from entry-level execution to autonomous delivery in {top_tool}. Eliminate code/design revision cycles and deliver features end-to-end.",
                "target_compensation": f"{format_inr(int(base_salary * 1.15))} - {format_inr(int(base_salary * 1.25))}",
                "unlock_skill": f"Production proficiency in {second_tool}"
            },
            {
                "phase": "Phase 2: Senior Elevation",
                "timeline": "Year 2 - 3",
                "target_role": f"Senior {primary_focus} Specialist",
                "focus": f"Lead technical design pods, establish coding/engineering standards, and mentor incoming junior engineers across {top_tool} and {second_tool} workflows.",
                "target_compensation": f"{format_inr(int(base_salary * 1.35))} - {format_inr(int(base_salary * 1.50))}",
                "unlock_skill": "System architecture & CI/CD deployment"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"Lead {domain} Architect / Engineering Lead",
                "focus": f"Own critical cross-functional initiatives, author engineering RFCs, and direct technology evaluations that drive departmental business outcomes.",
                "target_compensation": f"{format_inr(int(base_salary * 1.60))} - {format_inr(int(base_salary * 1.85))}",
                "unlock_skill": "Cross-system scaling and leadership governance"
            }
        ]
    elif years < 6.0:
        career_roadmap = [
            {
                "phase": "Phase 1: Immediate Milestone",
                "timeline": "Next 6 - 12 Months",
                "target_role": f"Lead {domain} Engineer / Technical Pod Lead",
                "focus": f"Advance from {current_role}{company_suffix} into lead ownership. Drive sprint delivery for {primary_focus} initiatives and streamline team execution.",
                "target_compensation": next_salary_display,
                "unlock_skill": f"Advanced {top_tool} scaling & architectural RFCs"
            },
            {
                "phase": "Phase 2: Senior Elevation",
                "timeline": "Year 2 - 3",
                "target_role": f"Staff {domain} Architect / Principal Specialist",
                "focus": "Spearhead system-wide architectural transformation, resolve cross-service bottlenecks, and standardize engineering quality across multiple teams.",
                "target_compensation": f"{format_inr(int(base_salary * 1.30))} - {format_inr(int(base_salary * 1.45))}",
                "unlock_skill": "Multi-system distributed design & performance tuning"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"Director of {domain} Engineering / Head of Technology",
                "focus": "Executive technical governance, talent scaling, engineering budget allocation, and alignment of technical capabilities with enterprise business strategy.",
                "target_compensation": f"{format_inr(int(base_salary * 1.55))} - {format_inr(int(base_salary * 1.85))}+",
                "unlock_skill": "Strategic technology roadmapping & executive management"
            }
        ]
    else:
        career_roadmap = [
            {
                "phase": "Phase 1: Immediate Milestone",
                "timeline": "Next 6 - 12 Months",
                "target_role": f"Principal {domain} Engineer / Engineering Manager",
                "focus": f"Leverage {years:.1f} years of tenure and {current_role} experience to drive strategic architectural initiatives and technical alignment across engineering squads.",
                "target_compensation": next_salary_display,
                "unlock_skill": "Enterprise platform architecture & strategic governance"
            },
            {
                "phase": "Phase 2: Senior Elevation",
                "timeline": "Year 2 - 3",
                "target_role": f"Director of {domain} Engineering",
                "focus": "Direct multiple engineering teams, establish engineering excellence KPIs, optimize infrastructure CAPEX/OPEX, and recruit top engineering talent.",
                "target_compensation": f"{format_inr(int(base_salary * 1.25))} - {format_inr(int(base_salary * 1.45))}",
                "unlock_skill": "Multi-team organizational leadership & budget ownership"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"VP of Engineering / Chief Technology Officer (CTO)",
                "focus": "Executive C-level technology vision, global infrastructure resilience, digital transformation, and investor/board-level technology alignment.",
                "target_compensation": f"{format_inr(int(base_salary * 1.50))} - {format_inr(int(base_salary * 1.90))}+",
                "unlock_skill": "Executive enterprise leadership & board-level strategy"
            }
        ]

    # 5. Dynamic Tailored Skill Bridges (Contextual to Candidate's ACTUAL Stack)
    tailored_gaps = []
    if domain == "Software":
        if "typescript" not in skill_names_lower:
            tailored_gaps.append({
                "skill": "TypeScript Strict Typing",
                "impact": "+15% Salary Premium",
                "rationale": f"Adding static typing over your existing JavaScript stack eliminates runtime exceptions and is required by 85%+ of Tier-1 software teams."
            })
        if not any(k in skill_names_lower for k in ['redis', 'memcached']):
            tailored_gaps.append({
                "skill": "Distributed In-Memory Caching (Redis)",
                "impact": "+12% Salary Premium",
                "rationale": "Essential for backend microservices to minimize database roundtrips and handle high concurrent user traffic."
            })
        if not any(k in skill_names_lower for k in ['kubernetes', 'terraform']):
            tailored_gaps.append({
                "skill": "Kubernetes & Infrastructure-as-Code",
                "impact": "+18% Salary Premium",
                "rationale": f"Complements your {top_tool} experience by enabling automated cluster orchestration and zero-downtime deployment pipelines."
            })
        if not tailored_gaps:
            tailored_gaps.append({
                "skill": "High-Concurrency System Design",
                "impact": "+20% Salary Premium",
                "rationale": "Designing fault-tolerant distributed consensus algorithms and event-streaming pipelines (Kafka) for 500K+ RPS scale."
            })
            tailored_gaps.append({
                "skill": "Generative AI Agent Integration",
                "impact": "+22% Salary Premium",
                "rationale": "Integrating vector embeddings, RAG architectures, and autonomous AI agents directly into production application backends."
            })
    elif domain == "Mechanical":
        if not any(k in skill_names_lower for k in ['dfm', 'dfa', 'dfm / dfa']):
            tailored_gaps.append({
                "skill": "DFM / DFA (Design for Manufacturing)",
                "impact": "+16% Salary Premium",
                "rationale": f"Directly optimizes tooling costs and cycle times for components designed in {top_tool}, proving commercial impact."
            })
        if not any(k in skill_names_lower for k in ['gd&t (geometric dimensioning)', 'gd&t']):
            tailored_gaps.append({
                "skill": "GD&T ASME Y14.5 Stackup Analysis",
                "impact": "+14% Salary Premium",
                "rationale": "Mandatory for production release and supplier precision inspection, bridging 3D CAD models with physical factory quality control."
            })
        if not any(k in skill_names_lower for k in ['ansys', 'fea / stress analysis', 'cfd / fluid dynamics']):
            tailored_gaps.append({
                "skill": "Multiphysics FEA / CFD Simulation",
                "impact": "+18% Salary Premium",
                "rationale": "Elevates purely geometric CAD modeling into computational stress, thermal, and fatigue life prediction."
            })
        if not tailored_gaps:
            tailored_gaps.append({
                "skill": "Additive Manufacturing for Production (DMLS)",
                "impact": "+15% Salary Premium",
                "rationale": "Designing topology-optimized metallic components for flight-ready aerospace and high-performance automotive platforms."
            })
            tailored_gaps.append({
                "skill": "Digital Twin & Real-Time Sensor Telemetry",
                "impact": "+18% Salary Premium",
                "rationale": "Connecting physical hardware sensor telemetry with real-time computational mechanical models."
            })
    else:
        tailored_gaps.append({
            "skill": "Advanced Data Analytics & KPI Dashboards",
            "impact": "+14% Salary Premium",
            "rationale": "Transforms operational domain knowledge into executive-level visibility and quantified process optimization."
        })
        tailored_gaps.append({
            "skill": "Agile / Scrum Delivery Leadership",
            "impact": "+12% Salary Premium",
            "rationale": "Demonstrates structured cross-functional dependency management and sprint predictability."
        })

    # High ROI Compensation Premiums (specific skill bonuses)
    comp_premiums = [
        {"skill": tailored_gaps[0]["skill"], "premium": tailored_gaps[0]["impact"], "details": f"Unlocks next-tier {career_roadmap[0]['target_role']} compensation."},
        {"skill": tailored_gaps[1]["skill"] if len(tailored_gaps) > 1 else "Cloud Architecture", "premium": tailored_gaps[1]["impact"] if len(tailored_gaps) > 1 else "+15% Market Premium", "details": "Qualifies candidate for cross-functional technical leadership roles."}
    ]

    # Target Industry Matches
    if domain == "Software":
        industry_matches = [
            {"name": "Cloud Infrastructure & Enterprise SaaS", "match": "95%", "reason": f"High demand for engineers skilled in {top_tool} and microservices."},
            {"name": "FinTech & Real-Time Digital Banking", "match": "91%", "reason": "Requires high-throughput backend systems and modern frontend dashboards."},
            {"name": "HealthTech & Telemedicine Platforms", "match": "87%", "reason": "Growing demand for secure web platforms and distributed APIs."}
        ]
        roles = [
            career_roadmap[0]["target_role"],
            f"{primary_focus} Specialist",
            "Cloud & Distributed Systems Architect",
            "Full Stack Technical Lead"
        ]
        industries = ["Cloud Infrastructure & SaaS", "FinTech & Digital Banking", "HealthTech & Telehealth", "E-Commerce Platforms"]
    elif domain == "Mechanical":
        industry_matches = [
            {"name": "Automotive & Electric Vehicles (EV)", "match": "96%", "reason": f"Surging demand for CAD/FEA engineers in lightweighting and battery packaging with {top_tool}."},
            {"name": "Aerospace & Defense Systems", "match": "92%", "reason": f"Strict adherence to {top_tool} standards, stress analysis, and GD&T."},
            {"name": "Robotics & Industrial Automation", "match": "88%", "reason": "High volume of design roles for precision end-effectors and automated tooling."}
        ]
        roles = [
            career_roadmap[0]["target_role"],
            f"{primary_focus} Specialist",
            "Thermal & Structural FEA Engineer",
            "Hardware Product Development Lead"
        ]
        industries = ["Automotive & Electric Vehicles", "Aerospace & Defense", "Robotics & Automation", "Medical Devices"]
    else:
        industry_matches = [
            {"name": "Enterprise Technology Consulting", "match": "90%", "reason": "Demand for structured problem solving and technical implementation."},
            {"name": "Operations & Logistics Infrastructure", "match": "86%", "reason": "Focus on system efficiency, cost reduction, and process automation."}
        ]
        roles = [
            career_roadmap[0]["target_role"],
            "Technical Solutions Lead",
            "Cross-Functional Project Manager",
            "Process Improvement Consultant"
        ]
        industries = ["Enterprise Technology", "Management Consulting", "Healthcare Operations", "Financial Services"]

    # Market insights
    market_insights = [
        f"Compensation Benchmark: {salary_display} based on {years:.1f} years demonstrated experience and an ATS Score of {score}/100.",
        f"Specialization Premium: Candidate profile in '{primary_focus}' commands a ~15-22% premium over generalist applicants.",
        f"Top Hiring Demand: {industry_matches[0]['name']} currently accounts for the highest volume of openings matching your skill matrix ({industry_matches[0]['match']} Match)."
    ]

    return {
        "candidate_name": candidate_name,
        "current_role": current_role,
        "company": company,
        "domain": domain,
        "primary_focus": primary_focus,
        "seniority": seniority,
        "years": years,
        "years_numeric": years,
        "percentile": percentile,
        "market_standing": market_standing,
        "salary_range": salary_display,
        "next_level_salary": next_salary_display,
        "career_roadmap": career_roadmap,
        "tailored_gaps": tailored_gaps[:2],
        "comp_premiums": comp_premiums,
        "industry_matches": industry_matches,
        "experience_level": f"{seniority} ({years:.1f} yrs)",
        "salary_insights": [
            f"Current Market Value: {salary_display} based on {years:.1f} yrs tenure in {primary_focus}",
            f"Next Promotion Target: {next_salary_display} as {career_roadmap[0]['target_role']}",
            f"Top Comp Multiplier: {comp_premiums[0]['skill']} ({comp_premiums[0]['premium']})"
        ],
        "skill_gaps": [f"{g['skill']}: {g['rationale']}" for g in tailored_gaps[:2]],
        "industry_trends": [f"{ind['name']} ({ind['match']} Match): {ind['reason']}" for ind in industry_matches],
        "career_path": [f"{step['phase']} ({step['timeline']}): {step['target_role']} — {step['focus']}" for step in career_roadmap],
        "roles": roles,
        "industries": industries,
        "market_insights": market_insights
    }

# ============================================================================
# 7. DYNAMIC RADAR CHART DATA
# ============================================================================
def generate_radar_chart_data(skills, domain, score_info):
    """
    Generates dynamic Radar Chart dimensions matching the candidate's actual domain
    instead of a hardcoded software chart.
    """
    base_score = score_info["score"]
    
    if domain == "Mechanical":
        labels = [
            'CAD & 3D Modeling',
            'FEA & Simulation',
            'Manufacturing (CNC/3D)',
            'GD&T & Standards',
            'Materials & Testing',
            'Project Management',
            'Process Optimization',
            'Quality Control'
        ]
        # Calculate dynamic proficiencies based on detected skills
        skill_str = " ".join([s["name"].lower() for s in skills])
        cad_score = 92 if any(k in skill_str for k in ['solidworks', 'autocad', 'catia']) else 70
        fea_score = 88 if any(k in skill_str for k in ['ansys', 'fea', 'cfd', 'stress']) else 65
        mfg_score = 85 if any(k in skill_str for k in ['cnc', '3d printing', 'injection']) else 60
        gdt_score = 90 if any(k in skill_str for k in ['gd&t', 'iso', 'asme']) else 65
        mat_score = 82 if any(k in skill_str for k in ['composite', 'materials', 'fatigue']) else 65
        pm_score = 80 if any(k in skill_str for k in ['project', 'agile', 'led']) else 60
        proc_score = 85 if any(k in skill_str for k in ['six sigma', 'cost', 'reduction']) else 65
        qc_score = 88 if any(k in skill_str for k in ['quality', 'inspection', 'testing']) else 70
        values = [cad_score, fea_score, mfg_score, gdt_score, mat_score, pm_score, proc_score, qc_score]
    elif domain == "Software":
        labels = [
            'Frontend & UI/UX',
            'Backend & Microservices',
            'Cloud & AWS/DevOps',
            'Databases & SQL/NoSQL',
            'System Architecture',
            'CI/CD & Automation',
            'Agile & Team Leadership',
            'Problem Solving & Scale'
        ]
        skill_str = " ".join([s["name"].lower() for s in skills])
        fe_score = 90 if any(k in skill_str for k in ['react', 'vue', 'angular', 'html']) else 70
        be_score = 88 if any(k in skill_str for k in ['node', 'express', 'django', 'python', 'java']) else 68
        cloud_score = 85 if any(k in skill_str for k in ['aws', 'azure', 'docker', 'kubernetes']) else 60
        db_score = 86 if any(k in skill_str for k in ['mongodb', 'postgres', 'sql', 'redis']) else 65
        arch_score = 84 if any(k in skill_str for k in ['microservices', 'restful', 'graphql']) else 65
        cicd_score = 88 if any(k in skill_str for k in ['ci/cd', 'docker', 'git']) else 62
        lead_score = 82 if any(k in skill_str for k in ['agile', 'mentoring', 'led']) else 60
        scale_score = 85 if score_info["stats"]["quantified_bullets"] >= 3 else 70
        values = [fe_score, be_score, cloud_score, db_score, arch_score, cicd_score, lead_score, scale_score]
    else:
        labels = [
            'Domain Competency',
            'Project Management',
            'Data Analysis',
            'Process Improvement',
            'Stakeholder Management',
            'Technical Communication',
            'Quality Assurance',
            'Strategic Planning'
        ]
        values = [80, 75, 70, 78, 82, 85, 74, 76]

    return {
        "labels": labels,
        "values": values
    }

# ============================================================================
# 8. ROLE-BASED DYNAMIC RECOMMENDATIONS ENGINE
# ============================================================================
ROLE_TAXONOMY = {
    'mechanical-engineer': {
        'title': 'Mechanical Engineer',
        'domain': 'Mechanical',
        'core_skills': ['SolidWorks', 'AutoCAD', 'ANSYS', 'CATIA', 'GD&T', 'Manufacturing Processes'],
        'advanced_skills': ['DFM / DFA', 'FEA', 'CFD', 'PDM / PLM', 'Six Sigma', 'Thermodynamics'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1500000), 'senior': (1500000, 2800000)},
        'companies': ['Tesla', 'Boeing', 'Tata Motors', 'Mahindra', 'L&T', 'General Electric', 'Bosch', 'Apple Hardware'],
        'target_cert': 'CSWP (Certified SOLIDWORKS Professional) or Six Sigma Green Belt',
        'growth_potential': 'High demand across EV, Robotics, and Aerospace sectors'
    },
    'software-engineer': {
        'title': 'Software Engineer',
        'domain': 'Software',
        'core_skills': ['JavaScript', 'TypeScript', 'React', 'Node.js', 'Python', 'SQL', 'Git', 'REST APIs'],
        'advanced_skills': ['AWS', 'Docker', 'Kubernetes', 'Microservices', 'System Design', 'Redis', 'CI/CD', 'GraphQL'],
        'salary_base': {'entry': (550000, 900000), 'mid': (900000, 1800000), 'senior': (1800000, 3500000)},
        'companies': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Netflix', 'Uber', 'Atlassian', 'Stripe'],
        'target_cert': 'AWS Certified Solutions Architect or CKA (Kubernetes)',
        'growth_potential': 'Exponential growth across Cloud, AI platforms, and SaaS products'
    },
    'data-scientist': {
        'title': 'Data Scientist',
        'domain': 'Data/AI',
        'core_skills': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-Learn', 'Statistics'],
        'advanced_skills': ['Deep Learning', 'PyTorch', 'TensorFlow', 'NLP', 'MLOps', 'FastAPI', 'Docker'],
        'salary_base': {'entry': (600000, 950000), 'mid': (1000000, 1900000), 'senior': (1900000, 3600000)},
        'companies': ['OpenAI', 'Google DeepMind', 'Amazon', 'Netflix', 'Uber', 'Spotify', 'Fractal Analytics'],
        'target_cert': 'Databricks Certified Machine Learning Associate or AWS ML Specialty',
        'growth_potential': 'Surging enterprise demand for Generative AI, RAG, and predictive analytics'
    },
    'product-manager': {
        'title': 'Product Manager',
        'domain': 'Management',
        'core_skills': ['Product Strategy', 'User Research', 'Agile / Scrum', 'Roadmapping', 'Data Analysis', 'Wireframing'],
        'advanced_skills': ['A/B Testing', 'SQL', 'Market Sizing', 'Stakeholder Management', 'Go-To-Market'],
        'salary_base': {'entry': (600000, 1000000), 'mid': (1100000, 2000000), 'senior': (2000000, 3800000)},
        'companies': ['Google', 'Apple', 'Microsoft', 'Swiggy', 'Zomato', 'CRED', 'Amazon', 'Uber'],
        'target_cert': 'Certified Scrum Product Owner (CSPO) or Pragmatic Institute Certified',
        'growth_potential': 'Leadership trajectory with direct influence on product vision and revenue'
    },
    'devops-engineer': {
        'title': 'DevOps & Cloud Engineer',
        'domain': 'Cloud/DevOps',
        'core_skills': ['Linux', 'AWS', 'Docker', 'Kubernetes', 'CI/CD Pipelines', 'Git', 'Python'],
        'advanced_skills': ['Terraform', 'Ansible', 'Prometheus', 'Grafana', 'Security / DevSecOps', 'Helm'],
        'salary_base': {'entry': (550000, 900000), 'mid': (1000000, 1800000), 'senior': (1800000, 3400000)},
        'companies': ['AWS', 'Google Cloud', 'Microsoft', 'Red Hat', 'HashiCorp', 'Datadog', 'CrowdStrike'],
        'target_cert': 'CKA (Certified Kubernetes Administrator) or AWS DevOps Engineer Professional',
        'growth_potential': 'Critical role across all digital businesses with high salary leverage'
    },
    'ui-ux-designer': {
        'title': 'UI/UX Designer',
        'domain': 'Design',
        'core_skills': ['Figma', 'Wireframing', 'Prototyping', 'User Research', 'Design Systems', 'Information Architecture'],
        'advanced_skills': ['Interaction Design', 'Usability Testing', 'HTML/CSS Basics', 'Design Tokens', 'Micro-interactions'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1400000), 'senior': (1400000, 2600000)},
        'companies': ['Adobe', 'Canva', 'Airbnb', 'Figma', 'Spotify', 'Razorpay', 'CRED'],
        'target_cert': 'Google UX Design Professional Certificate or Nielsen Norman Group UX Certified',
        'growth_potential': 'Strong demand in customer-facing consumer apps and B2B platforms'
    },
    'project-manager': {
        'title': 'Project / Delivery Manager',
        'domain': 'Management',
        'core_skills': ['Agile', 'Scrum', 'Risk Management', 'Sprint Planning', 'Stakeholder Communication', 'Jira'],
        'advanced_skills': ['PMP', 'CSM Certification', 'Resource Allocation', 'Vendor Management', 'Cross-Team Governance'],
        'salary_base': {'entry': (550000, 850000), 'mid': (900000, 1600000), 'senior': (1600000, 3000000)},
        'companies': ['TCS', 'Infosys', 'Accenture', 'Deloitte', 'Cognizant', 'Capgemini', 'IBM'],
        'target_cert': 'PMP (Project Management Professional) or PMI-ACP',
        'growth_potential': 'Essential for orchestrating high-value, multi-crore digital transformations'
    },
    'business-analyst': {
        'title': 'Business Analyst',
        'domain': 'Analytics',
        'core_skills': ['SQL', 'Excel', 'Power BI / Tableau', 'Requirements Gathering', 'Process Flowcharting'],
        'advanced_skills': ['Python Analytics', 'Financial Forecasting', 'Gap Analysis', 'Agile User Stories'],
        'salary_base': {'entry': (500000, 800000), 'mid': (850000, 1500000), 'senior': (1500000, 2600000)},
        'companies': ['Deloitte', 'EY', 'KPMG', 'PwC', 'McKinsey', 'ZS Associates'],
        'target_cert': 'CBAP (Certified Business Analysis Professional) or Microsoft Power BI Data Analyst',
        'growth_potential': 'Bridges engineering capabilities with executive business strategy'
    },
    'marketing-manager': {
        'title': 'Digital Marketing Manager',
        'domain': 'Marketing',
        'core_skills': ['SEO / SEM', 'Google Analytics', 'Performance Marketing', 'Content Strategy', 'Social Media'],
        'advanced_skills': ['Marketing Automation', 'Growth Hacking', 'Conversion Rate Optimization', 'Brand Marketing'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1400000), 'senior': (1400000, 2500000)},
        'companies': ['Unilever', 'Procter & Gamble', 'Zomato', 'Amazon', 'Flipkart', 'Nykaa'],
        'target_cert': 'HubSpot Inbound Marketing or Google Ads & Analytics Certified',
        'growth_potential': 'Critical role driving direct user acquisition and brand capitalization'
    },
    'sales-representative': {
        'title': 'Sales / Account Executive',
        'domain': 'Sales',
        'core_skills': ['Lead Generation', 'CRM', 'B2B Sales', 'Negotiation', 'Pipeline Management'],
        'advanced_skills': ['Enterprise Deal Closing', 'Solution Selling', 'Account Expansion', 'Cold Outreach'],
        'salary_base': {'entry': (400000, 700000), 'mid': (750000, 1300000), 'senior': (1300000, 2400000)},
        'companies': ['Salesforce', 'Zoho', 'Freshworks', 'Oracle', 'HubSpot', 'Dell'],
        'target_cert': 'Salesforce Certified Administrator or Certified Professional Sales Person (CPSP)',
        'growth_potential': 'High commission incentives and direct revenue contribution'
    },
    'hr-specialist': {
        'title': 'HR Specialist / Talent Partner',
        'domain': 'Human Resources',
        'core_skills': ['Technical Recruitment', 'HRIS Systems', 'Employee Relations', 'Onboarding', 'Labor Compliance'],
        'advanced_skills': ['Talent Analytics', 'Compensation & Benefits', 'Performance Management', 'Employer Branding'],
        'salary_base': {'entry': (400000, 700000), 'mid': (700000, 1200000), 'senior': (1200000, 2200000)},
        'companies': ['Infosys', 'TCS', 'Wipro', 'Accenture', 'HCL', 'Google People Ops'],
        'target_cert': 'SHRM-CP or PHR (Professional in Human Resources)',
        'growth_potential': 'Strategic importance in building top talent pipelines and retention'
    }
}

def generate_role_recommendations(role_id, experience_level, resume_data=None):
    """
    Produces customized, non-static role recommendations dynamically calibrated against
    the candidate's actual resume data (skills, experience years, ATS score, weaknesses).
    """
    role_info = ROLE_TAXONOMY.get(role_id)
    if not role_info:
        role_info = ROLE_TAXONOMY['software-engineer']
        role_id = 'software-engineer'

    exp_level = (experience_level or 'mid').lower()
    if exp_level not in ['entry', 'mid', 'senior']:
        exp_level = 'mid'

    all_role_skills = role_info['core_skills'] + role_info['advanced_skills']
    
    if resume_data:
        # Extract candidate parameters
        career_intel = resume_data.get('career_intelligence', {})
        cand_name = career_intel.get('candidate_name') or 'Candidate'
        current_role = career_intel.get('current_role') or resume_data.get('detected_domain') or 'Specialist'
        company = career_intel.get('company') or ''
        cand_domain = resume_data.get('primary_domain', '')
        years = float(resume_data.get('experience', {}).get('years') or 2.0)
        ats_score = int(resume_data.get('score', 75))
        
        # Build normalized candidate skill set
        raw_skills = resume_data.get('skills', [])
        cand_skills_norm = set()
        for s in raw_skills:
            cand_skills_norm.add(s.lower())
            clean_s = re.sub(r'\(.*?\)', '', s).strip().lower()
            cand_skills_norm.add(clean_s)
            for sub in re.split(r'[/,&]', clean_s):
                if len(sub.strip()) >= 2:
                    cand_skills_norm.add(sub.strip())

        cand_text = (resume_data.get('extracted_text') or '').lower()

        matched_skills = []
        missing_skills = []
        for s in all_role_skills:
            parts = [p.strip().lower() for p in re.split(r'[/,&]', s)]
            is_matched = False
            for p in parts:
                if len(p) < 2:
                    continue
                if p in cand_skills_norm:
                    is_matched = True
                    break
                pattern = r'\b' + re.escape(p) + r'\b'
                if re.search(pattern, cand_text):
                    is_matched = True
                    break
            if is_matched:
                matched_skills.append(s)
            else:
                missing_skills.append(s)

        # Dynamic match percentage computation
        skill_ratio = len(matched_skills) / max(1, len(all_role_skills))
        domain_match = 1.0 if (cand_domain.lower() in role_info['domain'].lower() or role_info['domain'].lower() in cand_domain.lower()) else 0.4
        score_factor = ats_score / 100.0
        
        match_percentage = int((skill_ratio * 55) + (domain_match * 25) + (score_factor * 20))
        match_percentage = min(98, max(38, match_percentage))

        # Dynamic salary calculation tailored to candidate's real profile
        base_min, base_max = role_info['salary_base'][exp_level]
        exp_multiplier = 1.0 + (min(years, 12.0) * 0.04)
        ats_multiplier = 0.95 + (ats_score / 100.0 * 0.15)
        adj_min = int(base_min * exp_multiplier * ats_multiplier / 10000) * 10000
        adj_max = int(base_max * exp_multiplier * ats_multiplier / 10000) * 10000
        salary_str = f"{format_inr(adj_min)} - {format_inr(adj_max)}"

        top_matched = matched_skills[:4]
        top_missing = missing_skills[:4]
        primary_missing = missing_skills[0] if missing_skills else "Advanced Architecture"
        primary_matched = matched_skills[0] if matched_skills else f"{role_info['domain']} Core"

        # Construct candidate-grounded 4-step action plan
        comp_context = f" at {company}" if company else ""
        action_plan = [
            {
                "step": "Priority Skill Bridge",
                "title": f"Master {primary_missing}",
                "description": f"Build a practical demonstration project combining {primary_missing} with your verified {primary_matched} capabilities to eliminate your #1 technical gap for {role_info['title']} roles."
            },
            {
                "step": "Duty Bullet Transformation",
                "title": f"Quantify Achievements as {current_role}",
                "description": f"Rewrite work experience bullets from your tenure{comp_context} using measurable KPIs (%, ₹, latency reductions, or throughput scale) rather than passive responsibility descriptions."
            },
            {
                "step": "Industry Credential",
                "title": f"Attain {role_info['target_cert']}",
                "description": f"Obtain {role_info['target_cert']} to formally demonstrate verified competency and fast-track recruiter screening."
            },
            {
                "step": "Recruiter Positioning",
                "title": f"Strategic Pitch for {role_info['companies'][0]} & {role_info['companies'][1]}",
                "description": f"In interviews and cover notes, highlight your unique foundation in {cand_domain} along with proficiencies in {', '.join(top_matched[:2]) if top_matched else 'core engineering'}."
            }
        ]

        interview_tips = [
            f"Be ready to explain how you apply {primary_matched} to solve real-world problems.",
            f"Prepare a case study describing how you would implement or learn {primary_missing} in a production environment."
        ]

        return {
            "has_resume": True,
            "candidate_name": cand_name,
            "current_role": current_role,
            "company": company,
            "role_id": role_id,
            "role_title": role_info['title'],
            "experience_level": exp_level.title(),
            "match_percentage": match_percentage,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "salary_range": salary_str,
            "salary_boost": f"+{min(35, max(14, len(missing_skills) * 4))}% upon mastering {primary_missing}",
            "companies": role_info['companies'],
            "action_plan": action_plan,
            "interview_tips": interview_tips,
            "target_cert": role_info['target_cert'],
            "growth_potential": role_info.get('growth_potential', 'High growth demand')
        }
    else:
        base_min, base_max = role_info['salary_base'][exp_level]
        salary_str = f"{format_inr(base_min)} - {format_inr(base_max)}"
        return {
            "has_resume": False,
            "role_id": role_id,
            "role_title": role_info['title'],
            "experience_level": exp_level.title(),
            "match_percentage": None,
            "matched_skills": [],
            "missing_skills": role_info['core_skills'],
            "salary_range": salary_str,
            "salary_boost": "+20-30% with advanced certifications",
            "companies": role_info['companies'],
            "action_plan": [
                {
                    "step": "Skill Mastery",
                    "title": f"Build {role_info['core_skills'][0]} Proficiency",
                    "description": f"Develop production-level expertise in {', '.join(role_info['core_skills'][:3])}."
                },
                {
                    "step": "Target Credential",
                    "title": f"Attain {role_info['target_cert']}",
                    "description": f"Validate your expertise with {role_info['target_cert']}."
                }
            ],
            "interview_tips": [
                f"Master core fundamentals of {role_info['core_skills'][0]}.",
                "Upload your resume to get 100% personalized skill match scores and bullet rewrites."
            ],
            "target_cert": role_info['target_cert'],
            "growth_potential": role_info.get('growth_potential', 'High growth demand')
        }

# ============================================================================
# 9. MASTER DYNAMIC ANALYSIS FUNCTION
# ============================================================================
def analyze_resume_comprehensively(text):
    """
    Executes a complete, dynamic assessment of a resume text.
    Returns rich, dynamic JSON payload compatible with frontend requirements.
    """
    # 1. Clean and validate input
    if not text or len(text.strip()) < 20:
        return {
            "error": "The resume text is empty or too short. Please upload a valid resume document."
        }
    
    # 2. Extract Skills & Detect Domain
    skills_list, primary_domain = extract_skills_robust(text)
    
    # 3. Calculate Accurate Experience Timeline
    exp_info = calculate_experience_timeline(text)
    
    # 4. Compute Dynamic ATS Score
    score_info = calculate_ats_score_breakdown(text, skills_list, exp_info)
    
    # 5. Generate Candidate-Specific Strengths & Weaknesses
    strengths, improvements, recommendations = generate_candidate_insights(
        text, skills_list, exp_info, score_info, primary_domain
    )
    
    # 6. Generate Career Intelligence & Market Insights
    career_intel = generate_career_intelligence_data(
        primary_domain, exp_info, score_info, skills_list, text=text
    )
    
    # 7. Generate Dynamic Radar Chart Data
    radar_data = generate_radar_chart_data(skills_list, primary_domain, score_info)
    
    # Calculate match percentage
    match_pct = max(65, min(96, score_info["score"] + 2))
    
    # Determine demand and growth potential
    if score_info["score"] >= 80:
        demand_level = "Very High"
        growth_pot = "Exceptional"
    elif score_info["score"] >= 65:
        demand_level = "High"
        growth_pot = "Strong"
    else:
        demand_level = "Moderate"
        growth_pot = "Good"

    # Assemble complete payload
    domain_display = f"{primary_domain} Engineering" if primary_domain in ["Mechanical", "Software", "Civil", "Electrical"] else primary_domain

    result = {
        "score": score_info["score"],
        "primary_domain": primary_domain,
        "detected_domain": domain_display,
        "score_breakdown": score_info["breakdown"],
        "skills": [s["name"] for s in skills_list],
        "detailed_skills": skills_list,
        "strengths": strengths,
        "improvements": improvements,
        "recommendations": recommendations,
        "experience": {
            "years": exp_info["final_years"],
            "level": exp_info["display_text"],
            "seniority": exp_info["seniority"]
        },
        "career_match": {
            "roles": career_intel["roles"],
            "industries": career_intel["industries"],
            "match_percentage": match_pct
        },
        "market_value": {
            "salary_range": career_intel["salary_range"],
            "demand_level": demand_level,
            "growth_potential": growth_pot
        },
        "career_intelligence": career_intel,
        "radar_chart": radar_data,
        "radar_competencies": {
            "domain": primary_domain,
            "labels": radar_data["labels"],
            "values": radar_data["values"]
        },
        "stats": score_info["stats"]
    }

    # Map primary domain to default role id and experience level
    domain_to_role = {
        "Software": "software-engineer",
        "Mechanical": "mechanical-engineer",
        "Data/AI": "data-scientist",
        "Cloud/DevOps": "devops-engineer",
        "DevOps": "devops-engineer",
        "Cloud": "devops-engineer",
        "Design": "ui-ux-designer",
        "Management": "product-manager"
    }
    default_role_id = domain_to_role.get(primary_domain, "software-engineer" if primary_domain == "Software" else "mechanical-engineer" if primary_domain == "Mechanical" else "project-manager")
    default_exp_level = "entry" if exp_info["final_years"] < 2.5 else "mid" if exp_info["final_years"] < 6.0 else "senior"

    # Pre-generate candidate-grounded role recommendations
    role_recs = generate_role_recommendations(default_role_id, default_exp_level, resume_data=result)
    result["target_role_id"] = default_role_id
    result["target_experience_level"] = default_exp_level
    result["role_recommendations"] = role_recs

    return result
