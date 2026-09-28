const express = require('express');
const router = express.Router();
const resumeController = require('../controllers/resumeController');
const auth = require('../middleware/auth');
const upload = require('../middleware/upload');

// Protected routes - all require authentication
router.use(auth);

// Resume management
router.post('/upload', upload.single('resume'), resumeController.uploadResume);
router.get('/', resumeController.getUserResumes);
router.get('/:id', resumeController.getResumeById);
router.put('/:id', resumeController.updateResume);
router.delete('/:id', resumeController.deleteResume);

// Analysis routes
router.post('/:id/analyze', resumeController.analyzeResume);
router.get('/:id/analysis', resumeController.getAnalysis);
router.post('/:id/optimize', resumeController.optimizeResume);
router.get('/:id/insights', resumeController.getAIInsights);

// Batch operations
router.post('/batch-analyze', resumeController.batchAnalyze);
router.get('/analytics/summary', resumeController.getAnalyticsSummary);

// Export routes
router.get('/:id/export/pdf', resumeController.exportToPDF);
router.get('/:id/export/json', resumeController.exportToJSON);

module.exports = router; 