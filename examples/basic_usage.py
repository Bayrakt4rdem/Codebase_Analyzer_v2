#!/usr/bin/env python3
"""
Basic usage example for Codebase Analyzer.

This example demonstrates how to use the analyzer programmatically
instead of using the CLI interface.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the analyzer
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_analyzer import CodebaseAnalyzer
from core.analyzer_v2 import AdvancedCodebaseAnalyzer
from formatters.advanced_formatter import AdvancedReportFormatter


def simple_analysis_example():
    """Example: Simple codebase analysis with basic statistics."""
    print("=" * 60)
    print("EXAMPLE 1: Simple Analysis")
    print("=" * 60)
    
    # Initialize the basic analyzer
    analyzer = CodebaseAnalyzer()
    
    # Analyze current directory (or specify a path)
    project_path = "."
    results = analyzer.analyze(project_path)
    
    # Print basic statistics
    print(f"\nProject: {project_path}")
    print(f"Total Files: {results['total_files']}")
    print(f"Total Size: {results['total_size_human']}")
    print(f"Total Lines: {results['total_lines']}")
    
    print("\nLines by Language:")
    for lang, lines in sorted(results['lines_by_language'].items(), 
                              key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {lang}: {lines:,} lines")
    
    print("\nTop 5 Largest Files:")
    for file_path, size in results['largest_files'][:5]:
        size_mb = size / (1024 * 1024)
        print(f"  {file_path}: {size_mb:.2f} MB")


def advanced_analysis_example():
    """Example: Advanced analysis with quality metrics and TODO tracking."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Advanced Analysis")
    print("=" * 60)
    
    # Initialize the advanced analyzer with all features
    analyzer = AdvancedCodebaseAnalyzer(
        enable_todos=True,
        enable_dependencies=True,
        enable_tests=True,
        enable_docs=True,
        enable_config=True,
        enable_quality=True,
        enable_complexity=True
    )
    
    # Analyze the project
    project_path = "."
    base_results, advanced_results = analyzer.analyze_advanced(project_path)
    
    # Print quality score
    if advanced_results and 'quality_score' in advanced_results:
        quality = advanced_results['quality_score']
        print(f"\nQuality Score: {quality['score']:.1f}/100 (Grade: {quality['grade']})")
        print(f"  Test Coverage: {quality['test_coverage']}/100")
        print(f"  Documentation: {quality['documentation']}/100")
        print(f"  Code Organization: {quality['code_organization']}/100")
    
    # Print TODO summary
    if advanced_results and 'todos' in advanced_results:
        todos = advanced_results['todos']
        total_todos = sum(len(items) for items in todos.values())
        print(f"\nTODO Items Found: {total_todos}")
        for marker, items in todos.items():
            if items:
                print(f"  {marker}: {len(items)}")
    
    # Print test coverage
    if advanced_results and 'tests' in advanced_results:
        tests = advanced_results['tests']
        print(f"\nTest Files: {tests['test_file_count']}")
        print(f"Test Coverage: {tests['coverage_percentage']:.1f}%")


def export_to_json_example():
    """Example: Export analysis results to JSON."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Export to JSON")
    print("=" * 60)
    
    import json
    
    # Analyze with advanced features
    analyzer = AdvancedCodebaseAnalyzer(
        enable_todos=True,
        enable_quality=True
    )
    
    base_results, advanced_results = analyzer.analyze_advanced(".")
    
    # Combine results
    full_results = {
        'basic_stats': base_results,
        'advanced_analysis': advanced_results
    }
    
    # Export to JSON file
    output_file = "analysis_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_results, f, indent=2, default=str)
    
    print(f"\nResults exported to: {output_file}")
    print(f"File size: {Path(output_file).stat().st_size:,} bytes")


def formatted_report_example():
    """Example: Generate a formatted console report."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Formatted Report")
    print("=" * 60)
    
    # Run analysis
    analyzer = AdvancedCodebaseAnalyzer(
        enable_todos=True,
        enable_quality=True,
        enable_complexity=True
    )
    
    base_results, advanced_results = analyzer.analyze_advanced(".")
    
    # Use the formatter to display results
    formatter = AdvancedReportFormatter(use_colors=True)
    
    # Print formatted sections
    print("\n" + formatter.format_header("Code Analysis Report"))
    print(formatter.format_basic_stats(base_results))
    
    if advanced_results and 'quality_score' in advanced_results:
        print(formatter.format_quality_score(advanced_results['quality_score']))
    
    if advanced_results and 'complexity' in advanced_results:
        print(formatter.format_complexity(advanced_results['complexity']))


if __name__ == '__main__':
    # Run all examples
    print("\nCodebase Analyzer - Usage Examples\n")
    
    try:
        simple_analysis_example()
        advanced_analysis_example()
        export_to_json_example()
        formatted_report_example()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
