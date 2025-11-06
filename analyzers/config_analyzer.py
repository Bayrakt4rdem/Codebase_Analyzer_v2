"""
Configuration file analyzer - detects config files and potential secrets.
"""

import re
from pathlib import Path
from typing import Dict, List, Set


class ConfigAnalyzer:
    CONFIG_EXTENSIONS = {
        '.env', '.yaml', '.yml', '.json', '.toml',
        '.ini', '.cfg', '.conf', '.config'
    }
    
    CONFIG_FILENAMES = {
        'config.py', 'settings.py', 'configuration.py',
        '.env.example', '.env.local', '.env.production',
        'docker-compose.yml', 'docker-compose.yaml'
    }
    
    SECRET_PATTERNS = [
        (r'password\s*[=:]\s*["\'](.+?)["\']', 'password'),
        (r'api[_-]?key\s*[=:]\s*["\'](.+?)["\']', 'api_key'),
        (r'secret\s*[=:]\s*["\'](.+?)["\']', 'secret'),
        (r'token\s*[=:]\s*["\'](.+?)["\']', 'token'),
        (r'auth[_-]?key\s*[=:]\s*["\'](.+?)["\']', 'auth_key'),
    ]
    
    def __init__(self):
        self.config_files = []
        self.env_files = []
        self.potential_secrets = []
        self.required_configs_missing = []
        
    def analyze_file(self, file_path: Path) -> None:
        if self._is_config_file(file_path):
            self.config_files.append(file_path)
            
            if '.env' in file_path.name:
                self.env_files.append(file_path)
            
            self._scan_for_secrets(file_path)
    
    def _is_config_file(self, file_path: Path) -> bool:
        if file_path.suffix.lower() in self.CONFIG_EXTENSIONS:
            return True
        if file_path.name in self.CONFIG_FILENAMES:
            return True
        return False
    
    def _scan_for_secrets(self, file_path: Path) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for line_num, line in enumerate(content.split('\n'), 1):
                    for pattern, secret_type in self.SECRET_PATTERNS:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match and not self._is_safe_value(match.group(1)):
                            self.potential_secrets.append({
                                'file': file_path,
                                'line': line_num,
                                'type': secret_type,
                                'context': line.strip()[:100]
                            })
        except (PermissionError, OSError):
            pass
    
    def _is_safe_value(self, value: str) -> bool:
        safe_indicators = [
            'your_', 'example', 'test', 'dummy', 'placeholder',
            'xxx', '***', '...', 'changeme', 'replace'
        ]
        return any(indicator in value.lower() for indicator in safe_indicators)
    
    def check_required_configs(self, base_path: Path) -> None:
        required = [
            ('.env', 'Environment variables'),
            ('.gitignore', 'Git ignore file'),
            ('requirements.txt', 'Python dependencies') if (base_path / '*.py').exists() else None,
            ('package.json', 'Node dependencies') if (base_path / '*.js').exists() else None,
        ]
        
        for config_tuple in required:
            if config_tuple and not (base_path / config_tuple[0]).exists():
                self.required_configs_missing.append(config_tuple)
    
    def get_report(self) -> Dict:
        return {
            'config_files': [str(f) for f in self.config_files],
            'config_count': len(self.config_files),
            'env_files': [str(f) for f in self.env_files],
            'potential_secrets': self.potential_secrets[:10],
            'secret_count': len(self.potential_secrets),
            'missing_configs': self.required_configs_missing
        }
