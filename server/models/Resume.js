const mongoose = require('mongoose');

const resumeSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  originalFile: {
    filename: String,
    originalName: String,
    mimetype: String,
    size: Number,
    path: String
  },
  extractedText: {
    type: String,
    required: true
  },
  parsedData: {
    personalInfo: {
      name: String,
      email: String,
      phone: String,
      location: String,
      linkedin: String,
      website: String
    },
    summary: String,
    experience: [{
      title: String,
      company: String,
      location: String,
      startDate: String,
      endDate: String,
      current: Boolean,
      description: String,
      achievements: [String]
    }],
    education: [{
      degree: String,
      institution: String,
      location: String,
      startDate: String,
      endDate: String,
      gpa: String,
      relevantCourses: [String]
    }],
    skills: [{
      category: String,
      skills: [String]
    }],
    certifications: [{
      name: String,
      issuer: String,
      date: String,
      expiryDate: String
    }],
    projects: [{
      name: String,
      description: String,
      technologies: [String],
      link: String,
      startDate: String,
      endDate: String
    }],
    languages: [{
      language: String,
      proficiency: String
    }]
  },
  analysis: {
    overallScore: {
      type: Number,
      min: 0,
      max: 100
    },
    strengths: [{
      category: String,
      items: [String],
      score: Number
    }],
    weaknesses: [{
      category: String,
      items: [String],
      score: Number
    }],
    suggestions: [{
      category: String,
      suggestions: [String],
      priority: {
        type: String,
        enum: ['high', 'medium', 'low']
      }
    }],
    keywordAnalysis: {
      found: [String],
      missing: [String],
      score: Number
    },
    atsCompatibility: {
      score: Number,
      issues: [String],
      recommendations: [String]
    }
  },
  aiInsights: {
    careerPath: {
      currentLevel: String,
      suggestedNextSteps: [String],
      timeline: String
    },
    skillGaps: [{
      skill: String,
      importance: Number,
      resources: [String]
    }],
    marketTrends: {
      inDemandSkills: [String],
      salaryInsights: {
        current: Number,
        potential: Number,
        currency: String
      },
      industryTrends: [String]
    },
    jobRecommendations: [{
      title: String,
      company: String,
      matchScore: Number,
      requirements: [String],
      salary: {
        min: Number,
        max: Number,
        currency: String
      }
    }]
  },
  metadata: {
    fileType: {
      type: String,
      enum: ['pdf', 'docx', 'txt']
    },
    processingTime: Number,
    wordCount: Number,
    lastAnalyzed: {
      type: Date,
      default: Date.now
    },
    version: {
      type: Number,
      default: 1
    }
  },
  status: {
    type: String,
    enum: ['processing', 'completed', 'failed', 'archived'],
    default: 'processing'
  },
  tags: [String],
  isPublic: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
});

// Indexes for better query performance
resumeSchema.index({ user: 1, createdAt: -1 });
resumeSchema.index({ 'analysis.overallScore': -1 });
resumeSchema.index({ 'parsedData.skills.skills': 1 });
resumeSchema.index({ status: 1 });

// Virtual for formatted analysis score
resumeSchema.virtual('formattedScore').get(function() {
  if (!this.analysis.overallScore) return 'N/A';
  return `${this.analysis.overallScore}/100`;
});

// Method to get summary of analysis
resumeSchema.methods.getAnalysisSummary = function() {
  return {
    score: this.analysis.overallScore,
    strengths: this.analysis.strengths.length,
    weaknesses: this.analysis.weaknesses.length,
    suggestions: this.analysis.suggestions.length,
    lastAnalyzed: this.metadata.lastAnalyzed
  };
};

// Method to update analysis
resumeSchema.methods.updateAnalysis = function(newAnalysis) {
  this.analysis = { ...this.analysis, ...newAnalysis };
  this.metadata.lastAnalyzed = new Date();
  this.status = 'completed';
  return this.save();
};

// Ensure virtual fields are serialized
resumeSchema.set('toJSON', { virtuals: true });

module.exports = mongoose.model('Resume', resumeSchema); 