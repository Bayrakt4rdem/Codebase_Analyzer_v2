"""
Advanced codebase analyzer - orchestrates all analysis modules.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_analyzer import CodebaseAnalyzer
from utils.progress import ProgressBar
from utils.colors import Colors, green, yellow, red, cyan, bold


class AdvancedCodebaseAnalyzer(CodebaseAnalyzer):
    """Extended analyzer with advanced features."""
    
    def __init__(self, path: str, mode: str = 'simple', features: Optional[List[str]] = None, show_progress: bool = True):
        super().__init__(path)
        self.mode = mode
        self.features = features or []
        self.base_path = self.path  # For compatibility
        self.show_progress = show_progress
        
        self.todo_tracker = None
        self.dependency_analyzer = None
        self.test_analyzer = None
        self.config_analyzer = None
        self.doc_analyzer = None
        self.quality_scorer = None
        self.complexity_analyzer = None
        
        self._init_advanced_analyzers()
    
    def _init_advanced_analyzers(self):
        """Initialize advanced analyzers based on mode and features."""
        if self.mode == 'advanced' or self.features:
            self._load_analyzers()
    
    def _load_analyzers(self):
        """Lazy load analyzer modules."""
        try:
            from analyzers.todo_tracker import TodoTracker
            from analyzers.dependency_analyzer import DependencyAnalyzer
            from analyzers.test_analyzer import TestAnalyzer
            from analyzers.config_analyzer import ConfigAnalyzer
            from analyzers.doc_analyzer import DocAnalyzer
            from analyzers.quality_scorer import QualityScorer
            from analyzers.complexity_analyzer import ComplexityAnalyzer
            
            if self.mode == 'advanced' or 'todos' in self.features:
                self.todo_tracker = TodoTracker()
            
            if self.mode == 'advanced' or 'dependencies' in self.features:
                self.dependency_analyzer = DependencyAnalyzer()
            
            if self.mode == 'advanced' or 'tests' in self.features:
                self.test_analyzer = TestAnalyzer()
            
            if self.mode == 'advanced' or 'config' in self.features:
                self.config_analyzer = ConfigAnalyzer()
            
            if self.mode == 'advanced' or 'docs' in self.features:
                self.doc_analyzer = DocAnalyzer()
            
            if self.mode == 'advanced' or 'quality' in self.features:
                self.quality_scorer = QualityScorer()
            
            if self.mode == 'advanced' or 'complexity' in self.features:
                self.complexity_analyzer = ComplexityAnalyzer()
                
        except ImportError as e:
            print(f"Warning: Could not load advanced analyzers: {e}")
    
    def analyze(self) -> Dict:
        """Perform comprehensive analysis - delegates to parent."""
        return super().analyze()
    
    def _run_advanced_analyzers(self, file_path: Path, line_count: int):
        """Run advanced analysis on each file."""
        if self.todo_tracker:
            self.todo_tracker.analyze(file_path)
        
        if self.dependency_analyzer:
            self.dependency_analyzer.analyze_file(file_path, self.path)
        
        if self.test_analyzer:
            self.test_analyzer.analyze_file(file_path, line_count, self.path)
        
        if self.config_analyzer:
            self.config_analyzer.analyze_file(file_path)
        
        if self.doc_analyzer:
            self.doc_analyzer.analyze_file(file_path)
        
        if self.complexity_analyzer and file_path.suffix == '.py':
            self.complexity_analyzer.analyze_file(str(file_path))
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive report with advanced features."""
        base_report = super()._generate_report()
        
        report = {
            'basic': base_report,
            'mode': self.mode,
        }
        
        if self.mode == 'simple':
            return report
        
        advanced_reports = {}
        
        if self.todo_tracker:
            advanced_reports['todos'] = self.todo_tracker.get_report()
        
        if self.dependency_analyzer:
            self.dependency_analyzer.detect_circular_dependencies()
            advanced_reports['dependencies'] = self.dependency_analyzer.get_report()
        
        if self.test_analyzer:
            advanced_reports['tests'] = self.test_analyzer.get_report()
        
        if self.config_analyzer:
            self.config_analyzer.check_required_configs(self.path)
            advanced_reports['config'] = self.config_analyzer.get_report()
        
        if self.doc_analyzer:
            advanced_reports['documentation'] = self.doc_analyzer.get_report()
        
        if self.complexity_analyzer:
            complexity_results = self.complexity_analyzer.analyze_directory(self.path)
            advanced_reports['complexity'] = self.complexity_analyzer.export_to_dict(complexity_results)
        
        if self.quality_scorer:
            quality_input = {
                'base': base_report,
                'test': advanced_reports.get('tests'),
                'documentation': advanced_reports.get('documentation'),
                'todos': advanced_reports.get('todos'),
                'config': advanced_reports.get('config'),
            }
            advanced_reports['quality'] = self.quality_scorer.calculate(quality_input)
        
        report['advanced'] = advanced_reports
        
        return report
