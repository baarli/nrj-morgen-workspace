#!/usr/bin/env python3
"""
📚 Documentation Generator - Automatisk generering av dokumentasjon
"""

import os
import sys
from datetime import datetime
from pathlib import Path

class DocumentationGenerator:
    """Generer automatisk dokumentasjon for systemet"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.docs_dir = self.workspace / 'docs' / 'auto-generated'
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
    def count_files_by_type(self) -> dict:
        """Tell filer etter type"""
        counts = {
            'python': 0,
            'shell': 0,
            'markdown': 0,
            'json': 0,
            'html': 0
        }
        
        for root, dirs, files in os.walk(self.workspace):
            # Skip node_modules og .git
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    counts['python'] += 1
                elif file.endswith('.sh'):
                    counts['shell'] += 1
                elif file.endswith('.md'):
                    counts['markdown'] += 1
                elif file.endswith('.json'):
                    counts['json'] += 1
                elif file.endswith('.html'):
                    counts['html'] += 1
        
        return counts
    
    def list_skills(self) -> list:
        """List alle skills"""
        skills_dir = self.workspace / 'skills'
        skills = []
        
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_file = skill_dir / 'SKILL.md'
                    if skill_file.exists():
                        skills.append(skill_dir.name)
        
        return sorted(skills)
    
    def generate_system_overview(self) -> str:
        """Generer system oversikt"""
        
        file_counts = self.count_files_by_type()
        skills = self.list_skills()
        
        doc = f"""# 📚 System Oversikt - Auto-generert

**Generert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 Filstatistikk

| Type | Antall |
|------|--------|
| Python Scripts | {file_counts['python']} |
| Shell Scripts | {file_counts['shell']} |
| Markdown Files | {file_counts['markdown']} |
| JSON Files | {file_counts['json']} |
| HTML Files | {file_counts['html']} |
| **Totalt** | **{sum(file_counts.values())}** |

---

## 🎓 Skills ({len(skills)} totalt)

"""
        
        for skill in skills:
            doc += f"- {skill}\n"
        
        doc += f"""

---

## 🛠️ Hovedverktøy

### System Overvåking
- `system_health_dashboard.py` - Sanntidsovervåking
- `performance_monitor.py` - Ytelsesmålinger
- `security_audit_service.py` - Sikkerhetsaudit

### NRJ Morgen Verktøy
- `nrj_growth_tracker.py` - Vekstsporing
- `podcast_promoter.py` - Sosial medie-promotering
- `podcast_analytics_dashboard.py` - Analytics dashboard
- `content_strategy_optimizer.py` - Innholdsstrategi

### Automatisering
- `auto_backup.py` - Automatisk backup
- `task_master.py` - Oppgavehåndtering
- `system_cleanup.sh` - Systemopprydding

### Morning Routine
- `morning_routine_enhancer.py` - Forbedret Morning Routine
- `recency_scoring.py` - Freskhet-vektlegging
- `social_media_poster.py` - Sosial posting

---

## 📁 Viktige Mapper

```
/root/.openclaw/workspace/
├── scripts/          # Python og shell scripts
├── skills/           # Skill moduler
├── docs/             # Dokumentasjon
├── brain/            # System data og rapporter
│   ├── backups/      # Automatiske backups
│   ├── reports/      # Genererte rapporter
│   └── metrics/      # System metrics
├── memory/           # Daglige logger
└── mission-control/  # Dashboard
```

---

## 🔧 Rask Kommandoer

```bash
# System health sjekk
python3 scripts/system_health_dashboard.py

# Performance monitor
python3 scripts/performance_monitor.py

# Daglig rapport
python3 scripts/nrj_daily_report.py

# Podcast analytics
python3 scripts/podcast_analytics_dashboard.py

# System cleanup
bash scripts/system_cleanup.sh

# Auto backup
python3 scripts/auto_backup.py
```

---

*Denne dokumentasjonen ble generert automatisk av DocumentationGenerator*
"""
        
        return doc
    
    def save_documentation(self):
        """Lagre dokumentasjon"""
        doc = self.generate_system_overview()
        
        output_file = self.docs_dir / 'system-overview.md'
        with open(output_file, 'w') as f:
            f.write(doc)
        
        return output_file


def main():
    """Main entry point"""
    gen = DocumentationGenerator()
    output_file = gen.save_documentation()
    
    print(f"✅ Dokumentasjon generert: {output_file}")
    print(f"\n📊 System statistikk:")
    
    counts = gen.count_files_by_type()
    for type_name, count in counts.items():
        if count > 0:
            print(f"  {type_name}: {count}")
    
    print(f"\n🎓 Skills: {len(gen.list_skills())}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
