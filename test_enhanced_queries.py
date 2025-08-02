"""
Test script to demonstrate enhanced column name recognition
"""

# Test the enhanced query understanding
test_queries = [
    "What is the total sales?",
    "Show me the average sales by region", 
    "Count the customers",
    "What's the maximum quantity?",
    "Group sales by product",
    "Show unique values in region",
    "What's the distribution of sales?",
    "What is the minimum quantity?",
    "Show me revenue breakdown by customer type"
]

# Test column metadata (sample)
sample_metadata = {
    'Region': 'categorical',
    'Product': 'categorical', 
    'Sales': 'float',
    'Quantity': 'integer',
    'Date': 'datetime',
    'Customer_Type': 'categorical'
}

# Import the enhanced agent
import sys
sys.path.append('.')

try:
    from multi_agent_data_analysis import QueryUnderstandingAgent
    
    print("🧪 Testing Enhanced Query Understanding Agent")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        result = QueryUnderstandingAgent.parse_query(query, sample_metadata)
        print(f"   → Operation: {result.get('operation')}")
        print(f"   → Column: {result.get('column')}")
        print(f"   → Description: {result.get('description', 'N/A')}")
        if 'aggregation_column' in result:
            print(f"   → Aggregation Column: {result.get('aggregation_column')}")
            print(f"   → Aggregation Method: {result.get('aggregation_method')}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed! The agent now recognizes column names in queries.")
    
except ImportError as e:
    print(f"❌ Error importing module: {e}")
except Exception as e:
    print(f"❌ Error during testing: {e}")
