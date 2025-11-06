"""
Quality scorer - calculates overall codebase health score.
"""

from typing import Dict, List


class QualityScorer:
    WEIGHTS = {
        'test_coverage': 0.30,
        'documentation': 0.25,
        'code_organization': 0.20,
        'technical_debt': 0.15,
        'security': 0.10,
    }
    
    def __init__(self):
        self.scores = {}
        self.grade = 'F'
        self.overall_score = 0
        
    def calculate(self, reports: Dict) -> Dict:
        test_score = self._score_tests(reports.get('test', {}))
        doc_score = self._score_documentation(reports.get('documentation', {}))
        org_score = self._score_organization(reports.get('base', {}))
        debt_score = self._score_technical_debt(reports.get('todos', {}))
        security_score = self._score_security(reports.get('config', {}))
        
        self.scores = {
            'test_coverage': test_score,
            'documentation': doc_score,
            'code_organization': org_score,
            'technical_debt': debt_score,
            'security': security_score,
        }
        
        self.overall_score = sum(
            score * self.WEIGHTS[category]
            for category, score in self.scores.items()
        )
        
        self.grade = self._calculate_grade(self.overall_score)
        
        return self.get_report()
    
    def _score_tests(self, test_report: Dict) -> int:
        if not test_report:
            return 50
        
        coverage = test_report.get('coverage_estimate', 0)
        if coverage >= 80:
            return 100
        elif coverage >= 60:
            return 85
        elif coverage >= 40:
            return 70
        elif coverage >= 20:
            return 55
        return 40
    
    def _score_documentation(self, doc_report: Dict) -> int:
        if not doc_report:
            return 50
        
        coverage = doc_report.get('overall_coverage', 0)
        has_readme = doc_report.get('readme_present', False)
        
        score = coverage
        if has_readme:
            score += 10
        
        return min(100, score)
    
    def _score_organization(self, base_report: Dict) -> int:
        if not base_report:
            return 70
        
        score = 80
        
        avg_lines = base_report.get('avg_lines_per_file', 0)
        if avg_lines > 500:
            score -= 20
        elif avg_lines > 300:
            score -= 10
        
        empty_ratio = base_report.get('empty_file_count', 0) / max(base_report.get('total_files', 1), 1)
        if empty_ratio > 0.1:
            score -= 10
        
        return max(0, score)
    
    def _score_technical_debt(self, todo_report: Dict) -> int:
        if not todo_report:
            return 80
        
        total_count = todo_report.get('total_count', 0)
        total_files = 100  # Placeholder
        
        todos_per_file = total_count / max(total_files, 1)
        
        if todos_per_file < 0.5:
            return 100
        elif todos_per_file < 1.5:
            return 80
        elif todos_per_file < 3:
            return 60
        return 40
    
    def _score_security(self, config_report: Dict) -> int:
        if not config_report:
            return 70
        
        secret_count = config_report.get('secret_count', 0)
        
        if secret_count == 0:
            return 100
        elif secret_count <= 2:
            return 70
        elif secret_count <= 5:
            return 50
        return 30
    
    def _calculate_grade(self, score: float) -> str:
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D+'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    def get_report(self) -> Dict:
        return {
            'overall_score': round(self.overall_score, 2),
            'grade': self.grade,
            'category_scores': {k: round(v, 2) for k, v in self.scores.items()},
            'recommendations': self._get_recommendations()
        }
    
    def _get_recommendations(self) -> List[str]:
        recs = []
        
        if self.scores.get('test_coverage', 0) < 70:
            recs.append("Increase test coverage")
        if self.scores.get('documentation', 0) < 70:
            recs.append("Improve documentation")
        if self.scores.get('technical_debt', 0) < 70:
            recs.append("Address technical debt (TODOs/FIXMEs)")
        if self.scores.get('security', 0) < 70:
            recs.append("Review potential security issues")
        if self.scores.get('code_organization', 0) < 70:
            recs.append("Refactor large files")
        
        return recs
