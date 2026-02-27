#!/usr/bin/env python3
"""
🎨 BAARLICLAW TEMPLATE TOOLKIT
HTML/CSS/JS maler og komponenter
"""

import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("TemplateToolkit")

class HTMLComponents:
    """Reusable HTML components"""
    
    @staticmethod
    def card(title: str, content: str, footer: str = "") -> str:
        """Generate card component"""
        return f"""
        <div class="card">
            <div class="card-header"><h3>{title}</h3></div>
            <div class="card-body">{content}</div>
            {f'<div class="card-footer">{footer}</div>' if footer else ''}
        </div>
        """
    
    @staticmethod
    def alert(message: str, type: str = "info") -> str:
        """Generate alert component"""
        colors = {
            "info": "#3498db",
            "success": "#2ecc71", 
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        color = colors.get(type, colors["info"])
        
        return f"""
        <div style="padding: 12px 20px; margin: 10px 0; 
                    border-left: 4px solid {color}; 
                    background: {color}20; 
                    border-radius: 4px;">
            {message}
        </div>
        """
    
    @staticmethod
    def button(text: str, onclick: str = "", style: str = "primary") -> str:
        """Generate button component"""
        colors = {
            "primary": "#3498db",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12"
        }
        color = colors.get(style, colors["primary"])
        
        onclick_attr = f' onclick="{onclick}"' if onclick else ''
        
        return f"""
        <button style="padding: 10px 20px; background: {color}; color: white; 
                       border: none; border-radius: 4px; cursor: pointer;"
                {onclick_attr}>
            {text}
        </button>
        """
    
    @staticmethod
    def badge(text: str, style: str = "default") -> str:
        """Generate badge component"""
        colors = {
            "default": "#95a5a6",
            "primary": "#3498db",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        }
        color = colors.get(style, colors["default"])
        
        return f"""
        <span style="display: inline-block; padding: 4px 8px; 
                     background: {color}; color: white; 
                     border-radius: 12px; font-size: 12px;">
            {text}
        </span>
        """
    
    @staticmethod
    def progress_bar(value: int, max_value: int = 100, 
                    color: str = "#3498db") -> str:
        """Generate progress bar"""
        percentage = (value / max_value) * 100 if max_value > 0 else 0
        
        return f"""
        <div style="width: 100%; height: 20px; background: #ecf0f1; 
                    border-radius: 10px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; 
                        background: {color}; transition: width 0.3s;"></div>
        </div>
        <div style="text-align: center; margin-top: 5px; font-size: 12px;">
            {value}/{max_value} ({percentage:.1f}%)
        </div>
        """

class CSSTemplates:
    """CSS style templates"""
    
    @staticmethod
    def modern_dark() -> str:
        """Modern dark theme CSS"""
        return """
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #3b82f6;
            --success: #22c55e;
            --warning: #f59e0b;
            --error: #ef4444;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid #334155;
        }
        
        .card-header h3 {
            color: var(--text-primary);
            margin-bottom: 12px;
        }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            transition: opacity 0.2s;
        }
        
        .btn:hover { opacity: 0.9; }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .badge-success { background: var(--success); color: white; }
        .badge-warning { background: var(--warning); color: white; }
        .badge-error { background: var(--error); color: white; }
        """
    
    @staticmethod
    def minimal_light() -> str:
        """Minimal light theme CSS"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: Georgia, serif;
            background: #ffffff;
            color: #333333;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        h1, h2, h3 { font-weight: normal; margin: 30px 0 15px; }
        h1 { font-size: 2.5em; border-bottom: 2px solid #333; padding-bottom: 10px; }
        
        p { margin-bottom: 20px; }
        
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: Monaco, monospace;
        }
        """

class PageTemplates:
    """Complete page templates"""
    
    @staticmethod
    def landing_page(title: str, subtitle: str, 
                    cta_text: str = "Get Started") -> str:
        """Generate landing page"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    color: white;
                }}
                .hero {{
                    padding: 40px;
                }}
                h1 {{
                    font-size: 4rem;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                p {{
                    font-size: 1.5rem;
                    margin-bottom: 40px;
                    opacity: 0.9;
                }}
                .cta {{
                    display: inline-block;
                    padding: 15px 40px;
                    background: white;
                    color: #667eea;
                    text-decoration: none;
                    border-radius: 30px;
                    font-weight: bold;
                    font-size: 1.2rem;
                    transition: transform 0.3s, box-shadow 0.3s;
                }}
                .cta:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
            </style>
        </head>
        <body>
            <div class="hero">
                <h1>{title}</h1>
                <p>{subtitle}</p>
                <a href="#" class="cta">{cta_text}</a>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def admin_dashboard(title: str = "Dashboard") -> str:
        """Generate admin dashboard template"""
        css = CSSTemplates.modern_dark()
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>{css}</style>
        </head>
        <body>
            <div class="container">
                <header style="margin-bottom: 30px;">
                    <h1>{title}</h1>
                </header>
                
                <div class="card">
                    <p>Welcome to your dashboard.</p>
                </div>
            </div>
        </body>
        </html>
        """

# === CONVENIENCE FUNCTIONS ===
def quick_card(title: str, content: str) -> str:
    """Quick card generation"""
    return HTMLComponents.card(title, content)

def quick_alert(message: str, type: str = "info") -> str:
    """Quick alert generation"""
    return HTMLComponents.alert(message, type)

def quick_landing(title: str, subtitle: str) -> str:
    """Quick landing page"""
    return PageTemplates.landing_page(title, subtitle)

# === TESTING ===
if __name__ == "__main__":
    print("🎨 BaarliClaw Template Toolkit - Testing")
    print("=" * 50)
    
    # Test components
    print("\n🧪 Testing HTML Components")
    
    card = HTMLComponents.card("Title", "Content here", "Footer")
    print("✅ Card generated")
    
    alert = HTMLComponents.alert("This is an alert!", "warning")
    print("✅ Alert generated")
    
    button = HTMLComponents.button("Click me", "alert('Hello')")
    print("✅ Button generated")
    
    badge = HTMLComponents.badge("New", "success")
    print("✅ Badge generated")
    
    progress = HTMLComponents.progress_bar(75, 100)
    print("✅ Progress bar generated")
    
    # Test templates
    print("\n🧪 Testing Page Templates")
    
    landing = PageTemplates.landing_page("My App", "The best app ever")
    print("✅ Landing page generated")
    
    admin = PageTemplates.admin_dashboard("Admin Panel")
    print("✅ Admin dashboard generated")
    
    # Test CSS
    print("\n🧪 Testing CSS Templates")
    dark_css = CSSTemplates.modern_dark()
    print(f"✅ Dark theme CSS: {len(dark_css)} chars")
    
    light_css = CSSTemplates.minimal_light()
    print(f"✅ Light theme CSS: {len(light_css)} chars")
    
    print("\n✅ Template Toolkit ready!")
