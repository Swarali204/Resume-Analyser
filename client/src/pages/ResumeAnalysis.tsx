import React from 'react';
import { useParams, Link } from 'react-router-dom';

const ResumeAnalysis: React.FC = () => {
  const { id } = useParams();

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-xl shadow p-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">
              Resume Analysis
            </h1>
            <p className="text-gray-600 mt-2">
              AI-powered analysis of your resume.
            </p>
          </div>

          <Link
            to="/"
            className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            Dashboard
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              ATS Score
            </h2>
            <p className="text-4xl font-bold text-indigo-600 mt-3">
              --
            </p>
            <p className="text-gray-500 mt-2">
              Analysis ID: {id || 'N/A'}
            </p>
          </div>

          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Skills
            </h2>
            <p className="text-gray-600 mt-3">
              Your extracted skills will appear here after analysis.
            </p>
          </div>
        </div>

        <div className="mt-6 border rounded-xl p-6">
          <h2 className="text-xl font-semibold text-gray-800">
            Recommendations
          </h2>

          <p className="text-gray-600 mt-3">
            Personalized resume recommendations will appear here after
            the backend analysis is completed.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResumeAnalysis;