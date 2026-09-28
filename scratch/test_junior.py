import requests

junior_text = """ALEX SMITH
Junior Frontend Developer
alex.smith@email.com | (555) 321-7654

PROFESSIONAL SUMMARY
Motivated Junior Frontend Developer with 1+ years experience building web applications with React, JavaScript, and modern CSS.

TECHNICAL SKILLS
Frontend: React, JavaScript, HTML5, CSS3, Tailwind CSS
Tools: Git, GitHub, VS Code

EXPERIENCE
Junior Frontend Developer | WebStudio Agency | 2023 - Present
• Built responsive UI components with React and Tailwind CSS
• Fixed frontend bugs and optimized page loading times
• Collaborated in weekly agile sprints
"""

r_jr = requests.post('http://127.0.0.1:5000/analyze', json={'resume_text': junior_text}).json()
ci = r_jr['career_intelligence']
print('JR Name:', ci['candidate_name'])
print('JR Role:', ci['current_role'])
print('JR Company:', ci['company'])
print('JR Standing:', ci['percentile'], '|', ci['market_standing'])
print('JR Salary:', ci['salary_range'], '-> Next:', ci['next_level_salary'])
print('JR Roadmap Step 1:', ci['career_roadmap'][0]['target_role'], '| Comp:', ci['career_roadmap'][0]['target_compensation'])
print('JR Unlock Skill:', ci['career_roadmap'][0]['unlock_skill'])
print('JR Gaps:', [g['skill'] for g in ci['tailored_gaps']])
