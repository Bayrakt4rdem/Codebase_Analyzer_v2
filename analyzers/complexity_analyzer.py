"""
Cyclomatic Complexity Analyzer

Analyzes code complexity using McCabe complexity metrics.
Provides function-level and file-level complexity scores.
"""

import ast
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class ComplexityAnalyzer:
    """Analyze cyclomatic complexity of Python code."""
    
    # Complexity thresholds (McCabe recommendations)
    SIMPLE = 10      # Low risk
    MODERATE = 20    # Moderate risk
    COMPLEX = 30     # High risk
    VERY_COMPLEX = 50  # Very high risk
    
    def __init__(self):
        """Initialize complexity analyzer."""
        self.results = {}
        
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze complexity of a Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary containing complexity metrics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=file_path)
            
            # Analyze all functions and methods
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_complexity(node)
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'complexity': complexity,
                        'risk': self._get_risk_level(complexity)
                    })
            
            # Calculate file-level metrics
            total_complexity = sum(f['complexity'] for f in functions)
            avg_complexity = total_complexity / len(functions) if functions else 0
            max_complexity = max((f['complexity'] for f in functions), default=0)
            
            return {
                'file': file_path,
                'functions': functions,
                'total_functions': len(functions),
                'total_complexity': total_complexity,
                'avg_complexity': avg_complexity,
                'max_complexity': max_complexity,
                'high_complexity_count': sum(1 for f in functions if f['complexity'] >= self.MODERATE)
            }
            
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'functions': [],
                'total_functions': 0,
                'total_complexity': 0,
                'avg_complexity': 0,
                'max_complexity': 0,
                'high_complexity_count': 0
            }
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """
        Calculate McCabe complexity for a function node.
        
        Complexity = 1 (base) + decision points
        Decision points: if, elif, for, while, and, or, except, with, assert, comprehensions
        
        Args:
            node: AST node (FunctionDef or AsyncFunctionDef)
            
        Returns:
            Cyclomatic complexity score
        """
        complexity = 1  # Base complexity
        
        # Use a custom walker that doesn't enter nested function definitions
        for child in self._walk_no_nested_functions(node):
            # Control flow statements
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            
            # Exception handlers
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            
            # Boolean operators (and, or)
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            
            # Comprehensions - count each generator and if clause
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                for generator in child.generators:
                    complexity += 1  # Each generator adds complexity
                    complexity += len(generator.ifs)  # Each filter adds complexity
            
            # With statements
            elif isinstance(child, (ast.With, ast.AsyncWith)):
                complexity += 1
            
            # Assert statements
            elif isinstance(child, ast.Assert):
                complexity += 1
        
        return complexity
    
    def _walk_no_nested_functions(self, node: ast.AST):
        """
        Walk AST nodes but don't enter nested function definitions.
        This ensures we only count complexity for the current function.
        """
        from collections import deque
        
        todo = deque([node])
        while todo:
            node = todo.popleft()
            yield node
            
            for child in ast.iter_child_nodes(node):
                # Don't enter nested function/class definitions
                if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    todo.append(child)
    
    def _get_risk_level(self, complexity: int) -> str:
        """
        Get risk level based on complexity score.
        
        Args:
            complexity: Complexity score
            
        Returns:
            Risk level string
        """
        if complexity < self.SIMPLE:
            return 'simple'
        elif complexity < self.MODERATE:
            return 'moderate'
        elif complexity < self.COMPLEX:
            return 'complex'
        elif complexity < self.VERY_COMPLEX:
            return 'very_complex'
        else:
            return 'extreme'
    
    def analyze_directory(self, directory: str, extensions: Tuple[str, ...] = ('.py',)) -> Dict:
        """
        Analyze all Python files in a directory.
        
        Args:
            directory: Path to directory
            extensions: File extensions to analyze
            
        Returns:
            Aggregated complexity metrics
        """
        path = Path(directory)
        all_results = []
        
        # Find all Python files
        for ext in extensions:
            for file_path in path.rglob(f'*{ext}'):
                if file_path.is_file():
                    result = self.analyze_file(str(file_path))
                    all_results.append(result)
        
        # Aggregate metrics
        total_files = len(all_results)
        total_functions = sum(r['total_functions'] for r in all_results)
        total_complexity = sum(r['total_complexity'] for r in all_results)
        avg_complexity = total_complexity / total_functions if total_functions else 0
        high_complexity_funcs = sum(r['high_complexity_count'] for r in all_results)
        
        # Find most complex functions across all files
        all_functions = []
        for result in all_results:
            for func in result['functions']:
                all_functions.append({
                    'file': result['file'],
                    'name': func['name'],
                    'line': func['line'],
                    'complexity': func['complexity'],
                    'risk': func['risk']
                })
        
        # Sort by complexity
        all_functions.sort(key=lambda x: x['complexity'], reverse=True)
        
        return {
            'directory': directory,
            'total_files': total_files,
            'total_functions': total_functions,
            'total_complexity': total_complexity,
            'avg_complexity': avg_complexity,
            'high_complexity_count': high_complexity_funcs,
            'top_complex_functions': all_functions[:10],  # Top 10 most complex
            'files': all_results
        }
    
    def print_report(self, results: Dict):
        """
        Print a formatted complexity report.
        
        Args:
            results: Results from analyze_directory()
        """
        print("\n" + "="*80)
        print("  CYCLOMATIC COMPLEXITY REPORT")
        print("="*80)
        
        print(f"\nDirectory: {results['directory']}")
        print(f"Total Files: {results['total_files']}")
        print(f"Total Functions: {results['total_functions']}")
        print(f"Average Complexity: {results['avg_complexity']:.2f}")
        print(f"High Complexity Functions (>={self.MODERATE}): {results['high_complexity_count']}")
        
        # Top complex functions
        if results['top_complex_functions']:
            print("\n" + "-"*80)
            print("TOP 10 MOST COMPLEX FUNCTIONS")
            print("-"*80)
            
            for i, func in enumerate(results['top_complex_functions'][:10], 1):
                file_path = Path(func['file']).name
                risk_symbol = self._get_risk_symbol(func['risk'])
                print(f"{i:2d}. {risk_symbol} {func['name']:<30} "
                      f"Complexity: {func['complexity']:3d} "
                      f"({file_path}:{func['line']})")
        
        print("\n" + "="*80)
    
    def _get_risk_symbol(self, risk: str) -> str:
        """Get symbol for risk level."""
        symbols = {
            'simple': 'OK',
            'moderate': '!',
            'complex': '!!',
            'very_complex': '!!!',
            'extreme': '!!!!!'
        }
        return symbols.get(risk, '?')
    
    def export_to_dict(self, results: Dict) -> Dict:
        """
        Export results in a JSON-serializable format.
        
        Args:
            results: Results from analyze_directory()
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            'summary': {
                'total_files': results['total_files'],
                'total_functions': results['total_functions'],
                'avg_complexity': round(results['avg_complexity'], 2),
                'high_complexity_count': results['high_complexity_count']
            },
            'top_complex_functions': results['top_complex_functions'][:20],
            'files': [
                {
                    'file': r['file'],
                    'total_functions': r['total_functions'],
                    'avg_complexity': round(r['avg_complexity'], 2),
                    'max_complexity': r['max_complexity'],
                    'high_complexity_count': r['high_complexity_count']
                }
                for r in results['files']
                if r['total_functions'] > 0
            ]
        }


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python complexity_analyzer.py <directory>")
        sys.exit(1)
    
    analyzer = ComplexityAnalyzer()
    results = analyzer.analyze_directory(sys.argv[1])
    analyzer.print_report(results)


if __name__ == '__main__':
    main()
