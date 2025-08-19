# Multi-Agent Data Analysis API Backend

This FastAPI backend implements the same multi-agent system as the Streamlit application, providing REST API endpoints for data analysis.

## Architecture

The API maintains the same 5-agent architecture:

1. **File Ingestion Agent** (`APIFileIngestionAgent`) - Handles file uploads and data preprocessing
2. **Query Understanding Agent** (`APIQueryUnderstandingAgent`) - Parses natural language queries into structured plans
3. **Data Analysis Agent** (`APIDataAnalysisAgent`) - Executes pandas operations based on analysis plans
4. **Visualization Agent** (`APIVisualizationAgent`) - Generates matplotlib charts as base64 images
5. **Response Generation Agent** (`APIResponseGenerationAgent`) - Formats results for JSON responses

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
# Using the batch script (Windows)
run_api_backend.bat

# Or manually
uvicorn api_backend:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API
```bash
python test_api_backend.py
```

### 4. Access Documentation
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## API Endpoints

### Core Endpoints

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "message": "Multi-Agent Data Analysis API is running"
}
```

#### `POST /upload-file`
Upload and process data files (CSV, Excel, TXT).

**Parameters:**
- `file`: File upload (multipart/form-data)
- `session_id`: Optional session ID

**Response:**
```json
{
    "session_id": "uuid-string",
    "status": "success",
    "message": "File uploaded successfully",
    "metadata": {
        "filename": "data.csv",
        "rows": 1000,
        "columns": 5,
        "column_types": {
            "column1": "integer",
            "column2": "categorical"
        }
    }
}
```

#### `POST /load-default-data`
Load the default mining process database.

**Parameters:**
- `session_id`: Optional session ID

**Response:**
```json
{
    "session_id": "uuid-string",
    "status": "success",
    "message": "Default mining process database loaded successfully",
    "metadata": { ... }
}
```

#### `POST /analyze-query`
Process natural language queries and return analysis results.

**Request Body:**
```json
{
    "query": "What is the total sales by region?",
    "session_id": "optional-session-id",
    "enable_visualization": true
}
```

**Response:**
```json
{
    "session_id": "uuid-string",
    "status": "completed",
    "analysis_plan": {
        "operation": "groupby",
        "column": "region",
        "aggregation_column": "sales",
        "aggregation_method": "sum",
        "visualization_type": "bar_chart",
        "description": "Sum of sales by region"
    },
    "result": {
        "query": "What is the total sales by region?",
        "description": "Sum of sales by region",
        "chart_image": "base64-encoded-png-image",
        "data": {
            "type": "series",
            "values": {"North": 1000, "South": 1500},
            "formatted": "North    1000\nSouth    1500"
        }
    },
    "message": "Analysis completed successfully"
}
```

### Session Management

#### `GET /session-status/{session_id}`
Get session status and information.

#### `GET /column-metadata/{session_id}`
Get column metadata and types for a session.

#### `GET /analysis-history/{session_id}`
Get analysis history for a session.

#### `DELETE /clear-session/{session_id}`
Clear all data for a session.

#### `GET /sessions`
List all active sessions (debugging endpoint).

## Query Types Supported

The API supports the same natural language queries as the Streamlit app:

### Aggregation Queries
- `"What is the total sales?"` → Sum operation
- `"Show me the average revenue"` → Mean operation
- `"What's the maximum quantity?"` → Max operation
- `"What's the minimum price?"` → Min operation

### Counting Queries
- `"Count the number of customers"` → Count operation
- `"How many records are there?"` → Total count
- `"Count unique products"` → Unique count

### Grouping Queries
- `"Group sales by region"` → GroupBy operation
- `"Show revenue breakdown by product"` → GroupBy with aggregation
- `"Average sales by category"` → GroupBy with mean

### Statistical Queries
- `"Show distribution of ages"` → Statistical summary
- `"Histogram of prices"` → Distribution analysis

### Column-Specific Queries
The API intelligently maps queries to actual column names using:
- Exact matches (case-insensitive)
- Synonym matching
- Partial string matching
- Business term recognition

## Data Types

The API handles the same data types as the Streamlit app:

- **integer**: Numeric columns with whole numbers
- **float**: Numeric columns with decimal numbers
- **categorical**: Text columns with limited unique values
- **text**: General text columns
- **datetime**: Date/time columns

## Visualization

When `enable_visualization: true`, the API generates matplotlib charts and returns them as base64-encoded PNG images. Chart types include:

- **Bar Charts**: For aggregated data, counts, and grouped results
- **Line Charts**: For trends and averages
- **Histograms**: For distributions
- **Text Visualizations**: For summary statistics

## Session Management

The API uses in-memory session storage (use Redis/database for production):

- Each session maintains its own dataset and metadata
- Sessions persist analysis history
- Multiple concurrent sessions supported
- Automatic session creation on first request

## Error Handling

The API provides detailed error messages for:
- Unsupported file formats
- Missing session data
- Invalid queries
- Analysis failures
- Chart generation errors

## Example Usage

### Python Client
```python
import requests
import json

BASE_URL = "http://localhost:8001"

# Load default data
response = requests.post(f"{BASE_URL}/load-default-data")
session_id = response.json()['session_id']

# Analyze query
payload = {
    "query": "What is the total sales by region?",
    "session_id": session_id,
    "enable_visualization": True
}

response = requests.post(f"{BASE_URL}/analyze-query", json=payload)
result = response.json()

print(f"Description: {result['result']['description']}")
print(f"Data: {result['result']['data']}")

# Chart is available as base64 image in result['result']['chart_image']
```

### JavaScript Client
```javascript
const BASE_URL = 'http://localhost:8001';

// Load default data
const loadData = await fetch(`${BASE_URL}/load-default-data`, {
    method: 'POST'
});
const { session_id } = await loadData.json();

// Analyze query
const analyzeQuery = await fetch(`${BASE_URL}/analyze-query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: 'What is the total sales by region?',
        session_id: session_id,
        enable_visualization: true
    })
});

const result = await analyzeQuery.json();
console.log(result.result);
```

## Production Considerations

For production deployment:

1. **Database**: Replace in-memory sessions with Redis/PostgreSQL
2. **Authentication**: Add JWT or API key authentication
3. **Rate Limiting**: Implement request rate limiting
4. **File Storage**: Use cloud storage for uploaded files
5. **Monitoring**: Add logging, metrics, and health checks
6. **Security**: Enable HTTPS, validate file types, sanitize inputs
7. **Scaling**: Use multiple workers, load balancing

## Testing

Run the comprehensive test suite:
```bash
python test_api_backend.py
```

The test suite covers:
- Health checks
- Default data loading
- File uploads
- Query analysis with various patterns
- Session management
- Error handling
- Chart generation

## Compatibility

This API backend maintains 100% functional compatibility with the original Streamlit application, implementing the same:

- Agent architecture and logic
- Query understanding patterns
- Data analysis operations
- Visualization generation
- Column type detection
- Business term recognition
- Error handling strategies

The API can serve as a drop-in replacement for the Streamlit backend, enabling:
- Web applications (React, Vue, Angular)
- Mobile applications
- Desktop applications
- Integration with other systems
- Automated data processing pipelines
