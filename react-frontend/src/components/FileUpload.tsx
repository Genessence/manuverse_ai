import React, { useCallback, useState } from 'react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  loading?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, loading = false }) => {
  const [dragOver, setDragOver] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileUpload(files[0]);
    }
  }, [onFileUpload]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileUpload(files[0]);
    }
  }, [onFileUpload]);

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">📁 File Upload</h2>
      
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragOver
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="space-y-4">
          <div className="text-4xl">📊</div>
          <div>
            <p className="text-gray-600">
              Drag and drop your file here, or{' '}
              <label className="text-blue-600 hover:text-blue-500 cursor-pointer">
                browse
                <input
                  type="file"
                  className="hidden"
                  accept=".csv,.xlsx,.xls,.txt"
                  onChange={handleFileChange}
                />
              </label>
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Supports CSV, Excel (.xlsx, .xls), and text files
            </p>
          </div>
        </div>
      </div>

      {loading && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="loading-spinner"></div>
            <span className="text-blue-800">Uploading file...</span>
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p><strong>💡 Tips:</strong></p>
        <ul className="list-disc list-inside space-y-1 mt-2">
          <li>Upload CSV files for best results</li>
          <li>Ensure your data has clear column headers</li>
          <li>Large files may take longer to process</li>
          <li>The system will automatically detect column types</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload;
