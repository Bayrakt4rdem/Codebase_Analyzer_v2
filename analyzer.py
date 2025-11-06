"""
Core analyzer module for codebase analysis.
"""

import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import mimetypes


class CodebaseAnalyzer:
    """Analyzes a codebase and provides comprehensive statistics."""
    
    # Directories and files to ignore
    IGNORE_DIRS = {
        '__pycache__', '.git', '.venv', 'venv', 'env', 
        'node_modules', '.pytest_cache', '.mypy_cache',
        'dist', 'build', 'egg-info', '.tox', '.coverage',
        '.idea', '.vscode', '__pypackages__'
    }
    
    IGNORE_EXTENSIONS = {
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
        '.exe', '.bin', '.obj', '.o', '.a', '.lib',
        '.class', '.jar', '.war', '.ear'
    }
    
    # Common code file extensions by language
    LANGUAGE_EXTENSIONS = {
        'Python': ['.py', '.pyw', '.pyx', '.pxd', '.pxi'],
        'JavaScript': ['.js', '.jsx', '.mjs', '.cjs'],
        'TypeScript': ['.ts', '.tsx'],
        'Java': ['.java'],
        'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.h', '.hxx'],
        'C': ['.c', '.h'],
        'C#': ['.cs'],
        'Go': ['.go'],
        'Rust': ['.rs'],
        'Ruby': ['.rb'],
        'PHP': ['.php'],
        'Swift': ['.swift'],
        'Kotlin': ['.kt', '.kts'],
        'HTML': ['.html', '.htm'],
        'CSS': ['.css', '.scss', '.sass', '.less'],
        'SQL': ['.sql'],
        'Shell': ['.sh', '.bash', '.zsh'],
        'PowerShell': ['.ps1', '.psm1', '.psd1'],
        'Markdown': ['.md', '.markdown'],
        'Text': ['.txt', '.log', '.csv', '.tsv'],
        'YAML': ['.yaml', '.yml'],
        'JSON': ['.json'],
        'XML': ['.xml'],
        'TOML': ['.toml'],
        'INI': ['.ini', '.cfg', '.conf'],
    }
    
    def __init__(self, path: str):
        """Initialize the analyzer with a codebase path."""
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise ValueError(f"Path does not exist: {path}")
        if not self.path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        
        # Statistics
        self.total_size = 0
        self.total_files = 0
        self.total_dirs = 0
        self.lines_by_language = defaultdict(int)
        self.files_by_language = defaultdict(int)
        self.size_by_language = defaultdict(int)
        self.lines_per_file_by_language = defaultdict(list)  # Track individual file line counts
        self.file_sizes = []
        self.file_lines = []
        self.empty_files = []  # Track empty files
        self.empty_by_folder = defaultdict(int)  # Track empty files per folder
        self.pycache_size = 0
        self.pycache_files = 0
        self.venv_size = 0
        self.venv_files = 0
        self.venv_dirs = []  # Track venv directories and their sizes
        self.ignored_size = 0
        self.ignored_files = 0
        self.ignored_by_type = defaultdict(lambda: {'count': 0, 'size': 0})  # Track ignored file types
        
        # Temporal statistics
        self.oldest_file = None
        self.oldest_date = None
        self.newest_file = None
        self.newest_date = None
        
    def _get_language(self, file_path: Path) -> str:
        """Determine the programming language based on file extension."""
        ext = file_path.suffix.lower()
        for language, extensions in self.LANGUAGE_EXTENSIONS.items():
            if ext in extensions:
                return language
        return 'Other'
    
    def _should_ignore_dir(self, dir_name: str) -> bool:
        """Check if directory should be ignored."""
        return dir_name in self.IGNORE_DIRS or dir_name.startswith('.')
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored."""
        # Ignore by extension
        if file_path.suffix.lower() in self.IGNORE_EXTENSIONS:
            return True
        # Ignore hidden files
        if file_path.name.startswith('.'):
            return True
        # Ignore lock files
        if file_path.name.endswith(('.lock', '.log')):
            return True
        return False
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file, handling encoding issues."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return sum(1 for _ in f)
            except (UnicodeDecodeError, PermissionError):
                continue
        # If all encodings fail, try binary mode
        try:
            with open(file_path, 'rb') as f:
                return sum(1 for _ in f)
        except:
            return 0
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file."""
        # Check by extension first
        ext = file_path.suffix.lower()
        for extensions in self.LANGUAGE_EXTENSIONS.values():
            if ext in extensions:
                return True
        
        # Check by mimetype
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith('text'):
            return True
        
        # Try to read first few bytes
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(512)
                if b'\x00' in chunk:  # Binary files often have null bytes
                    return False
                return True
        except:
            return False
    
    def analyze(self) -> Dict:
        """Perform comprehensive analysis of the codebase."""
        print(f"Analyzing codebase: {self.path}")
        print("This may take a moment...\n")
        
        for root, dirs, files in os.walk(self.path):
            root_path = Path(root)
            
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore_dir(d)]
            
            # Track special directories
            current_dir_name = root_path.name
            is_pycache = current_dir_name == '__pycache__'
            is_venv = current_dir_name in {'venv', '.venv', 'env'}
            
            # Track venv directory
            if is_venv and root_path not in [v[0] for v in self.venv_dirs]:
                self.venv_dirs.append([root_path, 0])  # [path, size]
            
            self.total_dirs += len(dirs)
            
            for file in files:
                file_path = root_path / file
                
                try:
                    file_stat = file_path.stat()
                    file_size = file_stat.st_size
                    file_mtime = file_stat.st_mtime
                except (OSError, PermissionError):
                    continue
                
                # Track special directory sizes
                if is_pycache:
                    self.pycache_size += file_size
                    self.ignored_size += file_size
                    continue
                
                if is_venv:
                    self.venv_size += file_size
                    # Update venv directory size
                    for venv_info in self.venv_dirs:
                        if str(root_path).startswith(str(venv_info[0])):
                            venv_info[1] += file_size
                            break
                    self.ignored_size += file_size
                    continue
                
                # Skip ignored files
                if self._should_ignore_file(file_path):
                    self.ignored_size += file_size
                    self.ignored_files += 1
                    # Categorize ignored files
                    if file_path.suffix.lower() in self.IGNORE_EXTENSIONS:
                        category = f"Binary files ({file_path.suffix})"
                    elif file_path.name.startswith('.'):
                        category = "Hidden files"
                    elif file_path.name.endswith(('.lock', '.log')):
                        category = "Lock/Log files"
                    else:
                        category = "Other ignored"
                    self.ignored_by_type[category]['count'] += 1
                    self.ignored_by_type[category]['size'] += file_size
                    continue
                
                # Count this file
                self.total_files += 1
                self.total_size += file_size
                
                # Track oldest and newest files
                if self.oldest_date is None or file_mtime < self.oldest_date:
                    self.oldest_date = file_mtime
                    self.oldest_file = file_path
                if self.newest_date is None or file_mtime > self.newest_date:
                    self.newest_date = file_mtime
                    self.newest_file = file_path
                
                # Determine language and count lines for text files
                language = self._get_language(file_path)
                self.files_by_language[language] += 1
                self.size_by_language[language] += file_size
                
                # Count lines for code files
                if self._is_text_file(file_path):
                    line_count = self._count_lines(file_path)
                    self.lines_by_language[language] += line_count
                    self.lines_per_file_by_language[language].append(line_count)
                    self.file_lines.append((file_path, line_count, language))
                    
                    # Track empty files
                    if line_count == 0:
                        self.empty_files.append((file_path, language))
                        self.empty_by_folder[str(file_path.parent)] += 1
                
                self.file_sizes.append((file_path, file_size, language))
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive report from collected statistics."""
        # Sort files by size and lines
        self.file_sizes.sort(key=lambda x: x[1], reverse=True)
        self.file_lines.sort(key=lambda x: x[1], reverse=True)
        
        # Sort empty files by folder
        top_empty_folders = sorted(
            self.empty_by_folder.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Calculate averages
        total_lines = sum(self.lines_by_language.values())
        avg_lines_per_file = total_lines / self.total_files if self.total_files > 0 else 0
        
        # Calculate average lines per file by language
        avg_lines_by_language = {}
        for lang, line_counts in self.lines_per_file_by_language.items():
            if line_counts:
                avg_lines_by_language[lang] = sum(line_counts) / len(line_counts)
        
        # Determine primary language
        primary_language = max(self.lines_by_language.items(), key=lambda x: x[1])[0] if self.lines_by_language else "Unknown"
        
        # Identify outliers
        files_with_lines = [x[1] for x in self.file_lines]
        if files_with_lines:
            avg_lines = sum(files_with_lines) / len(files_with_lines)
            too_long = [x for x in self.file_lines if x[1] > avg_lines * 3]
            too_short = [x for x in self.file_lines if x[1] < 10 and x[1] > 0]
        else:
            too_long = []
            too_short = []
        
        report = {
            'path': str(self.path),
            'total_size': self.total_size,
            'total_files': self.total_files,
            'total_dirs': self.total_dirs,
            'total_lines': total_lines,
            'avg_lines_per_file': avg_lines_per_file,
            'primary_language': primary_language,
            'lines_by_language': dict(self.lines_by_language),
            'files_by_language': dict(self.files_by_language),
            'size_by_language': dict(self.size_by_language),
            'avg_lines_by_language': avg_lines_by_language,
            'top_largest_files': self.file_sizes[:10],
            'too_long_files': too_long[:20],
            'too_short_files': too_short[:20],
            'empty_files': self.empty_files,
            'empty_file_count': len(self.empty_files),
            'top_empty_folders': top_empty_folders,
            'pycache_size': self.pycache_size,
            'pycache_files': self.pycache_files,
            'venv_size': self.venv_size,
            'venv_files': self.venv_files,
            'venv_dirs': self.venv_dirs,
            'ignored_size': self.ignored_size,
            'ignored_files': self.ignored_files,
            'ignored_by_type': dict(self.ignored_by_type),
            'oldest_file': self.oldest_file,
            'oldest_date': self.oldest_date,
            'newest_file': self.newest_file,
            'newest_date': self.newest_date,
        }
        
        return report
