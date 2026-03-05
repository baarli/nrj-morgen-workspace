#!/usr/bin/env python3
"""
Vev Skill Suggester
Foreslår relevante skills basert på bruker-input
"""
import os
import sys
import re
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
SKILLS_DIR = f"{WORKSPACE}/skills"

# Keyword to skill mapping
KEYWORD_MAP = {
    r"\b(e-post|email|gmail|sende mail)\b": ["gmail"],
    r"\b(nrj|radio|morgen|sending|sak)\b": ["nrj-dashboard-system", "content-aggregator", "mission-control"],
    r"\b(podkast|episode|lytter|clip)\b": ["podcast-manager"],
    r"\b(github|git|commit|push|pull)\b": ["github"],
    r"\b(skill|lære|forbedre|system)\b": ["self-improvement", "skill-creator", "system-manager"],
    r"\b(feil|error|bug|problem)\b": ["self-improvement"],
    r"\b(mission control|dashboard|saksliste)\b": ["mission-control", "nrj-dashboard-system"],
    r"\b(telegram|bot|melding)\b": ["telegram"],
    r"\b(vær|weather|forecast)\b": ["weather"],
    r"\b(kode|programmer|script|python|bash)\b": ["coding-agent", "code-quality-checker"],
    r"\b(cron|jobb|schedule|automat)\b": ["system-manager"],
    r"\b(news|nyhet|søk|search)\b": ["content-aggregator"],
}

def scan_skills():
    """Scan all available skills"""
    skills = {}
    for skill_dir in Path(SKILLS_DIR).iterdir():
        if skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()
                name = skill_dir.name
                # Extract first non-header line as description
                desc = ""
                for line in content.split('\n')[:10]:
                    if line.strip() and not line.startswith('#'):
                        desc = line.strip()[:80]
                        break
                skills[name] = desc
    return skills

def suggest_skills(user_input):
    """Suggest skills based on user input"""
    user_input_lower = user_input.lower()
    suggested = set()
    
    for pattern, skill_list in KEYWORD_MAP.items():
        if re.search(pattern, user_input_lower, re.IGNORECASE):
            suggested.update(skill_list)
    
    return list(suggested)

def main():
    if len(sys.argv) < 2:
        print("Usage: vev-skill-suggest 'your query here'")
        print("Or run interactively:")
        user_input = input("What do you want to do? > ")
    else:
        user_input = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print("🔍 SKILL SUGGESTIONS")
    print("=" * 60)
    print()
    print(f"Query: '{user_input}'")
    print()
    
    all_skills = scan_skills()
    suggestions = suggest_skills(user_input)
    
    if suggestions:
        print("💡 Relevant skills found:")
        print()
        for skill_name in suggestions:
            if skill_name in all_skills:
                print(f"   📚 {skill_name}")
                print(f"      {all_skills[skill_name]}")
                print(f"      File: {SKILLS_DIR}/{skill_name}/SKILL.md")
                print()
    else:
        print("🤔 No specific skills matched.")
        print("   Available skill categories:")
        categories = {}
        for name in all_skills:
            cat = name.split('-')[0] if '-' in name else 'other'
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)
        
        for cat, skills in sorted(categories.items())[:5]:
            print(f"   • {cat}: {', '.join(skills[:3])}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
