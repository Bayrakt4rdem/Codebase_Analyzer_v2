"""
Test coverage analyzer - estimates test coverage based on file patterns.
"""

import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


class TestAnalyzer:
    TEST_PATTERNS = [
        r'^test_.*\.py$',
        r'.*_test\.py$',
        r'^tests?\.py$',
        r'.*\.test\.py$',
    ]
    
    TEST_DIRS = {'test', 'tests', '__tests__', 'spec', 'specs'}
    
    def __init__(self):
        self.test_files = []
        self.source_files = []
        self.test_lines = 0
        self.source_lines = 0
        self.modules_with_tests = set()
        self.modules_without_tests = set()
        self.test_by_module = defaultdict(list)
        
    def analyze_file(self, file_path: Path, line_count: int, base_path: Path) -> None:
        if file_path.suffix != '.py':
            return
            
        is_test = self._is_test_file(file_path)
        
        if is_test:
            self.test_files.append(file_path)
            self.test_lines += line_count
            self._associate_test_with_module(file_path, base_path)
        else:
            if not self._is_excluded(file_path):
                self.source_files.append(file_path)
                self.source_lines += line_count
                module_name = self._get_module_name(file_path, base_path)
                if module_name not in self.modules_with_tests:
                    self.modules_without_tests.add(str(file_path))
    
    def _is_test_file(self, file_path: Path) -> bool:
        if any(part in self.TEST_DIRS for part in file_path.parts):
            return True
        
        for pattern in self.TEST_PATTERNS:
            if re.match(pattern, file_path.name):
                return True
        return False
    
    def _is_excluded(self, file_path: Path) -> bool:
        excluded = {'__init__.py', 'setup.py', 'conf.py', 'manage.py'}
        return file_path.name in excluded
    
    def _get_module_name(self, file_path: Path, base_path: Path) -> str:
        try:
            return str(file_path.relative_to(base_path)).replace('\\', '/').replace('.py', '')
        except ValueError:
            return file_path.stem
    
    def _associate_test_with_module(self, test_file: Path, base_path: Path) -> None:
        name = test_file.stem
        module_name = name.replace('test_', '').replace('_test', '')
        self.modules_with_tests.add(module_name)
        self.test_by_module[module_name].append(test_file)
    
    def get_report(self) -> Dict:
        total_files = len(self.test_files) + len(self.source_files)
        total_lines = self.test_lines + self.source_lines
        
        test_file_ratio = (len(self.test_files) / total_files * 100) if total_files > 0 else 0
        test_line_ratio = (self.test_lines / total_lines * 100) if total_lines > 0 else 0
        
        coverage_estimate = min(test_file_ratio, test_line_ratio)
        
        grade = 'F'
        if coverage_estimate >= 80:
            grade = 'A'
        elif coverage_estimate >= 60:
            grade = 'B'
        elif coverage_estimate >= 40:
            grade = 'C'
        elif coverage_estimate >= 20:
            grade = 'D'
        
        return {
            'test_files': len(self.test_files),
            'source_files': len(self.source_files),
            'test_lines': self.test_lines,
            'source_lines': self.source_lines,
            'test_file_ratio': round(test_file_ratio, 2),
            'test_line_ratio': round(test_line_ratio, 2),
            'coverage_estimate': round(coverage_estimate, 2),
            'grade': grade,
            'untested_files': list(self.modules_without_tests)[:20],
            'total_untested': len(self.modules_without_tests)
        }
