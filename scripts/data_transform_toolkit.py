#!/usr/bin/env python3
"""
🔄 BAARLICLAW DATA TRANSFORM TOOLKIT
Data-transformasjon og -konvertering
"""

import os
import sys
import json
import csv
import re
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("DataTransformToolkit")

class DataTransformer:
    """Transform data between formats"""
    
    @staticmethod
    def json_to_csv(json_data: List[Dict], 
                    output_path: Optional[str] = None) -> Optional[str]:
        """Convert JSON to CSV"""
        if not json_data:
            return None
        
        # Get all unique keys
        keys = set()
        for item in json_data:
            keys.update(item.keys())
        keys = sorted(keys)
        
        # Create CSV
        lines = []
        lines.append(','.join(keys))
        
        for item in json_data:
            row = []
            for key in keys:
                value = item.get(key, '')
                # Escape commas and quotes
                if isinstance(value, str):
                    value = value.replace('"', '""')
                    if ',' in value or '"' in value:
                        value = f'"{value}"'
                row.append(str(value))
            lines.append(','.join(row))
        
        csv_content = '\n'.join(lines)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(csv_content)
            logger.info(f"CSV saved to {output_path}")
        
        return csv_content
    
    @staticmethod
    def csv_to_json(csv_content: str) -> List[Dict]:
        """Convert CSV to JSON"""
        lines = csv_content.strip().split('\n')
        if not lines:
            return []
        
        # Parse header
        reader = csv.DictReader(lines)
        return list(reader)
    
    @staticmethod
    def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataTransformer.flatten_dict(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def unflatten_dict(d: Dict, sep: str = '_') -> Dict:
        """Unflatten dictionary"""
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            target = result
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value
        return result
    
    @staticmethod
    def rename_keys(data: Dict, key_map: Dict[str, str]) -> Dict:
        """Rename dictionary keys"""
        return {key_map.get(k, k): v for k, v in data.items()}
    
    @staticmethod
    def filter_keys(data: Dict, keys: List[str]) -> Dict:
        """Filter dictionary to only include certain keys"""
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def convert_types(data: Dict, type_map: Dict[str, type]) -> Dict:
        """Convert values to specific types"""
        result = {}
        for key, value in data.items():
            if key in type_map:
                try:
                    result[key] = type_map[key](value)
                except (ValueError, TypeError):
                    result[key] = value
            else:
                result[key] = value
        return result

class TextTransformer:
    """Text transformation utilities"""
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(name: str) -> str:
        """Convert snake_case to CamelCase"""
        return ''.join(word.capitalize() for word in name.split('_'))
    
    @staticmethod
    def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
        """Truncate text to length"""
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract email addresses from text"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(pattern, text)
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """Remove extra whitespace"""
        return ' '.join(text.split())

class DateTimeTransformer:
    """Date/time transformation utilities"""
    
    FORMATS = {
        'iso': '%Y-%m-%dT%H:%M:%S',
        'date': '%Y-%m-%d',
        'datetime': '%Y-%m-%d %H:%M:%S',
        'time': '%H:%M:%S',
        'readable': '%B %d, %Y at %I:%M %p',
        'compact': '%Y%m%d_%H%M%S'
    }
    
    @classmethod
    def format_datetime(cls, dt: datetime, format_name: str = 'iso') -> str:
        """Format datetime to string"""
        fmt = cls.FORMATS.get(format_name, cls.FORMATS['iso'])
        return dt.strftime(fmt)
    
    @classmethod
    def parse_datetime(cls, text: str, format_name: str = 'iso') -> Optional[datetime]:
        """Parse datetime from string"""
        fmt = cls.FORMATS.get(format_name, cls.FORMATS['iso'])
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            return None
    
    @staticmethod
    def to_timestamp(dt: datetime) -> int:
        """Convert datetime to Unix timestamp"""
        return int(dt.timestamp())
    
    @staticmethod
    def from_timestamp(ts: int) -> datetime:
        """Convert Unix timestamp to datetime"""
        return datetime.fromtimestamp(ts)
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """Add days to datetime"""
        from datetime import timedelta
        return dt + timedelta(days=days)

# === CONVENIENCE FUNCTIONS ===
def quick_json_to_csv(json_data: List[Dict], output: str) -> bool:
    """Quick JSON to CSV conversion"""
    result = DataTransformer.json_to_csv(json_data, output)
    return result is not None

def quick_slug(text: str) -> str:
    """Quick slug generation"""
    return TextTransformer.slugify(text)

def quick_camel_to_snake(name: str) -> str:
    """Quick case conversion"""
    return TextTransformer.camel_to_snake(name)

# === TESTING ===
if __name__ == "__main__":
    print("🔄 BaarliClaw Data Transform Toolkit - Testing")
    print("=" * 50)
    
    # Test data transformation
    print("\n🧪 Testing Data Transformer")
    
    test_data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "Los Angeles"}
    ]
    
    csv = DataTransformer.json_to_csv(test_data)
    print("✅ JSON to CSV:")
    print(csv)
    
    # Test flatten
    nested = {"user": {"name": "John", "address": {"city": "NYC"}}}
    flat = DataTransformer.flatten_dict(nested)
    print(f"✅ Flattened: {flat}")
    
    # Test text transformation
    print("\n🧪 Testing Text Transformer")
    
    text = "Hello World Test"
    slug = TextTransformer.slugify(text)
    print(f"✅ Slug: '{text}' -> '{slug}'")
    
    camel = "helloWorldTest"
    snake = TextTransformer.camel_to_snake(camel)
    print(f"✅ Camel to snake: '{camel}' -> '{snake}'")
    
    long_text = "This is a very long text that needs to be truncated"
    truncated = TextTransformer.truncate(long_text, 20)
    print(f"✅ Truncated: '{truncated}'")
    
    # Test datetime
    print("\n🧪 Testing DateTime Transformer")
    
    now = datetime.now()
    formatted = DateTimeTransformer.format_datetime(now, 'readable')
    print(f"✅ Formatted: {formatted}")
    
    print("\n✅ Data Transform Toolkit ready!")
