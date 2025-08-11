import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import QueryInterface from './components/QueryInterface';
import AgentStatus from './components/AgentStatus';
import AnalysisResults from './components/AnalysisResults';
import AnalysisHistory from './components/AnalysisHistory';
import { AnalysisResult, AgentStep, FileMetadata } from './types';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  // State management
  const [currentStep, setCurrentStep] = useState<'upload' | 'query' | 'analysis' | 'results'>('upload');
  const [fileMetadata, setFileMetadata] = useState<FileMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enableVisualization, setEnableVisualization] = useState(true);
  
  // Analysis state
  const [agentSteps, setAgentSteps] = useState<AgentStep[]>([]);
  const [currentResult, setCurrentResult] = useState<AnalysisResult | null>(null);
  const [analysisHistory, setAnalysisHistory] = useState<AnalysisResult[]>([]);

  // Load analysis history on component mount
  useEffect(() => {
    loadAnalysisHistory();
    checkDataStatus();
  }, []);

  const checkDataStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/data/info`);
      if (response.data.data_loaded) {
        setCurrentStep('query');
        setFileMetadata({
          filename: 'Default Mining Dataset',
          size: 0,
          type: 'text/csv',
          uploadedAt: new Date().toISOString()
        });
      }
    } catch (err) {
      console.log('No default data loaded');
    }
  };

  const loadAnalysisHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/history`);
      setAnalysisHistory(response.data.history || []);
    } catch (err) {
      console.error('Failed to load analysis history:', err);
    }
  };

  const handleFileUpload = useCallback(async (file: File) => {
    try {
      setLoading(true);
      setError(null);
      
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const metadata: FileMetadata = {
        filename: response.data.filename,
        size: file.size,
        type: file.type,
        uploadedAt: new Date().toISOString()
      };
      
      setFileMetadata(metadata);
      setCurrentStep('query');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleQuerySubmit = useCallback(async (query: string) => {
    try {
      setLoading(true);
      setError(null);
      setCurrentStep('analysis');
      
      // Clear previous results for conversational flow
      setCurrentResult(null);
      setAgentSteps([]);
      
      // Start analysis
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        query,
        enableVisualization
      });
      
      const sessionId = response.data.session_id;
      
      // Poll for status updates
      const pollInterval = setInterval(async () => {
        try {
          const statusResponse = await axios.get(`${API_BASE_URL}/status/${sessionId}`);
          const sessionData = statusResponse.data;
          
          // Convert API steps to AgentStep format
          const steps: AgentStep[] = sessionData.steps.map((step: any) => ({
            name: step.name,
            status: step.status,
            description: step.message || step.name
          }));
          
          setAgentSteps(steps);
          
          if (sessionData.status === 'completed' && sessionData.result) {
            clearInterval(pollInterval);
            setCurrentResult(sessionData.result);
            setCurrentStep('results');
            setLoading(false);
            await loadAnalysisHistory();
            
            // Auto return to query step after 3 seconds for conversational flow
            setTimeout(() => {
              setCurrentStep('query');
              setCurrentResult(null);
              setAgentSteps([]);
            }, 5000);
            
          } else if (sessionData.status === 'error') {
            clearInterval(pollInterval);
            setError(sessionData.error || 'Analysis failed');
            setLoading(false);
            
            // Return to query step after error
            setTimeout(() => {
              setCurrentStep('query');
              setError(null);
            }, 3000);
          }
        } catch (err) {
          console.error('Failed to fetch status:', err);
        }
      }, 1000);
      
      // Clear interval after 60 seconds to prevent indefinite polling
      setTimeout(() => {
        clearInterval(pollInterval);
        if (loading) {
          setError('Analysis timeout - please try again');
          setLoading(false);
          // Return to query step after timeout
          setTimeout(() => {
            setCurrentStep('query');
            setError(null);
          }, 3000);
        }
      }, 60000);
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start analysis');
      setLoading(false);
      
      // Return to query step after error
      setTimeout(() => {
        setCurrentStep('query');
        setError(null);
      }, 3000);
    }
  }, [enableVisualization, loading]);

  const handleAskAnotherQuestion = useCallback(() => {
    setCurrentStep('query');
    setCurrentResult(null);
    setAgentSteps([]);
    setError(null);
  }, []);

  const handleRerunAnalysis = useCallback((query: string) => {
    handleQuerySubmit(query);
  }, [handleQuerySubmit]);

  const handleClearHistory = useCallback(async () => {
    try {
      await axios.delete(`${API_BASE_URL}/history`);
      setAnalysisHistory([]);
    } catch (err) {
      console.error('Failed to clear history:', err);
    }
  }, []);

  const handleStartOver = useCallback(() => {
    setCurrentStep('upload');
    setFileMetadata(null);
    setCurrentResult(null);
    setAgentSteps([]);
    setError(null);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">🤖</span>
                <h1 className="text-2xl font-bold text-gray-900">Multi-Agent Data Analysis</h1>
              </div>
              
              {fileMetadata && (
                <div className="text-sm text-gray-500">
                  📁 {fileMetadata.filename}
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2 text-sm">
                <input
                  type="checkbox"
                  checked={enableVisualization}
                  onChange={(e) => setEnableVisualization(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span>Enable Visualizations</span>
              </label>
              
              {currentStep !== 'upload' && (
                <button
                  onClick={handleStartOver}
                  className="btn-secondary"
                >
                  Start Over
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center space-x-2">
              <span className="text-red-500">❌</span>
              <span className="text-red-800 font-medium">Error</span>
            </div>
            <p className="text-red-700 mt-1">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {currentStep === 'upload' && (
              <FileUpload 
                onFileUpload={handleFileUpload}
                loading={loading}
              />
            )}
            
            {currentStep === 'query' && (
              <QueryInterface 
                onQuerySubmit={handleQuerySubmit}
                loading={loading}
                fileMetadata={fileMetadata}
              />
            )}
            
            {currentStep === 'analysis' && (
              <AgentStatus 
                steps={agentSteps}
                loading={loading}
              />
            )}
            
            {currentStep === 'results' && currentResult && (
              <div className="space-y-4">
                <AnalysisResults 
                  result={currentResult}
                  enableVisualization={enableVisualization}
                />
                
                {/* Conversational flow - Ask Another Question */}
                <div className="bg-white p-6 rounded-lg shadow-sm border">
                  <div className="text-center">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      💬 Ready for another question?
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Ask me anything else about your data!
                    </p>
                    <button
                      onClick={handleAskAnotherQuestion}
                      className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium"
                    >
                      Ask Another Question
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <AnalysisHistory 
              analysisHistory={analysisHistory}
              onRerunAnalysis={handleRerunAnalysis}
              onClearHistory={handleClearHistory}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            Multi-Agent Data Analysis System • Powered by AI
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
