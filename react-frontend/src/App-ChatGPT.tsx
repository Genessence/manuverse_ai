import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import AgentStatus from './components/AgentStatus';
import AnalysisResults from './components/AnalysisResults';
import { AnalysisResult, AgentStep, FileMetadata } from './types';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'thinking';
  content: string;
  result?: AnalysisResult;
  steps?: AgentStep[];
  timestamp: string;
}

function App() {
  // State management
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentStep, setCurrentStep] = useState<'upload' | 'chat'>('upload');
  const [fileMetadata, setFileMetadata] = useState<FileMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enableVisualization, setEnableVisualization] = useState(true);
  
  // Chat state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [analysisHistory, setAnalysisHistory] = useState<AnalysisResult[]>([]);
  const [currentInput, setCurrentInput] = useState('');

  // Load analysis history on component mount
  useEffect(() => {
    loadAnalysisHistory();
    checkDataStatus();
  }, []);

  const checkDataStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/data/info`);
      if (response.data.data_loaded) {
        setCurrentStep('chat');
        setFileMetadata({
          filename: 'Default Mining Dataset',
          size: 0,
          type: 'text/csv',
          uploadedAt: new Date().toISOString()
        });
        // Add welcome message
        const welcomeMessage: ChatMessage = {
          id: 'welcome',
          type: 'assistant',
          content: `👋 Hi! I'm your AI data analyst. I have loaded the **${response.data.shape[0].toLocaleString()} rows** mining dataset with **${response.data.shape[1]} columns**. What would you like to explore?`,
          timestamp: new Date().toISOString()
        };
        setChatMessages([welcomeMessage]);
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
      setCurrentStep('chat');
      
      // Add file upload success message
      const uploadMessage: ChatMessage = {
        id: `upload-${Date.now()}`,
        type: 'assistant',
        content: `✅ **${file.name}** uploaded successfully!\n\n**${response.data.shape[0].toLocaleString()}** rows and **${response.data.shape[1]}** columns detected. What would you like to analyze?`,
        timestamp: new Date().toISOString()
      };
      setChatMessages([uploadMessage]);
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleQuerySubmit = useCallback(async (query: string) => {
    if (!query.trim() || loading) return;
    
    try {
      setLoading(true);
      setError(null);
      setCurrentInput('');
      
      // Add user message
      const userMessage: ChatMessage = {
        id: `user-${Date.now()}`,
        type: 'user',
        content: query,
        timestamp: new Date().toISOString()
      };
      
      // Add thinking message
      const thinkingMessage: ChatMessage = {
        id: `thinking-${Date.now()}`,
        type: 'thinking',
        content: 'Analyzing your question...',
        steps: [],
        timestamp: new Date().toISOString()
      };
      
      setChatMessages(prev => [...prev, userMessage, thinkingMessage]);
      
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
          
          // Update thinking message with steps
          setChatMessages(prev => 
            prev.map(msg => 
              msg.id === thinkingMessage.id 
                ? { ...msg, steps }
                : msg
            )
          );
          
          if (sessionData.status === 'completed' && sessionData.result) {
            clearInterval(pollInterval);
            
            // Replace thinking message with result
            const resultMessage: ChatMessage = {
              id: `result-${Date.now()}`,
              type: 'assistant',
              content: sessionData.result.description || 'Analysis completed',
              result: sessionData.result,
              timestamp: new Date().toISOString()
            };
            
            setChatMessages(prev => 
              prev.filter(msg => msg.id !== thinkingMessage.id).concat(resultMessage)
            );
            
            setLoading(false);
            await loadAnalysisHistory();
            
          } else if (sessionData.status === 'error') {
            clearInterval(pollInterval);
            
            // Replace thinking message with error
            const errorMessage: ChatMessage = {
              id: `error-${Date.now()}`,
              type: 'assistant',
              content: `❌ Sorry, I encountered an error: ${sessionData.error || 'Analysis failed'}`,
              timestamp: new Date().toISOString()
            };
            
            setChatMessages(prev => 
              prev.filter(msg => msg.id !== thinkingMessage.id).concat(errorMessage)
            );
            
            setLoading(false);
          }
        } catch (err) {
          console.error('Failed to fetch status:', err);
        }
      }, 1000);
      
      // Clear interval after 60 seconds
      setTimeout(() => {
        clearInterval(pollInterval);
        if (loading) {
          const timeoutMessage: ChatMessage = {
            id: `timeout-${Date.now()}`,
            type: 'assistant',
            content: '⏱️ Analysis timeout - please try again with a simpler query.',
            timestamp: new Date().toISOString()
          };
          
          setChatMessages(prev => 
            prev.filter(msg => msg.id !== thinkingMessage.id).concat(timeoutMessage)
          );
          
          setLoading(false);
        }
      }, 60000);
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start analysis');
      setLoading(false);
    }
  }, [enableVisualization, loading]);

  const handleNewChat = useCallback(() => {
    setChatMessages([]);
    setError(null);
    
    if (fileMetadata) {
      const welcomeMessage: ChatMessage = {
        id: `welcome-${Date.now()}`,
        type: 'assistant',
        content: `👋 Hi! I'm ready to help you analyze your data. What would you like to explore?`,
        timestamp: new Date().toISOString()
      };
      setChatMessages([welcomeMessage]);
    }
  }, [fileMetadata]);

  const handleClearHistory = useCallback(async () => {
    try {
      await axios.delete(`${API_BASE_URL}/history`);
      setAnalysisHistory([]);
    } catch (err) {
      console.error('Failed to clear history:', err);
    }
  }, []);

  const renderMessage = (message: ChatMessage) => {
    const isUser = message.type === 'user';
    
    return (
      <div key={message.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
        <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-semibold ${
              isUser ? 'bg-blue-600' : 'bg-green-600'
            }`}>
              {isUser ? 'U' : '🤖'}
            </div>
          </div>
          
          {/* Message Content */}
          <div className={`rounded-lg px-4 py-2 ${
            isUser 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-100 text-gray-900 border'
          }`}>
            {message.type === 'thinking' ? (
              <div>
                <div className="flex items-center space-x-2 mb-2">
                  <div className="animate-spin h-4 w-4 border-2 border-gray-400 border-t-transparent rounded-full"></div>
                  <span className="text-gray-600">{message.content}</span>
                </div>
                {message.steps && message.steps.length > 0 && (
                  <AgentStatus steps={message.steps} loading={loading} />
                )}
              </div>
            ) : (
              <div>
                <div className="prose prose-sm max-w-none" 
                     dangerouslySetInnerHTML={{ __html: message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>') }} 
                />
                
                {message.result && (
                  <div className="mt-4">
                    <AnalysisResults 
                      result={message.result}
                      enableVisualization={enableVisualization}
                    />
                  </div>
                )}
              </div>
            )}
            
            {/* Timestamp */}
            <div className={`text-xs mt-1 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-gray-900 text-white transition-all duration-300 overflow-hidden flex flex-col`}>
        {/* Sidebar Header */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Chat History</h2>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-400 hover:text-white"
            >
              {sidebarOpen ? '←' : '→'}
            </button>
          </div>
        </div>
        
        {/* New Chat Button */}
        <div className="p-4">
          <button
            onClick={handleNewChat}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            ➕ New Chat
          </button>
        </div>
        
        {/* History List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {analysisHistory.slice().reverse().map((item, index) => (
            <div 
              key={`${item.timestamp}-${index}`}
              className="p-3 rounded-lg bg-gray-800 hover:bg-gray-700 cursor-pointer transition-colors"
              onClick={() => {
                const userMessage: ChatMessage = {
                  id: `history-user-${Date.now()}`,
                  type: 'user',
                  content: item.query,
                  timestamp: item.timestamp
                };
                const resultMessage: ChatMessage = {
                  id: `history-result-${Date.now()}`,
                  type: 'assistant',
                  content: item.description,
                  result: item,
                  timestamp: item.timestamp
                };
                setChatMessages([userMessage, resultMessage]);
              }}
            >
              <div className="text-sm text-gray-300 truncate">
                {item.query}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {new Date(item.timestamp).toLocaleDateString()}
              </div>
            </div>
          ))}
          
          {analysisHistory.length === 0 && (
            <div className="text-gray-500 text-center py-8">
              No chat history yet
            </div>
          )}
        </div>
        
        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-700 space-y-2">
          <button
            onClick={handleClearHistory}
            className="w-full text-gray-400 hover:text-white text-sm py-2 transition-colors"
          >
            🗑️ Clear History
          </button>
          
          <div className="flex items-center space-x-2 text-xs">
            <input
              type="checkbox"
              id="viz-toggle"
              checked={enableVisualization}
              onChange={(e) => setEnableVisualization(e.target.checked)}
              className="rounded"
            />
            <label htmlFor="viz-toggle" className="text-gray-400">
              Enable Visualizations
            </label>
          </div>
        </div>
      </div>
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {!sidebarOpen && (
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="text-gray-600 hover:text-gray-900"
                >
                  ☰
                </button>
              )}
              <h1 className="text-xl font-semibold text-gray-900">
                🤖 AI Data Analyst
              </h1>
              {fileMetadata && (
                <span className="text-sm text-gray-500">
                  • {fileMetadata.filename}
                </span>
              )}
            </div>
            
            {currentStep === 'chat' && (
              <button
                onClick={() => setCurrentStep('upload')}
                className="text-sm text-gray-600 hover:text-gray-900 border border-gray-300 px-3 py-1 rounded"
              >
                Upload New File
              </button>
            )}
          </div>
        </header>
        
        {/* Chat Messages */}
        {currentStep === 'upload' ? (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="max-w-md w-full">
              <FileUpload 
                onFileUpload={handleFileUpload}
                loading={loading}
              />
            </div>
          </div>
        ) : (
          <>
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6">
              {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="text-red-800">{error}</div>
                </div>
              )}
              
              {chatMessages.map(renderMessage)}
              
              {chatMessages.length === 0 && !loading && (
                <div className="text-center text-gray-500 py-12">
                  <div className="text-6xl mb-4">🤖</div>
                  <h3 className="text-xl font-semibold mb-2">Ready to analyze your data!</h3>
                  <p>Ask me anything about your dataset and I'll provide detailed insights.</p>
                </div>
              )}
            </div>
            
            {/* Input Area */}
            <div className="border-t border-gray-200 bg-white p-4">
              <div className="max-w-4xl mx-auto">
                <form onSubmit={(e) => {
                  e.preventDefault();
                  handleQuerySubmit(currentInput);
                }} className="flex space-x-4">
                  <input
                    type="text"
                    value={currentInput}
                    onChange={(e) => setCurrentInput(e.target.value)}
                    placeholder="Ask anything about your data..."
                    disabled={loading}
                    className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 disabled:bg-gray-100"
                  />
                  <button
                    type="submit"
                    disabled={!currentInput.trim() || loading}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {loading ? '⏳' : '→'}
                  </button>
                </form>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
