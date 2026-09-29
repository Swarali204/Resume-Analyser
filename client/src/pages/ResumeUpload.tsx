import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const ResumeUpload: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      toast.error('Please upload a PDF or Word document.');
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = () => {
    if (!file) {
      toast.error('Please select a resume first.');
      return;
    }

    toast.success('Resume selected successfully!');
    navigate('/');
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-xl shadow p-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Upload Resume
        </h1>

        <p className="text-gray-600 mt-2 mb-8">
          Upload your resume to get AI-powered analysis and career insights.
        </p>

        <label className="block border-2 border-dashed border-gray-300 rounded-xl p-10 text-center cursor-pointer hover:border-indigo-500 transition">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="text-gray-600">
            <p className="text-lg font-medium">
              {file ? file.name : 'Choose your resume'}
            </p>

            <p className="text-sm mt-2">
              Supported formats: PDF, DOC, DOCX
            </p>
          </div>
        </label>

        <button
          onClick={handleUpload}
          className="mt-6 w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
        >
          Upload Resume
        </button>
      </div>
    </div>
  );
};

export default ResumeUpload;