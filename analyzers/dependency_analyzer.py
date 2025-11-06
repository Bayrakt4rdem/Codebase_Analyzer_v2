"""
Dependency and import analyzer for Python projects.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter


class DependencyAnalyzer:
    def __init__(self):
        self.imports = defaultdict(set)  # file -> set of imports
        self.imported_by = defaultdict(set)  # module -> files that import it
        self.import_counts = Counter()
        self.external_imports = set()
        self.internal_imports = set()
        self.circular_deps = []
        
    def analyze_file(self, file_path: Path, project_root: Path) -> None:
        if file_path.suffix != '.py':
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self._parse_imports(content, file_path, project_root)
        except (PermissionError, OSError, SyntaxError):
            pass
    
    def _parse_imports(self, content: str, file_path: Path, project_root: Path) -> None:
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_import(alias.name, file_path, project_root)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._add_import(node.module, file_path, project_root)
        except SyntaxError:
            self._fallback_parse(content, file_path, project_root)
    
    def _fallback_parse(self, content: str, file_path: Path, project_root: Path) -> None:
        import_pattern = r'^\s*(?:from\s+([\w.]+)\s+)?import\s+([\w,\s.]+)'
        for line in content.split('\n'):
            match = re.match(import_pattern, line)
            if match:
                module = match.group(1) or match.group(2).split(',')[0].strip()
                self._add_import(module, file_path, project_root)
    
    def _add_import(self, module_name: str, file_path: Path, project_root: Path) -> None:
        base_module = module_name.split('.')[0]
        
        self.imports[file_path].add(base_module)
        self.imported_by[base_module].add(file_path)
        self.import_counts[base_module] += 1
        
        if self._is_internal_module(base_module, project_root):
            self.internal_imports.add(base_module)
        else:
            self.external_imports.add(base_module)
    
    def _is_internal_module(self, module_name: str, project_root: Path) -> bool:
        potential_paths = [
            project_root / f"{module_name}.py",
            project_root / module_name / "__init__.py"
        ]
        return any(p.exists() for p in potential_paths)
    
    def detect_circular_dependencies(self) -> List[Tuple[str, str]]:
        for file_path, imports in self.imports.items():
            for imported_module in imports:
                if imported_module in self.imports:
                    if file_path.stem in self.imports.get(Path(imported_module), set()):
                        self.circular_deps.append((str(file_path), imported_module))
        return self.circular_deps
    
    def get_report(self) -> Dict:
        most_imported = self.import_counts.most_common(10)
        
        return {
            'total_imports': sum(len(imports) for imports in self.imports.values()),
            'unique_modules': len(self.import_counts),
            'external_dependencies': sorted(list(self.external_imports)),
            'internal_modules': sorted(list(self.internal_imports)),
            'most_imported': most_imported,
            'circular_dependencies': self.circular_deps,
            'import_count': len(self.imports),
            'unused_imports_hint': len([m for m, count in self.import_counts.items() if count == 1])
        }
