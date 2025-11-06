"""
Advanced report formatter for displaying comprehensive analysis.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict


class AdvancedReportFormatter:
    """Formats advanced analysis reports."""
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def format_number(num: int) -> str:
        return f"{num:,}"
    
    @staticmethod
    def print_header(title: str):
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    @staticmethod
    def print_subheader(title: str):
        print(f"\n{title}")
        print("-" * 80)
    
    @staticmethod
    def format_quality_score(report: Dict):
        """Format quality score section."""
        quality = report.get('advanced', {}).get('quality', {})
        if not quality:
            return
        
        AdvancedReportFormatter.print_subheader(">> Code Quality Score")
        
        score = quality.get('overall_score', 0)
        grade = quality.get('grade', 'F')
        
        print(f"  Overall Grade: {grade} ({score}/100)")
        print()
        
        category_scores = quality.get('category_scores', {})
        for category, cat_score in category_scores.items():
            icon = "[OK]" if cat_score >= 70 else "[!!]" if cat_score >= 50 else "[XX]"
            cat_name = category.replace('_', ' ').title()
            status = "Excellent" if cat_score >= 90 else "Good" if cat_score >= 70 else "Acceptable" if cat_score >= 50 else "Needs Work"
            print(f"  {icon} {cat_name:<20} {cat_score:>3.0f}/100  ({status})")
        
        recommendations = quality.get('recommendations', [])
        if recommendations:
            print("\n  >> Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"    {i}. {rec}")
    
    @staticmethod
    def format_todos(report: Dict, base_path: Path):
        """Format TODO/FIXME tracking section."""
        todos = report.get('advanced', {}).get('todos', {})
        if not todos or todos.get('total_count', 0) == 0:
            return
        
        AdvancedReportFormatter.print_subheader(f">> Technical Debt ({todos['total_count']} items)")
        
        by_priority = todos.get('by_priority', {})
        
        if 'high' in by_priority:
            items = by_priority['high'][:5]
            print(f"\n  🔴 High Priority (FIXME/XXX/BUG): {len(by_priority['high'])}")
            for item in items:
                rel_path = AdvancedReportFormatter._get_relative_path(item['file'], base_path)
                print(f"    • {rel_path}:{item['line']}")
                if item['message']:
                    print(f"      {item['message'][:70]}")
        
        if 'medium' in by_priority:
            count = len(by_priority['medium'])
            print(f"\n  - Medium Priority (TODO): {count}")
            for item in by_priority['medium'][:3]:
                rel_path = AdvancedReportFormatter._get_relative_path(item['file'], base_path)
                print(f"    • {rel_path}:{item['line']}")
                if item['message']:
                    print(f"      {item['message'][:70]}")
            if count > 3:
                print(f"    ... and {count - 3} more")
        
        if 'code_smell' in by_priority:
            count = len(by_priority['code_smell'])
            print(f"\n  [!!]  Code Smells (HACK/TEMP): {count}")
    
    @staticmethod
    def format_dependencies(report: Dict):
        """Format dependency analysis section."""
        deps = report.get('advanced', {}).get('dependencies', {})
        if not deps:
            return
        
        AdvancedReportFormatter.print_subheader(f">> Dependencies ({deps.get('total_imports', 0)} imports)")
        
        print(f"  Unique Modules:  {deps.get('unique_modules', 0)}")
        print(f"  External Deps:   {len(deps.get('external_dependencies', []))}")
        print(f"  Internal Modules: {len(deps.get('internal_modules', []))}")
        
        most_imported = deps.get('most_imported', [])
        if most_imported:
            print("\n  Most Imported:")
            for module, count in most_imported[:5]:
                print(f"    • {module:<30} ({count} times)")
        
        circular = deps.get('circular_dependencies', [])
        if circular:
            print(f"\n  [!!]  Circular Dependencies Found: {len(circular)}")
            for file1, file2 in circular[:3]:
                print(f"    • {Path(file1).name} ↔ {file2}")
    
    @staticmethod
    def format_tests(report: Dict):
        """Format test coverage section."""
        tests = report.get('advanced', {}).get('tests', {})
        if not tests:
            return
        
        AdvancedReportFormatter.print_subheader(f">> Test Coverage: {tests.get('coverage_estimate', 0)}% ({tests.get('grade', 'F')})")
        
        print(f"  Test Files:      {tests.get('test_files', 0)}/{tests.get('test_files', 0) + tests.get('source_files', 0)} ({tests.get('test_file_ratio', 0)}%)")
        print(f"  Test Lines:      {AdvancedReportFormatter.format_number(tests.get('test_lines', 0))}/{AdvancedReportFormatter.format_number(tests.get('test_lines', 0) + tests.get('source_lines', 0))} ({tests.get('test_line_ratio', 0)}%)")
        
        untested = tests.get('total_untested', 0)
        if untested > 0:
            print(f"\n  [!!]  Untested Files: {untested}")
            for file_path in tests.get('untested_files', [])[:5]:
                print(f"    • {Path(file_path).name}")
    
    @staticmethod
    def format_documentation(report: Dict):
        """Format documentation coverage section."""
        docs = report.get('advanced', {}).get('documentation', {})
        if not docs:
            return
        
        AdvancedReportFormatter.print_subheader(f">> Documentation: {docs.get('overall_coverage', 0)}% ({docs.get('grade', 'F')})")
        
        print(f"  README Present:       {'[OK]' if docs.get('readme_present') else '[XX]'}")
        print(f"  Module Docstrings:    {docs.get('module_coverage', 0)}%")
        print(f"  Class Docstrings:     {docs.get('class_coverage', 0)}%")
        print(f"  Function Docstrings:  {docs.get('function_coverage', 0)}%")
        
        undoc_count = docs.get('total_undocumented', 0)
        if undoc_count > 0:
            print(f"\n  [!!]  Undocumented Files: {undoc_count}")
            for file_path in docs.get('undocumented_files', [])[:3]:
                print(f"    • {file_path}")
    
    @staticmethod
    def format_config(report: Dict):
        """Format configuration analysis section."""
        config = report.get('advanced', {}).get('config', {})
        if not config:
            return
        
        AdvancedReportFormatter.print_subheader(f">>  Configuration ({config.get('config_count', 0)} files)")
        
        env_files = config.get('env_files', [])
        if env_files:
            print(f"  Environment Files: {len(env_files)}")
            for env_file in env_files[:3]:
                print(f"    • {Path(env_file).name}")
        
        secrets = config.get('secret_count', 0)
        if secrets > 0:
            print(f"\n  [!!]  Potential Secrets: {secrets} warnings")
            for secret in config.get('potential_secrets', [])[:3]:
                print(f"    • {Path(secret['file']).name}:{secret['line']} - {secret['type']}")
        
        missing = config.get('missing_configs', [])
        if missing:
            print("\n  Missing Recommended Configs:")
            for cfg_file, description in missing:
                print(f"    [XX] {cfg_file} - {description}")
    
    @staticmethod
    def _get_relative_path(file_path: Path, base_path: Path) -> str:
        try:
            return str(file_path.relative_to(base_path))
        except ValueError:
            return str(file_path)
