"""
Multi-Agent Streamlit Prototype for Data Analysis

This application implements a multi-agent system for data analysis with the following components:
1. File Ingestion Agent - Handles CSV, Excel, and DOC file uploads
2. Query Understanding Agent - Translates user queries into structured plans
3. Data Analysis Agent - Executes analysis plans on the data
4. Visualization Agent - Generates matplotlib charts
5. Response Generation Agent - Formats final responses

Author: AI Assistant
Date: August 2, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
import io
import base64
from typing import Dict, Any, Optional, Tuple
import tempfile
import os

# Set matplotlib backend for Streamlit compatibility
matplotlib.use('Agg')

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Agent Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class FileIngestionAgent:
    """Handles file upload and data ingestion"""
    
    @staticmethod
    def ingest_file(uploaded_file) -> Optional[pd.DataFrame]:
        """
        Reads uploaded file and returns a pandas DataFrame
        Supports CSV, Excel, and basic text files
        """
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_extension in ['txt', 'doc']:
                # For text/doc files, create a simple DataFrame
                content = str(uploaded_file.read(), "utf-8")
                lines = content.split('\n')
                df = pd.DataFrame({'text_content': lines})
            else:
                st.error(f"Unsupported file format: {file_extension}")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    
    @staticmethod
    def get_column_metadata(df: pd.DataFrame) -> Dict[str, str]:
        """Extract column names and their inferred data types"""
        metadata = {}
        for col in df.columns:
            dtype = str(df[col].dtype)
            if dtype.startswith('int'):
                metadata[col] = 'integer'
            elif dtype.startswith('float'):
                metadata[col] = 'float'
            elif dtype == 'object':
                # Check if it's actually dates or categories
                if df[col].nunique() < len(df) * 0.5:
                    metadata[col] = 'categorical'
                else:
                    metadata[col] = 'text'
            elif 'datetime' in dtype:
                metadata[col] = 'datetime'
            else:
                metadata[col] = 'text'
        
        return metadata

class QueryUnderstandingAgent:
    """Translates user queries into structured analysis plans"""
    
    @staticmethod
    def find_column_in_query(query: str, columns: list) -> str:
        """
        Find the most likely column name mentioned in the query
        """
        query_lower = query.lower()
        
        # Direct exact matches (case insensitive)
        for col in columns:
            if col.lower() in query_lower:
                return col
        
        # Enhanced column synonyms and business terms
        column_synonyms = {
            'sales': ['sale', 'revenue', 'income', 'earnings', 'money', 'amount', 'value', 'turnover'],
            'quantity': ['qty', 'amount', 'number', 'count', 'volume', 'units', 'pieces'],
            'region': ['area', 'location', 'place', 'territory', 'zone', 'district'],
            'product': ['item', 'goods', 'merchandise', 'sku', 'article'],
            'customer': ['client', 'buyer', 'user', 'consumer', 'purchaser'],
            'date': ['time', 'when', 'period', 'timestamp'],
            'price': ['cost', 'value', 'rate', 'fee', 'charge'],
            'category': ['type', 'kind', 'group', 'class', 'segment'],
            'name': ['title', 'label', 'identifier'],
            'id': ['identifier', 'key', 'reference'],
            'status': ['state', 'condition', 'stage'],
            'total': ['sum', 'aggregate', 'overall'],
            'average': ['mean', 'avg'],
            'employee': ['worker', 'staff', 'personnel'],
            'department': ['dept', 'division', 'unit'],
            'order': ['purchase', 'transaction', 'request']
        }
        
        # Check for synonym matches with exact column names
        for col in columns:
            col_lower = col.lower()
            # Check if any part of column name matches synonyms
            for base_word, synonyms in column_synonyms.items():
                if base_word in col_lower or any(syn in col_lower for syn in synonyms):
                    if any(syn in query_lower for syn in [base_word] + synonyms):
                        return col
        
        # Check for partial string matches with better scoring
        best_match = None
        best_score = 0
        
        for col in columns:
            col_words = col.lower().replace('_', ' ').split()
            score = 0
            
            for word in col_words:
                if len(word) > 2 and word in query_lower:
                    score += len(word)  # Longer matches get higher scores
            
            if score > best_score:
                best_score = score
                best_match = col
        
        # Only return if we found a reasonable match
        if best_score > 2:  # At least 3 characters matched
            return best_match
        
        # Last resort: check if query contains numbers and find numeric columns
        if any(char.isdigit() for char in query_lower):
            numeric_keywords = ['total', 'sum', 'count', 'amount', 'value', 'number']
            if any(keyword in query_lower for keyword in numeric_keywords):
                # Return first column that might contain numbers
                for col in columns:
                    if any(term in col.lower() for term in ['sales', 'quantity', 'amount', 'price', 'value', 'count']):
                        return col
        
        return None
    
    @staticmethod
    def parse_query(user_query: str, column_metadata: Dict[str, str]) -> Dict[str, Any]:
        """
        Enhanced query parsing that recognizes column names and operations
        """
        
        query_lower = user_query.lower()
        columns = list(column_metadata.keys())
        
        # Find mentioned column
        target_column = QueryUnderstandingAgent.find_column_in_query(user_query, columns)
        
        # Categorize columns by type
        numeric_cols = [col for col, dtype in column_metadata.items() 
                       if dtype in ['integer', 'float']]
        categorical_cols = [col for col, dtype in column_metadata.items() 
                           if dtype == 'categorical']
        text_cols = [col for col, dtype in column_metadata.items() 
                    if dtype == 'text']
        
        # Enhanced pattern matching with column awareness
        if any(word in query_lower for word in ['sum', 'total', 'add up']):
            # Use found column if numeric, otherwise first numeric column
            if target_column and target_column in numeric_cols:
                return {
                    'operation': 'sum',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Sum of {target_column}"
                }
            elif numeric_cols:
                return {
                    'operation': 'sum',
                    'column': numeric_cols[0],
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Sum of {numeric_cols[0]}"
                }
        
        elif any(word in query_lower for word in ['average', 'mean', 'avg']):
            if target_column and target_column in numeric_cols:
                return {
                    'operation': 'mean',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'line_chart',
                    'description': f"Average of {target_column}"
                }
            elif numeric_cols:
                return {
                    'operation': 'mean',
                    'column': numeric_cols[0],
                    'filters': None,
                    'visualization_type': 'line_chart',
                    'description': f"Average of {numeric_cols[0]}"
                }
        
        elif any(word in query_lower for word in ['count', 'number of', 'how many']):
            if target_column:
                return {
                    'operation': 'count',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Count of {target_column}"
                }
            else:
                return {
                    'operation': 'count',
                    'column': columns[0] if columns else 'index',
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': "Total record count"
                }
        
        elif any(word in query_lower for word in ['group', 'by', 'breakdown', 'split']):
            # Try to find both grouping column and aggregation column
            group_col = None
            agg_col = None
            
            # Look for categorical column for grouping
            if target_column and target_column in categorical_cols:
                group_col = target_column
            elif categorical_cols:
                group_col = categorical_cols[0]
            
            # Look for numeric column for aggregation
            for col in numeric_cols:
                if col.lower() in query_lower or col != target_column:
                    agg_col = col
                    break
            
            if not agg_col and numeric_cols:
                agg_col = numeric_cols[0]
            
            if group_col and agg_col:
                agg_method = 'sum'
                if any(word in query_lower for word in ['average', 'mean']):
                    agg_method = 'mean'
                elif any(word in query_lower for word in ['count']):
                    agg_method = 'count'
                
                return {
                    'operation': 'groupby',
                    'column': group_col,
                    'aggregation_column': agg_col,
                    'aggregation_method': agg_method,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"{agg_method.title()} of {agg_col} by {group_col}"
                }
        
        elif any(word in query_lower for word in ['distribution', 'histogram', 'spread']):
            if target_column and target_column in numeric_cols:
                return {
                    'operation': 'distribution',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'histogram',
                    'description': f"Distribution of {target_column}"
                }
            elif numeric_cols:
                return {
                    'operation': 'distribution',
                    'column': numeric_cols[0],
                    'filters': None,
                    'visualization_type': 'histogram',
                    'description': f"Distribution of {numeric_cols[0]}"
                }
        
        elif any(word in query_lower for word in ['max', 'maximum', 'highest', 'largest']):
            if target_column and target_column in numeric_cols:
                return {
                    'operation': 'max',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Maximum {target_column}"
                }
            elif numeric_cols:
                return {
                    'operation': 'max',
                    'column': numeric_cols[0],
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Maximum {numeric_cols[0]}"
                }
        
        elif any(word in query_lower for word in ['min', 'minimum', 'lowest', 'smallest']):
            if target_column and target_column in numeric_cols:
                return {
                    'operation': 'min',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Minimum {target_column}"
                }
            elif numeric_cols:
                return {
                    'operation': 'min',
                    'column': numeric_cols[0],
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Minimum {numeric_cols[0]}"
                }
        
        elif any(word in query_lower for word in ['unique', 'distinct', 'different']):
            if target_column:
                return {
                    'operation': 'unique',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Unique values in {target_column}"
                }
        
        # If target column is found but no specific operation, provide column summary
        if target_column:
            if target_column in numeric_cols:
                return {
                    'operation': 'describe',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'histogram',
                    'description': f"Summary statistics for {target_column}"
                }
            else:
                return {
                    'operation': 'value_counts',
                    'column': target_column,
                    'filters': None,
                    'visualization_type': 'bar_chart',
                    'description': f"Value counts for {target_column}"
                }
        
        # Default fallback - show overall summary
        return {
            'operation': 'describe',
            'column': 'all',
            'filters': None,
            'visualization_type': 'table',
            'description': "Overall dataset summary"
        }

class DataAnalysisAgent:
    """Executes data analysis based on structured plans"""
    
    @staticmethod
    def execute_analysis(df: pd.DataFrame, plan: Dict[str, Any]) -> Tuple[Any, str]:
        """
        Execute the analysis plan on the DataFrame
        Returns the result and a description
        """
        try:
            operation = plan.get('operation')
            column = plan.get('column')
            description = plan.get('description', 'Analysis result')
            
            if operation == 'sum' and column in df.columns:
                result = df[column].sum()
                description = f"Sum of {column}: {result:,.2f}"
                return result, description
            
            elif operation == 'mean' and column in df.columns:
                result = df[column].mean()
                description = f"Average of {column}: {result:.2f}"
                return result, description
            
            elif operation == 'max' and column in df.columns:
                result = df[column].max()
                description = f"Maximum {column}: {result:,.2f}"
                return result, description
            
            elif operation == 'min' and column in df.columns:
                result = df[column].min()
                description = f"Minimum {column}: {result:,.2f}"
                return result, description
            
            elif operation == 'count':
                if column in df.columns:
                    result = df[column].count()  # Count non-null values
                    description = f"Count of non-null values in {column}: {result:,}"
                else:
                    result = len(df)
                    description = f"Total number of records: {result:,}"
                return result, description
            
            elif operation == 'unique' and column in df.columns:
                result = df[column].nunique()
                unique_values = df[column].unique()[:10]  # Show first 10 unique values
                description = f"Number of unique values in {column}: {result}\nSample values: {', '.join(map(str, unique_values))}"
                return result, description
            
            elif operation == 'value_counts' and column in df.columns:
                result = df[column].value_counts().head(10)  # Top 10 values
                description = f"Value counts for {column} (top 10)"
                return result, description
            
            elif operation == 'groupby':
                group_col = plan.get('column')
                agg_col = plan.get('aggregation_column')
                agg_method = plan.get('aggregation_method', 'sum')
                
                if group_col in df.columns and agg_col in df.columns:
                    if agg_method == 'sum':
                        result = df.groupby(group_col)[agg_col].sum().sort_values(ascending=False)
                    elif agg_method == 'mean':
                        result = df.groupby(group_col)[agg_col].mean().sort_values(ascending=False)
                    elif agg_method == 'count':
                        result = df.groupby(group_col)[agg_col].count().sort_values(ascending=False)
                    else:
                        result = df.groupby(group_col)[agg_col].sum().sort_values(ascending=False)
                    
                    description = f"{agg_method.title()} of {agg_col} by {group_col}"
                    return result, description
            
            elif operation == 'distribution' and column in df.columns:
                result = df[column].describe()
                description = f"Statistical distribution of {column}"
                return result, description
            
            elif operation == 'describe':
                if column == 'all':
                    result = df.describe()
                    description = "Statistical summary of all numeric columns"
                elif column in df.columns:
                    if df[column].dtype in ['int64', 'float64']:
                        result = df[column].describe()
                        description = f"Statistical summary of {column}"
                    else:
                        result = df[column].describe()
                        description = f"Summary of {column}"
                else:
                    result = df.head()
                    description = "First 5 rows of the dataset"
                return result, description
            
            else:
                # Fallback to basic info
                result = df.head()
                description = "First 5 rows of the dataset"
                return result, description
                
        except Exception as e:
            error_msg = f"Error in analysis: {str(e)}"
            return None, error_msg

class VisualizationAgent:
    """Generates matplotlib chart code based on analysis results"""
    
    @staticmethod
    def generate_chart_code(query: str, data: Any, chart_type: str, description: str) -> str:
        """
        Enhanced chart generation with better handling of different data types
        """
        
        if chart_type == 'bar_chart' and hasattr(data, 'index'):
            # For grouped data or series
            return f"""
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Data preparation
x_labels = {list(data.index) if hasattr(data, 'index') else ['Value']}
y_values = {list(data.values) if hasattr(data, 'values') else [data]}

# Create bar chart
bars = ax.bar(range(len(x_labels)), y_values, color='steelblue', alpha=0.8, edgecolor='navy', linewidth=0.8)

# Customize chart
ax.set_xlabel('Categories', fontsize=12, fontweight='bold')
ax.set_ylabel('Values', fontsize=12, fontweight='bold')
ax.set_title('{description}', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, rotation=45, ha='right')

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{{height:,.1f}}', ha='center', va='bottom', fontweight='bold')

# Add grid and styling
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('#f8f9fa')
plt.tight_layout()
"""
        
        elif chart_type == 'line_chart':
            return f"""
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Data preparation
if hasattr(data, 'index') and hasattr(data, 'values'):
    x_data = range(len(data.index))
    y_data = list(data.values)
    x_labels = list(data.index)
else:
    x_data = range(len([data] if not hasattr(data, '__iter__') else list(data)))
    y_data = [data] if not hasattr(data, '__iter__') else list(data)
    x_labels = [f'Point {{i+1}}' for i in range(len(y_data))]

# Create line chart
line = ax.plot(x_data, y_data, marker='o', linewidth=3, markersize=8, 
               color='darkblue', markerfacecolor='lightblue', markeredgecolor='darkblue', markeredgewidth=2)

# Customize chart
ax.set_xlabel('Data Points', fontsize=12, fontweight='bold')
ax.set_ylabel('Values', fontsize=12, fontweight='bold')
ax.set_title('{description}', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x_data[::max(1, len(x_data)//10)])  # Show max 10 labels
ax.set_xticklabels([x_labels[i] for i in range(0, len(x_labels), max(1, len(x_labels)//10))], rotation=45, ha='right')

# Add grid and styling
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('#f8f9fa')
plt.tight_layout()
"""
        
        elif chart_type == 'histogram':
            return f"""
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Data preparation
if hasattr(data, 'values'):
    data_values = list(data.values)
elif hasattr(data, '__iter__') and not isinstance(data, str):
    data_values = list(data)
else:
    data_values = [data]

# Create histogram
n, bins, patches = ax.hist(data_values, bins=min(20, len(set(data_values))), 
                          color='lightblue', alpha=0.7, edgecolor='darkblue', linewidth=1.2)

# Customize chart
ax.set_xlabel('Values', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax.set_title('{description}', fontsize=14, fontweight='bold', pad=20)

# Add statistics text
mean_val = np.mean(data_values)
std_val = np.std(data_values)
ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {{mean_val:.2f}}')
ax.legend()

# Add grid and styling
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('#f8f9fa')
plt.tight_layout()
"""
        
        else:
            # Default visualization for text or summary data
            return f"""
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Create a text-based visualization
info_text = "{description}\\n\\n"
if hasattr(data, 'to_string'):
    info_text += data.to_string()
else:
    info_text += str(data)

ax.text(0.5, 0.5, info_text, transform=ax.transAxes, 
        ha='center', va='center', fontsize=12, 
        bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8),
        wrap=True)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('{description}', fontsize=14, fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout()
"""

class ResponseGenerationAgent:
    """Formats final responses and displays charts"""
    
    @staticmethod
    def generate_response(query: str, analysis_result: Any, description: str, 
                         chart_code: str) -> Tuple[str, Any]:
        """
        Generate a comprehensive response including text and visualization
        """
        
        # Create text response
        response_text = f"""
## Analysis Results

**Your Query:** {query}

**Finding:** {description}

**Details:**
"""
        
        # Add specific details based on result type
        if isinstance(analysis_result, (int, float)):
            response_text += f"- Calculated value: {analysis_result:,.2f}\n"
        elif hasattr(analysis_result, 'to_string'):
            response_text += f"```\n{analysis_result.to_string()}\n```\n"
        else:
            response_text += f"- Result: {str(analysis_result)}\n"
        
        # Execute chart code
        chart_fig = None
        try:
            # Create a new namespace for chart execution
            chart_namespace = {
                'plt': plt,
                'np': np,
                'data': analysis_result
            }
            
            # Execute the generated chart code
            exec(chart_code, chart_namespace)
            
            # Get the current figure
            chart_fig = plt.gcf()
            
        except Exception as e:
            response_text += f"\n⚠️ Chart generation error: {str(e)}\n"
        
        return response_text, chart_fig

def main():
    """Main Streamlit application"""
    
    st.title("🤖 Multi-Agent Data Analysis System")
    st.markdown("---")
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'column_metadata' not in st.session_state:
        st.session_state.column_metadata = {}
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    # Sidebar for file upload
    st.sidebar.header("📁 File Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls', 'txt', 'doc'],
        help="Upload CSV, Excel, or text files for analysis"
    )
    
    # File ingestion
    if uploaded_file is not None:
        # Reset session state when new file is uploaded
        if st.session_state.get('current_file') != uploaded_file.name:
            st.session_state.data = None
            st.session_state.column_metadata = {}
            st.session_state.analysis_history = []
            st.session_state.current_file = uploaded_file.name
        
        # Process file
        if st.session_state.data is None:
            with st.spinner("🔍 File Ingestion Agent processing..."):
                df = FileIngestionAgent.ingest_file(uploaded_file)
                
                if df is not None:
                    st.session_state.data = df
                    st.session_state.column_metadata = FileIngestionAgent.get_column_metadata(df)
                    
                    st.sidebar.success(f"✅ File loaded: {uploaded_file.name}")
                    st.sidebar.write(f"**Rows:** {len(df):,}")
                    st.sidebar.write(f"**Columns:** {len(df.columns)}")
        
        # Display data preview
        if st.session_state.data is not None:
            st.header("📊 Data Preview")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(st.session_state.data.head(10), use_container_width=True)
            
            with col2:
                st.subheader("Column Types")
                metadata_df = pd.DataFrame(
                    list(st.session_state.column_metadata.items()),
                    columns=['Column', 'Type']
                )
                st.dataframe(metadata_df, use_container_width=True)
            
            st.markdown("---")
            
            # Query interface
            st.header("💬 Ask Your Question")
            
            # Show available columns for reference
            if st.session_state.column_metadata:
                with st.expander("📋 Available Columns (Click to see all columns)", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Numeric Columns:**")
                        numeric_cols = [col for col, dtype in st.session_state.column_metadata.items() 
                                       if dtype in ['integer', 'float']]
                        for col in numeric_cols:
                            st.write(f"• `{col}`")
                    
                    with col2:
                        st.write("**Categorical Columns:**")
                        categorical_cols = [col for col, dtype in st.session_state.column_metadata.items() 
                                           if dtype == 'categorical']
                        for col in categorical_cols:
                            st.write(f"• `{col}`")
                        
                        st.write("**Text Columns:**")
                        text_cols = [col for col, dtype in st.session_state.column_metadata.items() 
                                    if dtype == 'text']
                        for col in text_cols:
                            st.write(f"• `{col}`")
            
            # Example queries
            st.subheader("Example Queries:")
            
            # Generate dynamic examples based on available columns
            if st.session_state.column_metadata:
                numeric_cols = [col for col, dtype in st.session_state.column_metadata.items() 
                               if dtype in ['integer', 'float']]
                categorical_cols = [col for col, dtype in st.session_state.column_metadata.items() 
                                   if dtype == 'categorical']
                
                example_queries = []
                
                # Add specific examples based on available columns
                if numeric_cols:
                    example_queries.append(f"What is the total {numeric_cols[0]}?")
                    example_queries.append(f"Show me the average {numeric_cols[0]}")
                    if len(numeric_cols) > 1:
                        example_queries.append(f"What's the maximum {numeric_cols[1]}?")
                
                if categorical_cols and numeric_cols:
                    example_queries.append(f"Group {numeric_cols[0]} by {categorical_cols[0]}")
                    example_queries.append(f"Show {numeric_cols[0]} breakdown by {categorical_cols[0]}")
                
                if categorical_cols:
                    example_queries.append(f"Count unique values in {categorical_cols[0]}")
                
                # Ensure we have at least 5 examples
                while len(example_queries) < 5:
                    example_queries.extend([
                        "Show me the distribution of values",
                        "Count the number of records",
                        "What are the summary statistics?",
                        "Show unique values in the first column",
                        "Give me an overview of the data"
                    ])
                
                example_queries = example_queries[:5]  # Limit to 5
            else:
                # Default examples when no data is loaded
                example_queries = [
                    "What is the total sales?",
                    "Show me the average revenue by region", 
                    "Count the number of customers",
                    "Show me a distribution histogram",
                    "Group the data by category"
                ]
            
            cols = st.columns(len(example_queries))
            for i, example in enumerate(example_queries):
                if cols[i].button(example, key=f"example_{i}"):
                    st.session_state.current_query = example
            
            # Query input
            query = st.text_area(
                "Enter your data analysis question:",
                value=st.session_state.get('current_query', ''),
                placeholder="e.g., 'What is the total sales by region?' or 'Show me the distribution of ages'",
                height=100
            )
            
            # Process query
            if st.button("🚀 Analyze", type="primary", use_container_width=True):
                if query.strip():
                    with st.spinner("🤖 Multi-agent system processing..."):
                        
                        # Agent 1: Query Understanding
                        st.write("🧠 **Query Understanding Agent** parsing request...")
                        plan = QueryUnderstandingAgent.parse_query(
                            query, st.session_state.column_metadata
                        )
                        
                        with st.expander("📋 Analysis Plan", expanded=False):
                            st.json(plan)
                            
                            # Show which column was detected
                            if plan.get('column'):
                                detected_col = plan.get('column')
                                st.info(f"🎯 **Detected Column:** `{detected_col}`")
                                
                                if 'aggregation_column' in plan:
                                    agg_col = plan.get('aggregation_column')
                                    st.info(f"📊 **Aggregation Column:** `{agg_col}`")
                        
                        # Agent 2: Data Analysis
                        st.write("📈 **Data Analysis Agent** executing analysis...")
                        analysis_result, description = DataAnalysisAgent.execute_analysis(
                            st.session_state.data, plan
                        )
                        
                        if analysis_result is not None:
                            # Agent 3: Visualization
                            st.write("🎨 **Visualization Agent** generating chart...")
                            chart_code = VisualizationAgent.generate_chart_code(
                                query, analysis_result, 
                                plan.get('visualization_type', 'bar_chart'),
                                description
                            )
                            
                            # Agent 4: Response Generation
                            st.write("📝 **Response Generation Agent** formatting results...")
                            response_text, chart_fig = ResponseGenerationAgent.generate_response(
                                query, analysis_result, description, chart_code
                            )
                            
                            # Display results
                            st.markdown("---")
                            st.markdown(response_text)
                            
                            if chart_fig:
                                st.pyplot(chart_fig)
                                plt.close(chart_fig)  # Clean up
                            
                            # Save to history
                            st.session_state.analysis_history.append({
                                'query': query,
                                'plan': plan,
                                'result': description,
                                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                        
                        else:
                            st.error(f"Analysis failed: {description}")
                
                else:
                    st.warning("Please enter a query!")
            
            # Analysis history
            if st.session_state.analysis_history:
                st.markdown("---")
                st.header("📚 Analysis History")
                
                for i, item in enumerate(reversed(st.session_state.analysis_history)):
                    with st.expander(f"Query {len(st.session_state.analysis_history) - i}: {item['query'][:50]}..."):
                        st.write(f"**Time:** {item['timestamp']}")
                        st.write(f"**Query:** {item['query']}")
                        st.write(f"**Result:** {item['result']}")
                        st.json(item['plan'])
    
    else:
        # Welcome screen
        st.header("Welcome to the Multi-Agent Data Analysis System! 👋")
        
        st.markdown("""
        This prototype demonstrates a multi-agent system for data analysis with the following components:
        
        ### 🤖 Agent Architecture
        
        1. **📁 File Ingestion Agent**
           - Handles CSV, Excel, and text file uploads
           - Automatically detects column types and metadata
        
        2. **🧠 Query Understanding Agent**
           - Translates natural language queries into structured analysis plans
           - Maps user intent to specific data operations
        
        3. **📈 Data Analysis Agent**
           - Executes analysis plans using pandas operations
           - Supports aggregations, grouping, and statistical analysis
        
        4. **🎨 Visualization Agent**
           - Generates matplotlib chart code dynamically
           - Creates appropriate visualizations based on data and query type
        
        5. **📝 Response Generation Agent**
           - Formats comprehensive responses with text and charts
           - Presents results in a user-friendly format
        
        ### 🚀 Getting Started
        
        1. **Upload a file** using the sidebar (CSV, Excel, or text files)
        2. **Ask questions** about your data in natural language
        3. **View results** including charts and detailed analysis
        4. **Explore history** of your previous analyses
        
        ### 💡 Example Queries
        
        - "What is the total **sales**?" (uses specific column name)
        - "Show me the average **revenue** by **region**" (groups by column)
        - "Count the number of **customers**" (counts specific column)
        - "What's the maximum **quantity**?" (finds max in column)
        - "Group **sales** by **product**" (advanced grouping)
        - "Show unique values in **customer_type**" (categorical analysis)
        - "What's the distribution of **prices**?" (statistical distribution)
        
        **Tips for better results:**
        - Use actual column names from your data
        - Be specific about what you want to analyze
        - Try operations like: sum, average, count, max, min, group by
        - Ask about distributions and unique values
        
        **Ready to begin?** Upload a file to start your analysis! 📊
        """)
        
        # Sample data generation for demo
        st.markdown("---")
        st.subheader("🎲 Want to try with sample data?")
        
        if st.button("Generate Sample Sales Data"):
            # Create sample data
            np.random.seed(42)
            sample_data = pd.DataFrame({
                'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
                'Product': np.random.choice(['A', 'B', 'C', 'D'], 100),
                'Sales': np.random.randint(100, 1000, 100),
                'Quantity': np.random.randint(1, 50, 100),
                'Date': pd.date_range('2024-01-01', periods=100, freq='D')
            })
            
            st.session_state.data = sample_data
            st.session_state.column_metadata = FileIngestionAgent.get_column_metadata(sample_data)
            st.session_state.current_file = "sample_sales_data.csv"
            
            st.success("✅ Sample data generated! Scroll up to see the data preview.")
            st.rerun()

if __name__ == "__main__":
    main()
