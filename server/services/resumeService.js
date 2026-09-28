const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');
const fs = require('fs');
const natural = require('natural');

// Extract text from different file formats
exports.extractText = async (filePath, mimetype) => {
  try {
    const fileBuffer = fs.readFileSync(filePath);
    
    if (mimetype === 'application/pdf') {
      const data = await pdfParse(fileBuffer);
      return data.text;
    } else if (mimetype.includes('word') || mimetype.includes('docx')) {
      const result = await mammoth.extractRawText({ buffer: fileBuffer });
      return result.value;
    } else if (mimetype.includes('text') || mimetype.includes('plain')) {
      return fileBuffer.toString('utf-8');
    } else {
      throw new Error('Unsupported file format');
    }
  } catch (error) {
    console.error('Text extraction error:', error);
    throw new Error('Failed to extract text from file');
  }
};

// Parse resume text into structured data
exports.parseResume = async (text) => {
  try {
    const parsedData = {
      personalInfo: extractPersonalInfo(text),
      summary: extractSummary(text),
      experience: extractExperience(text),
      education: extractEducation(text),
      skills: extractSkills(text),
      certifications: extractCertifications(text),
      projects: extractProjects(text),
      languages: extractLanguages(text)
    };

    return parsedData;
  } catch (error) {
    console.error('Resume parsing error:', error);
    throw new Error('Failed to parse resume data');
  }
};

// Extract personal information
function extractPersonalInfo(text) {
  const personalInfo = {
    name: '',
    email: '',
    phone: '',
    location: '',
    linkedin: '',
    website: ''
  };

  // Extract email
  const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
  const emails = text.match(emailRegex);
  if (emails && emails.length > 0) {
    personalInfo.email = emails[0];
  }

  // Extract phone number
  const phoneRegex = /(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g;
  const phones = text.match(phoneRegex);
  if (phones && phones.length > 0) {
    personalInfo.phone = phones[0];
  }

  // Extract LinkedIn URL
  const linkedinRegex = /(https?:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?/g;
  const linkedinUrls = text.match(linkedinRegex);
  if (linkedinUrls && linkedinUrls.length > 0) {
    personalInfo.linkedin = linkedinUrls[0];
  }

  // Extract website
  const websiteRegex = /(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?/g;
  const websites = text.match(websiteRegex);
  if (websites && websites.length > 0) {
    // Filter out common domains that aren't personal websites
    const personalWebsites = websites.filter(site => 
      !site.includes('linkedin.com') && 
      !site.includes('gmail.com') && 
      !site.includes('yahoo.com') &&
      !site.includes('hotmail.com')
    );
    if (personalWebsites.length > 0) {
      personalInfo.website = personalWebsites[0];
    }
  }

  // Extract name (usually at the top of the resume)
  const lines = text.split('\n').slice(0, 10);
  for (const line of lines) {
    const cleanLine = line.trim();
    if (cleanLine && cleanLine.length > 2 && cleanLine.length < 50) {
      // Check if line looks like a name (contains letters, spaces, no special chars)
      if (/^[A-Za-z\s]+$/.test(cleanLine) && cleanLine.split(' ').length >= 2) {
        personalInfo.name = cleanLine;
        break;
      }
    }
  }

  // Extract location (look for city, state patterns)
  const locationRegex = /([A-Za-z\s]+,\s*[A-Z]{2})/g;
  const locations = text.match(locationRegex);
  if (locations && locations.length > 0) {
    personalInfo.location = locations[0];
  }

  return personalInfo;
}

// Extract summary/objective
function extractSummary(text) {
  const summaryKeywords = ['summary', 'objective', 'profile', 'about'];
  const lines = text.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].toLowerCase();
    if (summaryKeywords.some(keyword => line.includes(keyword))) {
      // Get the next few lines as summary
      let summary = '';
      for (let j = i + 1; j < Math.min(i + 5, lines.length); j++) {
        const summaryLine = lines[j].trim();
        if (summaryLine && summaryLine.length > 10) {
          summary += summaryLine + ' ';
        } else if (summaryLine.length === 0 && summary) {
          break;
        }
      }
      return summary.trim();
    }
  }
  
  return '';
}

// Extract work experience
function extractExperience(text) {
  const experience = [];
  const experienceKeywords = ['experience', 'employment', 'work history', 'professional experience'];
  const lines = text.split('\n');
  
  let inExperienceSection = false;
  let currentExperience = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    // Check if we're entering experience section
    if (!inExperienceSection && experienceKeywords.some(keyword => lowerLine.includes(keyword))) {
      inExperienceSection = true;
      continue;
    }
    
    if (inExperienceSection) {
      // Look for job titles (usually in caps or followed by company)
      if (line && line.length > 3 && line.length < 100) {
        // Check if line looks like a job title
        if (isJobTitle(line)) {
          if (currentExperience) {
            experience.push(currentExperience);
          }
          currentExperience = {
            title: line,
            company: '',
            location: '',
            startDate: '',
            endDate: '',
            current: false,
            description: '',
            achievements: []
          };
        } else if (currentExperience && !currentExperience.company) {
          // This might be the company name
          currentExperience.company = line;
        } else if (currentExperience && !currentExperience.location) {
          // Check if this looks like a location
          if (line.includes(',') && line.length < 50) {
            currentExperience.location = line;
          }
        } else if (currentExperience && !currentExperience.startDate) {
          // Look for date patterns
          const dateMatch = extractDateRange(line);
          if (dateMatch) {
            currentExperience.startDate = dateMatch.start;
            currentExperience.endDate = dateMatch.end;
            currentExperience.current = dateMatch.current;
          }
        } else if (currentExperience && line.length > 10) {
          // This might be description
          currentExperience.description += line + ' ';
        }
      }
    }
  }
  
  if (currentExperience) {
    experience.push(currentExperience);
  }
  
  return experience;
}

// Extract education
function extractEducation(text) {
  const education = [];
  const educationKeywords = ['education', 'academic', 'degree', 'university', 'college'];
  const lines = text.split('\n');
  
  let inEducationSection = false;
  let currentEducation = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    if (!inEducationSection && educationKeywords.some(keyword => lowerLine.includes(keyword))) {
      inEducationSection = true;
      continue;
    }
    
    if (inEducationSection) {
      if (line && line.length > 3) {
        if (isDegree(line)) {
          if (currentEducation) {
            education.push(currentEducation);
          }
          currentEducation = {
            degree: line,
            institution: '',
            location: '',
            startDate: '',
            endDate: '',
            gpa: '',
            relevantCourses: []
          };
        } else if (currentEducation && !currentEducation.institution) {
          currentEducation.institution = line;
        } else if (currentEducation && line.includes('GPA')) {
          const gpaMatch = line.match(/GPA[:\s]*([0-9.]+)/i);
          if (gpaMatch) {
            currentEducation.gpa = gpaMatch[1];
          }
        }
      }
    }
  }
  
  if (currentEducation) {
    education.push(currentEducation);
  }
  
  return education;
}

// Extract skills
function extractSkills(text) {
  const skills = [];
  const skillKeywords = ['skills', 'technical skills', 'competencies', 'expertise'];
  const lines = text.split('\n');
  
  let inSkillsSection = false;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    if (!inSkillsSection && skillKeywords.some(keyword => lowerLine.includes(keyword))) {
      inSkillsSection = true;
      continue;
    }
    
    if (inSkillsSection) {
      if (line && line.length > 2) {
        // Split by common delimiters
        const skillList = line.split(/[,;|•]/);
        skillList.forEach(skill => {
          const cleanSkill = skill.trim();
          if (cleanSkill && cleanSkill.length > 2 && cleanSkill.length < 50) {
            skills.push(cleanSkill);
          }
        });
      }
    }
  }
  
  // Group skills by category
  const categorizedSkills = categorizeSkills(skills);
  return categorizedSkills;
}

// Extract certifications
function extractCertifications(text) {
  const certifications = [];
  const certKeywords = ['certification', 'certified', 'license', 'accreditation'];
  const lines = text.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    if (certKeywords.some(keyword => lowerLine.includes(keyword))) {
      const cert = {
        name: line,
        issuer: '',
        date: '',
        expiryDate: ''
      };
      
      // Look for issuer in next few lines
      for (let j = i + 1; j < Math.min(i + 3, lines.length); j++) {
        const nextLine = lines[j].trim();
        if (nextLine && !cert.issuer) {
          cert.issuer = nextLine;
          break;
        }
      }
      
      certifications.push(cert);
    }
  }
  
  return certifications;
}

// Extract projects
function extractProjects(text) {
  const projects = [];
  const projectKeywords = ['project', 'portfolio', 'achievement'];
  const lines = text.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    if (projectKeywords.some(keyword => lowerLine.includes(keyword))) {
      const project = {
        name: line,
        description: '',
        technologies: [],
        link: '',
        startDate: '',
        endDate: ''
      };
      
      // Get description from next few lines
      for (let j = i + 1; j < Math.min(i + 5, lines.length); j++) {
        const nextLine = lines[j].trim();
        if (nextLine && nextLine.length > 10) {
          project.description += nextLine + ' ';
        } else if (nextLine.length === 0 && project.description) {
          break;
        }
      }
      
      projects.push(project);
    }
  }
  
  return projects;
}

// Extract languages
function extractLanguages(text) {
  const languages = [];
  const languageKeywords = ['language', 'languages', 'fluent', 'proficient'];
  const lines = text.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const lowerLine = line.toLowerCase();
    
    if (languageKeywords.some(keyword => lowerLine.includes(keyword))) {
      const languageList = line.split(/[,;]/);
      languageList.forEach(lang => {
        const cleanLang = lang.trim();
        if (cleanLang && cleanLang.length > 2) {
          languages.push({
            language: cleanLang,
            proficiency: 'Proficient'
          });
        }
      });
    }
  }
  
  return languages;
}

// Helper functions
function isJobTitle(line) {
  const jobTitleKeywords = ['manager', 'director', 'engineer', 'developer', 'analyst', 'specialist', 'coordinator', 'assistant'];
  const lowerLine = line.toLowerCase();
  return jobTitleKeywords.some(keyword => lowerLine.includes(keyword)) || 
         (line.length > 5 && line.length < 50 && /^[A-Za-z\s]+$/.test(line));
}

function isDegree(line) {
  const degreeKeywords = ['bachelor', 'master', 'phd', 'associate', 'diploma', 'certificate'];
  const lowerLine = line.toLowerCase();
  return degreeKeywords.some(keyword => lowerLine.includes(keyword));
}

function extractDateRange(line) {
  const dateRegex = /(\w+\s+\d{4})\s*[-–—]\s*(\w+\s+\d{4}|present|current)/i;
  const match = line.match(dateRegex);
  
  if (match) {
    return {
      start: match[1],
      end: match[2],
      current: match[2].toLowerCase().includes('present') || match[2].toLowerCase().includes('current')
    };
  }
  
  return null;
}

function categorizeSkills(skills) {
  const categories = {
    'Programming Languages': [],
    'Frameworks & Libraries': [],
    'Databases': [],
    'Cloud & DevOps': [],
    'Tools & Platforms': [],
    'Soft Skills': []
  };
  
  const skillCategories = {
    'Programming Languages': ['javascript', 'python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
    'Frameworks & Libraries': ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel'],
    'Databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server'],
    'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd'],
    'Tools & Platforms': ['git', 'jira', 'confluence', 'slack', 'figma', 'adobe', 'microsoft office']
  };
  
  skills.forEach(skill => {
    const lowerSkill = skill.toLowerCase();
    let categorized = false;
    
    for (const [category, keywords] of Object.entries(skillCategories)) {
      if (keywords.some(keyword => lowerSkill.includes(keyword))) {
        categories[category].push(skill);
        categorized = true;
        break;
      }
    }
    
    if (!categorized) {
      categories['Soft Skills'].push(skill);
    }
  });
  
  // Convert to array format
  return Object.entries(categories)
    .filter(([category, skills]) => skills.length > 0)
    .map(([category, skills]) => ({
      category,
      skills
    }));
} 