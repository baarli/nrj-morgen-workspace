#!/usr/bin/env python3
"""
🧰 BAARLICLAW TOOLKIT - INTEGRATION DEMO
Viser hvordan verktøyene brukes i praksis
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

# Import alle verktøy
from baarliclaw_toolkit import setup_logging, BraveSearchClient
from validation_toolkit import Validator
from data_analyzer import TextAnalyzer, DataVisualizer
from string_toolkit import StringUtils
from date_toolkit import DateUtils
from collections_toolkit import ListUtils, DictUtils
from math_toolkit import Statistics
from color_toolkit import ColorUtils
from uuid_toolkit import UUIDUtils
from cli_toolkit import TerminalUI, Colors

# Setup
logger = setup_logging("toolkit-demo")

def demo_validation():
    """Demo: validation_toolkit"""
    print(f"\n{Colors.CYAN}📋 DEMO: Validation Toolkit{Colors.RESET}")
    print("-" * 50)
    
    # Valider e-post
    emails = ["test@example.com", "invalid-email", "user@domain.org"]
    for email in emails:
        result = Validator.email(email)
        status = "✅" if result.valid else "❌"
        error_msg = result.errors[0] if result.errors else "OK"
        print(f"{status} {email}: {error_msg}")
    
    # Valider URL
    url = "https://example.com/path?query=value"
    result = Validator.url(url)
    print(f"\n🔗 URL: {url}")
    print(f"   Valid: {result.valid}")
    print(f"   Normalized: {result.cleaned_value}")

def demo_string_utils():
    """Demo: string_toolkit"""
    print(f"\n{Colors.CYAN}📝 DEMO: String Toolkit{Colors.RESET}")
    print("-" * 50)
    
    text = "Hello World Example"
    print(f"Original: {text}")
    print(f"camelCase: {StringUtils.camel_case(text)}")
    print(f"snake_case: {StringUtils.snake_case(text)}")
    print(f"kebab-case: {StringUtils.kebab_case(text)}")
    print(f"Title Case: {StringUtils.title_case(text)}")
    
    # Similarity
    str1 = "hello world"
    str2 = "hallo verden"
    similarity = StringUtils.similarity(str1, str2)
    print(f"\nSimilarity '{str1}' vs '{str2}': {similarity:.2%}")

def demo_data_analysis():
    """Demo: data_analyzer"""
    print(f"\n{Colors.CYAN}📊 DEMO: Data Analyzer{Colors.RESET}")
    print("-" * 50)
    
    # Tekstanalyse
    text = "Dette er en fantastisk dag! Jeg er så glad og fornøyd."
    analyzer = TextAnalyzer()
    sentiment = analyzer.analyze_sentiment_simple(text)
    
    print(f"Tekst: {text}")
    print(f"Sentiment: Pos={sentiment['positive']:.2f}, Neg={sentiment['negative']:.2f}, Neu={sentiment['neutral']:.2f}")
    
    # Data visualisering
    data = [23, 45, 56, 78, 32, 67, 89, 12, 45, 67]
    print(f"\nData: {data}")
    print(f"ASCII Histogram:")
    visualizer = DataVisualizer()
    print(visualizer.create_ascii_chart(data))

def demo_math_stats():
    """Demo: math_toolkit"""
    print(f"\n{Colors.CYAN}🔢 DEMO: Math Toolkit{Colors.RESET}")
    print("-" * 50)
    
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    stats = Statistics.calculate(data)
    
    print(f"Data: {data}")
    print(f"Mean: {stats.mean:.2f}")
    print(f"Median: {stats.median:.2f}")
    print(f"Std Dev: {stats.std_dev:.2f}")
    print(f"Min: {stats.min}, Max: {stats.max}")

def demo_collections():
    """Demo: collections_toolkit"""
    print(f"\n{Colors.CYAN}📦 DEMO: Collections Toolkit{Colors.RESET}")
    print("-" * 50)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Chunk
    chunks = ListUtils.chunk(data, 3)
    print(f"Chunk (size 3): {chunks}")
    
    # Group by - manuell implementasjon
    items = [
        {'category': 'A', 'value': 1},
        {'category': 'B', 'value': 2},
        {'category': 'A', 'value': 3},
    ]
    grouped = {}
    for item in items:
        cat = item['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(item)
    print(f"\nGrouped by category: {grouped}")

def demo_date_utils():
    """Demo: date_toolkit"""
    print(f"\n{Colors.CYAN}📅 DEMO: Date Toolkit{Colors.RESET}")
    print("-" * 50)
    
    now = DateUtils.now()
    print(f"Now: {DateUtils.format(now)}")
    
    tomorrow = DateUtils.add_days(now, 1)
    print(f"Tomorrow: {DateUtils.format(tomorrow)}")
    
    next_week = DateUtils.add_days(now, 7)
    print(f"Next week: {DateUtils.format(next_week)}")
    
    # Parse date
    parsed = DateUtils.parse("2026-02-28")
    print(f"\nParsed: {DateUtils.format(parsed)}")

def demo_colors():
    """Demo: color_toolkit"""
    print(f"\n{Colors.CYAN}🎨 DEMO: Color Toolkit{Colors.RESET}")
    print("-" * 50)
    
    hex_color = "#FF5733"
    rgb = ColorUtils.hex_to_rgb(hex_color)
    print(f"Hex: {hex_color}")
    print(f"RGB: {rgb}")
    
    back_to_hex = ColorUtils.rgb_to_hex(*rgb)
    print(f"Back to hex: {back_to_hex}")
    
    # Lighten/darken
    lighter = ColorUtils.lighten(hex_color, 20)
    darker = ColorUtils.darken(hex_color, 20)
    print(f"Lighter: {lighter}")
    print(f"Darker: {darker}")

def demo_uuid():
    """Demo: uuid_toolkit"""
    print(f"\n{Colors.CYAN}🔑 DEMO: UUID Toolkit{Colors.RESET}")
    print("-" * 50)
    
    print(f"UUID v4: {UUIDUtils.generate_v4()}")
    print(f"Short UUID: {UUIDUtils.generate_short()}")
    print(f"From name: {UUIDUtils.from_name('test')}")
    print(f"Is valid: {UUIDUtils.is_valid('e058baae-7728-4896-be5c-756d8c8e11ec')}")

def demo_cli():
    """Demo: cli_toolkit"""
    print(f"\n{Colors.CYAN}💻 DEMO: CLI Toolkit{Colors.RESET}")
    print("-" * 50)
    
    # Table
    headers = ["Name", "Age", "City"]
    rows = [
        ["John Doe", "30", "New York"],
        ["Jane Smith", "25", "Los Angeles"],
        ["Bob Johnson", "35", "Chicago"]
    ]
    
    print("Table:")
    TerminalUI.print_table(headers, rows)
    
    # Progress bar
    print("\nProgress:")
    TerminalUI.print_progress(75, 100, width=40)
    print()

def main():
    """Kjør alle demos"""
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}🧰 BAARLICLAW TOOLKIT - INTEGRATION DEMO{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print("\nDette viser hvordan verktøyene brukes i praksis!")
    
    demo_validation()
    demo_string_utils()
    demo_data_analysis()
    demo_math_stats()
    demo_collections()
    demo_date_utils()
    demo_colors()
    demo_uuid()
    demo_cli()
    
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ DEMO FULLFØRT!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print("\nAlle verktøy er nå integrert og klare for bruk!")

if __name__ == "__main__":
    main()
