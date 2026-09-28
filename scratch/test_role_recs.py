import re

ROLE_TAXONOMY = {
    'mechanical-engineer': {
        'title': 'Mechanical Engineer',
        'domain': 'Mechanical',
        'core_skills': ['SolidWorks', 'AutoCAD', 'ANSYS', 'CATIA', 'GD&T', 'Manufacturing Processes'],
        'advanced_skills': ['DFM / DFA', 'FEA', 'CFD', 'PDM / PLM', 'Six Sigma', 'Thermodynamics'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1500000), 'senior': (1500000, 2800000)},
        'companies': ['Tesla', 'Boeing', 'Tata Motors', 'Mahindra', 'L&T', 'General Electric', 'Bosch', 'Apple Hardware'],
        'target_cert': 'CSWP (Certified SOLIDWORKS Professional) or Six Sigma Green Belt'
    },
    'software-engineer': {
        'title': 'Software Engineer',
        'domain': 'Software',
        'core_skills': ['JavaScript', 'TypeScript', 'React', 'Node.js', 'Python', 'SQL', 'Git', 'REST APIs'],
        'advanced_skills': ['AWS', 'Docker', 'Kubernetes', 'Microservices', 'System Design', 'Redis', 'CI/CD', 'GraphQL'],
        'salary_base': {'entry': (550000, 900000), 'mid': (900000, 1800000), 'senior': (1800000, 3500000)},
        'companies': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Netflix', 'Uber', 'Atlassian', 'Stripe'],
        'target_cert': 'AWS Certified Solutions Architect or CKA (Kubernetes)'
    },
    'data-scientist': {
        'title': 'Data Scientist',
        'domain': 'Data/AI',
        'core_skills': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-Learn', 'Statistics'],
        'advanced_skills': ['Deep Learning', 'PyTorch', 'TensorFlow', 'NLP', 'MLOps', 'FastAPI', 'Docker'],
        'salary_base': {'entry': (600000, 950000), 'mid': (1000000, 1900000), 'senior': (1900000, 3600000)},
        'companies': ['OpenAI', 'Google DeepMind', 'Amazon', 'Netflix', 'Uber', 'Spotify', 'Fractal Analytics'],
        'target_cert': 'Databricks Certified Machine Learning Associate or AWS ML Specialty'
    },
    'product-manager': {
        'title': 'Product Manager',
        'domain': 'Management',
        'core_skills': ['Product Strategy', 'User Research', 'Agile / Scrum', 'Roadmapping', 'Data Analysis', 'Wireframing'],
        'advanced_skills': ['A/B Testing', 'SQL', 'Market Sizing', 'Stakeholder Management', 'Go-To-Market'],
        'salary_base': {'entry': (600000, 1000000), 'mid': (1100000, 2000000), 'senior': (2000000, 3800000)},
        'companies': ['Google', 'Apple', 'Microsoft', 'Swiggy', 'Zomato', 'CRED', 'Amazon', 'Uber'],
        'target_cert': 'Certified Scrum Product Owner (CSPO) or Pragmatic Institute Certified'
    },
    'devops-engineer': {
        'title': 'DevOps & Cloud Engineer',
        'domain': 'Cloud/DevOps',
        'core_skills': ['Linux', 'AWS', 'Docker', 'Kubernetes', 'CI/CD Pipelines', 'Git', 'Python'],
        'advanced_skills': ['Terraform', 'Ansible', 'Prometheus', 'Grafana', 'Security / DevSecOps', 'Helm'],
        'salary_base': {'entry': (550000, 900000), 'mid': (1000000, 1800000), 'senior': (1800000, 3400000)},
        'companies': ['AWS', 'Google Cloud', 'Microsoft', 'Red Hat', 'HashiCorp', 'Datadog', 'CrowdStrike'],
        'target_cert': 'CKA (Certified Kubernetes Administrator) or AWS DevOps Engineer Professional'
    },
    'ui-ux-designer': {
        'title': 'UI/UX Designer',
        'domain': 'Design',
        'core_skills': ['Figma', 'Wireframing', 'Prototyping', 'User Research', 'Design Systems', 'Information Architecture'],
        'advanced_skills': ['Interaction Design', 'Usability Testing', 'HTML/CSS Basics', 'Design Tokens', 'Micro-interactions'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1400000), 'senior': (1400000, 2600000)},
        'companies': ['Adobe', 'Canva', 'Airbnb', 'Figma', 'Spotify', 'Razorpay', 'CRED'],
        'target_cert': 'Google UX Design Professional Certificate or Nielsen Norman Group UX Certified'
    },
    'project-manager': {
        'title': 'Project / Delivery Manager',
        'domain': 'Management',
        'core_skills': ['Agile', 'Scrum', 'Risk Management', 'Sprint Planning', 'Stakeholder Communication', 'Jira'],
        'advanced_skills': ['PMP', 'CSM Certification', 'Resource Allocation', 'Vendor Management', 'Cross-Team Governance'],
        'salary_base': {'entry': (550000, 850000), 'mid': (900000, 1600000), 'senior': (1600000, 3000000)},
        'companies': ['TCS', 'Infosys', 'Accenture', 'Deloitte', 'Cognizant', 'Capgemini', 'IBM'],
        'target_cert': 'PMP (Project Management Professional) or PMI-ACP'
    },
    'business-analyst': {
        'title': 'Business Analyst',
        'domain': 'Analytics',
        'core_skills': ['SQL', 'Excel', 'Power BI / Tableau', 'Requirements Gathering', 'Process Flowcharting'],
        'advanced_skills': ['Python Analytics', 'Financial Forecasting', 'Gap Analysis', 'Agile User Stories'],
        'salary_base': {'entry': (500000, 800000), 'mid': (850000, 1500000), 'senior': (1500000, 2600000)},
        'companies': ['Deloitte', 'EY', 'KPMG', 'PwC', 'McKinsey', 'ZS Associates'],
        'target_cert': 'CBAP (Certified Business Analysis Professional) or Microsoft Power BI Data Analyst'
    },
    'marketing-manager': {
        'title': 'Digital Marketing Manager',
        'domain': 'Marketing',
        'core_skills': ['SEO / SEM', 'Google Analytics', 'Performance Marketing', 'Content Strategy', 'Social Media'],
        'advanced_skills': ['Marketing Automation', 'Growth Hacking', 'Conversion Rate Optimization', 'Brand Marketing'],
        'salary_base': {'entry': (450000, 750000), 'mid': (800000, 1400000), 'senior': (1400000, 2500000)},
        'companies': ['Unilever', 'Procter & Gamble', 'Zomato', 'Amazon', 'Flipkart', 'Nykaa'],
        'target_cert': 'HubSpot Inbound Marketing or Google Ads & Analytics Certified'
    },
    'sales-representative': {
        'title': 'Sales / Account Executive',
        'domain': 'Sales',
        'core_skills': ['Lead Generation', 'CRM', 'B2B Sales', 'Negotiation', 'Pipeline Management'],
        'advanced_skills': ['Enterprise Deal Closing', 'Solution Selling', 'Account Expansion', 'Cold Outreach'],
        'salary_base': {'entry': (400000, 700000), 'mid': (750000, 1300000), 'senior': (1300000, 2400000)},
        'companies': ['Salesforce', 'Zoho', 'Freshworks', 'Oracle', 'HubSpot', 'Dell'],
        'target_cert': 'Salesforce Certified Administrator or Certified Professional Sales Person (CPSP)'
    },
    'hr-specialist': {
        'title': 'HR Specialist / Talent Partner',
        'domain': 'Human Resources',
        'core_skills': ['Technical Recruitment', 'HRIS Systems', 'Employee Relations', 'Onboarding', 'Labor Compliance'],
        'advanced_skills': ['Talent Analytics', 'Compensation & Benefits', 'Performance Management', 'Employer Branding'],
        'salary_base': {'entry': (400000, 700000), 'mid': (700000, 1200000), 'senior': (1200000, 2200000)},
        'companies': ['Infosys', 'TCS', 'Wipro', 'Accenture', 'HCL', 'Google People Ops'],
        'target_cert': 'SHRM-CP or PHR (Professional in Human Resources)'
    }
}

def generate_role_recommendations(role_id, experience_level, resume_data=None):
    role_info = ROLE_TAXONOMY.get(role_id)
    if not role_info:
        role_info = ROLE_TAXONOMY['software-engineer']
        role_id = 'software-engineer'

    exp_level = (experience_level or 'mid').lower()
    if exp_level not in ['entry', 'mid', 'senior']:
        exp_level = 'mid'

    all_role_skills = role_info['core_skills'] + role_info['advanced_skills']
    
    if resume_data:
        cand_name = resume_data.get('career_intelligence', {}).get('candidate_name') or 'Candidate'
        current_role = resume_data.get('career_intelligence', {}).get('current_role') or 'Specialist'
        company = resume_data.get('career_intelligence', {}).get('company') or ''
        cand_domain = resume_data.get('primary_domain', '')
        years = float(resume_data.get('experience', {}).get('years') or 2.0)
        ats_score = int(resume_data.get('score', 75))
        cand_skills = [s.lower() for s in resume_data.get('skills', [])]
        cand_text = resume_data.get('extracted_text', '').lower()

        matched_skills = []
        missing_skills = []
        for s in all_role_skills:
            parts = [p.strip().lower() for p in re.split(r'[/,&]', s)]
            if any(p in cand_skills or p in cand_text for p in parts if len(p) >= 2):
                matched_skills.append(s)
            else:
                missing_skills.append(s)

        # Dynamic match score
        skill_ratio = len(matched_skills) / max(1, len(all_role_skills))
        domain_match = 1.0 if cand_domain.lower() in role_info['domain'].lower() or role_info['domain'].lower() in cand_domain.lower() else 0.4
        score_factor = ats_score / 100.0
        
        match_percentage = int((skill_ratio * 55) + (domain_match * 25) + (score_factor * 20))
        match_percentage = min(98, max(38, match_percentage))

        # Dynamic salary calculation tailored to candidate's real profile
        base_min, base_max = role_info['salary_base'][exp_level]
        # Multiplier from years and ATS score
        exp_multiplier = 1.0 + (min(years, 12.0) * 0.04)
        ats_multiplier = 0.95 + (ats_score / 100.0 * 0.15)
        adj_min = int(base_min * exp_multiplier * ats_multiplier / 10000) * 10000
        adj_max = int(base_max * exp_multiplier * ats_multiplier / 10000) * 10000
        salary_str = f"₹{adj_min:,} - ₹{adj_max:,}"

        top_matched = matched_skills[:3]
        top_missing = missing_skills[:3]
        primary_missing = missing_skills[0] if missing_skills else "Advanced Architecture"
        primary_matched = matched_skills[0] if matched_skills else f"{role_info['domain']} Fundamentals"

        action_plan = [
            {
                "step": "Priority Skill Bridge",
                "title": f"Master {primary_missing}",
                "description": f"Build a project demonstrating {primary_missing} alongside your proven {primary_matched} capabilities to close the top technical gap for this role."
            },
            {
                "step": "Duty Bullet Transformation",
                "title": f"Quantify {current_role} Achievements",
                "description": f"Rewrite work history bullets with tangible metrics (%, $, latency, or time saved) demonstrating impact at {company or 'your current organization'}."
            },
            {
                "step": "Industry Credential",
                "title": f"Target {role_info['target_cert']}",
                "description": f"Attain {role_info['target_cert']} to validate formal competency and fast-track recruiter screening."
            },
            {
                "step": "Recruiter Positioning",
                "title": f"Strategic Pitch for {role_info['companies'][0]} & {role_info['companies'][1]}",
                "description": f"Highlight your {cand_domain} background and proficiencies in {', '.join(top_matched[:2]) if top_matched else 'core skills'} to stand out in interviews."
            }
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
            "target_cert": role_info['target_cert']
        }
    else:
        # Fallback benchmark
        base_min, base_max = role_info['salary_base'][exp_level]
        salary_str = f"₹{base_min:,} - ₹{base_max:,}"
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
            "target_cert": role_info['target_cert']
        }

# Test with sw and me
import sys
sys.path.append('backend')
from resume_engine import analyze_resume_comprehensively
with open('backend/software_engineer_resume.txt') as f: sw = f.read()
with open('backend/mechanical_engineer_resume.txt') as f: me = f.read()
r_sw = analyze_resume_comprehensively(sw)
r_me = analyze_resume_comprehensively(me)

print("--- SW Resume on Software Engineer Role ---")
sw_on_swe = generate_role_recommendations('software-engineer', 'mid', r_sw)
print(f"Candidate: {sw_on_swe['candidate_name']} ({sw_on_swe['current_role']})")
print(f"Match: {sw_on_swe['match_percentage']}%")
print(f"Matched Skills: {sw_on_swe['matched_skills']}")
print(f"Missing Skills: {sw_on_swe['missing_skills']}")
print(f"Salary: {sw_on_swe['salary_range']}")
print("Action Plan Step 1:", sw_on_swe['action_plan'][0])

print("\n--- ME Resume on Mechanical Engineer Role ---")
me_on_mech = generate_role_recommendations('mechanical-engineer', 'mid', r_me)
print(f"Candidate: {me_on_mech['candidate_name']} ({me_on_mech['current_role']})")
print(f"Match: {me_on_mech['match_percentage']}%")
print(f"Matched Skills: {me_on_mech['matched_skills']}")
print(f"Missing Skills: {me_on_mech['missing_skills']}")
print(f"Salary: {me_on_mech['salary_range']}")
print("Action Plan Step 1:", me_on_mech['action_plan'][0])

print("\n--- Cross Test: ME Resume on Software Engineer Role ---")
me_on_swe = generate_role_recommendations('software-engineer', 'entry', r_me)
print(f"Candidate: {me_on_swe['candidate_name']} ({me_on_swe['current_role']})")
print(f"Match: {me_on_swe['match_percentage']}%")
print(f"Matched Skills: {me_on_swe['matched_skills']}")
print(f"Missing Skills: {me_on_swe['missing_skills']}")
print(f"Salary: {me_on_swe['salary_range']}")
