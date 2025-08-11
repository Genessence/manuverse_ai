# Multi-Agent Data Analysis - React Frontend

A modern React TypeScript frontend for the multi-agent data analysis system.

## Features

- 🎯 **File Upload**: Drag-and-drop CSV/Excel file upload with validation
- 🤖 **Multi-Agent Processing**: Visual feedback of agent pipeline execution
- 📊 **Interactive Charts**: Dynamic data visualization with Recharts
- 📱 **Responsive Design**: Mobile-first design with Tailwind CSS
- 🔄 **Analysis History**: Track and re-run previous analyses
- ⚡ **Real-time Updates**: Live status updates during processing

## Tech Stack

- **React 18.2.0** - Frontend framework
- **TypeScript** - Type safety and better developer experience
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Data visualization library
- **Axios** - HTTP client for API communication

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python backend running (see main project README)

### Installation

```bash
cd react-frontend
npm install
```

### Development

```bash
# Start development server
npm start

# Run in background
npm run build
npm run serve
```

The app will be available at `http://localhost:3000`

## Project Structure

```
react-frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── FileUpload.tsx      # Drag-drop file upload
│   │   ├── QueryInterface.tsx  # Query input form
│   │   ├── AgentStatus.tsx     # Agent pipeline status
│   │   ├── AnalysisResults.tsx # Results display with charts
│   │   └── AnalysisHistory.tsx # Previous analyses
│   ├── types.ts               # TypeScript interfaces
│   ├── App.tsx               # Main application component
│   ├── index.tsx            # React DOM root
│   └── index.css           # Global styles with Tailwind
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

The frontend communicates with the Python backend via HTTP API:

- `POST /upload` - File upload
- `POST /analyze` - Query analysis
- `GET /status` - Agent status updates

## Components Overview

### FileUpload
- Drag-and-drop file upload
- File type validation (CSV, Excel)
- Upload progress feedback
- File metadata display

### QueryInterface  
- Natural language query input
- Query validation
- Submit with loading states
- Enable/disable visualizations toggle

### AgentStatus
- Real-time agent pipeline status
- Step-by-step progress indication
- Error handling and retry options
- Animated status indicators

### AnalysisResults
- Dynamic chart generation (Bar, Line, Pie)
- Tabular data display
- Query and result descriptions
- Downloadable results

### AnalysisHistory
- Previous analysis tracking
- Re-run previous queries
- Clear history functionality
- Timestamp and metadata

## Styling

Uses Tailwind CSS with custom animations and components:

- **Responsive grid layouts**
- **Smooth transitions and animations** 
- **Consistent color scheme**
- **Accessible focus states**
- **Loading and status indicators**

## Development Notes

- All components are fully typed with TypeScript
- Error boundaries handle component failures gracefully  
- Responsive design works on mobile and desktop
- Follows React best practices and hooks patterns
- Optimized for performance with proper state management

## Building for Production

```bash
npm run build
```

Creates optimized production build in `build/` directory.

## Environment Variables

Create `.env.local` for local development:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

## Contributing

1. Follow TypeScript best practices
2. Use Tailwind utility classes
3. Add proper error handling
4. Test responsive design
5. Update type definitions as needed
