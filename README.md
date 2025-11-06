# Codebase Analyzer# Codebase Analyzer



A Python CLI tool for analyzing codebases. Get insights into your project structure, code quality, technical debt, and more.A comprehensive CLI tool for analyzing project codebases, providing detailed statistics about file counts, sizes, lines of code, and more.



## What it does## Features



This tool scans your project and gives you detailed statistics about code organization, test coverage, documentation, dependencies, and potential issues. It helps identify areas that need attention before they become problems.- **Overall Statistics**

  - Total size (in human-readable format)

## Quick Start  - Total file count

  - Total directory count

```bash  - Total lines of code

# Basic analysis  - Average lines per file

python cli.py .

- **Language Analysis**

# Full analysis with all features  - Lines of code by programming language

python cli.py . --advanced  - File count by language

  - Size by language

# Specific features only  - Percentage distribution

python cli.py . --todos --dependencies --tests

```- **File Analysis**

  - Top 10 largest files (by size)

No installation needed - pure Python stdlib, zero dependencies.  - Top 10 longest files (by line count)

  - Top 10 shortest files

## Features  - Files that are potentially too long (>3x average)

  - Files that are potentially too short (<10 lines)

**Code Statistics**

- Lines of code by language- **Smart Filtering**

- File size distribution  - Automatically excludes:

- Project structure overview    - `__pycache__` directories and `.pyc` files

    - Virtual environments (`venv`, `.venv`, `env`)

**Quality Analysis**    - Node modules

- TODO/FIXME/HACK tracking    - Build artifacts (`.o`, `.so`, `.dll`, etc.)

- Test coverage estimation    - Hidden files and directories

- Documentation coverage    - Lock files and logs

- Cyclomatic complexity metrics  - Separately tracks size of:

- Overall quality score (A-F grading)    - `__pycache__` directories

    - Virtual environment directories

**Technical Debt**    - All ignored/cached files

- Dependency analysis (internal vs external)

- Configuration file scanning- **Export Support**

- Circular dependency detection  - Export reports to text files

- Missing documentation warnings  - Console output with formatted tables



**Export Options**## Installation

- JSON format for programmatic access

- Colored terminal output with progress barsNo external dependencies required! Uses only Python standard library.

- Detailed reports with recommendations

## Usage

## Usage Examples

### Basic Usage

```bash

# Simple mode (default)```bash

python cli.py /path/to/project# Analyze current directory

python cli.py

# Advanced mode with everything

python cli.py . --advanced# Analyze specific directory

python cli.py /path/to/project

# Complexity analysis

python cli.py . --complexity# Analyze relative path

python cli.py ../my-project

# Export to JSON```

python cli.py . --advanced --export json --output report.json

### Export Report

# Specific analyzers

python cli.py . --todos --dependencies --docs --tests```bash

```# Export to text file

python cli.py . --export report.txt

## What gets analyzed

# Export analysis of another project

The tool automatically detects and analyzes:python cli.py ../another-project --export analysis.txt

- Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Rust, Ruby, PHP```

- HTML, CSS, SQL, Shell scripts

- Config files (JSON, YAML, TOML, INI, .env)### Help

- Documentation (Markdown, README files)

```bash

It intelligently skips build artifacts, virtual environments, node_modules, and other non-source files.python cli.py --help

```

## Quality Scoring

## Examples

The advanced mode calculates an overall quality score based on:

- Test coverage (do you have tests?)### Analyzing Current Project

- Documentation (README, docstrings, comments)

- Code organization (file structure, naming)```bash

- Technical debt (TODOs, complexity, config issues)cd CodeBase_Analyzer_v2

- Security (hardcoded secrets, unsafe patterns)python cli.py .

```

You'll get a letter grade (A-F) and specific recommendations for improvement.

### Analyzing Another Project

## Command-line Options

```bash

```python cli.py ../my-project

positional arguments:```

  path                  Directory to analyze (default: current dir)

### Quick Analysis with Export

mode options:

  --simple              Basic stats only (default)```bash

  --advanced            Enable all analyzers# Analyze and export to JSON

python cli.py . --export json --output report.json

feature flags:```

  --todos               Track TODO/FIXME/HACK comments

  --dependencies        Analyze imports and dependencies## Output Format

  --tests               Estimate test coverage

  --docs                Check documentation coverageThe tool provides a well-formatted report with the following sections:

  --config              Scan configuration files

  --quality             Calculate quality score1. **Overall Statistics** - Total size, files, directories, lines

  --complexity          Analyze cyclomatic complexity2. **Ignored/Cache Sizes** - Size of __pycache__, venv, and other ignored items

3. **Lines of Code by Language** - Breakdown with percentages

output options:4. **File Count by Language** - Distribution of files

  --export FORMAT       Export format (json)5. **Top Largest Files** - Files taking up most disk space

  --output FILE         Output file path6. **Top Longest Files** - Files with most lines of code

  --no-progress         Disable progress bars7. **Potentially Too Long Files** - Files exceeding 3x average length

  --no-color            Disable colored output8. **Top Shortest Files** - Smallest files by line count

```9. **Potentially Too Short Files** - Files with less than 10 lines



## Project Structure## Supported Languages



```The analyzer recognizes and categorizes the following languages:

codebase_analyzer_v2/

├── cli.py                      # Command-line interface- Python, JavaScript, TypeScript

├── core/- Java, C++, C, C#

│   ├── base_analyzer.py        # File scanning and basic stats- Go, Rust, Ruby, PHP

│   └── analyzer_v2.py          # Advanced analysis orchestrator- Swift, Kotlin

├── analyzers/- HTML, CSS, SQL

│   ├── todo_tracker.py         # TODO/FIXME finder- Shell, PowerShell

│   ├── dependency_analyzer.py  # Import analysis- Markdown, YAML, JSON, XML

│   ├── test_analyzer.py        # Test coverage estimator- TOML, INI

│   ├── doc_analyzer.py         # Documentation checker- And more...

│   ├── config_analyzer.py      # Config file scanner

│   ├── complexity_analyzer.py  # Cyclomatic complexity## Architecture

│   └── quality_scorer.py       # Overall quality grading

├── formatters/- `analyzer.py` - Core analysis logic

│   └── advanced_formatter.py   # Report formatting- `formatter.py` - Report formatting and display

├── exporters/- `cli.py` - Command-line interface

│   └── json_exporter.py        # JSON export- `__init__.py` - Package initialization

└── utils/

    ├── colors.py               # Terminal colors (cross-platform)## Requirements

    └── progress.py             # Progress bars

```- Python 3.6 or higher

- No external dependencies

## Requirements

## Notes

- Python 3.6+

- No external dependencies- The tool automatically handles encoding issues when reading files

- Binary files are properly detected and excluded from line counts

Works on Windows, Linux, and macOS.- Large codebases may take a few moments to analyze

- The tool is safe to run and only reads files (no modifications)

## Notes

The tool only reads files, never modifies anything. It handles encoding issues gracefully and skips binary files automatically. Large projects may take a minute to analyze - progress bars keep you updated.

If you find bugs or have feature requests, contributions are welcome.
