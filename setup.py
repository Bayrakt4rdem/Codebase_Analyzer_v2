"""
Setup configuration for Codebase Analyzer v2
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="codebase-analyzer-v2",
    version="2.0.0",
    author="Bayrakt4rdem",
    author_email="",
    description="A comprehensive CLI tool for analyzing codebases with quality metrics and technical debt detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*", "examples", "examples.*", "debug", "debug.*", "memory-bank", "memory-bank.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "pylint>=2.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "codebase-analyzer=cli:main",
            "cba=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
    keywords=[
        "code-analysis",
        "static-analysis",
        "code-quality",
        "technical-debt",
        "complexity-analysis",
        "codebase-metrics",
        "code-metrics",
        "quality-score",
        "cyclomatic-complexity",
        "test-coverage",
        "documentation-coverage",
        "dependency-analysis",
        "todo-tracker",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2/issues",
        "Source": "https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2",
        "Documentation": "https://github.com/Bayrakt4rdem/Codebase_Analyzer_v2/blob/main/docs/README.md",
    },
)
