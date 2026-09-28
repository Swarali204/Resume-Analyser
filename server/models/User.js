const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  profile: {
    phone: String,
    location: String,
    linkedin: String,
    github: String,
    website: String,
    bio: String,
    avatar: String
  },
  career: {
    currentRole: String,
    yearsOfExperience: Number,
    industry: String,
    skills: [String],
    interests: [String],
    targetRoles: [String],
    salaryExpectation: {
      min: Number,
      max: Number,
      currency: {
        type: String,
        default: 'USD'
      }
    }
  },
  preferences: {
    jobAlerts: {
      type: Boolean,
      default: true
    },
    emailNotifications: {
      type: Boolean,
      default: true
    },
    privacySettings: {
      profileVisibility: {
        type: String,
        enum: ['public', 'private', 'connections'],
        default: 'public'
      }
    }
  },
  analytics: {
    totalResumes: {
      type: Number,
      default: 0
    },
    totalAnalyses: {
      type: Number,
      default: 0
    },
    lastLogin: Date,
    accountCreated: {
      type: Date,
      default: Date.now
    }
  },
  isVerified: {
    type: Boolean,
    default: false
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Index for better query performance
userSchema.index({ email: 1 });
userSchema.index({ 'career.skills': 1 });
userSchema.index({ 'career.industry': 1 });

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Method to compare password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Method to get public profile (without sensitive data)
userSchema.methods.getPublicProfile = function() {
  const userObject = this.toObject();
  delete userObject.password;
  delete userObject.__v;
  return userObject;
};

// Virtual for full name
userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});

// Ensure virtual fields are serialized
userSchema.set('toJSON', { virtuals: true });

module.exports = mongoose.model('User', userSchema); 