<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Multi-Agent Data Analysis System

This is a Streamlit prototype that implements a multi-agent system for data analysis. The system consists of several specialized agents that work together to process user queries and generate insights from uploaded data files.

## Architecture Overview

The application follows a modular agent-based architecture:

1. **FileIngestionAgent**: Handles file upload and data preprocessing
2. **QueryUnderstandingAgent**: Parses natural language queries into structured plans
3. **DataAnalysisAgent**: Executes pandas operations based on analysis plans
4. **VisualizationAgent**: Generates matplotlib chart code
5. **ResponseGenerationAgent**: Formats results and displays visualizations

## Development Guidelines

- Each agent is implemented as a separate class with static methods
- Use pandas for all data manipulation operations
- Generate matplotlib code as strings for dynamic chart creation
- Maintain session state for data persistence across user interactions
- Follow Streamlit best practices for UI components
- Handle errors gracefully and provide user-friendly feedback

## Code Style

- Use type hints for function parameters and return values
- Include comprehensive docstrings for all methods
- Follow PEP 8 conventions for code formatting
- Use descriptive variable names and clear code structure
- Implement proper error handling and validation

## Testing Considerations

- Test with various file formats (CSV, Excel, text)
- Validate query parsing for different user input patterns
- Ensure chart generation works for different data types
- Test session state management and data persistence
- Verify error handling for edge cases
