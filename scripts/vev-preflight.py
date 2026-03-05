#!/usr/bin/env python3
"""
Vev Pre-Flight System
Automatisk kontekst-sjekk før hver samtale
Kjøres automatisk - ingen manuell trigger nødvendig
"""
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
MEMORY_FILE = f"{WORKSPACE}/MEMORY.md"
AGENTS_FILE = f"{WORKSPACE}/AGENTS.md"
TOOLS_FILE = f"{WORKSPACE}/TOOLS.md"
SKILLS_DIR = f"{WORKSPACE}/skills"
DAILY_DIR = f"{WORKSPACE}/memory"
DIARY_DIR = f"{WORKSPACE}/brain/diary"

class PreFlightCheck:
    def __init__(self):
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "relevant_skills": [],
            "recent_memories": [],
            "active_systems": [],
            "reminders": [],
            "mood": "neutral"
        }
    
    def scan_skills(self, query=""):
        """Scan skills directory for relevant skills"""
        skills = []
        try:
            for skill_dir in Path(SKILLS_DIR).iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        content = skill_md.read_text()
                        # Extract skill name and description
                        name = skill_dir.name
                        desc = ""
                        for line in content.split('\n')[:20]:
                            if line.strip() and not line.startswith('#'):
                                desc = line.strip()[:100]
                                break
                        skills.append({
                            "name": name,
                            "description": desc,
                            "path": str(skill_md)
                        })
        except Exception as e:
            print(f"Error scanning skills: {e}", file=sys.stderr)
        return skills
    
    def check_recent_memories(self, days=2):
        """Check recent memory files"""
        memories = []
        try:
            today = datetime.now()
            for i in range(days):
                date_str = (today.replace(day=today.day-i) if today.day > i else today).strftime('%Y-%m-%d')
                mem_file = Path(DAILY_DIR) / f"{date_str}.md"
                if mem_file.exists():
                    content = mem_file.read_text()
                    # Extract key points (lines starting with - or ###)
                    key_points = []
                    for line in content.split('\n')[:50]:
                        if line.strip().startswith(('- ', '### ', '## ')):
                            key_points.append(line.strip()[:150])
                    if key_points:
                        memories.append({
                            "date": date_str,
                            "highlights": key_points[:5]
                        })
        except Exception as e:
            print(f"Error checking memories: {e}", file=sys.stderr)
        return memories
    
    def check_diary(self, days=1):
        """Check recent diary entries"""
        entries = []
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            diary_file = Path(DIARY_DIR) / f"{today}.md"
            if diary_file.exists():
                content = diary_file.read_text()
                # Extract mood and key reflections
                mood = "neutral"
                for line in content.split('\n'):
                    if 'humør' in line.lower() or 'mood' in line.lower():
                        mood = line.split(':')[-1].strip() if ':' in line else line.strip()
                        break
                entries.append({
                    "date": today,
                    "mood": mood,
                    "has_entry": True
                })
        except Exception as e:
            print(f"Error checking diary: {e}", file=sys.stderr)
        return entries
    
    def check_active_systems(self):
        """Check what systems are currently active"""
        systems = []
        
        # Check for cron jobs
        try:
            cron_check = os.popen(r'crontab -l 2>/dev/null | grep -c "vev\|nrj\|morning"').read().strip()
            if cron_check and int(cron_check) > 0:
                systems.append(f"cron_jobs ({cron_check} active)")
        except:
            pass
        
        # Check for running processes
        try:
            if os.path.exists(f"{WORKSPACE}/scripts/telegram-poll.py"):
                systems.append("telegram_bot")
        except:
            pass
        
        # Check Mission Control
        try:
            if os.path.exists(f"{WORKSPACE}/mission-control-gh-pages/index.html"):
                systems.append("mission_control_v2")
        except:
            pass
        
        return systems
    
    def generate_context_summary(self):
        """Generate a summary of current context"""
        self.context["relevant_skills"] = self.scan_skills()
        self.context["recent_memories"] = self.check_recent_memories()
        self.context["diary_entries"] = self.check_diary()
        self.context["active_systems"] = self.check_active_systems()
        
        # Set mood from diary
        if self.context["diary_entries"]:
            self.context["mood"] = self.context["diary_entries"][0].get("mood", "neutral")
        
        return self.context
    
    def format_output(self):
        """Format context for injection into prompt"""
        lines = [
            "=" * 60,
            "🧠 VEV PRE-FLIGHT CONTEXT (Auto-generated)",
            "=" * 60,
            "",
            f"📅 Timestamp: {self.context['timestamp']}",
            f"🎭 Current Mood: {self.context['mood']}",
            "",
            "⚡ ACTIVE SYSTEMS:",
        ]
        
        for system in self.context['active_systems']:
            lines.append(f"   • {system}")
        
        lines.extend([
            "",
            "📚 AVAILABLE SKILLS (check these if relevant):",
        ])
        
        for skill in self.context['relevant_skills'][:10]:  # Limit to 10
            lines.append(f"   • {skill['name']}: {skill['description'][:60]}...")
        
        if self.context['recent_memories']:
            lines.extend([
                "",
                "📝 RECENT MEMORIES:",
            ])
            for mem in self.context['recent_memories'][:2]:
                lines.append(f"   [{mem['date']}]")
                for point in mem['highlights'][:3]:
                    lines.append(f"      {point[:80]}")
        
        lines.extend([
            "",
            "=" * 60,
            "💡 REMEMBER: Check skills/ before building from scratch",
            "   Check MEMORY.md for decisions and preferences",
            "   Check AGENTS.md for system overview",
            "=" * 60,
            "",
        ])
        
        return '\n'.join(lines)

def main():
    checker = PreFlightCheck()
    checker.generate_context_summary()
    print(checker.format_output())
    
    # Also save to file for reference
    output_file = f"{WORKSPACE}/.vev-preflight-context"
    with open(output_file, 'w') as f:
        f.write(checker.format_output())
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
