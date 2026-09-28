const Resume = require('../models/Resume');
const User = require('../models/User');
const resumeService = require('../services/resumeService');
const aiService = require('../services/aiService');
const fs = require('fs');
const path = require('path');

// Upload and parse resume
exports.uploadResume = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: 'No file uploaded'
      });
    }

    const { originalname, filename, mimetype, size, path: filePath } = req.file;
    const userId = req.user.userId;

    // Extract text from file
    const extractedText = await resumeService.extractText(filePath, mimetype);
    
    // Parse resume data
    const parsedData = await resumeService.parseResume(extractedText);
    
    // Create resume document
    const resume = new Resume({
      user: userId,
      originalFile: {
        filename,
        originalName: originalname,
        mimetype,
        size,
        path: filePath
      },
      extractedText,
      parsedData,
      metadata: {
        fileType: path.extname(originalname).toLowerCase().replace('.', ''),
        wordCount: extractedText.split(/\s+/).length,
        processingTime: Date.now()
      }
    });

    await resume.save();

    // Update user analytics
    await User.findByIdAndUpdate(userId, {
      $inc: { 'analytics.totalResumes': 1 }
    });

    res.status(201).json({
      message: 'Resume uploaded successfully',
      resume: {
        id: resume._id,
        originalName,
        status: resume.status,
        metadata: resume.metadata
      }
    });
  } catch (error) {
    console.error('Upload resume error:', error);
    res.status(500).json({
      error: 'Failed to upload resume'
    });
  }
};

// Get user's resumes
exports.getUserResumes = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { page = 1, limit = 10, status } = req.query;

    const query = { user: userId };
    if (status) query.status = status;

    const resumes = await Resume.find(query)
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .select('-extractedText -parsedData');

    const total = await Resume.countDocuments(query);

    res.json({
      resumes,
      totalPages: Math.ceil(total / limit),
      currentPage: page,
      total
    });
  } catch (error) {
    console.error('Get user resumes error:', error);
    res.status(500).json({
      error: 'Failed to fetch resumes'
    });
  }
};

// Get specific resume
exports.getResumeById = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    res.json({ resume });
  } catch (error) {
    console.error('Get resume error:', error);
    res.status(500).json({
      error: 'Failed to fetch resume'
    });
  }
};

// Analyze resume with AI
exports.analyzeResume = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // Update status to processing
    resume.status = 'processing';
    await resume.save();

    // Perform AI analysis
    const analysis = await aiService.analyzeResume(resume.extractedText, resume.parsedData);
    
    // Update resume with analysis results
    resume.analysis = analysis;
    resume.status = 'completed';
    resume.metadata.lastAnalyzed = new Date();
    await resume.save();

    // Update user analytics
    await User.findByIdAndUpdate(userId, {
      $inc: { 'analytics.totalAnalyses': 1 }
    });

    res.json({
      message: 'Resume analysis completed',
      analysis: resume.analysis
    });
  } catch (error) {
    console.error('Analyze resume error:', error);
    res.status(500).json({
      error: 'Failed to analyze resume'
    });
  }
};

// Get analysis results
exports.getAnalysis = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    if (resume.status !== 'completed') {
      return res.status(400).json({
        error: 'Resume analysis not completed'
      });
    }

    res.json({
      analysis: resume.analysis,
      metadata: resume.metadata
    });
  } catch (error) {
    console.error('Get analysis error:', error);
    res.status(500).json({
      error: 'Failed to fetch analysis'
    });
  }
};

// Get AI insights
exports.getAIInsights = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // Generate AI insights if not already present
    if (!resume.aiInsights || Object.keys(resume.aiInsights).length === 0) {
      const insights = await aiService.generateInsights(resume.parsedData, resume.analysis);
      resume.aiInsights = insights;
      await resume.save();
    }

    res.json({
      insights: resume.aiInsights
    });
  } catch (error) {
    console.error('Get AI insights error:', error);
    res.status(500).json({
      error: 'Failed to generate insights'
    });
  }
};

// Optimize resume
exports.optimizeResume = async (req, res) => {
  try {
    const { id } = req.params;
    const { targetRole, targetCompany } = req.body;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // Generate optimization suggestions
    const optimization = await aiService.optimizeResume(
      resume.extractedText,
      resume.parsedData,
      targetRole,
      targetCompany
    );

    res.json({
      message: 'Resume optimization completed',
      optimization
    });
  } catch (error) {
    console.error('Optimize resume error:', error);
    res.status(500).json({
      error: 'Failed to optimize resume'
    });
  }
};

// Update resume
exports.updateResume = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const updates = req.body;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // Update allowed fields
    if (updates.tags) resume.tags = updates.tags;
    if (updates.isPublic !== undefined) resume.isPublic = updates.isPublic;
    if (updates.parsedData) resume.parsedData = updates.parsedData;

    await resume.save();

    res.json({
      message: 'Resume updated successfully',
      resume
    });
  } catch (error) {
    console.error('Update resume error:', error);
    res.status(500).json({
      error: 'Failed to update resume'
    });
  }
};

// Delete resume
exports.deleteResume = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // Delete file if exists
    if (resume.originalFile.path && fs.existsSync(resume.originalFile.path)) {
      fs.unlinkSync(resume.originalFile.path);
    }

    await Resume.findByIdAndDelete(id);

    res.json({
      message: 'Resume deleted successfully'
    });
  } catch (error) {
    console.error('Delete resume error:', error);
    res.status(500).json({
      error: 'Failed to delete resume'
    });
  }
};

// Batch analyze resumes
exports.batchAnalyze = async (req, res) => {
  try {
    const { resumeIds } = req.body;
    const userId = req.user.userId;

    const resumes = await Resume.find({
      _id: { $in: resumeIds },
      user: userId
    });

    const results = [];
    for (const resume of resumes) {
      try {
        const analysis = await aiService.analyzeResume(resume.extractedText, resume.parsedData);
        resume.analysis = analysis;
        resume.status = 'completed';
        resume.metadata.lastAnalyzed = new Date();
        await resume.save();
        
        results.push({
          id: resume._id,
          status: 'success',
          analysis: analysis
        });
      } catch (error) {
        results.push({
          id: resume._id,
          status: 'failed',
          error: error.message
        });
      }
    }

    res.json({
      message: 'Batch analysis completed',
      results
    });
  } catch (error) {
    console.error('Batch analyze error:', error);
    res.status(500).json({
      error: 'Failed to perform batch analysis'
    });
  }
};

// Get analytics summary
exports.getAnalyticsSummary = async (req, res) => {
  try {
    const userId = req.user.userId;

    const summary = await Resume.aggregate([
      { $match: { user: userId } },
      {
        $group: {
          _id: null,
          totalResumes: { $sum: 1 },
          averageScore: { $avg: '$analysis.overallScore' },
          completedAnalyses: {
            $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] }
          },
          processingAnalyses: {
            $sum: { $cond: [{ $eq: ['$status', 'processing'] }, 1, 0] }
          }
        }
      }
    ]);

    res.json({
      summary: summary[0] || {
        totalResumes: 0,
        averageScore: 0,
        completedAnalyses: 0,
        processingAnalyses: 0
      }
    });
  } catch (error) {
    console.error('Get analytics summary error:', error);
    res.status(500).json({
      error: 'Failed to fetch analytics summary'
    });
  }
};

// Export to PDF (placeholder)
exports.exportToPDF = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    // TODO: Implement PDF generation
    res.json({
      message: 'PDF export feature coming soon'
    });
  } catch (error) {
    console.error('Export to PDF error:', error);
    res.status(500).json({
      error: 'Failed to export to PDF'
    });
  }
};

// Export to JSON
exports.exportToJSON = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const resume = await Resume.findOne({ _id: id, user: userId });
    if (!resume) {
      return res.status(404).json({
        error: 'Resume not found'
      });
    }

    const exportData = {
      id: resume._id,
      originalName: resume.originalFile.originalName,
      parsedData: resume.parsedData,
      analysis: resume.analysis,
      aiInsights: resume.aiInsights,
      metadata: resume.metadata,
      createdAt: resume.createdAt,
      updatedAt: resume.updatedAt
    };

    res.json(exportData);
  } catch (error) {
    console.error('Export to JSON error:', error);
    res.status(500).json({
      error: 'Failed to export to JSON'
    });
  }
}; 