import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface User {
  _id: string;
  email: string;
  firstName: string;
  lastName: string;
  profile?: {
    phone?: string;
    location?: string;
    linkedin?: string;
    github?: string;
    website?: string;
    bio?: string;
    avatar?: string;
  };
  career?: {
    currentRole?: string;
    yearsOfExperience?: number;
    industry?: string;
    skills?: string[];
    interests?: string[];
    targetRoles?: string[];
  };
  analytics?: {
    totalResumes: number;
    totalAnalyses: number;
    lastLogin?: string;
    accountCreated: string;
  };
}

export interface LoginResponse {
  token: string;
  user: User;
  message: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

export const authService = {
  // Login user
  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await api.post('/auth/login', { email, password });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Login failed');
    }
  },

  // Register user
  async register(userData: RegisterData): Promise<LoginResponse> {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Registration failed');
    }
  },

  // Get user profile
  async getProfile(): Promise<User> {
    try {
      const response = await api.get('/auth/profile');
      return response.data.user;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to fetch profile');
    }
  },

  // Update user profile
  async updateProfile(profileData: Partial<User>): Promise<User> {
    try {
      const response = await api.put('/auth/profile', profileData);
      return response.data.user;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to update profile');
    }
  },

  // Change password
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await api.put('/auth/change-password', { currentPassword, newPassword });
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to change password');
    }
  },

  // Forgot password
  async forgotPassword(email: string): Promise<void> {
    try {
      await api.post('/auth/forgot-password', { email });
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to process password reset');
    }
  },

  // Reset password
  async resetPassword(token: string, newPassword: string): Promise<void> {
    try {
      await api.post(`/auth/reset-password/${token}`, { newPassword });
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to reset password');
    }
  },

  // Logout
  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch (error: any) {
      // Even if logout fails, we should still clear local storage
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
    }
  },

  // Refresh token
  async refreshToken(): Promise<{ token: string; user: User }> {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token available');
      }
      
      const response = await api.post('/auth/refresh-token', { token });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Failed to refresh token');
    }
  }
}; 