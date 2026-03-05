#!/usr/bin/env python3
"""
🎨 BAARLICLAW COLOR TOOLKIT
Fargehåndtering og -konvertering
"""

import re
import random
from typing import Tuple, Optional

class ColorUtils:
    """Color utilities"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSL"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2
        
        # Saturation
        if diff == 0:
            s = 0
        else:
            s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
        
        # Hue
        if diff == 0:
            h = 0
        elif max_val == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        
        return (h, s * 100, l * 100)
    
    @staticmethod
    def lighten(hex_color: str, amount: float = 0.1) -> str:
        """Lighten color"""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        r = min(255, int(r + (255 - r) * amount))
        g = min(255, int(g + (255 - g) * amount))
        b = min(255, int(b + (255 - b) * amount))
        return ColorUtils.rgb_to_hex(r, g, b)
    
    @staticmethod
    def darken(hex_color: str, amount: float = 0.1) -> str:
        """Darken color"""
        r, g, b = ColorUtils.hex_to_rgb(hex_color)
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        return ColorUtils.rgb_to_hex(r, g, b)
    
    @staticmethod
    def random_color() -> str:
        """Generate random color"""
        return ColorUtils.rgb_to_hex(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    
    @staticmethod
    def is_valid_hex(hex_color: str) -> bool:
        """Check if valid hex color"""
        return bool(re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color))

class TerminalColors:
    """Terminal color codes"""
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Colorize text"""
        return f"{color}{text}{TerminalColors.RESET}"

# === CONVENIENCE FUNCTIONS ===
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Quick hex to RGB"""
    return ColorUtils.hex_to_rgb(hex_color)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Quick RGB to hex"""
    return ColorUtils.rgb_to_hex(r, g, b)

def lighten_color(hex_color: str, amount: float = 0.1) -> str:
    """Quick lighten"""
    return ColorUtils.lighten(hex_color, amount)

# === TESTING ===
if __name__ == "__main__":
    print("🎨 BaarliClaw Color Toolkit - Testing")
    print("=" * 50)
    
    # Test hex/RGB conversion
    print("\n🧪 Testing Hex/RGB Conversion")
    hex_color = "#FF5733"
    rgb = ColorUtils.hex_to_rgb(hex_color)
    print(f"  {hex_color} -> RGB{rgb}")
    
    back_to_hex = ColorUtils.rgb_to_hex(*rgb)
    print(f"  RGB{rgb} -> {back_to_hex}")
    
    # Test HSL
    print("\n🧪 Testing HSL Conversion")
    hsl = ColorUtils.rgb_to_hsl(*rgb)
    print(f"  RGB{rgb} -> HSL{hsl}")
    
    # Test lighten/darken
    print("\n🧪 Testing Lighten/Darken")
    lighter = ColorUtils.lighten(hex_color, 0.2)
    darker = ColorUtils.darken(hex_color, 0.2)
    print(f"  Original: {hex_color}")
    print(f"  Lighter:  {lighter}")
    print(f"  Darker:   {darker}")
    
    # Test random
    print("\n🧪 Testing Random Color")
    random_color = ColorUtils.random_color()
    print(f"  Random: {random_color}")
    
    # Test terminal colors
    print("\n🧪 Testing Terminal Colors")
    print(TerminalColors.colorize("  Red text", TerminalColors.RED))
    print(TerminalColors.colorize("  Green text", TerminalColors.GREEN))
    print(TerminalColors.colorize("  Blue text", TerminalColors.BLUE))
    
    print("\n✅ Color Toolkit ready!")
