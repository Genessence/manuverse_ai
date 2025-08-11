"""
Test Script for Multi-Agent Data Analysis API Backend

This script tests all the API endpoints to ensure they work correctly
with the same logic and functionality as the Streamlit application.

Run this after starting the API server with: python run_api_backend.bat

Author: AI Assistant
Date: August 12, 2025
"""

import requests
import json
import base64
import io
from PIL import Image
import pandas as pd

# API Base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_load_default_data():
    """Test loading default mining data"""
    print("\n🏭 Testing default data loading...")
    response = requests.post(f"{BASE_URL}/load-default-data")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success: {data['message']}")
        print(f"Session ID: {data['session_id']}")
        print(f"Rows: {data['metadata']['rows']:,}")
        print(f"Columns: {data['metadata']['columns']}")
        return data['session_id']
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

def test_session_status(session_id):
    """Test session status endpoint"""
    print(f"\n📊 Testing session status for {session_id}...")
    response = requests.get(f"{BASE_URL}/session-status/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"Data loaded: {data['data_loaded']}")
        print(f"Using default data: {data['using_default_data']}")
        print(f"Current file: {data['current_file']}")
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def test_column_metadata(session_id):
    """Test column metadata endpoint"""
    print(f"\n📋 Testing column metadata for {session_id}...")
    response = requests.get(f"{BASE_URL}/column-metadata/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['column_metadata'])} columns")
        print("Numeric columns:", data['columns_by_type']['numeric'][:3])
        print("Categorical columns:", data['columns_by_type']['categorical'][:3])
        return data['columns_by_type']
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None

def test_query_analysis(session_id, test_queries):
    """Test query analysis with various queries"""
    print(f"\n💬 Testing query analysis for {session_id}...")
    
    results = []
    for i, query in enumerate(test_queries):
        print(f"\nQuery {i+1}: {query}")
        
        payload = {
            "query": query,
            "session_id": session_id,
            "enable_visualization": True
        }
        
        response = requests.post(f"{BASE_URL}/analyze-query", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"Description: {data['result']['description']}")
            print(f"Data type: {data['result']['data']['type']}")
            
            # Check if chart was generated
            if data['result']['chart_image']:
                print("📊 Chart generated successfully")
                # Optionally save chart image
                try:
                    chart_data = base64.b64decode(data['result']['chart_image'])
                    with open(f"test_chart_{i+1}.png", "wb") as f:
                        f.write(chart_data)
                    print(f"💾 Chart saved as test_chart_{i+1}.png")
                except Exception as e:
                    print(f"⚠️ Could not save chart: {e}")
            else:
                print("📈 No chart generated")
            
            results.append({
                'query': query,
                'success': True,
                'result': data['result']
            })
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            results.append({
                'query': query,
                'success': False,
                'error': response.text
            })
    
    return results

def test_analysis_history(session_id):
    """Test analysis history endpoint"""
    print(f"\n📚 Testing analysis history for {session_id}...")
    response = requests.get(f"{BASE_URL}/analysis-history/{session_id}")
    if response.status_code == 200:
        data = response.json()
        history_count = len(data['history'])
        print(f"✅ Found {history_count} analysis entries in history")
        
        if history_count > 0:
            last_analysis = data['history'][-1]
            print(f"Last query: {last_analysis['query']}")
            print(f"Timestamp: {last_analysis['timestamp']}")
        
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def test_upload_file():
    """Test file upload functionality"""
    print("\n📁 Testing file upload...")
    
    # Create a sample CSV file
    sample_data = pd.DataFrame({
        'Product': ['A', 'B', 'C', 'A', 'B'] * 20,
        'Sales': [100, 200, 150, 300, 250] * 20,
        'Region': ['North', 'South', 'East', 'West', 'North'] * 20,
        'Date': pd.date_range('2024-01-01', periods=100, freq='D')
    })
    
    # Save to temporary CSV
    csv_buffer = io.StringIO()
    sample_data.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue().encode('utf-8')
    
    files = {
        'file': ('test_data.csv', io.BytesIO(csv_content), 'text/csv')
    }
    
    response = requests.post(f"{BASE_URL}/upload-file", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ File uploaded successfully")
        print(f"Session ID: {data['session_id']}")
        print(f"Rows: {data['metadata']['rows']}")
        print(f"Columns: {data['metadata']['columns']}")
        return data['session_id']
    else:
        print(f"❌ Upload failed: {response.status_code} - {response.text}")
        return None

def test_list_sessions():
    """Test list sessions endpoint"""
    print("\n📝 Testing list sessions...")
    response = requests.get(f"{BASE_URL}/sessions")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} active sessions")
        for session in data['sessions']:
            print(f"  - {session['session_id'][:8]}... ({session['status']}) - {session['analysis_count']} analyses")
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Multi-Agent Data Analysis API Test Suite")
    print("=" * 60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("❌ Health check failed. Is the API server running?")
        return
    
    # Test 2: Load Default Data
    session_id = test_load_default_data()
    if not session_id:
        print("❌ Could not load default data. Trying file upload...")
        session_id = test_upload_file()
        if not session_id:
            print("❌ Could not create session with data. Aborting tests.")
            return
    
    # Test 3: Session Status
    test_session_status(session_id)
    
    # Test 4: Column Metadata
    column_types = test_column_metadata(session_id)
    
    # Test 5: Query Analysis with various queries
    test_queries = [
        "What is the total sales?",
        "Show me the average quantity",
        "Count the number of records",
        "Group sales by region",
        "What's the maximum value?",
        "Show unique products",
        "Distribution of sales"
    ]
    
    # Use mining-specific queries if we have default data
    if column_types and len(column_types.get('numeric', [])) > 0:
        # Adapt queries to actual column names
        numeric_cols = column_types['numeric']
        categorical_cols = column_types.get('categorical', [])
        
        adapted_queries = []
        if numeric_cols:
            adapted_queries.extend([
                f"What is the total {numeric_cols[0]}?",
                f"Show me the average {numeric_cols[0]}",
                f"What's the maximum {numeric_cols[0]}?"
            ])
            if len(numeric_cols) > 1:
                adapted_queries.append(f"Distribution of {numeric_cols[1]}")
        
        if categorical_cols and numeric_cols:
            adapted_queries.append(f"Group {numeric_cols[0]} by {categorical_cols[0]}")
        
        if categorical_cols:
            adapted_queries.append(f"Count unique values in {categorical_cols[0]}")
        
        test_queries = adapted_queries if adapted_queries else test_queries
    
    query_results = test_query_analysis(session_id, test_queries)
    
    # Test 6: Analysis History
    test_analysis_history(session_id)
    
    # Test 7: List All Sessions
    test_list_sessions()
    
    # Test 8: Upload Custom File
    upload_session_id = test_upload_file()
    if upload_session_id:
        print(f"\n🔄 Testing uploaded data queries...")
        upload_queries = [
            "What is the total Sales?",
            "Show me Sales by Region",
            "Count unique Products"
        ]
        test_query_analysis(upload_session_id, upload_queries)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 API Test Suite Completed!")
    
    successful_queries = sum(1 for result in query_results if result['success'])
    total_queries = len(query_results)
    
    print(f"Query Analysis: {successful_queries}/{total_queries} successful")
    
    if successful_queries == total_queries:
        print("✅ All tests passed! The API backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print(f"\n📖 API Documentation: {BASE_URL}/docs")
    print(f"🔍 Interactive API: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
