# 🚀 AI Resume Analyzer - Python Version

A powerful Python script that uses OpenAI's GPT-4 to analyze resumes and provide detailed feedback, career recommendations, and market insights.

## ✨ Features

- **AI-Powered Analysis**: Uses OpenAI GPT-4 for comprehensive resume review
- **Detailed Scoring**: Overall score from 0-100 with detailed breakdown
- **Skills Detection**: Identifies both technical and soft skills
- **Strengths & Weaknesses**: Highlights what's working and what needs improvement
- **Career Recommendations**: Suggests job roles and industries
- **Market Intelligence**: Provides salary ranges and demand analysis
- **Interactive Mode**: Analyze your own resume after seeing the demo

## 🛠️ Setup Instructions

### Step 1: Install Python Dependencies

**Option A: Using the setup script (Recommended)**
```bash
python setup.py
```

**Option B: Manual installation**
```bash
pip install openai
```

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Click "Create new secret key"
5. Copy the generated API key (keep it secure!)

### Step 3: Configure the Script

1. Open `resume_analyzer.py` in any text editor
2. Find this line: `openai.api_key = "your-api-key-here"`
3. Replace `"your-api-key-here"` with your actual API key
4. Save the file

### Step 4: Run the Analyzer

```bash
python resume_analyzer.py
```

## 📋 How to Use

### First Run (Demo Mode)
1. The script will first analyze an example resume
2. You'll see detailed results including:
   - Overall score
   - Detected skills
   - Strengths and areas for improvement
   - Career recommendations
   - Market value analysis

### Interactive Mode
1. After the demo, you'll be asked if you want to analyze your own resume
2. Type `yes` to continue
3. Copy and paste your resume text
4. Press Enter twice when done
5. Get your personalized analysis!

## 📊 Sample Output

```
🎯 RESUME ANALYSIS RESULTS
============================================================

📊 OVERALL SCORE: 85/100

🛠️  DETECTED SKILLS (8 found):
   • JavaScript
   • React
   • Python
   • Node.js
   • AWS
   • Docker
   • Leadership
   • Problem Solving

✅ STRENGTHS:
   • Strong technical skills
   • Clear project descriptions
   • Good formatting
   • Quantifiable achievements
   • Relevant experience

⚠️  AREAS FOR IMPROVEMENT:
   • Add more industry keywords
   • Expand summary section
   • Include certifications
   • Add more metrics

💡 AI RECOMMENDATIONS:
   • Include industry keywords
   • Add metrics to achievements
   • Enhance professional summary
   • Add relevant certifications

🎯 CAREER MATCH:
   Match Percentage: 92%
   Recommended Roles:
     • Software Engineer
     • Full Stack Developer
     • DevOps Engineer
   Suitable Industries:
     • Technology
     • Finance
     • Healthcare

💰 MARKET VALUE:
   Salary Range: $80,000 - $120,000
   Demand Level: High
   Growth Potential: Excellent
```

## 🔧 Customization

### Change AI Model
If GPT-4 is not available, change this line in the code:
```python
model="gpt-3.5-turbo"  # Instead of "gpt-4"
```

### Adjust Analysis Parameters
You can modify:
- `max_tokens`: Maximum response length (default: 1000)
- `temperature`: Response creativity (0.0-1.0, default: 0.3)
- Analysis categories in the prompt

## 💰 Cost Information

- **GPT-4**: ~$0.03 per 1K tokens (more expensive, better quality)
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens (cheaper, still good quality)
- Each analysis typically uses 500-1000 tokens

## 🚨 Important Notes

1. **API Key Security**: Never share your API key publicly
2. **Rate Limits**: OpenAI has rate limits on API calls
3. **Costs**: Each analysis costs money, so use wisely
4. **Data Privacy**: Your resume text is sent to OpenAI for analysis

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### "Invalid API key" Error
- Check that you've replaced the placeholder with your actual API key
- Ensure the API key is correct and active

### "Rate limit exceeded" Error
- Wait a few minutes before trying again
- Consider upgrading your OpenAI plan

### "Model not available" Error
- Change the model to "gpt-3.5-turbo"
- Check your OpenAI account access

## 📁 File Structure

```
├── resume_analyzer.py    # Main analysis script
├── setup.py             # Setup helper script
├── README_Python.md     # This file
└── advanced-index.html  # Web version (separate)
```

## 🤝 Contributing

Feel free to:
- Improve the analysis prompts
- Add more features
- Fix bugs
- Enhance the output formatting

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API key is correct
3. Ensure you have internet connection
4. Check OpenAI service status

---

**Happy Resume Analyzing! 🎯** 