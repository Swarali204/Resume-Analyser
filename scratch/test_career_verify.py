import sys
sys.path.append('backend')
from resume_engine import analyze_resume_comprehensively

with open('backend/software_engineer_resume.txt', 'r', encoding='utf-8') as f:
    sw = f.read()

with open('backend/mechanical_engineer_resume.txt', 'r', encoding='utf-8') as f:
    me = f.read()

r_sw = analyze_resume_comprehensively(sw)
r_me = analyze_resume_comprehensively(me)

print('=== SW CANDIDATE NAME & ROLE ===')
print('Name:', r_sw['career_intelligence'].get('candidate_name'))
print('Role:', r_sw['career_intelligence'].get('current_role'))
print('Company:', r_sw['career_intelligence'].get('company'))
print('Primary Focus:', r_sw['career_intelligence'].get('primary_focus'))
print('Salary Range:', r_sw['career_intelligence'].get('salary_range'))
print('Roadmap Step 1:', r_sw['career_intelligence'].get('career_roadmap', [{}])[0].get('target_role'))

print('\n=== ME CANDIDATE NAME & ROLE ===')
print('Name:', r_me['career_intelligence'].get('candidate_name'))
print('Role:', r_me['career_intelligence'].get('current_role'))
print('Company:', r_me['career_intelligence'].get('company'))
print('Primary Focus:', r_me['career_intelligence'].get('primary_focus'))
print('Salary Range:', r_me['career_intelligence'].get('salary_range'))
print('Roadmap Step 1:', r_me['career_intelligence'].get('career_roadmap', [{}])[0].get('target_role'))
