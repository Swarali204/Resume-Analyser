const OpenAI = require('openai');
const natural = require('natural');
const nlp = require('compromise');

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Common skills and keywords for different industries
const SKILL_KEYWORDS = {
  'software-development': [
    'JavaScript', 'Python', 'Java', 'React', 'Node.js', 'SQL', 'Git',
    'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'AI', 'Data Science'
  ],
  'marketing': [
    'Digital Marketing', 'SEO', 'SEM', 'Social Media', 'Content Marketing',
    'Google Analytics', 'Email Marketing', 'Brand Management', 'CRM'
  ],
  'finance': [
    'Financial Analysis', 'Excel', 'QuickBooks', 'Accounting', 'Budgeting',
    'Risk Management', 'Investment', 'Financial Modeling', 'SAP'
  ],
  'healthcare': [
    'Patient Care', 'Medical Terminology', 'HIPAA', 'Electronic Health Records',
    'Clinical Research', 'Nursing', 'Pharmacy', 'Healthcare Administration'
  ]
};

// Analyze resume with AI
exports.analyzeResume = async (text, parsedData) => {
  try {
    // Basic text analysis
    const textAnalysis = analyzeText(text);
    
    // AI-powered analysis using OpenAI
    const aiAnalysis = await performAIAnalysis(text, parsedData);
    
    // Combine results
    const analysis = {
      overallScore: calculateOverallScore(textAnalysis, aiAnalysis),
      strengths: aiAnalysis.strengths,
      weaknesses: aiAnalysis.weaknesses,
      suggestions: aiAnalysis.suggestions,
      keywordAnalysis: textAnalysis.keywordAnalysis,
      atsCompatibility: analyzeATSCompatibility(text, parsedData)
    };

    return analysis;
  } catch (error) {
    console.error('AI analysis error:', error);
    // Fallback to basic analysis
    return performBasicAnalysis(text, parsedData);
  }
};

// Perform AI analysis using OpenAI
async function performAIAnalysis(text, parsedData) {
  try {
    const prompt = `
    Analyze this resume and provide detailed feedback:
    
    Resume Text: ${text.substring(0, 3000)}
    
    Please provide analysis in the following JSON format:
    {
      "strengths": [
        {
          "category": "string",
          "items": ["string"],
          "score": number
        }
      ],
      "weaknesses": [
        {
          "category": "string", 
          "items": ["string"],
          "score": number
        }
      ],
      "suggestions": [
        {
          "category": "string",
          "suggestions": ["string"],
          "priority": "high|medium|low"
        }
      ]
    }
    
    Focus on:
    - Content quality and relevance
    - Skills and experience presentation
    - Professional achievements
    - Areas for improvement
    - Actionable suggestions
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: "You are an expert resume analyst and career coach. Provide constructive, actionable feedback."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.3,
      max_tokens: 1500
    });

    const response = completion.choices[0].message.content;
    return JSON.parse(response);
  } catch (error) {
    console.error('OpenAI analysis error:', error);
    throw error;
  }
}

// Analyze text using NLP
function analyzeText(text) {
  const doc = nlp(text);
  
  // Extract keywords
  const keywords = doc.match('#Noun+').out('array');
  const skills = extractSkills(text);
  
  // Analyze readability
  const sentences = doc.sentences().out('array');
  const words = text.split(/\s+/);
  const avgSentenceLength = words.length / sentences.length;
  
  return {
    wordCount: words.length,
    sentenceCount: sentences.length,
    avgSentenceLength,
    keywords: keywords.slice(0, 20),
    skills,
    keywordAnalysis: {
      found: skills,
      missing: [],
      score: calculateKeywordScore(skills)
    }
  };
}

// Extract skills from text
function extractSkills(text) {
  const allSkills = [];
  Object.values(SKILL_KEYWORDS).flat().forEach(skill => {
    if (text.toLowerCase().includes(skill.toLowerCase())) {
      allSkills.push(skill);
    }
  });
  return [...new Set(allSkills)];
}

// Calculate keyword score
function calculateKeywordScore(skills) {
  const maxSkills = 15; // Assume 15 skills is optimal
  return Math.min((skills.length / maxSkills) * 100, 100);
}

// Analyze ATS compatibility
function analyzeATSCompatibility(text, parsedData) {
  const issues = [];
  const recommendations = [];
  
  // Check for common ATS issues
  if (text.includes('graphic') || text.includes('image')) {
    issues.push('Contains graphics or images that may not be readable by ATS');
    recommendations.push('Remove graphics and use plain text formatting');
  }
  
  if (!parsedData.personalInfo.email) {
    issues.push('Missing email address');
    recommendations.push('Add a professional email address');
  }
  
  if (!parsedData.personalInfo.phone) {
    issues.push('Missing phone number');
    recommendations.push('Add a contact phone number');
  }
  
  if (parsedData.experience.length === 0) {
    issues.push('No work experience listed');
    recommendations.push('Add relevant work experience');
  }
  
  const score = Math.max(0, 100 - (issues.length * 15));
  
  return {
    score,
    issues,
    recommendations
  };
}

// Calculate overall score
function calculateOverallScore(textAnalysis, aiAnalysis) {
  const keywordScore = textAnalysis.keywordAnalysis.score;
  const atsScore = aiAnalysis.atsCompatibility?.score || 80;
  const strengthScore = aiAnalysis.strengths?.length * 10 || 0;
  const weaknessPenalty = aiAnalysis.weaknesses?.length * 5 || 0;
  
  const totalScore = (keywordScore + atsScore + strengthScore - weaknessPenalty) / 3;
  return Math.max(0, Math.min(100, totalScore));
}

// Generate career insights
exports.generateInsights = async (parsedData, analysis) => {
  try {
    const prompt = `
    Based on this resume data and analysis, provide career insights:
    
    Experience: ${JSON.stringify(parsedData.experience)}
    Skills: ${JSON.stringify(parsedData.skills)}
    Analysis Score: ${analysis.overallScore}
    
    Provide insights in JSON format:
    {
      "careerPath": {
        "currentLevel": "string",
        "suggestedNextSteps": ["string"],
        "timeline": "string"
      },
      "skillGaps": [
        {
          "skill": "string",
          "importance": number,
          "resources": ["string"]
        }
      ],
      "marketTrends": {
        "inDemandSkills": ["string"],
        "salaryInsights": {
          "current": number,
          "potential": number,
          "currency": "USD"
        },
        "industryTrends": ["string"]
      },
      "jobRecommendations": [
        {
          "title": "string",
          "company": "string",
          "matchScore": number,
          "requirements": ["string"],
          "salary": {
            "min": number,
            "max": number,
            "currency": "USD"
          }
        }
      ]
    }
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: "You are an expert career advisor and job market analyst."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.4,
      max_tokens: 2000
    });

    const response = completion.choices[0].message.content;
    return JSON.parse(response);
  } catch (error) {
    console.error('Generate insights error:', error);
    return generateBasicInsights(parsedData, analysis);
  }
};

// Optimize resume for specific role
exports.optimizeResume = async (text, parsedData, targetRole, targetCompany) => {
  try {
    const prompt = `
    Optimize this resume for the role of ${targetRole} at ${targetCompany}:
    
    Current Resume: ${text.substring(0, 2000)}
    
    Provide optimization suggestions in JSON format:
    {
      "summary": "string",
      "keywordOptimization": {
        "add": ["string"],
        "remove": ["string"],
        "emphasize": ["string"]
      },
      "contentSuggestions": [
        {
          "section": "string",
          "suggestions": ["string"],
          "priority": "high|medium|low"
        }
      ],
      "formatting": ["string"],
      "overallScore": number
    }
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: "You are an expert resume writer and career coach."
        },
        {
          role: "user",
          content: prompt
        }
      ],
      temperature: 0.3,
      max_tokens: 1500
    });

    const response = completion.choices[0].message.content;
    return JSON.parse(response);
  } catch (error) {
    console.error('Optimize resume error:', error);
    return generateBasicOptimization(text, targetRole);
  }
};

// Fallback functions for when AI is not available
function performBasicAnalysis(text, parsedData) {
  const textAnalysis = analyzeText(text);
  const atsCompatibility = analyzeATSCompatibility(text, parsedData);
  
  return {
    overallScore: calculateOverallScore(textAnalysis, { atsCompatibility }),
    strengths: [
      {
        category: 'Content',
        items: ['Resume uploaded successfully'],
        score: 70
      }
    ],
    weaknesses: [
      {
        category: 'Analysis',
        items: ['AI analysis not available'],
        score: 30
      }
    ],
    suggestions: [
      {
        category: 'General',
        suggestions: ['Consider upgrading to enable AI-powered analysis'],
        priority: 'medium'
      }
    ],
    keywordAnalysis: textAnalysis.keywordAnalysis,
    atsCompatibility
  };
}

function generateBasicInsights(parsedData, analysis) {
  return {
    careerPath: {
      currentLevel: 'Professional',
      suggestedNextSteps: ['Update skills', 'Network', 'Apply to relevant positions'],
      timeline: '3-6 months'
    },
    skillGaps: [
      {
        skill: 'Industry-specific skills',
        importance: 80,
        resources: ['Online courses', 'Certifications', 'Industry events']
      }
    ],
    marketTrends: {
      inDemandSkills: ['Digital skills', 'Communication', 'Problem solving'],
      salaryInsights: {
        current: 60000,
        potential: 80000,
        currency: 'USD'
      },
      industryTrends: ['Remote work', 'Digital transformation', 'Sustainability']
    },
    jobRecommendations: [
      {
        title: 'Professional Role',
        company: 'Various Companies',
        matchScore: 70,
        requirements: ['Relevant experience', 'Skills', 'Education'],
        salary: {
          min: 50000,
          max: 90000,
          currency: 'USD'
        }
      }
    ]
  };
}

function generateBasicOptimization(text, targetRole) {
  return {
    summary: 'Resume optimization suggestions',
    keywordOptimization: {
      add: ['Role-specific keywords'],
      remove: ['Generic terms'],
      emphasize: ['Relevant experience']
    },
    contentSuggestions: [
      {
        section: 'Summary',
        suggestions: ['Add a compelling summary'],
        priority: 'high'
      }
    ],
    formatting: ['Use clear headings', 'Consistent formatting'],
    overallScore: 75
  };
} 