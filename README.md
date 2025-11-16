# Codebase Analyzer

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)
[![Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)
[![PyPI](https://img.shields.io/badge/pip-installable-brightgreen.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)

A comprehensive CLI tool for analyzing codebases. Scan your projects to get insights into code quality, technical debt, complexity metrics, test coverage, and more. Zero external dependencies required.

## Overview

Codebase Analyzer provides detailed statistics about your project structure, helping you identify areas that need attention before they become problems. It performs static analysis on your source code and generates actionable reports with quality scores and recommendations.

## Key Features

### Code Statistics
- Lines of code breakdown by programming language
- File size distribution and analysis
- Project structure overview with detailed metrics
- Automatic detection of 20+ programming languages

### Quality Analysis
- Overall quality score with A-F letter grading
- TODO/FIXME/HACK comment tracking
- Test coverage estimation
- Documentation coverage metrics
- Cyclomatic complexity analysis
- Missing documentation warnings

### Technical Debt Detection
- Dependency analysis (internal vs external imports)
- Configuration file scanning
- Circular dependency detection
- Code smell identification
- Security pattern analysis

### Smart Filtering
Automatically excludes build artifacts and common non-source directories:
- Python cache (`__pycache__`, `*.pyc`)
- Virtual environments (`venv`, `.venv`, `env`)
- Node modules and package dependencies
- Build outputs (`.o`, `.so`, `.dll`, etc.)
- Hidden files and system directories

### Export Options
- JSON format for programmatic access
- Plain text reports with formatted tables
- Colored terminal output with progress indicators
- Detailed recommendations and actionable insights

## Installation

### Via pip (recommended)

```bash
# Install from local directory (inside CodeBase_Analyzer_v2 folder)
pip install -e .

# After installation, use the command anywhere
codebase-analyzer --help
# or use the shorter alias
cba --help

# Alternative: run as module (always works)
python -m cli --help
```

**Note:** If you get a PATH warning during installation, you can either:
1. Add the Scripts directory to your PATH (recommended)
2. Use `python -m cli` instead of `codebase-analyzer`

### Direct usage (without installation)

Clone the repository and run directly:

```bash
git clone https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2.git
cd Codebase_Analyzer_v2
python cli.py --help
```

**Requirements:**
- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Quick Start

### After pip installation

```bash
# Analyze current directory
codebase-analyzer .

# Full analysis with all features enabled
codebase-analyzer . --advanced

# Analyze specific project with export
codebase-analyzer /path/to/project --advanced --export json --output report.json

# Enable specific analyzers only
codebase-analyzer . --todos --dependencies --tests --complexity

# Use the shorter alias
cba . --advanced
```

### Without installation

```bash
# Analyze current directory
python cli.py .

# Full analysis with all features enabled
python cli.py . --advanced

# Analyze specific project with export
python cli.py /path/to/project --advanced --export json --output report.json

# Enable specific analyzers only
python cli.py . --todos --dependencies --tests --complexity
```

## Usage

### Basic Analysis

```bash
# Simple mode - basic statistics only
codebase-analyzer /path/to/project
# Or without pip install:
python cli.py /path/to/project

# Advanced mode - all analyzers enabled
codebase-analyzer . --advanced
# Or without pip install:
python cli.py . --advanced
```

### Selective Analysis

```bash
# Track TODO comments
codebase-analyzer . --todos
# Or: python cli.py . --todos

# Analyze dependencies
codebase-analyzer . --dependencies
# Or: python cli.py . --dependencies

# Check test coverage
codebase-analyzer . --tests
# Or: python cli.py . --tests

# Calculate complexity metrics
codebase-analyzer . --complexity
# Or: python cli.py . --complexity

# Combine multiple analyzers
codebase-analyzer . --todos --tests --docs --quality
# Or: python cli.py . --todos --tests --docs --quality
```

### Export Reports

```bash
# Export to JSON
codebase-analyzer . --advanced --export json --output report.json
# Or: python cli.py . --advanced --export json --output report.json

# Export to text file
codebase-analyzer . --export report.txt
# Or: python cli.py . --export report.txt

# Disable progress bars for cleaner output
codebase-analyzer . --no-progress --no-color > analysis.txt
# Or: python cli.py . --no-progress --no-color > analysis.txt
```

### Programmatic Usage

See `examples/basic_usage.py` for examples of using the analyzer in your own Python code:

```python
from codebase_analyzer_v2.core.analyzer_v2 import AdvancedCodebaseAnalyzer

analyzer = AdvancedCodebaseAnalyzer(
    enable_quality=True, 
    enable_complexity=True,
    show_progress=True
)
report = analyzer.analyze()
print(report)
```

## Command-Line Options

```
positional arguments:
  path                  Directory to analyze (default: current directory)

mode options:
  --simple              Basic statistics only (default)
  --advanced            Enable all analyzers

feature flags:
  --todos               Track TODO/FIXME/HACK comments
  --dependencies        Analyze imports and dependencies
  --tests               Estimate test coverage
  --docs                Check documentation coverage
  --config              Scan configuration files
  --quality             Calculate quality score
  --complexity          Analyze cyclomatic complexity

output options:
  --export FORMAT       Export format: json
  --output FILE         Output file path
  --no-progress         Disable progress bars
  --no-color            Disable colored output
```

## Supported Languages

The analyzer automatically detects and categorizes these languages:

**Programming Languages:**
Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala

**Web Technologies:**
HTML, CSS, SCSS, SASS, LESS

**Data & Config:**
JSON, YAML, TOML, XML, INI, ENV

**Query & Shell:**
SQL, Bash, PowerShell, Shell scripts

**Documentation:**
Markdown, ReStructuredText

## Output Structure

Analysis reports include:

1. **Overall Statistics** - Total size, file count, directory count, lines of code
2. **Language Breakdown** - Lines, files, and size distribution per language
3. **File Analysis** - Largest files, longest files, outlier detection
4. **Quality Metrics** - Test coverage, documentation score, complexity ratings
5. **Technical Debt** - TODOs, dependencies, configuration issues
6. **Recommendations** - Actionable improvements based on analysis

## Project Architecture

```
codebase_analyzer_v2/
├── cli.py                      # Command-line interface
├── core/
│   ├── base_analyzer.py        # File scanning and basic statistics
│   └── analyzer_v2.py          # Advanced analysis orchestration
├── analyzers/
│   ├── todo_tracker.py         # TODO/FIXME/HACK detection
│   ├── dependency_analyzer.py  # Import and dependency analysis
│   ├── test_analyzer.py        # Test coverage estimation
│   ├── doc_analyzer.py         # Documentation coverage checker
│   ├── config_analyzer.py      # Configuration file scanner
│   ├── complexity_analyzer.py  # Cyclomatic complexity calculator
│   └── quality_scorer.py       # Overall quality scoring
├── formatters/
│   └── advanced_formatter.py   # Report formatting and display
├── exporters/
│   └── json_exporter.py        # JSON export functionality
├── utils/
│   ├── colors.py               # Cross-platform terminal colors
│   └── progress.py             # Progress bar utilities
├── examples/
│   └── basic_usage.py          # Programmatic usage examples
├── tests/
│   ├── test_complexity_samples.py      # Complexity test samples
│   └── test_complexity_validation.py   # Complexity validation tests
└── debug/
    └── debug_complexity.py     # Complexity debugging utilities
```

## Quality Scoring

The advanced mode calculates an overall quality score (0-100) based on:

- **Test Coverage** - Presence and distribution of test files
- **Documentation** - README files, docstrings, inline comments
- **Code Organization** - File structure, naming conventions, modularity
- **Technical Debt** - TODO count, complexity metrics, configuration issues
- **Security** - Hardcoded secrets detection, unsafe patterns

Scores are translated to letter grades:
- A: 90-100 (Excellent)
- B: 80-89 (Good)
- C: 70-79 (Fair)
- D: 60-69 (Needs Improvement)
- F: 0-59 (Critical Issues)

## Platform Support

Works on all major operating systems:
- Windows (PowerShell, CMD)
- Linux (all distributions)
- macOS

Handles platform-specific file paths and encodings automatically.

## Performance

- Efficient file scanning with smart filtering
- Progress bars for large projects
- Typical analysis time: 1-5 seconds for projects under 10,000 files
- Memory efficient - processes files in streaming mode

## Safety

This tool only reads files and never modifies your source code:
- Read-only file access
- Graceful handling of encoding issues
- Automatic binary file detection and exclusion
- Safe to run on production codebases

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features or analyzers
- Submit pull requests
- Improve documentation

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with Python standard library only. No external dependencies required.
