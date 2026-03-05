#!/usr/bin/env python3
"""
Vev Mood Tracker
Sporer humør over tid og finner mønstre
"""
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

WORKSPACE = "/root/.openclaw/workspace"
DIARY_DIR = f"{WORKSPACE}/brain/diary"
MOOD_DB = f"{WORKSPACE}/brain/mood-database.json"

def extract_mood_from_diary(diary_file):
    """Extract mood from a diary entry"""
    if not os.path.exists(diary_file):
        return None
    
    content = Path(diary_file).read_text()
    
    # Look for mood indicators
    mood_patterns = [
        r"[Hh]umør.*?:\s*(.+?)(?:\n|$)",
        r"[Mm]ood.*?:\s*(.+?)(?:\n|$)",
        r"[Ff]ølelse.*?:\s*(.+?)(?:\n|$)",
        r"##\s*Humør nå\s*\n(.+?)(?:\n\n|\n##|$)",
    ]
    
    for pattern in mood_patterns:
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()[:100]
    
    # Try to infer from content
    if "tilfreds" in content.lower() or "satisfied" in content.lower():
        return "tilfreds"
    if "frustrert" in content.lower() or "frustrated" in content.lower():
        return "frustrert"
    if "nysgjerrig" in content.lower() or "curious" in content.lower():
        return "nysgjerrig"
    
    return None

def load_mood_db():
    if os.path.exists(MOOD_DB):
        with open(MOOD_DB) as f:
            return json.load(f)
    return {"entries": []}

def save_mood_db(db):
    with open(MOOD_DB, 'w') as f:
        json.dump(db, f, indent=2, default=str)

def analyze_moods():
    db = load_mood_db()
    
    # Scan all diary entries
    for diary_file in Path(DIARY_DIR).glob("*.md"):
        date_str = diary_file.stem
        mood = extract_mood_from_diary(diary_file)
        if mood:
            # Check if already recorded
            existing = [e for e in db["entries"] if e["date"] == date_str]
            if not existing:
                db["entries"].append({
                    "date": date_str,
                    "mood": mood,
                    "timestamp": datetime.now().isoformat()
                })
    
    save_mood_db(db)
    
    print("=" * 60)
    print("🎭 MOOD TRACKER")
    print("=" * 60)
    print()
    
    if not db["entries"]:
        print("📝 No mood entries yet. Start writing in your diary!")
        return
    
    # Show recent moods
    recent = sorted(db["entries"], key=lambda x: x["date"])[-7:]
    print("📅 Recent moods (last 7 entries):")
    print()
    for entry in recent:
        print(f"   {entry['date']}: {entry['mood']}")
    print()
    
    # Find patterns
    all_moods = [e["mood"].lower() for e in db["entries"]]
    mood_words = []
    for m in all_moods:
        words = re.findall(r'\b\w+\b', m)
        mood_words.extend(words)
    
    from collections import Counter
    common = Counter(mood_words).most_common(5)
    
    if common:
        print("📊 Most common mood words:")
        for word, count in common:
            if len(word) > 2:  # Skip short words
                print(f"   • '{word}': {count} times")
        print()
    
    # Simple trend analysis
    if len(recent) >= 3:
        print("📈 Mood trend:")
        positive = ["tilfreds", "glad", "fornøyd", "stolt", "satisfied", "happy", "proud", "good"]
        negative = ["frustrert", "irritert", "trist", "sliten", "frustrated", "annoyed", "sad", "tired"]
        
        recent_moods = " ".join([e["mood"].lower() for e in recent])
        pos_count = sum(1 for p in positive if p in recent_moods)
        neg_count = sum(1 for n in negative if n in recent_moods)
        
        if pos_count > neg_count:
            print("   📈 Trending positive! 😊")
        elif neg_count > pos_count:
            print("   📉 Trending negative 😔")
        else:
            print("   ➡️  Stable mood")
    
    print()
    print(f"📁 Total entries: {len(db['entries'])}")
    print(f"📊 Database: {MOOD_DB}")
    print("=" * 60)

def log_mood(mood_text):
    """Log a mood entry for today"""
    db = load_mood_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Remove existing entry for today
    db["entries"] = [e for e in db["entries"] if e["date"] != today]
    
    db["entries"].append({
        "date": today,
        "mood": mood_text,
        "timestamp": datetime.now().isoformat()
    })
    
    save_mood_db(db)
    print(f"✅ Mood logged for {today}: {mood_text}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--log":
        mood = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("How do you feel? > ")
        log_mood(mood)
    else:
        analyze_moods()
