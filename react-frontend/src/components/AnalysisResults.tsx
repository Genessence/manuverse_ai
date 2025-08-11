import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { AnalysisResult } from '../types';

interface AnalysisResultsProps {
  result: AnalysisResult;
  enableVisualization: boolean;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result, enableVisualization }) => {
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

  const renderChart = () => {
    if (!enableVisualization) return null;

    switch (result.chartType) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={result.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        );
      
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={result.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        );
      
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={result.data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {result.data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      
      default:
        return (
          <div className="p-8 text-center text-gray-500">
            <p>Chart type not supported: {result.chartType}</p>
          </div>
        );
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border animate-fadeIn">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">📊 Analysis Results</h2>
      
      <div className="space-y-6">
        {/* Query and Description */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-blue-900 mb-2">Your Query</h3>
          <p className="text-blue-800">{result.query}</p>
        </div>

        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-green-900 mb-2">Finding</h3>
          <p className="text-green-800">{result.description}</p>
        </div>

        {/* Text Results */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Details</h3>
          <div className="text-gray-700 whitespace-pre-wrap">{result.textResult}</div>
        </div>

        {/* Chart */}
        {enableVisualization ? (
          <div className="bg-white border rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Visualization</h3>
            {renderChart()}
          </div>
        ) : (
          <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600">📈</span>
              <span className="text-yellow-800 font-medium">Visualization disabled</span>
            </div>
            <p className="text-yellow-700 text-sm mt-1">
              Enable visualizations in the header to see charts for your data!
            </p>
          </div>
        )}

        {/* Data Table */}
        <div className="bg-white border rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Raw Data</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {Object.keys(result.data[0] || {}).map((key) => (
                    <th
                      key={key}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {result.data.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, cellIndex) => (
                      <td
                        key={cellIndex}
                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                      >
                        {typeof value === 'number' ? value.toLocaleString() : String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Metadata */}
        <div className="text-sm text-gray-500 border-t pt-4">
          <p>Analysis completed at: {new Date(result.timestamp).toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
