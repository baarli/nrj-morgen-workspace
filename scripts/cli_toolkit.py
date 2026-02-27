#!/usr/bin/env python3
"""
📋 BAARLICLAW CLI TOOLKIT
Kommandolinje-verktøy
"""

import sys
import argparse
from typing import List, Optional, Callable, Dict, Any

class CLIBuilder:
    """Build CLI applications"""
    
    def __init__(self, name: str, description: str = ""):
        self.parser = argparse.ArgumentParser(
            prog=name,
            description=description
        )
        self.subparsers = None
        self.commands: Dict[str, Callable] = {}
    
    def add_argument(self, *args, **kwargs):
        """Add argument"""
        self.parser.add_argument(*args, **kwargs)
        return self
    
    def add_command(self, name: str, func: Callable, help: str = ""):
        """Add subcommand"""
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(dest='command')
        
        subparser = self.subparsers.add_parser(name, help=help)
        self.commands[name] = (func, subparser)
        return subparser
    
    def parse(self, args: Optional[List[str]] = None):
        """Parse arguments"""
        return self.parser.parse_args(args)
    
    def run(self, args: Optional[List[str]] = None):
        """Run CLI"""
        parsed = self.parse(args)
        
        if hasattr(parsed, 'command') and parsed.command:
            func, _ = self.commands.get(parsed.command, (None, None))
            if func:
                # Convert args to kwargs
                kwargs = {k: v for k, v in vars(parsed).items() 
                         if k != 'command' and v is not None}
                return func(**kwargs)
        
        self.parser.print_help()

class TerminalUI:
    """Terminal UI utilities"""
    
    @staticmethod
    def print_table(headers: List[str], rows: List[List[str]]):
        """Print ASCII table"""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))
    
    @staticmethod
    def print_progress(current: int, total: int, width: int = 40):
        """Print progress bar"""
        pct = current / total if total > 0 else 0
        filled = int(width * pct)
        bar = '█' * filled + '░' * (width - filled)
        print(f"\r[{bar}] {pct*100:.1f}%", end='', flush=True)
        if current >= total:
            print()
    
    @staticmethod
    def ask(question: str, default: Optional[str] = None) -> str:
        """Ask user for input"""
        if default:
            prompt = f"{question} [{default}]: "
        else:
            prompt = f"{question}: "
        
        answer = input(prompt)
        return answer if answer else default
    
    @staticmethod
    def confirm(question: str, default: bool = False) -> bool:
        """Ask for confirmation"""
        suffix = " [Y/n]: " if default else " [y/N]: "
        answer = input(question + suffix).lower()
        
        if not answer:
            return default
        
        return answer in ('y', 'yes')
    
    @staticmethod
    def select(question: str, options: List[str]) -> int:
        """Let user select from options"""
        print(question)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input("Select (number): "))
                if 1 <= choice <= len(options):
                    return choice - 1
            except ValueError:
                pass
            print("Invalid choice, try again.")

class Colors:
    """Terminal colors"""
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    @classmethod
    def print(cls, text: str, color: str = ""):
        """Print colored text"""
        color_code = getattr(cls, color.upper(), "")
        print(f"{color_code}{text}{cls.RESET}")

# === CONVENIENCE FUNCTIONS ===
def print_success(text: str):
    """Print success message"""
    Colors.print(f"✓ {text}", "green")

def print_error(text: str):
    """Print error message"""
    Colors.print(f"✗ {text}", "red")

def print_warning(text: str):
    """Print warning message"""
    Colors.print(f"⚠ {text}", "yellow")

def print_info(text: str):
    """Print info message"""
    Colors.print(f"ℹ {text}", "blue")

# === TESTING ===
if __name__ == "__main__":
    print("📋 BaarliClaw CLI Toolkit - Testing")
    print("=" * 50)
    
    # Test table
    print("\n🧪 Testing Table")
    TerminalUI.print_table(
        ["Name", "Age", "City"],
        [
            ["John Doe", "30", "New York"],
            ["Jane Smith", "25", "Los Angeles"]
        ]
    )
    
    # Test progress bar
    print("\n🧪 Testing Progress Bar")
    import time
    for i in range(11):
        TerminalUI.print_progress(i, 10)
        time.sleep(0.05)
    
    # Test colors
    print("\n🧪 Testing Colors")
    print_success("Operation successful")
    print_error("An error occurred")
    print_warning("This is a warning")
    print_info("Information message")
    
    print("\n✅ CLI Toolkit ready!")
