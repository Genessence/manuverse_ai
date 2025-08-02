# Multi-Agent Streamlit Prototype for Data Analysis

A sophisticated Streamlit application that demonstrates a multi-agent system for automated data analysis. The system processes user queries in natural language and generates insights with visualizations from uploaded data files.

## 🚀 Features

### Multi-Agent Architecture
- **File Ingestion Agent**: Handles CSV, Excel, and text file uploads with automatic type detection
- **Query Understanding Agent**: Translates natural language queries into structured analysis plans
- **Data Analysis Agent**: Executes pandas operations based on query plans
- **Visualization Agent**: Dynamically generates matplotlib chart code
- **Response Generation Agent**: Formats comprehensive responses with text and visualizations

### Supported Operations
- **Aggregations**: Sum, average, count, statistical summaries
- **Grouping**: Group by categorical variables with aggregations
- **Distributions**: Histograms and statistical distributions
- **Time Series**: Basic time-based analysis (when date columns are present)
- **Custom Queries**: Flexible query parsing for various analysis types

### File Support
- **CSV files**: Comma-separated values with automatic delimiter detection
- **Excel files**: .xlsx and .xls formats with sheet processing
- **Text files**: Basic text processing and analysis

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.0+
- pandas 2.0.0+
- numpy 1.24.0+
- matplotlib 3.7.0+
- openpyxl 3.1.0+ (for Excel support)

## 🛠️ Installation

1. **Clone or download this repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run multi_agent_data_analysis.py
   ```

4. **Access the application** in your browser at `http://localhost:8501`

## 💡 Usage

### Getting Started
1. **Upload a file** using the sidebar file uploader
2. **Review the data preview** and column type detection
3. **Ask questions** about your data in the query box
4. **Click "Analyze"** to process your query through the multi-agent system
5. **View results** including generated charts and detailed analysis

### Example Queries
- `"What is the total sum of sales?"`
- `"Show me the average revenue by region"`
- `"Count the number of customers"`
- `"Create a histogram of ages"`
- `"Group the data by product category"`
- `"What's the distribution of prices?"`

### Sample Data
Click the "Generate Sample Sales Data" button to create demo data for testing the system.

## 🏗️ Architecture Details

### Agent Workflow
```
User Query → Query Understanding → Data Analysis → Visualization → Response Generation
     ↑              ↓                    ↓             ↓              ↓
File Upload → Column Metadata → Analysis Plan → Chart Code → Final Display
```

### Key Components

#### FileIngestionAgent
- Handles multiple file formats
- Automatic data type inference
- Column metadata extraction
- Error handling for corrupted files

#### QueryUnderstandingAgent
- Natural language processing (mock implementation)
- Query pattern matching
- Structured plan generation
- Intent classification

#### DataAnalysisAgent
- Pandas operations execution
- Statistical calculations
- Data aggregation and grouping
- Error-safe data processing

#### VisualizationAgent
- Dynamic matplotlib code generation
- Chart type selection based on data
- Customizable visualizations
- Code execution in isolated namespace

#### ResponseGenerationAgent
- Comprehensive response formatting
- Chart rendering and display
- Result summarization
- Error reporting

## 🔧 Configuration

### Session State Management
The application maintains state across user interactions:
- `data`: Current DataFrame
- `column_metadata`: Column type information
- `analysis_history`: Previous queries and results
- `current_file`: Current uploaded file name

### Customization Options
- Modify agent prompts in respective classes
- Add new analysis operations in `DataAnalysisAgent`
- Extend chart types in `VisualizationAgent`
- Customize UI layout in the main function

## 🐛 Troubleshooting

### Common Issues
1. **File Upload Errors**: Check file format and encoding
2. **Chart Display Issues**: Verify matplotlib backend configuration
3. **Memory Errors**: Large files may require chunking
4. **Query Parsing**: Use clear, descriptive language for queries

### Debug Mode
Add the following to enable debug information:
```python
st.set_option('client.showErrorDetails', True)
```

## 🔮 Future Enhancements

### Planned Features
- **Real API Integration**: Replace mock agents with actual Gemini API calls
- **Advanced Analytics**: Time series analysis, correlation matrices
- **Interactive Charts**: Plotly integration for dynamic visualizations
- **Export Options**: PDF reports, chart downloads
- **Multi-file Analysis**: Compare datasets across files
- **Natural Language Responses**: Enhanced response generation

### Scalability Improvements
- **Async Processing**: Non-blocking analysis for large datasets
- **Caching**: Redis integration for analysis results
- **Database Support**: Direct database connections
- **Cloud Storage**: S3/GCS file uploads

## 📝 Development

### Code Structure
```
multi_agent_data_analysis.py
├── FileIngestionAgent
├── QueryUnderstandingAgent
├── DataAnalysisAgent
├── VisualizationAgent
├── ResponseGenerationAgent
└── main() - Streamlit app logic
```

### Adding New Agents
1. Create a new class following the existing pattern
2. Implement static methods for agent operations
3. Add integration points in the main workflow
4. Update session state management as needed

### Testing
Test the application with various scenarios:
- Different file types and sizes
- Edge cases in queries
- Error conditions
- UI responsiveness

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:
- Bug fixes
- New agent types
- Enhanced query parsing
- Additional chart types
- UI/UX improvements

---

**Built with ❤️ using Streamlit and Python**
