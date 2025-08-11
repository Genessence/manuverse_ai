import React from 'react';
import { AnalysisResult } from '../types';

interface AnalysisHistoryProps {
  analysisHistory: AnalysisResult[];
  onRerunAnalysis: (query: string) => void;
  onClearHistory: () => void;
}

const AnalysisHistory: React.FC<AnalysisHistoryProps> = ({
  analysisHistory,
  onRerunAnalysis,
  onClearHistory
}) => {
  if (analysisHistory.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">📚 Analysis History</h2>
        <div className="text-center text-gray-500 py-8">
          <p>No analysis history yet. Start by asking questions about your data!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-900">📚 Analysis History</h2>
        <button
          onClick={onClearHistory}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
        >
          Clear History
        </button>
      </div>
      
      <div className="space-y-4">
        {analysisHistory.slice().reverse().map((result, index) => (
          <div key={index} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">{result.query}</h3>
                <p className="text-sm text-gray-600 mt-1">{result.description}</p>
              </div>
              <button
                onClick={() => onRerunAnalysis(result.query)}
                className="ml-4 px-3 py-1 text-sm bg-blue-100 text-blue-700 hover:bg-blue-200 rounded transition-colors"
              >
                Re-run
              </button>
            </div>
            
            <div className="flex justify-between items-center text-xs text-gray-500">
              <span>
                {result.data.length} rows • Chart: {result.chartType}
              </span>
              <span>
                {new Date(result.timestamp).toLocaleString()}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 text-sm text-gray-500 text-center">
        {analysisHistory.length} total analysis{analysisHistory.length !== 1 ? 'es' : ''}
      </div>
    </div>
  );
};

export default AnalysisHistory;
