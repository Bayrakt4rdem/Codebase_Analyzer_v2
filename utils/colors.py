"""
Cross-platform terminal colors without external dependencies.
Falls back gracefully on Windows if ANSI not supported.
"""

import sys
import os


class Colors:
    """ANSI color codes for terminal output."""
    
    # Check if we should use colors
    ENABLED = (
        hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        and os.getenv('NO_COLOR') is None
    )
    
    # Basic colors
    BLACK = '\033[30m' if ENABLED else ''
    RED = '\033[31m' if ENABLED else ''
    GREEN = '\033[32m' if ENABLED else ''
    YELLOW = '\033[33m' if ENABLED else ''
    BLUE = '\033[34m' if ENABLED else ''
    MAGENTA = '\033[35m' if ENABLED else ''
    CYAN = '\033[36m' if ENABLED else ''
    WHITE = '\033[37m' if ENABLED else ''
    
    # Bright colors
    BRIGHT_RED = '\033[91m' if ENABLED else ''
    BRIGHT_GREEN = '\033[92m' if ENABLED else ''
    BRIGHT_YELLOW = '\033[93m' if ENABLED else ''
    BRIGHT_BLUE = '\033[94m' if ENABLED else ''
    BRIGHT_MAGENTA = '\033[95m' if ENABLED else ''
    BRIGHT_CYAN = '\033[96m' if ENABLED else ''
    
    # Formatting
    BOLD = '\033[1m' if ENABLED else ''
    DIM = '\033[2m' if ENABLED else ''
    UNDERLINE = '\033[4m' if ENABLED else ''
    RESET = '\033[0m' if ENABLED else ''
    
    @staticmethod
    def enable():
        """Force enable colors."""
        # Enable ANSI on Windows 10+
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass
    
    @staticmethod
    def disable():
        """Disable colors."""
        Colors.ENABLED = False
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Wrap text in color codes."""
        if not Colors.ENABLED:
            return text
        return f"{color}{text}{Colors.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        """Green text for success."""
        return Colors.colorize(text, Colors.BRIGHT_GREEN)
    
    @staticmethod
    def error(text: str) -> str:
        """Red text for errors."""
        return Colors.colorize(text, Colors.BRIGHT_RED)
    
    @staticmethod
    def warning(text: str) -> str:
        """Yellow text for warnings."""
        return Colors.colorize(text, Colors.BRIGHT_YELLOW)
    
    @staticmethod
    def info(text: str) -> str:
        """Cyan text for info."""
        return Colors.colorize(text, Colors.BRIGHT_CYAN)
    
    @staticmethod
    def bold(text: str) -> str:
        """Bold text."""
        return Colors.colorize(text, Colors.BOLD)
    
    @staticmethod
    def dim(text: str) -> str:
        """Dimmed text."""
        return Colors.colorize(text, Colors.DIM)


# Convenience functions
def red(text: str) -> str:
    return Colors.error(text)

def green(text: str) -> str:
    return Colors.success(text)

def yellow(text: str) -> str:
    return Colors.warning(text)

def cyan(text: str) -> str:
    return Colors.info(text)

def bold(text: str) -> str:
    return Colors.bold(text)


# Initialize colors for Windows
if sys.platform == 'win32' and Colors.ENABLED:
    Colors.enable()
