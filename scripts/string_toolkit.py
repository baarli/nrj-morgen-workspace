#!/usr/bin/env python3
"""
📝 BAARLICLAW STRING TOOLKIT
Avansert streng-manipulasjon
"""

import re
import unicodedata
from typing import List, Optional, Dict, Tuple
from difflib import SequenceMatcher

class StringUtils:
    """String utilities"""
    
    @staticmethod
    def camel_case(text: str) -> str:
        """Convert to camelCase"""
        words = re.findall(r'[a-zA-Z0-9]+', text)
        if not words:
            return ""
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    @staticmethod
    def pascal_case(text: str) -> str:
        """Convert to PascalCase"""
        words = re.findall(r'[a-zA-Z0-9]+', text)
        return ''.join(word.capitalize() for word in words)
    
    @staticmethod
    def snake_case(text: str) -> str:
        """Convert to snake_case"""
        # Insert underscore before capital letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Replace spaces and hyphens with underscore
        s3 = re.sub(r'[-\s]+', '_', s2)
        return s3.lower().strip('_')
    
    @staticmethod
    def kebab_case(text: str) -> str:
        """Convert to kebab-case"""
        return StringUtils.snake_case(text).replace('_', '-')
    
    @staticmethod
    def title_case(text: str) -> str:
        """Convert to Title Case"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def remove_accents(text: str) -> str:
        """Remove accents from characters"""
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """Extract all numbers from text"""
        return [int(n) for n in re.findall(r'-?\d+', text)]
    
    @staticmethod
    def extract_words(text: str, min_length: int = 2) -> List[str]:
        """Extract words from text"""
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return [w for w in words if len(w) >= min_length]
    
    @staticmethod
    def similarity(str1: str, str2: str) -> float:
        """Calculate string similarity (0-1)"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    @staticmethod
    def levenshtein_distance(str1: str, str2: str) -> int:
        """Calculate Levenshtein distance"""
        if len(str1) < len(str2):
            return StringUtils.levenshtein_distance(str2, str1)
        
        if len(str2) == 0:
            return len(str1)
        
        previous_row = range(len(str2) + 1)
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def wrap(text: str, width: int = 80) -> List[str]:
        """Wrap text to width"""
        lines = []
        current_line = ""
        
        for word in text.split():
            if len(current_line) + len(word) + 1 <= width:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    @staticmethod
    def mask(text: str, visible_start: int = 2, 
             visible_end: int = 2, mask_char: str = "*") -> str:
        """Mask string (e.g., credit card)"""
        if len(text) <= visible_start + visible_end:
            return mask_char * len(text)
        
        return text[:visible_start] + mask_char * (len(text) - visible_start - visible_end) + text[-visible_end:]
    
    @staticmethod
    def pluralize(word: str, count: int = 2) -> str:
        """Simple pluralization"""
        if count == 1:
            return word
        
        if word.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return word + 'es'
        elif word.endswith('y') and word[-2] not in 'aeiou':
            return word[:-1] + 'ies'
        elif word.endswith('f'):
            return word[:-1] + 'ves'
        elif word.endswith('fe'):
            return word[:-2] + 'ves'
        else:
            return word + 's'

class TextFormatter:
    """Text formatting utilities"""
    
    @staticmethod
    def indent(text: str, spaces: int = 4) -> str:
        """Indent text"""
        prefix = " " * spaces
        return '\n'.join(prefix + line for line in text.split('\n'))
    
    @staticmethod
    def dedent(text: str) -> str:
        """Remove common leading whitespace"""
        lines = text.split('\n')
        # Find minimum indentation
        min_indent = float('inf')
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)
        
        if min_indent == float('inf'):
            return text
        
        return '\n'.join(line[min_indent:] for line in lines)
    
    @staticmethod
    def align_columns(lines: List[str], delimiter: str = "|") -> str:
        """Align columns in text"""
        # Parse rows
        rows = [line.split(delimiter) for line in lines]
        
        # Find max width for each column
        col_widths = []
        for row in rows:
            for i, cell in enumerate(row):
                width = len(cell.strip())
                if i >= len(col_widths):
                    col_widths.append(width)
                else:
                    col_widths[i] = max(col_widths[i], width)
        
        # Format rows
        result = []
        for row in rows:
            formatted = []
            for i, cell in enumerate(row):
                width = col_widths[i] if i < len(col_widths) else 0
                formatted.append(cell.strip().ljust(width))
            result.append(f" {delimiter} ".join(formatted))
        
        return '\n'.join(result)
    
    @staticmethod
    def create_table(headers: List[str], rows: List[List[str]]) -> str:
        """Create ASCII table"""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Build table
        lines = []
        
        # Header
        header = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
        lines.append(header)
        lines.append("-" * len(header))
        
        # Rows
        for row in rows:
            lines.append(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))
        
        return '\n'.join(lines)

# === CONVENIENCE FUNCTIONS ===
def to_camel(text: str) -> str:
    """Quick camelCase"""
    return StringUtils.camel_case(text)

def to_snake(text: str) -> str:
    """Quick snake_case"""
    return StringUtils.snake_case(text)

def str_similarity(s1: str, s2: str) -> float:
    """Quick similarity check"""
    return StringUtils.similarity(s1, s2)

# === TESTING ===
if __name__ == "__main__":
    print("📝 BaarliClaw String Toolkit - Testing")
    print("=" * 50)
    
    # Test case conversions
    print("\n🧪 Testing Case Conversions")
    test = "hello world example"
    print(f"  Original: {test}")
    print(f"  camelCase: {StringUtils.camel_case(test)}")
    print(f"  PascalCase: {StringUtils.pascal_case(test)}")
    print(f"  snake_case: {StringUtils.snake_case(test)}")
    print(f"  kebab-case: {StringUtils.kebab_case(test)}")
    
    # Test extraction
    print("\n🧪 Testing Extraction")
    text = "Price: $100, Quantity: 5 items"
    numbers = StringUtils.extract_numbers(text)
    print(f"  Numbers from '{text}': {numbers}")
    
    words = StringUtils.extract_words(text)
    print(f"  Words: {words}")
    
    # Test similarity
    print("\n🧪 Testing Similarity")
    s1, s2 = "hello world", "hello there"
    sim = StringUtils.similarity(s1, s2)
    dist = StringUtils.levenshtein_distance(s1, s2)
    print(f"  '{s1}' vs '{s2}'")
    print(f"  Similarity: {sim:.2%}")
    print(f"  Distance: {dist}")
    
    # Test masking
    print("\n🧪 Testing Masking")
    card = "1234567890123456"
    masked = StringUtils.mask(card, 4, 4)
    print(f"  Card: {card}")
    print(f"  Masked: {masked}")
    
    # Test table
    print("\n🧪 Testing Table Creation")
    headers = ["Name", "Age", "City"]
    rows = [
        ["John Doe", "30", "New York"],
        ["Jane Smith", "25", "Los Angeles"]
    ]
    table = TextFormatter.create_table(headers, rows)
    print(table)
    
    # Test pluralization
    print("\n🧪 Testing Pluralization")
    words = ["cat", "dog", "city", "box"]
    for word in words:
        print(f"  {word} -> {StringUtils.pluralize(word, 2)}")
    
    print("\n✅ String Toolkit ready!")
