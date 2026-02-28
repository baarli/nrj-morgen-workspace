#!/usr/bin/env python3
"""
✅ Task Master - Automatisk oppgavehåndtering og prioritering
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class TaskMaster:
    """Automatisk oppgavehåndtering for NRJ Morgen"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.tasks_file = self.workspace / 'brain' / 'tasks.json'
        self.tasks = self.load_tasks()
        
    def load_tasks(self) -> List[Dict]:
        """Last oppgaver fra fil"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_tasks(self):
        """Lagre oppgaver til fil"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, title: str, priority: str = 'medium', 
                 category: str = 'general', due_days: int = 7) -> Dict:
        """Legg til ny oppgave"""
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'priority': priority,  # critical, high, medium, low
            'category': category,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'due': (datetime.now() + timedelta(days=due_days)).isoformat(),
            'completed': None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        
        return task
    
    def complete_task(self, task_id: int) -> bool:
        """Merk oppgave som fullført"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed'] = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def get_pending_tasks(self) -> List[Dict]:
        """Hent ventende oppgaver sortert etter prioritet"""
        pending = [t for t in self.tasks if t['status'] == 'pending']
        
        # Sorter etter prioritet
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        pending.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return pending
    
    def get_tasks_by_category(self, category: str) -> List[Dict]:
        """Hent oppgaver etter kategori"""
        return [t for t in self.tasks if t['category'] == category]
    
    def auto_generate_tasks(self):
        """Generer automatiske oppgaver basert på system status"""
        
        new_tasks = []
        
        # Sjekk om backup finnes
        backup_dir = self.workspace / 'brain' / 'backups'
        if not any(backup_dir.glob('backup-*.tar.gz')):
            new_tasks.append({
                'title': 'Opprett første system backup',
                'priority': 'high',
                'category': 'maintenance',
                'due_days': 1
            })
        
        # Sjekk om det er gamle rapporter
        reports_dir = self.workspace / 'brain' / 'reports'
        if reports_dir.exists():
            old_reports = list(reports_dir.glob('*.md'))
            if len(old_reports) > 50:
                new_tasks.append({
                    'title': 'Rydd gamle rapporter',
                    'priority': 'low',
                    'category': 'maintenance',
                    'due_days': 7
                })
        
        # Legg til nye oppgaver
        for task_data in new_tasks:
            # Sjekk om oppgaven allerede finnes
            exists = any(t['title'] == task_data['title'] and t['status'] == 'pending' 
                        for t in self.tasks)
            if not exists:
                self.add_task(**task_data)
                print(f"  ✅ Auto-generated task: {task_data['title']}")
    
    def print_task_board(self):
        """Print oppgave-tavle"""
        
        print("\n" + "=" * 70)
        print("✅ TASK MASTER - OPPGAVEOVERSIKT")
        print("=" * 70)
        
        # Auto-generer oppgaver
        print("\n🤖 Sjekker for auto-oppgaver...")
        self.auto_generate_tasks()
        
        # Hent ventende oppgaver
        pending = self.get_pending_tasks()
        
        if pending:
            print(f"\n📋 Ventende oppgaver ({len(pending)}):")
            print("-" * 70)
            
            for task in pending[:10]:  # Vis maks 10
                priority_icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(task['priority'], '⚪')
                
                due_date = datetime.fromisoformat(task['due']).strftime('%m-%d')
                
                print(f"{priority_icon} #{task['id']} {task['title']}")
                print(f"   Prioritet: {task['priority']} | Kategori: {task['category']} | Frist: {due_date}")
                print()
        else:
            print("\n✨ Ingen ventende oppgaver!")
        
        # Statistikk
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['status'] == 'completed'])
        pending_count = len([t for t in self.tasks if t['status'] == 'pending'])
        
        print("-" * 70)
        print(f"📊 Statistikk: {total} totalt | {completed} fullført | {pending_count} ventende")
        print("=" * 70)


def main():
    """Main entry point"""
    task_master = TaskMaster()
    task_master.print_task_board()
    return 0


if __name__ == '__main__':
    sys.exit(main())
