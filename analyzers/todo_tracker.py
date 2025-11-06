"""
Technical debt tracker - scans for TODO, FIXME, HACK markers.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class TodoTracker:
    MARKERS = {
        'FIXME': {'priority': 'high', 'icon': '🔴'},
        'TODO': {'priority': 'medium', 'icon': '-'},
        'HACK': {'priority': 'code_smell', 'icon': '[!!]'},
        'XXX': {'priority': 'high', 'icon': '🔴'},
        'TEMP': {'priority': 'code_smell', 'icon': '[!!]'},
        'NOTE': {'priority': 'low', 'icon': '*'},
        'BUG': {'priority': 'high', 'icon': '🐛'},
    }
    
    def __init__(self):
        self.todos = defaultdict(list)
        self.by_priority = defaultdict(list)
        self.by_file = defaultdict(list)
        self.total_count = 0
        
    def analyze(self, file_path: Path, encoding='utf-8') -> None:
        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    self._scan_line(line, line_num, file_path)
        except (PermissionError, OSError):
            pass
    
    def _scan_line(self, line: str, line_num: int, file_path: Path) -> None:
        for marker, info in self.MARKERS.items():
            pattern = rf'#\s*{marker}[\s:]*(.+)|//\s*{marker}[\s:]*(.+)|/\*\s*{marker}[\s:]*(.+)'
            match = re.search(pattern, line, re.IGNORECASE)
            
            if match:
                message = (match.group(1) or match.group(2) or match.group(3) or '').strip()
                todo_item = {
                    'marker': marker,
                    'priority': info['priority'],
                    'message': message,
                    'file': file_path,
                    'line': line_num,
                    'icon': info['icon']
                }
                
                self.todos[marker].append(todo_item)
                self.by_priority[info['priority']].append(todo_item)
                self.by_file[file_path].append(todo_item)
                self.total_count += 1
                break
    
    def get_report(self) -> Dict:
        return {
            'total_count': self.total_count,
            'by_marker': dict(self.todos),
            'by_priority': dict(self.by_priority),
            'by_file': dict(self.by_file),
            'summary': {
                marker: len(items) for marker, items in self.todos.items()
            }
        }
