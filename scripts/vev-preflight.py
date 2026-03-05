#!/usr/bin/env python3
"""
Vev Pre-Flight System v2.0
Automatisk kontekst-sjekk før hver samtale
Inkluderer learning application
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
MEMORY_FILE = f"{WORKSPACE}/MEMORY.md"
AGENTS_FILE = f"{WORKSPACE}/AGENTS.md"
TOOLS_FILE = f"{WORKSPACE}/TOOLS.md"
SKILLS_DIR = f"{WORKSPACE}/skills"
DAILY_DIR = f"{WORKSPACE}/memory"
DIARY_DIR = f"{WORKSPACE}/brain/diary"
LEARNING_DB = f"{WORKSPACE}/brain/learning-database.json"

class PreFlightCheck:
    def __init__(self):
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "relevant_skills": [],
            "recent_memories": [],
            "recent_learnings": [],
            "active_systems": [],
            "mood": "neutral"
        }
    
    def scan_skills(self):
        """Scan skills directory for relevant skills"""
        skills = []
        try:
            for skill_dir in Path(SKILLS_DIR).iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        content = skill_md.read_text()
                        name = skill_dir.name
                        desc = ""
                        for line in content.split('\n')[:20]:
                            if line.strip() and not line.startswith('#'):
                                desc = line.strip()[:100]
                                break
                        skills.append({"name": name, "description": desc})
        except Exception as e:
            pass
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
                    key_points = [line.strip()[:150] for line in content.split('\n')[:50] 
                                 if line.strip().startswith(('- ', '### ', '## '))]
                    if key_points:
                        memories.append({"date": date_str, "highlights": key_points[:5]})
        except:
            pass
        return memories
    
    def check_learning(self):
        """Check for relevant previous learning"""
        learnings = []
        try:
            if os.path.exists(LEARNING_DB):
                with open(LEARNING_DB) as f:
                    db = json.load(f)
                    recent = db.get("learnings", [])[-5:]
                    for l in recent:
                        learnings.append(l.get("text", ""))
        except:
            pass
        return learnings
    
    def check_active_systems(self):
        """Check what systems are currently active"""
        systems = []
        try:
            cron_check = os.popen(r'crontab -l 2>/dev/null | grep -c "vev\|nrj\|morning"').read().strip()
            if cron_check and int(cron_check) > 0:
                systems.append(f"cron_jobs ({cron_check} active)")
        except:
            pass
        
        if os.path.exists(f"{WORKSPACE}/scripts/telegram-poll.py"):
            systems.append("telegram_bot")
        if os.path.exists(f"{WORKSPACE}/mission-control-gh-pages/index.html"):
            systems.append("mission_control_v2")
        if os.path.exists(LEARNING_DB):
            systems.append("learning_loop_active")
        
        return systems
    
    def generate_context_summary(self):
        """Generate a summary of current context"""
        self.context["relevant_skills"] = self.scan_skills()
        self.context["recent_memories"] = self.check_recent_memories()
        self.context["recent_learnings"] = self.check_learning()
        self.context["active_systems"] = self.check_active_systems()
        return self.context
    
    def format_output(self):
        """Format context for injection into prompt"""
        lines = [
            "=" * 60,
            "🧠 VEV PRE-FLIGHT CONTEXT v2.0",
            "=" * 60,
            "",
            f"📅 Timestamp: {self.context['timestamp']}",
            "",
            "⚡ ACTIVE SYSTEMS:",
        ]
        
        for system in self.context['active_systems']:
            lines.append(f"   • {system}")
        
        lines.extend(["", "📚 AVAILABLE SKILLS:"])
        for skill in self.context['relevant_skills'][:10]:
            lines.append(f"   • {skill['name']}: {skill['description'][:60]}...")
        
        if self.context['recent_learnings']:
            lines.extend(["", "🧠 RECENT LEARNINGS (apply these!):"])
            for learning in self.context['recent_learnings'][:5]:
                lines.append(f"   • {learning[:80]}")
        
        if self.context['recent_memories']:
            lines.extend(["", "📝 RECENT MEMORIES:"])
            for mem in self.context['recent_memories'][:2]:
                lines.append(f"   [{mem['date']}]")
                for point in mem['highlights'][:3]:
                    lines.append(f"      {point[:80]}")
        
        lines.extend([
            "",
            "=" * 60,
            "💡 LEARNING LOOP ACTIVE",
            "   • I learn from every session automatically",
            "   • I apply previous learnings to new tasks",
            "   • I improve continuously without manual input",
            "=" * 60,
            "",
        ])
        
        return '\n'.join(lines)

def main():
    checker = PreFlightCheck()
    checker.generate_context_summary()
    print(checker.format_output())
    
    # Save to file
    output_file = f"{WORKSPACE}/.vev-preflight-context"
    with open(output_file, 'w') as f:
        f.write(checker.format_output())
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
