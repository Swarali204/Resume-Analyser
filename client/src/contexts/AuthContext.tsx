import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';

interface User {
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

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  updateProfile: (profileData: Partial<User>) => Promise<void>;
}

interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on app start
    const token = localStorage.getItem('token');
    if (token) {
      authService.getProfile()
        .then(userData => {
          setUser(userData);
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const { token, user: userData } = await authService.login(email, password);
      localStorage.setItem('token', token);
      setUser(userData);
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      const { token, user: newUser } = await authService.register(userData);
      localStorage.setItem('token', token);
      setUser(newUser);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updateProfile = async (profileData: Partial<User>) => {
    try {
      const updatedUser = await authService.updateProfile(profileData);
      setUser(updatedUser);
    } catch (error) {
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    updateProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 