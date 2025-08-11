"""
Multi-Agent Data Analysis API Backend

This module provides FastAPI endpoints for the React frontend to communicate with
the multi-agent data analysis system.

Endpoints:
- POST /upload: Upload and process data files
- POST /analyze: Analyze data with natural language queries
- GET /status: Get current analysis status
- GET /history: Get analysis history
- DELETE /history: Clear analysis history
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import json
import io
import tempfile
import os
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
import asyncio
import logging

# Import the original multi-agent classes
from multi_agent_data_analysis import (
    FileIngestionAgent, 
    QueryUnderstandingAgent, 
    DataAnalysisAgent,
    VisualizationAgent,
    ResponseGenerationAgent
)

# API-specific agent wrappers
class APIQueryUnderstandingAgent:
    """API wrapper for QueryUnderstandingAgent"""
    
    @staticmethod
    def understand_query(query: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Convert query to analysis plan"""
        # Get column metadata
        metadata = FileIngestionAgent.get_column_metadata(data)
        # Parse the query using the original agent
        plan = QueryUnderstandingAgent.parse_query(query, metadata)
        return plan

class APIDataAnalysisAgent:
    """API wrapper for DataAnalysisAgent"""
    
    @staticmethod
    def execute_analysis(data: pd.DataFrame, plan: Dict[str, Any]) -> Any:
        """Execute analysis and return result"""
        result, description = DataAnalysisAgent.execute_analysis(data, plan)
        return result

class APIVisualizationAgent:
    """API wrapper for VisualizationAgent"""
    
    @staticmethod
    def generate_chart(result: Any, plan: Dict[str, Any]) -> str:
        """Generate chart code"""
        chart_type = plan.get('visualization_type', 'bar_chart')
        description = plan.get('description', 'Chart')
        query = plan.get('description', '')
        return VisualizationAgent.generate_chart_code(query, result, chart_type, description)

class APIResponseGenerationAgent:
    """API wrapper for ResponseGenerationAgent"""
    
    @staticmethod
    def generate_response(query: str, result: Any, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate formatted response"""
        description = plan.get('description', 'Analysis completed')
        
        # Format result for display
        if isinstance(result, pd.Series):
            detailed_response = result.to_string()
        elif isinstance(result, pd.DataFrame):
            detailed_response = result.to_string()
        else:
            detailed_response = str(result)
        
        return {
            "summary": description,
            "detailed_response": detailed_response
        }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="Multi-Agent Data Analysis API",
    description="API for multi-agent data analysis system",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state management
current_data: Optional[pd.DataFrame] = None
analysis_history: List[Dict[str, Any]] = []
current_analysis_status: Dict[str, Any] = {"status": "idle", "steps": []}
analysis_sessions: Dict[str, Dict[str, Any]] = {}

# Load default mining dataset
DEFAULT_DATA_PATH = "MiningProcess_Flotation_Plant_Database.csv"

def load_default_data():
    """Load the default mining dataset"""
    global current_data
    try:
        if os.path.exists(DEFAULT_DATA_PATH):
            current_data = pd.read_csv(DEFAULT_DATA_PATH)
            logger.info(f"Loaded default dataset with {len(current_data)} rows")
            return True
    except Exception as e:
        logger.error(f"Failed to load default data: {e}")
    return False

# Load default data on startup
load_default_data()

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Multi-Agent Data Analysis API starting up...")
    if current_data is not None:
        logger.info(f"Default dataset loaded: {current_data.shape}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Multi-Agent Data Analysis API",
        "status": "running",
        "version": "1.0.0",
        "data_loaded": current_data is not None,
        "data_shape": current_data.shape if current_data is not None else None
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a data file"""
    global current_data, current_analysis_status
    
    try:
        # Update status
        current_analysis_status = {
            "status": "processing",
            "steps": [
                {"name": "File Ingestion", "status": "running", "message": "Processing uploaded file..."}
            ]
        }
        
        # Read file content
        content = await file.read()
        
        # Create a file-like object
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Validate data
        if df.empty:
            raise HTTPException(status_code=400, detail="File is empty")
        
        current_data = df
        
        # Update status
        current_analysis_status = {
            "status": "completed",
            "steps": [
                {"name": "File Ingestion", "status": "completed", "message": "File processed successfully"}
            ]
        }
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "shape": df.shape,
            "columns": list(df.columns),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample_data": df.head().to_dict('records')
        }
        
    except Exception as e:
        current_analysis_status = {
            "status": "error",
            "steps": [
                {"name": "File Ingestion", "status": "error", "message": str(e)}
            ]
        }
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_data(request_data: Dict[str, Any], background_tasks: BackgroundTasks):
    """Analyze data with natural language query"""
    global current_data, analysis_history
    
    if current_data is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload a file first.")
    
    query = request_data.get("query", "").strip()
    enable_visualization = request_data.get("enableVisualization", True)
    
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Start background analysis
    background_tasks.add_task(run_analysis, session_id, query, enable_visualization)
    
    return {
        "session_id": session_id,
        "message": "Analysis started",
        "query": query
    }

async def run_analysis(session_id: str, query: str, enable_visualization: bool):
    """Run the multi-agent analysis in background"""
    global current_data, analysis_history, current_analysis_status, analysis_sessions
    
    try:
        # Initialize analysis status
        analysis_sessions[session_id] = {
            "status": "running",
            "query": query,
            "steps": [
                {"name": "Query Understanding", "status": "pending", "message": ""},
                {"name": "Data Analysis", "status": "pending", "message": ""},
                {"name": "Visualization", "status": "pending", "message": ""},
                {"name": "Response Generation", "status": "pending", "message": ""}
            ],
            "result": None
        }
        
        current_analysis_status = analysis_sessions[session_id]
        
        # Step 1: Query Understanding
        current_analysis_status["steps"][0] = {
            "name": "Query Understanding", 
            "status": "running", 
            "message": "Analyzing your question..."
        }
        await asyncio.sleep(0.5)  # Simulate processing time
        
        analysis_plan = APIQueryUnderstandingAgent.understand_query(query, current_data)
        
        current_analysis_status["steps"][0] = {
            "name": "Query Understanding", 
            "status": "completed", 
            "message": "Query understood successfully"
        }
        
        # Step 2: Data Analysis
        current_analysis_status["steps"][1] = {
            "name": "Data Analysis", 
            "status": "running", 
            "message": "Processing data..."
        }
        await asyncio.sleep(0.5)
        
        analysis_result = APIDataAnalysisAgent.execute_analysis(current_data, analysis_plan)
        
        current_analysis_status["steps"][1] = {
            "name": "Data Analysis", 
            "status": "completed", 
            "message": "Data analysis completed"
        }
        
        # Step 3: Visualization (if enabled)
        chart_data = None
        chart_type = "bar"
        
        if enable_visualization:
            current_analysis_status["steps"][2] = {
                "name": "Visualization", 
                "status": "running", 
                "message": "Creating visualization..."
            }
            await asyncio.sleep(0.5)
            
            chart_code = APIVisualizationAgent.generate_chart(analysis_result, analysis_plan)
            chart_type = analysis_plan.get('chart_type', 'bar')
            
            # Convert analysis_result to chart data format
            if isinstance(analysis_result, pd.DataFrame) and not analysis_result.empty:
                # Take first 20 rows for visualization
                viz_data = analysis_result.head(20)
                if len(viz_data.columns) >= 2:
                    chart_data = []
                    for _, row in viz_data.iterrows():
                        chart_data.append({
                            "name": str(row.iloc[0]),
                            "value": float(row.iloc[1]) if pd.api.types.is_numeric_dtype(row.iloc[1]) else 1
                        })
                else:
                    # Single column data
                    value_counts = viz_data.iloc[:, 0].value_counts().head(10)
                    chart_data = [{"name": str(k), "value": int(v)} for k, v in value_counts.items()]
            
            current_analysis_status["steps"][2] = {
                "name": "Visualization", 
                "status": "completed", 
                "message": "Visualization created"
            }
        else:
            current_analysis_status["steps"][2] = {
                "name": "Visualization", 
                "status": "skipped", 
                "message": "Visualization disabled"
            }
        
        # Step 4: Response Generation
        current_analysis_status["steps"][3] = {
            "name": "Response Generation", 
            "status": "running", 
            "message": "Formatting results..."
        }
        await asyncio.sleep(0.5)
        
        formatted_response = APIResponseGenerationAgent.generate_response(
            query, analysis_result, analysis_plan
        )
        
        current_analysis_status["steps"][3] = {
            "name": "Response Generation", 
            "status": "completed", 
            "message": "Response generated"
        }
        
        # Prepare final result
        result = {
            "query": query,
            "description": formatted_response.get("summary", "Analysis completed"),
            "textResult": formatted_response.get("detailed_response", str(analysis_result)),
            "data": chart_data or [],
            "chartType": chart_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update session result
        analysis_sessions[session_id]["result"] = result
        analysis_sessions[session_id]["status"] = "completed"
        current_analysis_status["status"] = "completed"
        
        # Add to history
        analysis_history.append(result)
        
        logger.info(f"Analysis completed for session {session_id}")
        
    except Exception as e:
        logger.error(f"Analysis error for session {session_id}: {e}")
        error_step = "Data Analysis"  # Default to data analysis step for errors
        
        for i, step in enumerate(current_analysis_status["steps"]):
            if step["status"] == "running":
                current_analysis_status["steps"][i] = {
                    "name": step["name"],
                    "status": "error",
                    "message": str(e)
                }
                error_step = step["name"]
                break
        
        analysis_sessions[session_id]["status"] = "error"
        analysis_sessions[session_id]["error"] = str(e)
        current_analysis_status["status"] = "error"

@app.get("/status/{session_id}")
async def get_analysis_status(session_id: str):
    """Get analysis status for a specific session"""
    if session_id in analysis_sessions:
        return analysis_sessions[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/status")
async def get_current_status():
    """Get current analysis status"""
    return current_analysis_status

@app.get("/history")
async def get_analysis_history():
    """Get analysis history"""
    return {
        "history": analysis_history,
        "total": len(analysis_history)
    }

@app.delete("/history")
async def clear_analysis_history():
    """Clear analysis history"""
    global analysis_history
    analysis_history = []
    return {"message": "Analysis history cleared"}

@app.get("/data/info")
async def get_data_info():
    """Get information about currently loaded data"""
    global current_data
    
    if current_data is None:
        return {"data_loaded": False}
    
    return {
        "data_loaded": True,
        "shape": current_data.shape,
        "columns": list(current_data.columns),
        "data_types": {col: str(dtype) for col, dtype in current_data.dtypes.items()},
        "sample_data": current_data.head().to_dict('records'),
        "missing_values": current_data.isnull().sum().to_dict(),
        "numeric_columns": list(current_data.select_dtypes(include=[np.number]).columns),
        "categorical_columns": list(current_data.select_dtypes(include=['object']).columns)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
