import openai
import json
import os
from typing import Dict, Any

# ============================================================================
# SETUP INSTRUCTIONS:
# 1. Install required packages: pip install openai
# 2. Get OpenAI API key from: https://platform.openai.com/api-keys
# 3. Replace "your-api-key-here" with your actual API key
# 4. Run this script: python resume_analyzer.py
# ============================================================================

# Set your OpenAI API key here
openai.api_key = "your-api-key-here"  # ⚠️ REPLACE WITH YOUR ACTUAL API KEY

import sys

# Ensure backend directory is in path for local resume_engine
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    import resume_engine
except ImportError:
    resume_engine = None

def analyze_resume(text: str) -> Dict[str, Any]:
    """
    Analyze a resume using OpenAI GPT-4 if configured, or fall back to
    the high-precision local resume_engine.
    """
    # Check if a custom valid OpenAI key is provided in environment or variable
    env_key = os.getenv("OPENAI_API_KEY", "").strip()
    api_key = openai.api_key if openai.api_key and openai.api_key != "your-api-key-here" else env_key

    if api_key and api_key != "your-api-key-here":
        try:
            openai.api_key = api_key
            prompt = f"""
You are an expert resume reviewer AI with 10+ years of experience in HR and recruitment. 
Analyze the following resume comprehensively and provide detailed feedback.

Resume Content:
{text}

Please analyze and return the following in JSON format:
{{
    "score": 85,
    "skills": ["JavaScript", "React", "Python"],
    "strengths": ["Strong technical skills"],
    "improvements": ["Add quantifiable achievements"],
    "recommendations": ["Include industry keywords"],
    "career_match": {{
        "roles": ["Software Engineer"],
        "industries": ["Technology"],
        "match_percentage": 92
    }},
    "market_value": {{
        "salary_range": "₹8,00,000 - ₹14,00,000",
        "demand_level": "High",
        "growth_potential": "Excellent"
    }}
}}
"""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
                request_timeout=2
            )
            content = response['choices'][0]['message']['content'].strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            return json.loads(content.strip())
        except Exception as e:
            print(f"⚠️ OpenAI API unavailable ({e}). Using advanced local resume engine...")

    # High-precision local assessment engine
    if resume_engine:
        local_result = resume_engine.analyze_resume_comprehensively(text)
        career_intel = local_result.get("career_intelligence", {})
        return {
            "score": local_result.get("score", 75),
            "score_breakdown": local_result.get("score_breakdown", {}),
            "detected_domain": local_result.get("detected_domain", "General Professional"),
            "experience": local_result.get("experience", {}),
            "skills": local_result.get("skills", []),
            "strengths": local_result.get("strengths", []),
            "improvements": local_result.get("improvements", []),
            "recommendations": local_result.get("recommendations", []),
            "career_match": {
                "roles": career_intel.get("career_path", ["Professional Specialist"]),
                "industries": [local_result.get("detected_domain", "General")],
                "match_percentage": min(98, max(65, local_result.get("score", 75) + 5))
            },
            "market_value": {
                "salary_range": career_intel.get("salary_insights", ["Competitive Market Rate"])[0] if career_intel.get("salary_insights") else "Competitive",
                "demand_level": "High" if local_result.get("score", 0) > 75 else "Moderate",
                "growth_potential": "Excellent"
            }
        }
    
    return {"error": "No resume analysis engine available."}

def print_analysis(analysis: Dict[str, Any]) -> None:
    """
    Print the analysis results in a formatted way.
    
    Args:
        analysis (dict): The analysis results from analyze_resume()
    """
    
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    print("\n" + "="*60)
    print("🎯 RESUME ANALYSIS RESULTS")
    print("="*60)
    
    # Overall Score & Detected Domain
    print(f"\n📊 OVERALL ATS SCORE: {analysis.get('score', 'N/A')}/100")
    if 'detected_domain' in analysis:
        exp_info = f" | Experience: {analysis['experience'].get('years', 'N/A')} yrs" if 'experience' in analysis else ""
        print(f"🎯 DETECTED DOMAIN: {analysis.get('detected_domain')}{exp_info}")
    
    # 5-Pillar ATS Breakdown if available
    if 'score_breakdown' in analysis and analysis['score_breakdown']:
        b = analysis['score_breakdown']
        print("\n📈 ATS SCORING BREAKDOWN:")
        for pillar, data in b.items():
            print(f"   • {pillar.capitalize():<14}: {data.get('score', 0)}/{data.get('max', 20)}")
    
    # Skills
    print(f"\n🛠️  VERIFIED SKILLS ({len(analysis.get('skills', []))} found):")
    for skill in analysis.get('skills', []):
        print(f"   • {skill}")
    
    # Strengths
    print(f"\n✅ STRENGTHS:")
    for strength in analysis.get('strengths', []):
        print(f"   • {strength}")
    
    # Areas for Improvement
    print(f"\n⚠️  AREAS FOR IMPROVEMENT:")
    for improvement in analysis.get('improvements', []):
        print(f"   • {improvement}")
    
    # Recommendations
    print(f"\n💡 AI RECOMMENDATIONS:")
    for rec in analysis.get('recommendations', []):
        print(f"   • {rec}")
    
    # Career Match
    if 'career_match' in analysis:
        career = analysis['career_match']
        print(f"\n🎯 CAREER MATCH:")
        print(f"   Match Percentage: {career.get('match_percentage', 'N/A')}%")
        print(f"   Recommended Roles:")
        for role in career.get('roles', []):
            print(f"     • {role}")
        print(f"   Suitable Industries:")
        for industry in career.get('industries', []):
            print(f"     • {industry}")
    
    # Market Value
    if 'market_value' in analysis:
        market = analysis['market_value']
        print(f"\n💰 MARKET VALUE:")
        print(f"   Salary Range: {market.get('salary_range', 'N/A')}")
        print(f"   Demand Level: {market.get('demand_level', 'N/A')}")
        print(f"   Growth Potential: {market.get('growth_potential', 'N/A')}")
    
    print("\n" + "="*60)

def main():
    """
    Main function to run the resume analyzer.
    """
    
    print("🚀 AI Resume Analyzer")
    print("="*40)
    
    # Check if API key is set or inform user of local engine mode
    if openai.api_key == "your-api-key-here" and not os.getenv("OPENAI_API_KEY"):
        print("ℹ️ Note: OpenAI key not set. Using advanced local resume engine with full offline precision.")
        print("="*40)
    
    # Example resume text
    example_resume = """
JOHN DOE
Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing scalable web applications using modern technologies. Passionate about clean code, user experience, and continuous learning.

TECHNICAL SKILLS
• Programming Languages: JavaScript, Python, Java, SQL
• Frameworks & Libraries: React, Node.js, Express, Django
• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
• Databases: MongoDB, PostgreSQL, Redis
• Tools: Git, VS Code, Postman, Jira

EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2022 - Present
• Led development of microservices architecture serving 100K+ users
• Implemented CI/CD pipeline reducing deployment time by 60%
• Mentored 3 junior developers and conducted code reviews
• Technologies: React, Node.js, AWS, Docker

Software Developer | StartupXYZ | 2020 - 2022
• Built full-stack web applications using React and Node.js
• Collaborated with cross-functional teams to deliver features
• Optimized database queries improving performance by 40%
• Technologies: JavaScript, Python, PostgreSQL

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2020

PROJECTS
E-commerce Platform: Built scalable online store with React, Node.js, and MongoDB
Task Management App: Created collaborative project management tool
Weather Dashboard: Developed real-time weather application using APIs
"""
    
    print("\n📝 Analyzing example resume...")
    print("-" * 40)
    
    # Analyze the resume
    result = analyze_resume(example_resume)
    
    # Print results
    print_analysis(result)
    
    # Interactive mode
    print("\n🤖 Would you like to analyze your own resume?")
    print("Type 'yes' to continue or 'no' to exit:")
    
    user_input = input("> ").lower().strip()
    
    if user_input in ['yes', 'y']:
        print("\n📝 Enter your resume text (press Enter twice when done):")
        print("(You can copy-paste from a Word/PDF document)")
        print("-" * 40)
        
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        
        resume_text = "\n".join(lines[:-1])  # Remove the last empty line
        
        if resume_text.strip():
            print("\n🔍 Analyzing your resume...")
            result = analyze_resume(resume_text)
            print_analysis(result)
        else:
            print("❌ No resume text provided.")

if __name__ == "__main__":
    main() 