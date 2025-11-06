#!/usr/bin/env python3
"""
Codebase Analyzer CLI - Comprehensive code analysis tool.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.analyzer_v2 import AdvancedCodebaseAnalyzer
from formatters.advanced_formatter import AdvancedReportFormatter
from utils.colors import Colors, green, yellow, red, cyan, bold

# Enable colors on Windows
Colors.enable()


def create_parser():
    parser = argparse.ArgumentParser(
        description='Analyze codebase structure, quality, and technical debt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .                           # Simple mode (default)
  %(prog)s . --advanced                # All advanced features
  %(prog)s . --todos --dependencies    # Specific features only
  %(prog)s /path/to/project --export json --output report.json
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to analyze (default: current directory)'
    )
    
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--simple',
        action='store_true',
        help='Simple mode with basic stats (default)'
    )
    mode_group.add_argument(
        '--advanced',
        action='store_true',
        help='Advanced mode with all features enabled'
    )
    
    feature_group = parser.add_argument_group('Feature Toggles')
    feature_group.add_argument(
        '--todos',
        action='store_true',
        help='Track TODO/FIXME/HACK markers'
    )
    feature_group.add_argument(
        '--dependencies',
        action='store_true',
        help='Analyze import dependencies'
    )
    feature_group.add_argument(
        '--tests',
        action='store_true',
        help='Analyze test coverage'
    )
    feature_group.add_argument(
        '--config',
        action='store_true',
        help='Analyze configuration files'
    )
    feature_group.add_argument(
        '--docs',
        action='store_true',
        help='Analyze documentation coverage'
    )
    feature_group.add_argument(
        '--quality',
        action='store_true',
        help='Calculate quality score'
    )
    feature_group.add_argument(
        '--complexity',
        action='store_true',
        help='Analyze cyclomatic complexity'
    )
    
    export_group = parser.add_argument_group('Export Options')
    export_group.add_argument(
        '--export',
        choices=['json', 'html', 'csv'],
        help='Export format (json/html/csv)'
    )
    export_group.add_argument(
        '--output',
        help='Output file path'
    )
    
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress indicators'
    )
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    target_path = Path(args.path).resolve()
    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)
    
    if not target_path.is_dir():
        print(f"Error: Path is not a directory: {target_path}", file=sys.stderr)
        sys.exit(1)
    
    mode = 'simple'
    features = []
    
    if args.advanced:
        mode = 'advanced'
    else:
        if args.todos:
            features.append('todos')
        if args.dependencies:
            features.append('dependencies')
        if args.tests:
            features.append('tests')
        if args.config:
            features.append('config')
        if args.docs:
            features.append('docs')
        if args.quality:
            features.append('quality')
        if args.complexity:
            features.append('complexity')
        
        if features:
            mode = 'advanced'
    
    try:
        print(f"{cyan('Analyzing:')} {target_path}")
        print(f"{cyan('Mode:')} {bold(mode.upper())}")
        if features:
            print(f"{cyan('Features:')} {', '.join(features)}")
        print()
        
        show_progress = not args.no_progress
        analyzer = AdvancedCodebaseAnalyzer(
            target_path, 
            mode=mode, 
            features=features if features else None,
            show_progress=show_progress
        )
        report = analyzer.analyze()
        
        if mode == 'simple' and not features:
            _print_simple_report(report, analyzer)
        else:
            _print_advanced_report(report, analyzer)
        
        if args.export:
            if not args.output:
                print("\nError: --output required when using --export", file=sys.stderr)
                sys.exit(1)
            _export_report(report, args.export, args.output)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError during analysis: {e}", file=sys.stderr)
        sys.exit(1)


def _print_simple_report(report: dict, analyzer):
    """Print simple mode report (v1 style)."""
    from core.base_analyzer import CodebaseAnalyzer
    
    print("\n" + "=" * 80)
    print(bold("  CODEBASE ANALYSIS REPORT"))
    print("=" * 80)
    
    stats = report['basic']
    print(f"\n{cyan('Total Files:')} {stats['total_files']:,}")
    print(f"{cyan('Total Lines:')} {stats['total_lines']:,}")
    print(f"{cyan('Total Size:')}  {CodebaseAnalyzer.format_size(stats['total_size'])}")
    
    if stats.get('empty_file_count', 0) > 0:
        print(f"{yellow('Empty Files:')} {stats['empty_file_count']}")
    
    if stats.get('lines_by_language'):
        print("\n" + "-" * 80)
        print(bold("Languages:"))
        print("-" * 80)
        
        for lang, lines in sorted(stats['lines_by_language'].items(), key=lambda x: x[1], reverse=True):
            file_count = stats['files_by_language'].get(lang, 0)
            print(f"\n{green(lang)}:")
            print(f"  Files: {file_count:,}")
            print(f"  Lines: {lines:,}")
            if file_count > 0:
                avg = lines / file_count
                print(f"  Avg Lines/File: {avg:.1f}")
    
    if stats.get('venv_size', 0) > 0:
        print("\n" + "-" * 80)
        print(f"{yellow('Virtual Environments:')}")
        print("-" * 80)
        for venv_path in stats.get('venv_dirs', []):
            print(f"  {venv_path}")
        print(f"  Total Size: {CodebaseAnalyzer.format_size(stats['venv_size'])}")
        print(f"  Total Files: {stats.get('venv_files', 0):,}")


def _print_advanced_report(report: dict, analyzer):
    """Print advanced mode report with all features."""
    _print_simple_report(report, analyzer)
    
    formatter = AdvancedReportFormatter()
    
    formatter.format_quality_score(report)
    formatter.format_todos(report, analyzer.base_path)
    formatter.format_dependencies(report)
    formatter.format_tests(report)
    formatter.format_documentation(report)
    formatter.format_config(report)


def _export_report(report: dict, format: str, output_path: str):
    """Export report to specified format."""
    print(f"\n{cyan('Exporting to')} {bold(format.upper())}: {output_path}")
    
    if format == 'json':
        import json
        
        def convert_paths(obj):
            if isinstance(obj, dict):
                return {str(k): convert_paths(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_paths(item) for item in obj]
            elif hasattr(obj, '__fspath__'):
                return str(obj)
            else:
                return obj
        
        clean_report = convert_paths(report)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_report, f, indent=2, default=str)
        print(green("[OK] JSON export complete"))
    
    elif format == 'html':
        print(yellow("[!!]  HTML export not yet implemented"))
    
    elif format == 'csv':
        print(yellow("[!!]  CSV export not yet implemented"))


if __name__ == '__main__':
    main()
