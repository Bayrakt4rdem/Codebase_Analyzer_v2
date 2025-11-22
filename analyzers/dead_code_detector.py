"""
Dead code detector - identifies unreferenced Python files in codebase.

Analyzes import relationships to find files that are never imported,
with intelligent exclusions to avoid false positives on legitimate standalone files.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DeadCodeDetector:
    """Detects potentially unused Python files in a project."""
    
    # Files/patterns that should never be flagged as dead code
    LEGITIMATE_STANDALONE = {
        'setup.py', 'setup.cfg', 'conftest.py',
        'manage.py', 'wsgi.py', 'asgi.py',
        '__main__.py', '__init__.py'
    }
    
    # Patterns for entry point files
    ENTRY_POINT_PATTERNS = [
        r'^main\.py$',
        r'^cli\.py$',
        r'^app\.py$',
        r'^run\.py$',
        r'^server\.py$',
        r'.*_cli\.py$',
        r'.*_main\.py$',
        r'launch.*\.py$',
    ]
    
    # Patterns for test files
    TEST_PATTERNS = [
        r'^test_.*\.py$',
        r'.*_test\.py$',
        r'^tests?\.py$',
    ]
    
    # Patterns for example/demo files
    EXAMPLE_PATTERNS = [
        r'^example.*\.py$',
        r'^demo.*\.py$',
        r'.*_example\.py$',
        r'.*_demo\.py$',
        r'^sample.*\.py$',
    ]
    
    # Patterns for debug/utility scripts
    UTILITY_PATTERNS = [
        r'^debug.*\.py$',
        r'^util.*\.py$',
        r'^helper.*\.py$',
        r'.*_debug\.py$',
        r'.*_util\.py$',
    ]
    
    def __init__(self):
        self.all_python_files: Set[Path] = set()
        self.imported_files: Set[Path] = set()
        self.imports_by_file: Dict[Path, Set[str]] = defaultdict(set)
        self.project_root: Path = None
        self.dead_code_candidates: List[Dict] = []
        
    def analyze_project(self, project_root: Path) -> None:
        """Analyze entire project for dead code."""
        self.project_root = project_root
        self._collect_all_python_files(project_root)
        self._analyze_all_imports()
        self._identify_dead_code()
    
    def _collect_all_python_files(self, root: Path) -> None:
        """Collect all Python files in the project."""
        ignore_dirs = {
            '__pycache__', '.git', '.venv', 'venv', 'env',
            'node_modules', '.pytest_cache', '.mypy_cache',
            'dist', 'build', '.egg-info', '.tox', '.coverage'
        }
        
        for py_file in root.rglob('*.py'):
            # Skip ignored directories
            if any(ignored in py_file.parts for ignored in ignore_dirs):
                continue
            
            self.all_python_files.add(py_file)
    
    def _analyze_all_imports(self) -> None:
        """Analyze imports in all Python files."""
        for py_file in self.all_python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self._parse_imports(content, py_file)
            except (PermissionError, OSError):
                continue
    
    def _parse_imports(self, content: str, source_file: Path) -> None:
        """Parse imports from a Python file."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._resolve_import(alias.name, source_file)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._resolve_import(node.module, source_file)
        except SyntaxError:
            # Fallback to regex parsing
            self._fallback_parse(content, source_file)
    
    def _fallback_parse(self, content: str, source_file: Path) -> None:
        """Fallback regex-based import parsing."""
        patterns = [
            r'^\s*import\s+([\w.]+)',
            r'^\s*from\s+([\w.]+)\s+import'
        ]
        
        for line in content.split('\n'):
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    module_name = match.group(1)
                    self._resolve_import(module_name, source_file)
    
    def _resolve_import(self, module_name: str, source_file: Path) -> None:
        """Resolve import to actual file and mark as imported."""
        self.imports_by_file[source_file].add(module_name)
        
        # Try to resolve to actual file
        parts = module_name.split('.')
        base_module = parts[0]
        
        # Check relative to project root
        potential_files = [
            self.project_root / f"{base_module}.py",
            self.project_root / base_module / "__init__.py",
        ]
        
        # Check relative to source file's directory
        source_dir = source_file.parent
        potential_files.extend([
            source_dir / f"{base_module}.py",
            source_dir / base_module / "__init__.py",
        ])
        
        # Check for full path resolution
        if len(parts) > 1:
            for i in range(1, len(parts) + 1):
                module_path = '/'.join(parts[:i]) + '.py'
                potential_files.append(self.project_root / module_path)
        
        for potential_file in potential_files:
            if potential_file.exists() and potential_file in self.all_python_files:
                self.imported_files.add(potential_file)
    
    def _identify_dead_code(self) -> None:
        """Identify files that are never imported."""
        for py_file in self.all_python_files:
            if py_file not in self.imported_files:
                confidence = self._assess_confidence(py_file)
                if confidence['level'] != 'excluded':
                    self.dead_code_candidates.append({
                        'file': py_file,
                        'relative_path': py_file.relative_to(self.project_root),
                        'confidence': confidence['level'],
                        'reason': confidence['reason'],
                        'size_bytes': py_file.stat().st_size,
                        'lines': self._count_lines(py_file)
                    })
    
    def _assess_confidence(self, py_file: Path) -> Dict[str, str]:
        """Assess confidence that file is actually dead code."""
        filename = py_file.name
        relative_path = py_file.relative_to(self.project_root)
        
        # Check if it's a legitimate standalone file
        if filename in self.LEGITIMATE_STANDALONE:
            return {'level': 'excluded', 'reason': 'Legitimate standalone file'}
        
        # Check if it's an entry point
        if self._matches_patterns(filename, self.ENTRY_POINT_PATTERNS):
            return {'level': 'excluded', 'reason': 'Entry point script'}
        
        # Check if it's in examples or tests directory
        path_str = str(relative_path).lower()
        if any(x in path_str for x in ['example', 'examples', 'demo', 'demos']):
            return {'level': 'excluded', 'reason': 'Example/demo file'}
        
        if any(x in path_str for x in ['test', 'tests', '__tests__', 'spec', 'specs']):
            return {'level': 'excluded', 'reason': 'Test file'}
        
        # Check test file patterns
        if self._matches_patterns(filename, self.TEST_PATTERNS):
            return {'level': 'excluded', 'reason': 'Test file'}
        
        # Check example patterns
        if self._matches_patterns(filename, self.EXAMPLE_PATTERNS):
            return {'level': 'excluded', 'reason': 'Example/demo file'}
        
        # Check utility/debug patterns
        if self._matches_patterns(filename, self.UTILITY_PATTERNS):
            return {'level': 'medium', 'reason': 'Debug/utility script - might be used directly'}
        
        # Check if file has if __name__ == '__main__' (likely a script)
        if self._has_main_block(py_file):
            return {'level': 'low', 'reason': 'Has main block - might be run directly'}
        
        # Check if file is very small (< 50 lines) - might be leftover
        lines = self._count_lines(py_file)
        if lines < 50:
            return {'level': 'high', 'reason': 'Small file never imported'}
        
        # Default: likely dead code
        return {'level': 'medium', 'reason': 'Not imported anywhere in project'}
    
    def _matches_patterns(self, filename: str, patterns: List[str]) -> bool:
        """Check if filename matches any of the given patterns."""
        return any(re.match(pattern, filename, re.IGNORECASE) for pattern in patterns)
    
    def _has_main_block(self, py_file: Path) -> bool:
        """Check if file has if __name__ == '__main__' block."""
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return '__name__' in content and '__main__' in content
        except (PermissionError, OSError):
            return False
    
    def _count_lines(self, py_file: Path) -> int:
        """Count lines in a file."""
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except (PermissionError, OSError):
            return 0
    
    def get_report(self) -> Dict:
        """Generate dead code detection report."""
        # Sort by confidence level
        confidence_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_candidates = sorted(
            self.dead_code_candidates,
            key=lambda x: (confidence_order.get(x['confidence'], 99), x['lines']),
            reverse=True
        )
        
        # Calculate statistics
        total_files = len(self.all_python_files)
        imported_count = len(self.imported_files)
        dead_code_count = len(self.dead_code_candidates)
        
        # Group by confidence
        by_confidence = defaultdict(list)
        total_lines = 0
        total_size = 0
        
        for candidate in sorted_candidates:
            by_confidence[candidate['confidence']].append(candidate)
            total_lines += candidate['lines']
            total_size += candidate['size_bytes']
        
        return {
            'total_python_files': total_files,
            'imported_files': imported_count,
            'dead_code_candidates': dead_code_count,
            'potential_savings_lines': total_lines,
            'potential_savings_bytes': total_size,
            'by_confidence': {
                'high': len(by_confidence['high']),
                'medium': len(by_confidence['medium']),
                'low': len(by_confidence['low']),
            },
            'candidates': sorted_candidates,
            'summary': self._generate_summary(sorted_candidates)
        }
    
    def _generate_summary(self, candidates: List[Dict]) -> str:
        """Generate human-readable summary."""
        if not candidates:
            return "No dead code detected! All Python files are referenced."
        
        high_conf = sum(1 for c in candidates if c['confidence'] == 'high')
        medium_conf = sum(1 for c in candidates if c['confidence'] == 'medium')
        low_conf = sum(1 for c in candidates if c['confidence'] == 'low')
        
        summary = f"Found {len(candidates)} potentially unused file(s): "
        summary += f"{high_conf} high confidence, {medium_conf} medium, {low_conf} low"
        
        return summary
