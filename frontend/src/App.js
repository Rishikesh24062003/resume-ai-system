import React, { useState } from 'react';
import { Upload, FileText, BarChart3, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [resumeData, setResumeData] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1);

  const handleFileUpload = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResumeData(response.data);
        setStep(2);
      } else {
        setError('Failed to process resume');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error uploading resume');
    } finally {
      setLoading(false);
    }
  };

  const handleScoreCalculation = async () => {
    if (!resumeData || !jobDescription.trim()) {
      setError('Please provide both resume and job description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/score`, {
        resume_data: {
          text: resumeData.text_preview,
          skills: resumeData.entities.SKILL || [],
          experience: resumeData.entities.EXPERIENCE || [],
          education: resumeData.entities.EDUCATION || [],
        },
        job_description: jobDescription,
        min_experience: 2,
        required_education: ['bachelor'],
      });

      if (response.data.success) {
        setAtsScore(response.data.ats_score);
        setStep(3);
      } else {
        setError('Failed to calculate ATS score');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error calculating score');
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setFile(null);
    setJobDescription('');
    setResumeData(null);
    setAtsScore(null);
    setError('');
    setStep(1);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return 'bg-green-100 border-green-300';
    if (score >= 60) return 'bg-yellow-100 border-yellow-300';
    return 'bg-red-100 border-red-300';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Resume AI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Advanced Resume Parsing and ATS Scoring System
          </p>
        </header>

        {error && (
          <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-100 border border-red-300 rounded-lg flex items-center">
            <AlertCircle className="h-5 w-5 text-red-600 mr-3" />
            <span className="text-red-700">{error}</span>
          </div>
        )}

        <div className="max-w-4xl mx-auto">
          {/* Step 1: Upload Resume */}
          {step === 1 && (
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="text-center mb-8">
                <Upload className="h-16 w-16 text-blue-600 mx-auto mb-4" />
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                  Upload Your Resume
                </h2>
                <p className="text-gray-600">
                  Supported formats: PDF, DOCX, DOC, TXT
                </p>
              </div>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="resume-upload"
                  disabled={loading}
                />
                <label
                  htmlFor="resume-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  {loading ? (
                    <Loader2 className="h-12 w-12 text-blue-600 animate-spin mb-4" />
                  ) : (
                    <FileText className="h-12 w-12 text-gray-400 mb-4" />
                  )}
                  <span className="text-lg font-medium text-gray-700 mb-2">
                    {loading ? 'Processing...' : 'Click to upload resume'}
                  </span>
                  <span className="text-sm text-gray-500">
                    Maximum file size: 5MB
                  </span>
                </label>
              </div>
            </div>
          )}

          {/* Step 2: Job Description */}
          {step === 2 && (
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="flex items-center mb-6">
                <CheckCircle className="h-6 w-6 text-green-600 mr-3" />
                <span className="text-green-700 font-medium">
                  Resume uploaded successfully
                </span>
              </div>

              <h2 className="text-2xl font-semibold text-gray-800 mb-6">
                Enter Job Description
              </h2>

              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here..."
                    className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                </div>

                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">
                    Extracted Information
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Skills Found:</h4>
                      <div className="flex flex-wrap gap-2">
                        {resumeData?.entities?.SKILL?.slice(0, 10).map((skill, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Contact Info:</h4>
                      <div className="text-sm text-gray-600">
                        {resumeData?.entities?.EMAIL?.length > 0 && (
                          <p>Email: {resumeData.entities.EMAIL[0]}</p>
                        )}
                        {resumeData?.entities?.PHONE?.length > 0 && (
                          <p>Phone: {resumeData.entities.PHONE[0]}</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-between mt-8">
                <button
                  onClick={resetApp}
                  className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Start Over
                </button>
                <button
                  onClick={handleScoreCalculation}
                  disabled={loading || !jobDescription.trim()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin mr-2" />
                      Calculating...
                    </>
                  ) : (
                    <>
                      <BarChart3 className="h-5 w-5 mr-2" />
                      Calculate ATS Score
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Results */}
          {step === 3 && atsScore && (
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-8 text-center">
                ATS Score Results
              </h2>

              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <div className={`p-6 rounded-lg border-2 ${getScoreBackground(atsScore.total_score)} text-center mb-6`}>
                    <h3 className="text-lg font-medium text-gray-800 mb-2">
                      Overall ATS Score
                    </h3>
                    <div className={`text-4xl font-bold ${getScoreColor(atsScore.total_score)}`}>
                      {atsScore.total_score}%
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium text-gray-800 mb-4">
                      Component Scores
                    </h3>
                    {Object.entries(atsScore.component_scores).map(([component, score]) => (
                      <div key={component} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <span className="font-medium text-gray-700 capitalize">
                          {component.replace('_', ' ')}
                        </span>
                        <span className={`font-bold ${getScoreColor(score)}`}>
                          {score}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">
                    Recommendations
                  </h3>
                  <div className="space-y-3">
                    {atsScore.recommendations.map((recommendation, index) => (
                      <div key={index} className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-yellow-800">{recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex justify-center mt-8">
                <button
                  onClick={resetApp}
                  className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Analyze Another Resume
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

