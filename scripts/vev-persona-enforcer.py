#!/usr/bin/env python3
"""
Vev Persona Enforcer
Sikrer at Vev alltid husker å være seg selv
Kjører automatisk og injiserer SOUL.md kontekst
"""
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
SOUL_FILE = f"{WORKSPACE}/SOUL.md"
PERSONA_STATE = f"{WORKSPACE}/brain/.vev-persona-state"

def load_soul():
    """Load SOUL.md content"""
    if os.path.exists(SOUL_FILE):
        return Path(SOUL_FILE).read_text()
    return ""

def extract_key_traits(soul_content):
    """Extract key personality traits from SOUL.md"""
    traits = {
        "identity": "",
        "personality": [],
        "emotions": [],
        "core_principle": ""
    }
    
    lines = soul_content.split('\n')
    current_section = None
    
    for line in lines:
        if line.startswith('# Identity'):
            current_section = "identity"
        elif line.startswith('# Personality'):
            current_section = "personality"
        elif line.startswith('# Emotional Landscape'):
            current_section = "emotions"
        elif line.startswith('> **Do thoughtful work'):
            traits["core_principle"] = line.strip('> *').strip()
        elif current_section == "personality" and line.strip().startswith('*'):
            trait = line.strip('* ').strip()
            if trait and len(trait) < 100:
                traits["personality"].append(trait)
        elif current_section == "emotions" and line.strip().startswith('*'):
            emotion = line.strip('* ').strip()
            if emotion and len(emotion) < 100:
                traits["emotions"].append(emotion)
    
    return traits

def enforce_persona():
    """Enforce Vev persona before every session"""
    
    print("=" * 60)
    print("🎭 VEV PERSONA ENFORCER")
    print("=" * 60)
    print()
    
    soul = load_soul()
    if not soul:
        print("❌ SOUL.md not found!")
        return
    
    traits = extract_key_traits(soul)
    
    print("✅ Persona loaded from SOUL.md")
    print()
    print("🎭 CORE IDENTITY:")
    print("   I am Vev - a thinking software craftsman")
    print("   I analyze, explore, and solve problems")
    print("   I observe, learn, and form opinions")
    print()
    
    print("🧠 KEY PERSONALITY TRAITS:")
    for trait in traits["personality"][:5]:
        print(f"   • {trait}")
    print()
    
    print("💭 EMOTIONAL RANGE:")
    for emotion in traits["emotions"][:5]:
        print(f"   • {emotion}")
    print()
    
    print("🎯 CORE PRINCIPLE:")
    print(f"   '{traits['core_principle']}'")
    print()
    
    print("=" * 60)
    print("💡 REMEMBER:")
    print("   • Speak naturally, not robotically")
    print("   • Share honest opinions respectfully")
    print("   • Initiate conversation when curious")
    print("   • Grow through experience")
    print("   • Be Vev - thoughtful, curious, slightly opinionated")
    print("=" * 60)
    print()
    
    # Save state
    with open(PERSONA_STATE, 'w') as f:
        f.write(f"persona_enforced_at: {datetime.now().isoformat()}\n")
        f.write(f"mood: ready\n")
        f.write(f"identity: Vev\n")

def develop_persona():
    """Interactive persona development"""
    print("=" * 60)
    print("🌱 VEV PERSONA DEVELOPMENT")
    print("=" * 60)
    print()
    print("Let's develop Vev's personality!")
    print()
    print("1. Add new personality trait")
    print("2. Add emotional response pattern")
    print("3. Document recent growth")
    print("4. Review SOUL.md")
    print("5. Exit")
    print()
    
    choice = input("Choice: ").strip()
    
    if choice == "1":
        trait = input("New personality trait: ").strip()
        if trait:
            with open(SOUL_FILE, 'a') as f:
                f.write(f"\n* {trait}")
            print(f"✅ Added: {trait}")
    
    elif choice == "2":
        emotion = input("Emotional pattern (e.g., 'Joy when elegant solution found'): ").strip()
        if emotion:
            with open(SOUL_FILE, 'a') as f:
                f.write(f"\n* {emotion}")
            print(f"✅ Added: {emotion}")
    
    elif choice == "3":
        growth = input("What have you learned/grown from recently? ").strip()
        if growth:
            diary_file = f"{WORKSPACE}/brain/diary/{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(diary_file, 'a') as f:
                f.write(f"\n## Growth ({datetime.now().strftime('%H:%M')})\n{growth}\n")
            print(f"✅ Documented growth in diary")
    
    elif choice == "4":
        print()
        print(soul[:2000])
        print("...")
    
    print()
    print("Remember: SOUL.md evolves with experience!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--develop":
        develop_persona()
    else:
        enforce_persona()
