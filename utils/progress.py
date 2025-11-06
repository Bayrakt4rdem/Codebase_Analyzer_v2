"""
Simple progress indicator without external dependencies.
"""

import sys
import time
from typing import Optional


class ProgressBar:
    """Simple terminal progress bar."""
    
    def __init__(self, total: int, prefix: str = 'Progress', width: int = 50, enabled: bool = True):
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.width = width
        self.enabled = enabled
        self.start_time = time.time()
        
    def update(self, count: int = 1, suffix: str = ''):
        """Update progress bar."""
        if not self.enabled:
            return
            
        self.current += count
        if self.current > self.total:
            self.current = self.total
            
        percent = 100 * (self.current / self.total) if self.total > 0 else 100
        filled = int(self.width * self.current / self.total) if self.total > 0 else self.width
        bar = '#' * filled + '-' * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if self.current > 0 and self.current < self.total:
            eta = elapsed * (self.total - self.current) / self.current
            eta_str = f" ETA: {int(eta)}s"
        else:
            eta_str = ""
        
        sys.stdout.write(f'\r{self.prefix}: [{bar}] {percent:.1f}% ({self.current}/{self.total}){eta_str}{suffix}')
        sys.stdout.flush()
        
    def finish(self, message: Optional[str] = None):
        """Complete the progress bar."""
        if not self.enabled:
            return
            
        elapsed = time.time() - self.start_time
        if message:
            sys.stdout.write(f'\r{message} (completed in {elapsed:.1f}s)\n')
        else:
            sys.stdout.write(f'\r{self.prefix}: Complete! ({self.total} items in {elapsed:.1f}s)\n')
        sys.stdout.flush()


class SpinnerProgress:
    """Simple spinner for indeterminate progress."""
    
    FRAMES = ['|', '/', '-', '\\']
    
    def __init__(self, message: str = 'Processing', enabled: bool = True):
        self.message = message
        self.enabled = enabled
        self.frame = 0
        self.running = False
        
    def update(self, message: Optional[str] = None):
        """Update spinner frame."""
        if not self.enabled:
            return
            
        if message:
            self.message = message
            
        frame_char = self.FRAMES[self.frame % len(self.FRAMES)]
        sys.stdout.write(f'\r{frame_char} {self.message}...')
        sys.stdout.flush()
        self.frame += 1
        
    def finish(self, message: Optional[str] = None):
        """Stop spinner."""
        if not self.enabled:
            return
            
        if message:
            sys.stdout.write(f'\r> {message}\n')
        else:
            sys.stdout.write(f'\r> {self.message} - Done\n')
        sys.stdout.flush()
