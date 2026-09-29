import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome, {user?.firstName || 'User'}!
        </h1>
        <p className="text-gray-600 mt-2">
          Analyze your resume and get personalized career insights.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          to="/upload"
          className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">
            Upload Resume
          </h2>
          <p className="text-gray-600 mt-2">
            Upload your resume for AI-powered analysis.
          </p>
        </Link>

        <Link
          to="/insights"
          className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">
            Career Insights
          </h2>
          <p className="text-gray-600 mt-2">
            Explore career recommendations and opportunities.
          </p>
        </Link>

        <Link
          to="/profile"
          className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition"
        >
          <h2 className="text-xl font-semibold text-gray-800">
            My Profile
          </h2>
          <p className="text-gray-600 mt-2">
            View and update your profile information.
          </p>
        </Link>
      </div>

      <div className="mt-8 bg-white rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Account Overview
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-500">Total Resumes</p>
            <p className="text-2xl font-bold text-indigo-600">
              {user?.analytics?.totalResumes || 0}
            </p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-500">Total Analyses</p>
            <p className="text-2xl font-bold text-indigo-600">
              {user?.analytics?.totalAnalyses || 0}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;