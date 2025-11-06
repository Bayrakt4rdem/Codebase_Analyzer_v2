"""
Documentation analyzer - checks for docstrings and documentation files.
"""

import ast
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


class DocAnalyzer:
    DOC_EXTENSIONS = {'.md', '.markdown', '.rst', '.txt'}
    DOC_FILENAMES = {'README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE', 'AUTHORS'}
    
    def __init__(self):
        self.doc_files = []
        self.readme_files = []
        self.total_modules = 0
        self.modules_with_docstrings = 0
        self.total_classes = 0
        self.classes_with_docstrings = 0
        self.total_functions = 0
        self.functions_with_docstrings = 0
        self.undocumented_files = []
        
    def analyze_file(self, file_path: Path) -> None:
        if file_path.suffix in self.DOC_EXTENSIONS or file_path.name in self.DOC_FILENAMES:
            self.doc_files.append(file_path)
            if 'readme' in file_path.name.lower():
                self.readme_files.append(file_path)
        
        if file_path.suffix == '.py':
            self._analyze_python_file(file_path)
    
    def _analyze_python_file(self, file_path: Path) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            tree = ast.parse(content)
            self.total_modules += 1
            
            module_docstring = ast.get_docstring(tree)
            if module_docstring:
                self.modules_with_docstrings += 1
            
            file_has_docs = bool(module_docstring)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.total_classes += 1
                    if ast.get_docstring(node):
                        self.classes_with_docstrings += 1
                        file_has_docs = True
                
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith('_'):  # Only count public functions
                        self.total_functions += 1
                        if ast.get_docstring(node):
                            self.functions_with_docstrings += 1
                            file_has_docs = True
            
            if not file_has_docs and file_path.name != '__init__.py':
                self.undocumented_files.append(file_path)
                
        except (SyntaxError, PermissionError, OSError):
            pass
    
    def get_report(self) -> Dict:
        module_coverage = (self.modules_with_docstrings / self.total_modules * 100) if self.total_modules > 0 else 0
        class_coverage = (self.classes_with_docstrings / self.total_classes * 100) if self.total_classes > 0 else 0
        function_coverage = (self.functions_with_docstrings / self.total_functions * 100) if self.total_functions > 0 else 0
        
        overall_coverage = (module_coverage + class_coverage + function_coverage) / 3 if self.total_modules > 0 else 0
        
        grade = 'F'
        if overall_coverage >= 80:
            grade = 'A'
        elif overall_coverage >= 60:
            grade = 'B'
        elif overall_coverage >= 40:
            grade = 'C'
        elif overall_coverage >= 20:
            grade = 'D'
        
        return {
            'doc_files': len(self.doc_files),
            'readme_present': len(self.readme_files) > 0,
            'module_coverage': round(module_coverage, 2),
            'class_coverage': round(class_coverage, 2),
            'function_coverage': round(function_coverage, 2),
            'overall_coverage': round(overall_coverage, 2),
            'grade': grade,
            'total_modules': self.total_modules,
            'total_classes': self.total_classes,
            'total_functions': self.total_functions,
            'undocumented_files': [str(f) for f in self.undocumented_files[:10]],
            'total_undocumented': len(self.undocumented_files)
        }
