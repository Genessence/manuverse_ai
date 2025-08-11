import React, { useState } from 'react';
import { FileMetadata } from '../types';

interface QueryInterfaceProps {
  onQuerySubmit: (query: string) => void;
  loading?: boolean;
  fileMetadata: FileMetadata | null;
}

const QueryInterface: React.FC<QueryInterfaceProps> = ({ 
  onQuerySubmit, 
  loading = false, 
  fileMetadata
}) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onQuerySubmit(query.trim());
    }
  };

  const sampleQueries = [
    "What are the top 5 values in the dataset?",
    "Show me the distribution of values",
    "Calculate the average of all numeric columns",
    "Find outliers in the data",
    "Show correlations between columns",
    "What is the data summary?",
    "Create a visualization of the main trends",
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">🤖 Ask Your Question</h2>
      
      {fileMetadata && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-800">
            ✅ Data loaded: <strong>{fileMetadata.filename}</strong>
          </p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
            What would you like to know about your data?
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask any question about your data in natural language..."
            className="input-primary min-h-[100px] resize-y"
            disabled={loading}
          />
        </div>
        
        <div className="flex space-x-3">
          <button
            type="submit"
            disabled={!query.trim() || loading}
            className={`btn-primary flex-1 ${
              (!query.trim() || loading) ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            {loading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="loading-spinner"></div>
                <span>Analyzing...</span>
              </div>
            ) : (
              'Analyze Data'
            )}
          </button>
        </div>
      </form>

      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">💡 Sample Questions:</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {sampleQueries.map((sampleQuery, index) => (
            <button
              key={index}
              onClick={() => setQuery(sampleQuery)}
              disabled={loading}
              className="p-2 text-left text-sm bg-gray-50 hover:bg-gray-100 rounded border text-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {sampleQuery}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="text-sm font-medium text-blue-900 mb-2">🎯 Tips for Better Results:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Be specific about what you want to analyze</li>
          <li>• Ask about specific columns by name if you know them</li>
          <li>• Request visualizations like "show me a chart of..."</li>
          <li>• Ask for comparisons between different data segments</li>
        </ul>
      </div>
    </div>
  );
};

export default QueryInterface;
