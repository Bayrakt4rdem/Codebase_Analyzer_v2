# Codebase Analyzer# Codebase Analyzer# Codebase Analyzer



[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)A Python CLI tool for analyzing codebases. Get insights into your project structure, code quality, technical debt, and more.A comprehensive CLI tool for analyzing project codebases, providing detailed statistics about file counts, sizes, lines of code, and more.

[![Dependencies](https://img.shields.io/badge/dependencies-0-success.svg)](https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2)



A comprehensive CLI tool for analyzing codebases. Scan your projects to get insights into code quality, technical debt, complexity metrics, test coverage, and more. Zero external dependencies required.

## What it does## Features

## Overview



Codebase Analyzer provides detailed statistics about your project structure, helping you identify areas that need attention before they become problems. It performs static analysis on your source code and generates actionable reports with quality scores and recommendations.

This tool scans your project and gives you detailed statistics about code organization, test coverage, documentation, dependencies, and potential issues. It helps identify areas that need attention before they become problems.- **Overall Statistics**

## Key Features

  - Total size (in human-readable format)

### Code Statistics

- Lines of code breakdown by programming language## Quick Start  - Total file count

- File size distribution and analysis

- Project structure overview with detailed metrics  - Total directory count

- Automatic detection of 20+ programming languages

```bash  - Total lines of code

### Quality Analysis

- Overall quality score with A-F letter grading# Basic analysis  - Average lines per file

- TODO/FIXME/HACK comment tracking

- Test coverage estimationpython cli.py .

- Documentation coverage metrics

- Cyclomatic complexity analysis- **Language Analysis**

- Missing documentation warnings

# Full analysis with all features  - Lines of code by programming language

### Technical Debt Detection

- Dependency analysis (internal vs external imports)python cli.py . --advanced  - File count by language

- Configuration file scanning

- Circular dependency detection  - Size by language

- Code smell identification

- Security pattern analysis# Specific features only  - Percentage distribution



### Smart Filteringpython cli.py . --todos --dependencies --tests

Automatically excludes build artifacts and common non-source directories:

- Python cache (`__pycache__`, `*.pyc`)```- **File Analysis**

- Virtual environments (`venv`, `.venv`, `env`)

- Node modules and package dependencies  - Top 10 largest files (by size)

- Build outputs (`.o`, `.so`, `.dll`, etc.)

- Hidden files and system directoriesNo installation needed - pure Python stdlib, zero dependencies.  - Top 10 longest files (by line count)



### Export Options  - Top 10 shortest files

- JSON format for programmatic access

- Plain text reports with formatted tables## Features  - Files that are potentially too long (>3x average)

- Colored terminal output with progress indicators

- Detailed recommendations and actionable insights  - Files that are potentially too short (<10 lines)



## Installation**Code Statistics**



No installation required. Clone the repository and run directly:- Lines of code by language- **Smart Filtering**



```bash- File size distribution  - Automatically excludes:

git clone https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2.git

cd Codebase_Analyzer_v2- Project structure overview    - `__pycache__` directories and `.pyc` files

python cli.py --help

```    - Virtual environments (`venv`, `.venv`, `env`)



**Requirements:****Quality Analysis**    - Node modules

- Python 3.6 or higher

- No external dependencies (uses Python standard library only)- TODO/FIXME/HACK tracking    - Build artifacts (`.o`, `.so`, `.dll`, etc.)



## Quick Start- Test coverage estimation    - Hidden files and directories



```bash- Documentation coverage    - Lock files and logs

# Analyze current directory

python cli.py .- Cyclomatic complexity metrics  - Separately tracks size of:



# Full analysis with all features enabled- Overall quality score (A-F grading)    - `__pycache__` directories

python cli.py . --advanced

    - Virtual environment directories

# Analyze specific project with export

python cli.py /path/to/project --advanced --export json --output report.json**Technical Debt**    - All ignored/cached files



# Enable specific analyzers only- Dependency analysis (internal vs external)

python cli.py . --todos --dependencies --tests --complexity

```- Configuration file scanning- **Export Support**



## Usage- Circular dependency detection  - Export reports to text files



### Basic Analysis- Missing documentation warnings  - Console output with formatted tables



```bash

# Simple mode - basic statistics only

python cli.py /path/to/project**Export Options**## Installation



# Advanced mode - all analyzers enabled- JSON format for programmatic access

python cli.py . --advanced

```- Colored terminal output with progress barsNo external dependencies required! Uses only Python standard library.



### Selective Analysis- Detailed reports with recommendations



```bash## Usage

# Track TODO comments

python cli.py . --todos## Usage Examples



# Analyze dependencies### Basic Usage

python cli.py . --dependencies

```bash

# Check test coverage

python cli.py . --tests# Simple mode (default)```bash



# Calculate complexity metricspython cli.py /path/to/project# Analyze current directory

python cli.py . --complexity

python cli.py

# Combine multiple analyzers

python cli.py . --todos --tests --docs --quality# Advanced mode with everything

```

python cli.py . --advanced# Analyze specific directory

### Export Reports

python cli.py /path/to/project

```bash

# Export to JSON# Complexity analysis

python cli.py . --advanced --export json --output report.json

python cli.py . --complexity# Analyze relative path

# Export to text file

python cli.py . --export report.txtpython cli.py ../my-project



# Disable progress bars for cleaner output# Export to JSON```

python cli.py . --no-progress --no-color > analysis.txt

```python cli.py . --advanced --export json --output report.json



### Programmatic Usage### Export Report



See `examples/basic_usage.py` for examples of using the analyzer in your own Python code:# Specific analyzers



```pythonpython cli.py . --todos --dependencies --docs --tests```bash

from core.analyzer_v2 import AdvancedCodebaseAnalyzer

```# Export to text file

analyzer = AdvancedCodebaseAnalyzer(enable_quality=True, enable_complexity=True)

base_results, advanced_results = analyzer.analyze_advanced("./my-project")python cli.py . --export report.txt

```

## What gets analyzed

## Command-Line Options

# Export analysis of another project

```

positional arguments:The tool automatically detects and analyzes:python cli.py ../another-project --export analysis.txt

  path                  Directory to analyze (default: current directory)

- Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Rust, Ruby, PHP```

mode options:

  --simple              Basic statistics only (default)- HTML, CSS, SQL, Shell scripts

  --advanced            Enable all analyzers

- Config files (JSON, YAML, TOML, INI, .env)### Help

feature flags:

  --todos               Track TODO/FIXME/HACK comments- Documentation (Markdown, README files)

  --dependencies        Analyze imports and dependencies

  --tests               Estimate test coverage```bash

  --docs                Check documentation coverage

  --config              Scan configuration filesIt intelligently skips build artifacts, virtual environments, node_modules, and other non-source files.python cli.py --help

  --quality             Calculate quality score

  --complexity          Analyze cyclomatic complexity```



output options:## Quality Scoring

  --export FORMAT       Export format: json

  --output FILE         Output file path## Examples

  --no-progress         Disable progress bars

  --no-color            Disable colored outputThe advanced mode calculates an overall quality score based on:

```

- Test coverage (do you have tests?)### Analyzing Current Project

## Supported Languages

- Documentation (README, docstrings, comments)

The analyzer automatically detects and categorizes these languages:

- Code organization (file structure, naming)```bash

**Programming Languages:**

Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala- Technical debt (TODOs, complexity, config issues)cd CodeBase_Analyzer_v2



**Web Technologies:**- Security (hardcoded secrets, unsafe patterns)python cli.py .

HTML, CSS, SCSS, SASS, LESS

```

**Data & Config:**

JSON, YAML, TOML, XML, INI, ENVYou'll get a letter grade (A-F) and specific recommendations for improvement.



**Query & Shell:**### Analyzing Another Project

SQL, Bash, PowerShell, Shell scripts

## Command-line Options

**Documentation:**

Markdown, ReStructuredText```bash



## Output Structure```python cli.py ../my-project



Analysis reports include:positional arguments:```



1. **Overall Statistics** - Total size, file count, directory count, lines of code  path                  Directory to analyze (default: current dir)

2. **Language Breakdown** - Lines, files, and size distribution per language

3. **File Analysis** - Largest files, longest files, outlier detection### Quick Analysis with Export

4. **Quality Metrics** - Test coverage, documentation score, complexity ratings

5. **Technical Debt** - TODOs, dependencies, configuration issuesmode options:

6. **Recommendations** - Actionable improvements based on analysis

  --simple              Basic stats only (default)```bash

## Project Architecture

  --advanced            Enable all analyzers# Analyze and export to JSON

```

codebase_analyzer_v2/python cli.py . --export json --output report.json

├── cli.py                      # Command-line interface

├── core/feature flags:```

│   ├── base_analyzer.py        # File scanning and basic statistics

│   └── analyzer_v2.py          # Advanced analysis orchestration  --todos               Track TODO/FIXME/HACK comments

├── analyzers/

│   ├── todo_tracker.py         # TODO/FIXME/HACK detection  --dependencies        Analyze imports and dependencies## Output Format

│   ├── dependency_analyzer.py  # Import and dependency analysis

│   ├── test_analyzer.py        # Test coverage estimation  --tests               Estimate test coverage

│   ├── doc_analyzer.py         # Documentation coverage checker

│   ├── config_analyzer.py      # Configuration file scanner  --docs                Check documentation coverageThe tool provides a well-formatted report with the following sections:

│   ├── complexity_analyzer.py  # Cyclomatic complexity calculator

│   └── quality_scorer.py       # Overall quality scoring  --config              Scan configuration files

├── formatters/

│   └── advanced_formatter.py   # Report formatting and display  --quality             Calculate quality score1. **Overall Statistics** - Total size, files, directories, lines

├── exporters/

│   └── json_exporter.py        # JSON export functionality  --complexity          Analyze cyclomatic complexity2. **Ignored/Cache Sizes** - Size of __pycache__, venv, and other ignored items

├── utils/

│   ├── colors.py               # Cross-platform terminal colors3. **Lines of Code by Language** - Breakdown with percentages

│   └── progress.py             # Progress bar utilities

├── examples/output options:4. **File Count by Language** - Distribution of files

│   └── basic_usage.py          # Programmatic usage examples

├── tests/  --export FORMAT       Export format (json)5. **Top Largest Files** - Files taking up most disk space

│   ├── test_complexity_samples.py      # Complexity test samples

│   └── test_complexity_validation.py   # Complexity validation tests  --output FILE         Output file path6. **Top Longest Files** - Files with most lines of code

└── debug/

    └── debug_complexity.py     # Complexity debugging utilities  --no-progress         Disable progress bars7. **Potentially Too Long Files** - Files exceeding 3x average length

```

  --no-color            Disable colored output8. **Top Shortest Files** - Smallest files by line count

## Quality Scoring

```9. **Potentially Too Short Files** - Files with less than 10 lines

The advanced mode calculates an overall quality score (0-100) based on:



- **Test Coverage** - Presence and distribution of test files

- **Documentation** - README files, docstrings, inline comments## Project Structure## Supported Languages

- **Code Organization** - File structure, naming conventions, modularity

- **Technical Debt** - TODO count, complexity metrics, configuration issues

- **Security** - Hardcoded secrets detection, unsafe patterns

```The analyzer recognizes and categorizes the following languages:

Scores are translated to letter grades:

- A: 90-100 (Excellent)codebase_analyzer_v2/

- B: 80-89 (Good)

- C: 70-79 (Fair)├── cli.py                      # Command-line interface- Python, JavaScript, TypeScript

- D: 60-69 (Needs Improvement)

- F: 0-59 (Critical Issues)├── core/- Java, C++, C, C#



## Platform Support│   ├── base_analyzer.py        # File scanning and basic stats- Go, Rust, Ruby, PHP



Works on all major operating systems:│   └── analyzer_v2.py          # Advanced analysis orchestrator- Swift, Kotlin

- Windows (PowerShell, CMD)

- Linux (all distributions)├── analyzers/- HTML, CSS, SQL

- macOS

│   ├── todo_tracker.py         # TODO/FIXME finder- Shell, PowerShell

Handles platform-specific file paths and encodings automatically.

│   ├── dependency_analyzer.py  # Import analysis- Markdown, YAML, JSON, XML

## Performance

│   ├── test_analyzer.py        # Test coverage estimator- TOML, INI

- Efficient file scanning with smart filtering

- Progress bars for large projects│   ├── doc_analyzer.py         # Documentation checker- And more...

- Typical analysis time: 1-5 seconds for projects under 10,000 files

- Memory efficient - processes files in streaming mode│   ├── config_analyzer.py      # Config file scanner



## Safety│   ├── complexity_analyzer.py  # Cyclomatic complexity## Architecture



This tool only reads files and never modifies your source code:│   └── quality_scorer.py       # Overall quality grading

- Read-only file access

- Graceful handling of encoding issues├── formatters/- `analyzer.py` - Core analysis logic

- Automatic binary file detection and exclusion

- Safe to run on production codebases│   └── advanced_formatter.py   # Report formatting- `formatter.py` - Report formatting and display



## Contributing├── exporters/- `cli.py` - Command-line interface



Contributions are welcome! Feel free to:│   └── json_exporter.py        # JSON export- `__init__.py` - Package initialization

- Report bugs or issues

- Suggest new features or analyzers└── utils/

- Submit pull requests

- Improve documentation    ├── colors.py               # Terminal colors (cross-platform)## Requirements



## License    └── progress.py             # Progress bars



MIT License - see LICENSE file for details```- Python 3.6 or higher



## Acknowledgments- No external dependencies



Built with Python standard library only. No external dependencies required.## Requirements


## Notes

- Python 3.6+

- No external dependencies- The tool automatically handles encoding issues when reading files

- Binary files are properly detected and excluded from line counts

Works on Windows, Linux, and macOS.- Large codebases may take a few moments to analyze

- The tool is safe to run and only reads files (no modifications)

## Notes

The tool only reads files, never modifies anything. It handles encoding issues gracefully and skips binary files automatically. Large projects may take a minute to analyze - progress bars keep you updated.

If you find bugs or have feature requests, contributions are welcome.
