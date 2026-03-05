#!/usr/bin/env python3
"""
Vev Error Pattern Recognition
Finner gjentatte feil og advarer om dem
"""
import os
import sys
import json
from datetime import datetime, timedelta
from collections import Counter

WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DB = f"{WORKSPACE}/brain/learning-database.json"
ERROR_PATTERNS_FILE = f"{WORKSPACE}/brain/error-patterns.json"

def load_learning_db():
    if os.path.exists(LEARNING_DB):
        with open(LEARNING_DB) as f:
            return json.load(f)
    return {"errors": []}

def load_error_patterns():
    if os.path.exists(ERROR_PATTERNS_FILE):
        with open(ERROR_PATTERNS_FILE) as f:
            return json.load(f)
    return {
        "patterns": {
            "supabase 400": "Sjekk at 'Prefer: return=minimal' header er satt",
            "permission denied": "Sjekk filrettigheter med ls -la",
            "connection refused": "Sjekk at tjenesten kjører",
            "syntax error": "Verifiser syntax før kjøring",
            "not found": "Sjekk at filen/stien eksisterer",
            "already exists": "Sjekk om filen allerede finnes før oppretting",
        }
    }

def analyze_errors():
    db = load_learning_db()
    errors = db.get("errors", [])
    
    print("=" * 60)
    print("⚠️ ERROR PATTERN ANALYSIS")
    print("=" * 60)
    print()
    
    if not errors:
        print("✅ No errors recorded yet!")
        return
    
    # Count recent errors (last 7 days)
    recent = []
    week_ago = datetime.now() - timedelta(days=7)
    for e in errors:
        try:
            e_time = datetime.fromisoformat(e.get("timestamp", ""))
            if e_time > week_ago:
                recent.append(e["text"])
        except:
            pass
    
    print(f"📊 Error statistics:")
    print(f"   Total errors: {len(errors)}")
    print(f"   Last 7 days: {len(recent)}")
    print()
    
    # Find repeated patterns
    error_texts = [e["text"].lower() for e in errors]
    patterns = load_error_patterns()
    
    matches_found = []
    for pattern_key, advice in patterns["patterns"].items():
        count = sum(1 for e in error_texts if pattern_key.lower() in e)
        if count >= 2:
            matches_found.append((pattern_key, count, advice))
    
    if matches_found:
        print("🚨 REPEATED ERROR PATTERNS DETECTED:")
        print()
        for pattern, count, advice in sorted(matches_found, key=lambda x: -x[1]):
            print(f"   ⚠️  '{pattern}'")
            print(f"      Occurred {count} times!")
            print(f"      💡 Advice: {advice}")
            print()
    else:
        print("✅ No repeated error patterns found")
        print()
        if recent:
            print("Recent errors (not repeated):")
            for e in recent[-3:]:
                print(f"   • {e[:60]}...")
    
    print("=" * 60)

def add_error_pattern(pattern, advice):
    """Add a new error pattern"""
    patterns = load_error_patterns()
    patterns["patterns"][pattern] = advice
    with open(ERROR_PATTERNS_FILE, 'w') as f:
        json.dump(patterns, f, indent=2)
    print(f"✅ Added error pattern: '{pattern}'")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--add":
        add_error_pattern(sys.argv[2], sys.argv[3])
    else:
        analyze_errors()
