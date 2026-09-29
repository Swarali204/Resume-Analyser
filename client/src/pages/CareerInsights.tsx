import React from 'react';

const CareerInsights: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-xl shadow p-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Career Insights
        </h1>

        <p className="text-gray-600 mt-2 mb-8">
          Get personalized insights and recommendations for your career.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Recommended Roles
            </h2>
            <p className="text-gray-600 mt-3">
              Career roles matching your skills and experience will appear
              here.
            </p>
          </div>

          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Skill Development
            </h2>
            <p className="text-gray-600 mt-3">
              Recommended skills and learning areas will appear here.
            </p>
          </div>

          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Career Growth
            </h2>
            <p className="text-gray-600 mt-3">
              Personalized career growth suggestions will appear here.
            </p>
          </div>

          <div className="border rounded-xl p-6">
            <h2 className="text-xl font-semibold text-gray-800">
              Resume Improvement
            </h2>
            <p className="text-gray-600 mt-3">
              Suggestions to improve your resume and increase its
              effectiveness will appear here.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerInsights;