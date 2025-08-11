export interface FileMetadata {
  filename: string;
  size: number;
  type: string;
  uploadedAt: string;
}

export interface AgentStep {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'error' | 'skipped';
  description: string;
}

export interface AnalysisResult {
  query: string;
  description: string;
  data: Array<{
    name: string;
    value: number;
    [key: string]: any;
  }>;
  chartType: 'bar' | 'line' | 'pie' | 'histogram' | 'table';
  textResult: string;
  timestamp: string;
}

export interface AnalysisHistoryItem {
  id: string;
  query: string;
  result: AnalysisResult;
  timestamp: string;
  hadVisualization: boolean;
}

export interface ColumnMetadata {
  [columnName: string]: 'integer' | 'float' | 'categorical' | 'text' | 'datetime';
}

export interface AnalysisPlan {
  operation: string;
  column: string;
  filters?: any;
  visualization_type: string;
  description: string;
  aggregation_column?: string;
  aggregation_method?: string;
}
