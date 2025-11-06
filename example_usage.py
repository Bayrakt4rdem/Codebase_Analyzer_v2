"""
Example: Using the Codebase Analyzer programmatically.
"""

from pathlib import Path
from analyzer import CodebaseAnalyzer
from formatter import ReportFormatter


def analyze_project(project_path: str):
    """Analyze a project and display the report."""
    print(f"Analyzing: {project_path}\n")
    
    analyzer = CodebaseAnalyzer(project_path)
    report = analyzer.analyze()
    
    ReportFormatter.format_report(report, Path(project_path))


def quick_stats(project_path: str):
    """Get quick statistics about a project."""
    analyzer = CodebaseAnalyzer(project_path)
    report = analyzer.analyze()
    
    print(f"\n📊 Quick Stats for: {project_path}")
    print(f"Files: {report['total_files']:,}")
    print(f"Lines: {report['total_lines']:,}")
    print(f"Size: {ReportFormatter.format_size(report['total_size'])}")
    
    if report['lines_by_language']:
        top_lang = max(report['lines_by_language'].items(), key=lambda x: x[1])
        print(f"Primary Language: {top_lang[0]} ({top_lang[1]:,} lines)")


if __name__ == '__main__':
    # Example 1: Full analysis of current directory
    print("=" * 80)
    print("Example 1: Full Analysis")
    print("=" * 80)
    analyze_project('.')
    
    # Example 2: Quick stats only
    print("\n" + "=" * 80)
    print("Example 2: Quick Statistics")
    print("=" * 80)
    quick_stats('..')
