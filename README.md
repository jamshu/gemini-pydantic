# Gemini-Pydantic Integration Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.5+-green.svg)](https://pydantic-docs.helpmanual.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python project demonstrating how to use Google's Gemini API with Pydantic for generating, validating, and processing structured data. This project transforms unreliable LLM text outputs into validated, type-safe Python objects for robust data processing.

## 🎯 Overview

Large Language Models like Gemini excel at generating human-like text but often return unstructured responses that are difficult to use in applications requiring predictable data formats. This project solves that problem by:

1. **Generating** structured JSON data from Gemini using carefully crafted prompts
2. **Cleaning** responses to handle common formatting issues (markdown code blocks, etc.)
3. **Validating** data against strict Pydantic schemas with comprehensive error handling
4. **Processing** validated data as Python objects for analysis and integration
5. **Exporting** results to various formats (JSON, CSV) with visualization capabilities

## ✨ Features

- 🤖 **Gemini API Integration**: Seamless connection to Google's Gemini AI
- 🛡️ **Data Validation**: Robust Pydantic models with comprehensive validation rules
- 🧹 **Response Cleaning**: Automatic handling of markdown formatting and LLM quirks
- 📊 **Data Analysis**: Built-in statistical analysis and reporting capabilities
- 📈 **Visualization**: Matplotlib-based charts and graphs for data insights
- 💾 **File Management**: JSON and CSV export/import functionality
- 🏗️ **Modular Architecture**: Clean separation of concerns with organized code structure
- ⚡ **Type Safety**: Full type hints and validation throughout the codebase
- 🔒 **Security**: Proper API key management with environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free tier available)
- Basic familiarity with Python and virtual environments

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd gemini-pydantic-tutorial
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Using uv (recommended)
   pip install uv
   uv pip install -r requirements.txt
   
   # Or using standard pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   touch .env
   
   # Add your Gemini API key
   echo "GEMINI_API_KEY=your_actual_api_key_here" >> .env
   ```

5. **Run the basic example**
   ```bash
   python examples/basic_example.py
   ```

## 📁 Project Structure

```
gemini-pydantic-tutorial/
├── 📄 README.md              # This file
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env                   # Environment variables (create this)
├── 📄 .gitignore            # Git ignore rules
├── 📄 main.py               # Main application entry point
│
├── 📁 config/               # Configuration management
│   ├── __init__.py
│   └── settings.py          # App settings and environment variables
│
├── 📁 models/               # Pydantic data models
│   ├── __init__.py
│   └── library.py           # Book and Library models with validation
│
├── 📁 services/             # Core business logic
│   ├── __init__.py
│   ├── gemini_client.py     # Gemini API client
│   └── data_processor.py    # Data processing pipeline
│
├── 📁 utils/                # Utility functions
│   ├── __init__.py
│   ├── json_cleaner.py      # JSON cleaning and validation
│   └── file_manager.py      # File I/O operations
│
├── 📁 analysis/             # Data analysis and visualization
│   ├── __init__.py
│   ├── data_analyzer.py     # Statistical analysis functions
│   └── visualizer.py        # Chart and graph generation
│
├── 📁 examples/             # Example usage scripts
│   ├── basic_example.py     # Simple usage demonstration
│   └── advanced_example.py  # Complex analysis example
│
└── 📁 output/               # Generated files (created automatically)
    ├── *.json               # Generated library data
    ├── *.csv                # Exported datasets
    └── *.png                # Visualization charts
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=1000
OUTPUT_DIR=output
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Navigate to the API section
4. Generate a new API key
5. Copy the key to your `.env` file

**Important**: Keep your API key secure and never commit it to version control!

## 📚 Usage Examples

### Basic Usage

```python
from services.data_processor import DataProcessor
from utils.file_manager import FileManager

# Initialize components
processor = DataProcessor()
file_manager = FileManager()

# Generate library data
library = processor.generate_and_parse_library(num_books=5)

# Work with the structured data
print(f"Library: {library.name}")
for book in library.books:
    print(f"  - {book.title} by {book.author} ({book.year})")

# Save to file
file_manager.save_library_json(library)
```

### Advanced Analysis

```python
from analysis.data_analyzer import LibraryAnalyzer
from analysis.visualizer import LibraryVisualizer

# Analyze the data
analyzer = LibraryAnalyzer()
visualizer = LibraryVisualizer()

# Generate comprehensive report
report = analyzer.generate_report(library)
print(report)

# Create visualizations
visualizer.create_all_visualizations(library)
```

### Custom Data Models

```python
from pydantic import BaseModel, Field
from typing import List

class CustomBook(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=1000, le=2025)
    genre: str = Field(default="Unknown")
    isbn: str = Field(regex=r'^\d{10}(\d{3})?$', default="")

# Use with the data processor
processor = DataProcessor()
# ... custom implementation
```

## 🔍 API Reference

### Core Classes

#### `DataProcessor`
Main orchestrator for the data generation and validation pipeline.

```python
class DataProcessor:
    def generate_and_parse_library(self, num_books: int = 5) -> Optional[Library]
    def parse_json_to_library(self, json_string: str) -> Optional[Library]
    def library_to_dict(self, library: Library) -> dict
    def library_to_json(self, library: Library, indent: int = 4) -> str
```

#### `LibraryAnalyzer`
Provides statistical analysis and reporting capabilities.

```python
class LibraryAnalyzer:
    def library_to_dataframe(self, library: Library) -> pd.DataFrame
    def basic_statistics(self, library: Library) -> Dict[str, Any]
    def decade_analysis(self, library: Library) -> Dict[str, int]
    def age_analysis(self, library: Library) -> Dict[str, Any]
    def generate_report(self, library: Library) -> str
```

#### `LibraryVisualizer`
Creates charts and visualizations for library data.

```python
class LibraryVisualizer:
    def plot_publication_years(self, library: Library, save: bool = True)
    def plot_books_by_decade(self, library: Library, save: bool = True)
    def plot_comprehensive_analysis(self, library: Library, save: bool = True)
    def create_all_visualizations(self, library: Library, save: bool = True)
```

### Data Models

#### `Book`
Represents a single book with validation.

```python
class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(gt=1000, le=current_year)
```

#### `Library`
Represents a collection of books with analysis methods.

```python
class Library(BaseModel):
    name: str = Field(min_length=1)
    books: List[Book]
    
    def get_books_by_author(self, author: str) -> List[Book]
    def get_books_after_year(self, year: int) -> List[Book]
    def get_average_publication_year(self) -> float
```

## 📊 Example Output

### Generated Library Data
```json
{
  "name": "The Grand Archive",
  "books": [
    {
      "title": "The Time Machine",
      "author": "H.G. Wells",
      "year": 1895
    },
    {
      "title": "Dune",
      "author": "Frank Herbert",
      "year": 1965
    }
  ]
}
```

### Analysis Report
```
📚 LIBRARY ANALYSIS REPORT
==================================================

Library: The Grand Archive
Total Books: 5
Unique Authors: 5

📅 TEMPORAL ANALYSIS
Publication Range: 1895 - 2019
Average Publication Year: 1952.4
Median Publication Year: 1965

📊 BOOKS BY DECADE:
  1890s: 1 book(s)
  1960s: 1 book(s)
  1980s: 1 book(s)
  2010s: 2 book(s)
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes with tests
3. Update documentation
4. Submit pull request

## 🚨 Troubleshooting

### Common Issues

#### API Key Not Found
```
ValueError: GEMINI_API_KEY not found in environment variables
```
**Solution**: Ensure your `.env` file exists and contains the API key.

#### JSON Parsing Errors
```
ValueError: Invalid JSON format: Expecting property name enclosed in double quotes
```
**Solution**: The JSON cleaner should handle this automatically. Check the raw response for unusual formatting.

#### Pydantic Validation Errors
```
ValidationError: 1 validation error for Library
```
**Solution**: Check that the generated data matches your model schema. Year values are commonly problematic.

#### Import Errors
```
ModuleNotFoundError: No module named 'matplotlib'
```
**Solution**: Install missing dependencies:
```bash
pip install matplotlib  # or the specific missing package
```

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export DEBUG=True
```

## 📈 Performance Considerations

### API Rate Limits
- Free tier: 15 requests per minute
- Monitor usage in Google AI Studio
- Implement retry logic for production use

### Memory Usage
- Large datasets may require chunking
- Consider using generators for processing many records
- Monitor memory usage with complex analyses

### Optimization Tips
- Cache API responses during development
- Batch multiple requests when possible
- Use async/await for concurrent processing

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure type hints are included
- Write clear commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI** for providing the Gemini API
- **Pydantic** for excellent data validation capabilities
- **Python Community** for the amazing ecosystem of libraries
- **Contributors** who help improve this project

## 📞 Support