import re

def test_dynamic_recommendations(text, skills, exp_info, score_info, domain):
    recommendations = []
    skill_names = [s["name"] for s in skills]
    skill_names_lower = {s.lower() for s in skill_names}
    text_lower = text.lower()
    
    top_domain_skills = [s["name"] for s in skills[:3]]
    years = float(exp_info.get("final_years", 2.0))
    cand_role = "Senior Software Engineer" if domain == "Software" else "Mechanical Design Engineer"
    cand_company = "TechCorp Inc." if domain == "Software" else "AutoTech Manufacturing"

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
                rewrite_ex = "Designed automated tooling fixtures in SolidWorks/AutoCAD, cutting cycle time by 20% and saving $45,000 in manufacturing scrap annually"
            elif any(k in sample_low for k in ['thermal', 'battery', 'cooling', 'fluid', 'heat', 'flow']):
                rewrite_ex = "Conducted CFD/thermal simulations on cooling enclosures, lowering peak operating temperatures by 8°C"
            else:
                rewrite_ex = "Engineered production CAD models in SolidWorks with GD&T datum tolerance callouts, cutting vendor tooling turnaround by 3 weeks"
            recommendations.append(f"Action Bullet Transformation: For your bullet \"{clean_sample}\", replace passive duty phrasing with Google's XYZ metric formula (\"Accomplished [X], as measured by [Y], by doing [Z]\"). Example: \"{rewrite_ex}\".")

    # 2. Context-Aware Technical Gap
    if domain == "Software":
        if not any(k in skill_names_lower for k in ['jest', 'cypress', 'testing', 'unit test', 'pytest', 'junit']):
            recommendations.append("Automated Test Coverage & TDD: While your full-stack proficiencies are strong, your resume lacks automated testing frameworks (Jest, Cypress, or PyTest). Adding bullet points with code coverage metrics (e.g. 'implemented Jest test suites achieving 85%+ code coverage') signals production-grade engineering rigor.")
        elif not any(k in skill_names_lower for k in ['typescript', 'ts']):
            recommendations.append("TypeScript Strict Typing: Adopting TypeScript over standard JavaScript eliminates runtime exceptions and is required by 85%+ of Tier-1 software engineering teams.")
        else:
            recommendations.append("Architectural Trade-Off Documentation: Highlight system design decisions (e.g., event streaming, microservices decoupling) to qualify for Senior/Staff roles.")

    elif domain == "Mechanical":
        if not any(k in skill_names_lower for k in ['dfm', 'dfa', 'dfm / dfa']):
            recommendations.append("DFM / DFA Tooling Optimization: Highlight specific Design for Manufacturing (DFM) and Design for Assembly (DFA) optimizations for machined or molded components to quantify tooling and scrap savings.")
        elif not any(k in skill_names_lower for k in ['plm', 'pdm', 'windchill', 'teamcenter']):
            recommendations.append("Enterprise PLM Workflow Integration: Explicitly cite experience with enterprise PDM/PLM systems (e.g., PTC Windchill or Siemens Teamcenter) to prove turnkey production handoff to vendor machine shops.")
        else:
            recommendations.append("Advanced Additive & Lightweighting: Showcase topology optimization and additive manufacturing (DMLS/SLS) for high-performance structural components.")

    # 3. Dual-Channel ATS Keyword Placement
    if top_domain_skills:
        recommendations.append(f"Dual-Channel ATS Keyword Optimization: Ensure your top proficiencies ({', '.join(top_domain_skills)}) appear both in your Technical Skills section and directly within accomplishment bullets with quantified business outcomes, boosting recruiter keyword relevance.")

    # 4. Next-Tier Career Elevation Milestone
    comp_ref = f" at {cand_company}" if cand_company else ""
    if years < 2.5:
        recommendations.append(f"Autonomous Proof-of-Work: As an emerging {cand_role}, feature 2-3 comprehensive end-to-end projects with demonstrable links/repositories to prove autonomous delivery and minimize onboarding oversight.")
    elif years < 6.0:
        recommendations.append(f"Senior Elevation Milestone: Leverage your {years:.1f} years as {cand_role}{comp_ref} to demonstrate end-to-end subsystem ownership, architectural decision-making, and mentorship of junior engineers.")
    else:
        recommendations.append(f"Staff & Leadership Trajectory: As a senior professional with {years:.1f} years experience, pivot bullet focus from implementation tasks to organizational velocity: authoring RFCs, reducing cross-service bottlenecks, and delivering business ROI.")

    # 5. Professional Verification & Portfolio Links
    has_github = bool(re.search(r'github\.com', text_lower))
    has_portfolio = bool(re.search(r'portfolio|behance|dribbble', text_lower))
    if domain == "Software" and not has_github:
        recommendations.append("Technical Proof-of-Work: Adding a clickable GitHub profile link showcasing your repositories and clean commit history provides tangible code proof to technical hiring managers.")
    elif domain == "Mechanical" and not has_portfolio:
        recommendations.append("Hardware Portfolio Visibility: Provide a link to a digital portfolio showcasing 3D CAD renders, exploded assembly schematics, and FEA stress contour plots for your key design projects.")

    return recommendations

import sys
sys.path.append('backend')
from resume_engine import analyze_resume_comprehensively
with open('backend/software_engineer_resume.txt') as f: sw = f.read()
with open('backend/mechanical_engineer_resume.txt') as f: me = f.read()

r_sw = analyze_resume_comprehensively(sw)
r_me = analyze_resume_comprehensively(me)

# Test real sample duty bullets:
sample_sw = {'bullets_unquantified_samples': ['Built RESTful APIs and frontend applications using React and Node.js']}
sample_me = {'bullets_unquantified_samples': ['Designed automotive components using SolidWorks and conducted FEA analysis']}

print("=== SW DYNAMIC RECOMMENDATIONS ===")
for r in test_dynamic_recommendations(sw, r_sw['detailed_skills'], r_sw['experience'], sample_sw, 'Software'):
    print(" •", r)

print("\n=== ME DYNAMIC RECOMMENDATIONS ===")
for r in test_dynamic_recommendations(me, r_me['detailed_skills'], r_me['experience'], sample_me, 'Mechanical'):
    print(" •", r)
