import React from 'react';
import { AgentStep } from '../types';

interface AgentStatusProps {
  steps: AgentStep[];
  loading?: boolean;
}

const AgentStatus: React.FC<AgentStatusProps> = ({ steps }) => {
  const getStatusIcon = (status: AgentStep['status']) => {
    switch (status) {
      case 'completed':
        return <span className="text-green-500">✅</span>;
      case 'running':
        return <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>;
      case 'error':
        return <span className="text-red-500">❌</span>;
      case 'skipped':
        return <span className="text-gray-400">⏭️</span>;
      default:
        return <span className="text-gray-400">⏳</span>;
    }
  };

  const getStatusColor = (status: AgentStep['status']) => {
    switch (status) {
      case 'completed':
        return 'text-green-700 bg-green-50 border-green-200';
      case 'running':
        return 'text-blue-700 bg-blue-50 border-blue-200';
      case 'error':
        return 'text-red-700 bg-red-50 border-red-200';
      default:
        return 'text-gray-500 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border animate-fadeIn">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">🤖 Multi-Agent Processing</h3>
      
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg border transition-all duration-300 ${getStatusColor(step.status)}`}
          >
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                {getStatusIcon(step.status)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">{step.name}</p>
                <p className="text-xs opacity-75">{step.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 text-xs text-gray-500">
        <p>Each agent specializes in a specific aspect of data analysis, working together to provide comprehensive insights.</p>
      </div>
    </div>
  );
};

export default AgentStatus;
