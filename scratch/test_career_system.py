import re
import json

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
        "name": name or "Candidate Profile",
        "role": role or "Engineering Specialist",
        "company": company or ""
    }

def generate_dynamic_career_intelligence(text, domain, exp_info, score_info, skills):
    """
    Generates a personalized, dynamic, non-repetitive career intelligence package.
    """
    years = float(exp_info.get("final_years", 1.0))
    score = int(score_info.get("score", 75))
    seniority = exp_info.get("seniority", "Professional")
    skill_names = [s["name"] for s in skills]
    skill_names_lower = {s.lower() for s in skill_names}
    
    profile = extract_candidate_profile(text)
    candidate_name = profile["name"]
    current_role = profile["role"]
    company = profile["company"]
    company_suffix = f" at {company}" if company else ""

    # Detect sub-specialty from actual skills
    sub_specialties = []
    if any(k in skill_names_lower for k in ['react', 'vue.js', 'angular', 'next.js', 'html5', 'css3 / modern css']):
        sub_specialties.append("Modern Frontend & Web UI")
    if any(k in skill_names_lower for k in ['node.js', 'express.js', 'django', 'spring boot', 'python', 'java', 'php', 'c#', 'c++']):
        sub_specialties.append("Backend APIs & Microservices")
    if any(k in skill_names_lower for k in ['aws', 'docker', 'kubernetes', 'ci/cd automation', 'git / version control']):
        sub_specialties.append("Cloud Infrastructure & DevOps")
    if any(k in skill_names_lower for k in ['solidworks', 'autocad', 'catia', 'fusion 360', 'inventor', 'product design']):
        sub_specialties.append("3D CAD & Product Design")
    if any(k in skill_names_lower for k in ['ansys', 'fea / stress analysis', 'cfd / fluid dynamics', 'thermal analysis']):
        sub_specialties.append("FEA & Multiphysics Simulation")
    if any(k in skill_names_lower for k in ['cnc machining & milling', '3d printing / additive mfg', 'injection molding', 'dfm / dfa']):
        sub_specialties.append("Precision Tooling & Manufacturing")
    if any(k in skill_names_lower for k in ['machine learning', 'deep learning', 'pytorch', 'tensorflow', 'pandas', 'nlp']):
        sub_specialties.append("AI / Machine Learning Systems")
    
    primary_focus = sub_specialties[0] if sub_specialties else f"{domain} Engineering"
    top_tool = skill_names[0] if skill_names else "Core Engineering"
    second_tool = skill_names[1] if len(skill_names) > 1 else "Modern Tooling"
    third_tool = skill_names[2] if len(skill_names) > 2 else "System Architecture"

    # Compensation calculation with realistic market brackets
    if domain == "Software":
        base_salary = int(72000 + (years * 12500) + (score * 220))
        next_salary = int(base_salary * 1.22)
    elif domain == "Mechanical":
        base_salary = int(66000 + (years * 10500) + (score * 190))
        next_salary = int(base_salary * 1.20)
    elif domain == "Data/AI":
        base_salary = int(78000 + (years * 13500) + (score * 240))
        next_salary = int(base_salary * 1.25)
    else:
        base_salary = int(60000 + (years * 9000) + (score * 170))
        next_salary = int(base_salary * 1.18)

    salary_display = f"${base_salary - 8000:,} - ${base_salary + 12000:,}"
    next_salary_display = f"${next_salary - 6000:,} - ${next_salary + 15000:,}"

    # Market competitiveness calculation
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

    # 3-Phase Progression ROADMAP (Customized to Candidate Name, Current Role, Domain & Experience)
    if years < 2.5:
        career_roadmap = [
            {
                "phase": "Phase 1: Immediate Milestone",
                "timeline": "Next 6 - 12 Months",
                "target_role": f"Mid-Level {domain} Engineer",
                "focus": f"Transition from entry-level execution to autonomous delivery in {top_tool}. Eliminate code/design revision cycles and deliver features end-to-end.",
                "target_compensation": f"${int(base_salary * 1.15):,} - ${int(base_salary * 1.25):,}",
                "unlock_skill": f"Production proficiency in {second_tool}"
            },
            {
                "phase": "Phase 2: Senior Elevation",
                "timeline": "Year 2 - 3",
                "target_role": f"Senior {primary_focus} Specialist",
                "focus": f"Lead technical design pods, establish coding/engineering standards, and mentor incoming junior engineers across {top_tool} and {second_tool} workflows.",
                "target_compensation": f"${int(base_salary * 1.35):,} - ${int(base_salary * 1.50):,}",
                "unlock_skill": f"System architecture & CI/CD deployment"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"Lead {domain} Architect / Engineering Lead",
                "focus": f"Own critical cross-functional initiatives, author engineering RFCs, and direct technology evaluations that drive departmental business outcomes.",
                "target_compensation": f"${int(base_salary * 1.60):,} - ${int(base_salary * 1.85):,}",
                "unlock_skill": f"Cross-system scaling and leadership governance"
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
                "focus": f"Spearhead system-wide architectural transformation, resolve cross-service bottlenecks, and standardize engineering quality across multiple teams.",
                "target_compensation": f"${int(base_salary * 1.30):,} - ${int(base_salary * 1.45):,}",
                "unlock_skill": f"Multi-system distributed design & performance tuning"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"Director of {domain} Engineering / Head of Technology",
                "focus": f"Executive technical governance, talent scaling, engineering budget allocation, and alignment of technical capabilities with enterprise business strategy.",
                "target_compensation": f"${int(base_salary * 1.55):,} - ${int(base_salary * 1.85):,}+",
                "unlock_skill": f"Strategic technology roadmapping & executive management"
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
                "unlock_skill": f"Enterprise platform architecture & strategic governance"
            },
            {
                "phase": "Phase 2: Senior Elevation",
                "timeline": "Year 2 - 3",
                "target_role": f"Director of {domain} Engineering",
                "focus": f"Direct multiple engineering teams, establish engineering excellence KPIs, optimize infrastructure CAPEX/OPEX, and recruit top engineering talent.",
                "target_compensation": f"${int(base_salary * 1.25):,} - ${int(base_salary * 1.45):,}",
                "unlock_skill": f"Multi-team organizational leadership & budget ownership"
            },
            {
                "phase": "Phase 3: Technical Leadership",
                "timeline": "Year 3 - 5",
                "target_role": f"VP of Engineering / Chief Technology Officer (CTO)",
                "focus": f"Executive C-level technology vision, global infrastructure resilience, digital transformation, and investor/board-level technology alignment.",
                "target_compensation": f"${int(base_salary * 1.50):,} - ${int(base_salary * 1.90):,}+",
                "unlock_skill": f"Executive enterprise leadership & board-level strategy"
            }
        ]

    # Dynamic Tailored Skill Bridges (Contextual to Candidate's ACTUAL Stack)
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
                "rationale": f"Essential for backend microservices to minimize database roundtrips and handle high concurrent user traffic."
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
                "rationale": f"Designing fault-tolerant distributed consensus algorithms and event-streaming pipelines (Kafka) for 500K+ RPS scale."
            })
            tailored_gaps.append({
                "skill": "Generative AI Agent Integration",
                "impact": "+22% Salary Premium",
                "rationale": f"Integrating vector embeddings, RAG architectures, and autonomous AI agents directly into production application backends."
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
                "rationale": f"Mandatory for production release and supplier precision inspection, bridging 3D CAD models with physical factory quality control."
            })
        if not any(k in skill_names_lower for k in ['ansys', 'fea / stress analysis', 'cfd / fluid dynamics']):
            tailored_gaps.append({
                "skill": "Multiphysics FEA / CFD Simulation",
                "impact": "+18% Salary Premium",
                "rationale": f"Elevates purely geometric CAD modeling into computational stress, thermal, and fatigue life prediction."
            })
        if not tailored_gaps:
            tailored_gaps.append({
                "skill": "Additive Manufacturing for Production (DMLS)",
                "impact": "+15% Salary Premium",
                "rationale": f"Designing topology-optimized metallic components for flight-ready aerospace and high-performance automotive platforms."
            })
            tailored_gaps.append({
                "skill": "Digital Twin & Real-Time Sensor Telemetry",
                "impact": "+18% Salary Premium",
                "rationale": f"Connecting physical hardware sensor telemetry with real-time computational mechanical models."
            })
    else:
        tailored_gaps.append({
            "skill": "Advanced Data Analytics & KPI Dashboards",
            "impact": "+14% Salary Premium",
            "rationale": f"Transforms operational domain knowledge into executive-level visibility and quantified process optimization."
        })
        tailored_gaps.append({
            "skill": "Agile / Scrum Delivery Leadership",
            "impact": "+12% Salary Premium",
            "rationale": f"Demonstrates structured cross-functional dependency management and sprint predictability."
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
            {"name": "FinTech & Real-Time Digital Banking", "match": "91%", "reason": f"Requires high-throughput backend systems and modern frontend dashboards."},
            {"name": "HealthTech & Telemedicine Platforms", "match": "87%", "reason": f"Growing demand for secure web platforms and distributed APIs."}
        ]
    elif domain == "Mechanical":
        industry_matches = [
            {"name": "Automotive & Electric Vehicles (EV)", "match": "96%", "reason": f"Surging demand for CAD/FEA engineers in lightweighting and battery packaging."},
            {"name": "Aerospace & Defense Systems", "match": "92%", "reason": f"Strict adherence to {skill_names[0] if skill_names else 'CAD'} standards, stress analysis, and GD&T."},
            {"name": "Robotics & Industrial Automation", "match": "88%", "reason": f"High volume of design roles for precision end-effectors and automated tooling."}
        ]
    else:
        industry_matches = [
            {"name": "Enterprise Technology Consulting", "match": "90%", "reason": "Demand for structured problem solving and technical implementation."},
            {"name": "Operations & Logistics Infrastructure", "match": "86%", "reason": "Focus on system efficiency, cost reduction, and process automation."}
        ]

    return {
        "candidate_name": candidate_name,
        "current_role": current_role,
        "company": company,
        "domain": domain,
        "primary_focus": primary_focus,
        "seniority": seniority,
        "years": years,
        "percentile": percentile,
        "market_standing": market_standing,
        "salary_range": salary_display,
        "next_level_salary": next_salary_display,
        "career_roadmap": career_roadmap,
        "tailored_gaps": tailored_gaps[:2],
        "comp_premiums": comp_premiums,
        "industry_matches": industry_matches,
        # Keep backward compatibility keys so old UI or other endpoints don't crash
        "experience_level": f"{seniority} ({years:.1f} yrs)",
        "salary_insights": [
            f"Current Market Value: {salary_display} based on {years:.1f} yrs tenure in {primary_focus}",
            f"Next Promotion Target: {next_salary_display} as {career_roadmap[0]['target_role']}",
            f"Top Comp Multiplier: {comp_premiums[0]['skill']} ({comp_premiums[0]['premium']})"
        ],
        "skill_gaps": [f"{g['skill']}: {g['rationale']}" for g in tailored_gaps[:2]],
        "industry_trends": [f"{ind['name']} ({ind['match']} Match): {ind['reason']}" for ind in industry_matches],
        "career_path": [f"{step['phase']} ({step['timeline']}): {step['target_role']} — {step['focus']}" for step in career_roadmap]
    }

with open('backend/software_engineer_resume.txt', 'r', encoding='utf-8') as f:
    sw = f.read()

with open('backend/mechanical_engineer_resume.txt', 'r', encoding='utf-8') as f:
    me = f.read()

import sys
sys.path.append('backend')
from resume_engine import extract_skills_robust, calculate_experience_timeline, calculate_ats_score_breakdown

sw_skills, sw_domain = extract_skills_robust(sw)
sw_exp = calculate_experience_timeline(sw)
sw_score = calculate_ats_score_breakdown(sw, sw_skills, sw_exp)

me_skills, me_domain = extract_skills_robust(me)
me_exp = calculate_experience_timeline(me)
me_score = calculate_ats_score_breakdown(me, me_skills, me_exp)

res_sw = generate_dynamic_career_intelligence(sw, sw_domain, sw_exp, sw_score, sw_skills)
res_me = generate_dynamic_career_intelligence(me, me_domain, me_exp, me_score, me_skills)

print("=== SW DYNAMIC CAREER INTEL ===")
print(json.dumps(res_sw, indent=2))

print("\n=== ME DYNAMIC CAREER INTEL ===")
print(json.dumps(res_me, indent=2))
