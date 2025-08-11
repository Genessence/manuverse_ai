# Multi-Agent Data Analysis System

A comprehensive full-stack application that uses multiple AI agents to analyze data through natural language queries. Features both a Streamlit prototype and a modern React frontend with FastAPI backend.

![Multi-Agent System](https://img.shields.io/badge/Multi--Agent-Data%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)

## 🎯 Features

- **🤖 Multi-Agent Architecture**: 5 specialized AI agents working in pipeline
- **📊 Smart Data Analysis**: Natural language to insights conversion
- **📈 Dynamic Visualizations**: Auto-generated charts based on data patterns
- **🔄 Analysis History**: Track and replay previous analyses
- **📱 Modern UI**: React TypeScript frontend with Tailwind CSS
- **⚡ Real-time Updates**: Live status of agent processing pipeline
- **📁 File Support**: CSV, Excel file uploads with validation
- **🎛️ Default Dataset**: Pre-loaded mining flotation plant database

## 🏗️ Architecture

### Multi-Agent Pipeline
1. **File Ingestion Agent** - Handles data upload and preprocessing
2. **Query Understanding Agent** - Converts natural language to analysis plans
3. **Data Analysis Agent** - Executes statistical analysis and computations
4. **Visualization Agent** - Generates appropriate charts and graphs
5. **Response Generation Agent** - Formats results for user consumption

### Tech Stack
- **Backend**: Python 3.10, FastAPI, pandas, numpy, matplotlib
- **Frontend**: React 18, TypeScript, Tailwind CSS, Recharts
- **Data Processing**: Intelligent column recognition, type inference
- **Charts**: Bar, Line, Pie charts with responsive design

## 🚀 Quick Start

### Option 1: Full Stack (Recommended)
```bash
# Clone and setup
git clone <repo-url>
cd multi-agent-data-analysis

# Start both backend and frontend
run_fullstack.bat
```

### Option 2: Individual Components

#### API Backend
```bash
# Setup and run API server
run_api.bat
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

#### React Frontend  
```bash
# Setup React (first time only)
setup_react.bat

# Run development server
run_react.bat  
# Frontend: http://localhost:3000
```

#### Streamlit Prototype
```bash
# Run original Streamlit app
setup_venv.bat
run_app.bat
# Streamlit: http://localhost:8501
```

## 📁 Project Structure

```
multi-agent-data-analysis/
├── 🐍 Python Backend
│   ├── multi_agent_data_analysis.py    # Main Streamlit app
│   ├── api_backend.py                  # FastAPI backend
│   ├── requirements.txt                # Python dependencies
│   └── MiningProcess_*.csv            # Default dataset
├── ⚛️ React Frontend
│   └── react-frontend/
│       ├── src/
│       │   ├── components/            # React components
│       │   ├── App.tsx               # Main application
│       │   └── types.ts              # TypeScript interfaces
│       ├── package.json              # Node dependencies
│       └── tailwind.config.js        # Tailwind configuration
├── 🚀 Deployment Scripts
│   ├── run_fullstack.bat            # Start everything
│   ├── run_api.bat                  # API server only
│   ├── run_react.bat                # Frontend only
│   └── setup_react.bat              # Frontend setup
└── 📚 Documentation
    ├── README.md                    # This file
    ├── DOCUMENTATION.md             # Detailed docs
    └── ENHANCEMENTS.md             # Feature roadmap
```

## 💡 Usage Examples

### Natural Language Queries
- **"What are the top 5 values in the dataset?"**
- **"Show me the distribution of Silica Concentrate"**
- **"Calculate the average of all numeric columns"**
- **"Find outliers in Flotation Column 01 Air Flow"**
- **"Create a visualization showing correlations"**
- **"What is the relationship between Iron Feed and Silica Feed?"**

### Smart Features
- **Column Recognition**: Automatically identifies column types and suggests analyses
- **Intelligent Charts**: Chooses appropriate visualizations based on data patterns
- **Error Handling**: Graceful handling of analysis failures with suggestions
- **History Tracking**: Save and replay previous successful analyses

## 🔧 API Endpoints

### FastAPI Backend (`http://localhost:8000`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check and system status |
| `POST` | `/upload` | Upload CSV/Excel files |
| `POST` | `/analyze` | Submit natural language queries |
| `GET` | `/status/{session_id}` | Get analysis progress |
| `GET` | `/history` | Retrieve analysis history |
| `DELETE` | `/history` | Clear analysis history |
| `GET` | `/data/info` | Get current dataset information |

### Request Examples
```bash
# Upload file
curl -X POST "http://localhost:8000/upload" -F "file=@data.csv"

# Analyze data
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the top 10 records", "enableVisualization": true}'
```

## 🛠️ Development

### Prerequisites
- **Python 3.10+** with pip
- **Node.js 18+** with npm  
- **Git** for version control

### Setup Development Environment
```bash
# Python virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r api_requirements.txt

# React dependencies
cd react-frontend
npm install
cd ..
```

### Running in Development Mode
```bash
# Terminal 1: API Backend (with hot reload)
uvicorn api_backend:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: React Frontend (with hot reload)  
cd react-frontend
npm start

# Terminal 3: Streamlit (optional)
streamlit run multi_agent_data_analysis.py
```

## 📊 Sample Datasets

### Default Mining Dataset
The system includes a comprehensive mining flotation plant dataset with:
- **536,000+ records** of real industrial data
- **24 columns** including sensors, flows, and concentrations
- **Features**: Iron/Silica feeds, flotation columns, pH levels, air flows

### Custom Data Support
- **CSV files**: Comma-separated values with headers
- **Excel files**: .xlsx and .xls formats
- **Automatic detection**: Column types, data patterns, missing values
- **Validation**: File format, size limits, data quality checks

## 🎨 UI Components

### React Frontend Features
- **File Upload**: Drag-and-drop with progress indicators
- **Query Interface**: Natural language input with suggestions
- **Agent Status**: Real-time pipeline visualization
- **Results Display**: Interactive charts and data tables
- **Analysis History**: Previous queries with re-run capability

### Responsive Design
- **Mobile-first**: Works on phones, tablets, desktops
- **Tailwind CSS**: Utility-first styling with custom components
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support

## 🔍 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill processes on specific ports
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Dependencies Issues**
```bash
# Reset Python environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Reset Node modules
rmdir /s node_modules
npm install
```

**File Upload Problems**
- Ensure CSV files have proper headers
- Check file size limits (100MB max)
- Verify file encoding (UTF-8 recommended)

## 🚀 Deployment

### Production Build
```bash
# Build React frontend
cd react-frontend
npm run build

# Serve static files with Python
python -m http.server 3000 --directory react-frontend/build

# Production API
uvicorn api_backend:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

### Code Style
- **Python**: Black formatter, PEP 8 compliance
- **React**: Prettier, ESLint configuration
- **TypeScript**: Strict mode enabled
- **Comments**: Document complex logic and API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- **Streamlit** for rapid prototyping capabilities
- **FastAPI** for high-performance async API framework
- **React** for modern frontend development
- **Tailwind CSS** for beautiful, responsive design
- **Recharts** for interactive data visualization
- **pandas** for powerful data analysis tools

---

**Made with ❤️ by the Multi-Agent Development Team**
