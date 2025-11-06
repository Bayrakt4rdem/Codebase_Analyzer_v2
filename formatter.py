"""
Report formatting utilities.
"""

from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime


class ReportFormatter:
    """Formats analysis reports for display."""
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def format_number(num: int) -> str:
        """Format number with thousand separators."""
        return f"{num:,}"
    
    @staticmethod
    def print_header(title: str):
        """Print a formatted section header."""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    @staticmethod
    def print_subheader(title: str):
        """Print a formatted subsection header."""
        print(f"\n{title}")
        print("-" * 80)
    
    @staticmethod
    def format_report(report: Dict, base_path: Path = None):
        """Format and print the complete analysis report."""
        if base_path is None:
            base_path = Path(report['path'])
        
        # Header
        ReportFormatter.print_header("CODEBASE ANALYSIS REPORT")
        print(f"Path: {report['path']}")
        
        # Overall Statistics
        ReportFormatter.print_subheader("📊 Overall Statistics")
        print(f"  Total Size:        {ReportFormatter.format_size(report['total_size'])}")
        print(f"  Total Files:       {ReportFormatter.format_number(report['total_files'])}")
        print(f"  Total Directories: {ReportFormatter.format_number(report['total_dirs'])}")
        print(f"  Total Lines:       {ReportFormatter.format_number(report['total_lines'])}")
        print(f"  Avg Lines/File:    {report['avg_lines_per_file']:.2f}")
        print(f"  Primary Language:  {report['primary_language']}")
        
        # Temporal information
        if report['oldest_date']:
            oldest_date = datetime.fromtimestamp(report['oldest_date']).strftime('%Y-%m-%d %H:%M:%S')
            oldest_file = ReportFormatter._get_relative_path(report['oldest_file'], base_path)
            print(f"  Oldest File:       {oldest_date}")
            print(f"                     {oldest_file}")
        
        if report['newest_date']:
            newest_date = datetime.fromtimestamp(report['newest_date']).strftime('%Y-%m-%d %H:%M:%S')
            newest_file = ReportFormatter._get_relative_path(report['newest_file'], base_path)
            print(f"  Last Updated:      {newest_date}")
            print(f"                     {newest_file}")
        
        # Language Statistics (merged with file count)
        if report['lines_by_language']:
            ReportFormatter.print_subheader("💻 Code Statistics by Language")
            sorted_langs = sorted(
                report['lines_by_language'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            print(f"  {'Language':<15} {'Lines':<12} {'Files':<8} {'Size':<12} {'Avg Lines/File':<16} {'%'}")
            print("  " + "-" * 76)
            for lang, lines in sorted_langs:
                files = report['files_by_language'].get(lang, 0)
                size = report['size_by_language'].get(lang, 0)
                avg_lines = report['avg_lines_by_language'].get(lang, 0)
                percentage = (lines / report['total_lines'] * 100) if report['total_lines'] > 0 else 0
                print(f"  {lang:<15} {ReportFormatter.format_number(lines):<12} "
                      f"{files:<8} {ReportFormatter.format_size(size):<12} "
                      f"{avg_lines:>14.1f}  {percentage:>5.1f}%")
        
        # Virtual Environment Analysis
        if report['venv_dirs']:
            ReportFormatter.print_subheader("🐍 Virtual Environment Analysis")
            print(f"  Found {len(report['venv_dirs'])} virtual environment(s)")
            print(f"  Total venv Size:  {ReportFormatter.format_size(report['venv_size'])} ({ReportFormatter.format_number(report['venv_files'])} files)")
            print("\n  Virtual Environments:")
            for i, (venv_path, venv_size) in enumerate(report['venv_dirs'], 1):
                rel_path = ReportFormatter._get_relative_path(venv_path, base_path)
                print(f"    {i}. {rel_path}")
                print(f"       Size: {ReportFormatter.format_size(venv_size)}")
        
        # Top largest files
        if report['top_largest_files']:
            ReportFormatter.print_subheader("📦 Top 10 Largest Files")
            for i, (file_path, size, lang) in enumerate(report['top_largest_files'], 1):
                rel_path = ReportFormatter._get_relative_path(file_path, base_path)
                print(f"  {i:2}. {ReportFormatter.format_size(size):>10}  [{lang:12}]  {rel_path}")
        
        # Too long files warning
        if report['too_long_files']:
            ReportFormatter.print_subheader("⚠️  Potentially Too Long Files (>3x average)")
            for i, (file_path, lines, lang) in enumerate(report['too_long_files'][:10], 1):
                rel_path = ReportFormatter._get_relative_path(file_path, base_path)
                print(f"  {i:2}. {ReportFormatter.format_number(lines):>6} lines  [{lang:12}]  {rel_path}")
            if len(report['too_long_files']) > 10:
                print(f"  ... and {len(report['too_long_files']) - 10} more")
        
        # Too short files warning
        if report['too_short_files']:
            ReportFormatter.print_subheader("⚠️  Potentially Too Short Files (<10 lines)")
            for i, (file_path, lines, lang) in enumerate(report['too_short_files'][:10], 1):
                rel_path = ReportFormatter._get_relative_path(file_path, base_path)
                print(f"  {i:2}. {lines:>6} lines  [{lang:12}]  {rel_path}")
            if len(report['too_short_files']) > 10:
                print(f"  ... and {len(report['too_short_files']) - 10} more")
        
        # Empty files analysis
        if report['empty_file_count'] > 0:
            ReportFormatter.print_subheader("📭 Empty Files Analysis")
            print(f"  Total Empty Files: {report['empty_file_count']}")
            
            if report['top_empty_folders']:
                print("\n  Top 5 Folders with Most Empty Files:")
                for i, (folder, count) in enumerate(report['top_empty_folders'], 1):
                    rel_folder = ReportFormatter._get_relative_path(Path(folder), base_path)
                    print(f"    {i}. {rel_folder}")
                    print(f"       {count} empty file(s)")
            
            # Show some examples
            if report['empty_files']:
                print("\n  Examples of Empty Files:")
                for i, (file_path, lang) in enumerate(report['empty_files'][:5], 1):
                    rel_path = ReportFormatter._get_relative_path(file_path, base_path)
                    print(f"    • [{lang:12}]  {rel_path}")
                if len(report['empty_files']) > 5:
                    print(f"    ... and {len(report['empty_files']) - 5} more")
        
        # Ignored files breakdown (moved to last)
        if report['ignored_size'] > 0:
            ReportFormatter.print_subheader("🗑️  Ignored Files Analysis")
            print(f"  Total Ignored:    {ReportFormatter.format_size(report['ignored_size'])} ({ReportFormatter.format_number(report['ignored_files'])} files)")
            
            if report['ignored_by_type']:
                print("\n  Breakdown by Type:")
                for ignore_type, stats in sorted(report['ignored_by_type'].items(), key=lambda x: x[1]['size'], reverse=True):
                    print(f"    • {ignore_type:<30} {ReportFormatter.format_size(stats['size']):<12} ({stats['count']} files)")
                
                print("\n  Why files are ignored:")
                print("    • __pycache__:   Python bytecode cache (auto-generated)")
                print("    • venv:          Virtual environment packages (dependencies)")
                print("    • Binary files:  Compiled files, executables (.pyc, .so, .dll, etc.)")
                print("    • Hidden files:  System/editor config files (start with .)")
                print("    • Lock/Log files: Temporary files (.lock, .log)")
        
        # Footer
        print("\n" + "=" * 80)
        print()
    
    @staticmethod
    def _get_relative_path(file_path: Path, base_path: Path) -> str:
        """Get relative path for display."""
        try:
            return str(file_path.relative_to(base_path))
        except ValueError:
            return str(file_path)
