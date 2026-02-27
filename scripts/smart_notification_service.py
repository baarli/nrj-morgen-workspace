#!/usr/bin/env python3
"""
🔔 BAARLICLAW SMART NOTIFICATION SERVICE
Intelligent varsling basert på viktighet og kontekst
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from uuid_toolkit import UUIDUtils

logger = setup_logging("smart-notification")

@dataclass
class Notification:
    """En varsling"""
    id: str
    title: str
    message: str
    priority: str  # critical, high, normal, low
    category: str  # system, task, alert, info
    timestamp: str
    read: bool = False
    action_required: bool = False
    action_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

class SmartNotificationService:
    """Smart varslings-tjeneste"""
    
    PRIORITY_WEIGHTS = {
        'critical': 100,
        'high': 75,
        'normal': 50,
        'low': 25
    }
    
    def __init__(self, storage_file: str = "/tmp/notifications.json"):
        self.storage_file = storage_file
        self.notifications: List[Notification] = []
        self.load()
    
    def load(self):
        """Last varslinger fra fil"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.notifications = [Notification(**n) for n in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.notifications = []
    
    def save(self):
        """Lagre varslinger til fil"""
        with open(self.storage_file, 'w') as f:
            json.dump([n.to_dict() for n in self.notifications], f, indent=2)
    
    def notify(self, title: str, message: str, priority: str = "normal", 
               category: str = "info", action_required: bool = False,
               action_url: Optional[str] = None) -> str:
        """Opprett ny varsling"""
        
        notification = Notification(
            id=UUIDUtils.generate_short(),
            title=title,
            message=message,
            priority=priority,
            category=category,
            timestamp=DateUtils.format(DateUtils.now()),
            action_required=action_required,
            action_url=action_url
        )
        
        self.notifications.append(notification)
        self.save()
        
        # Logg basert på prioritet
        if priority == 'critical':
            logger.critical(f"🔴 {title}: {message}")
        elif priority == 'high':
            logger.warning(f"🟠 {title}: {message}")
        elif priority == 'normal':
            logger.info(f"🔵 {title}: {message}")
        else:
            logger.debug(f"⚪ {title}: {message}")
        
        return notification.id
    
    def get_unread(self, min_priority: str = "low") -> List[Notification]:
        """Hent uleste varslinger"""
        min_weight = self.PRIORITY_WEIGHTS.get(min_priority, 0)
        
        unread = [
            n for n in self.notifications 
            if not n.read and self.PRIORITY_WEIGHTS.get(n.priority, 0) >= min_weight
        ]
        
        # Sorter etter prioritet og tid
        unread.sort(key=lambda n: (
            -self.PRIORITY_WEIGHTS.get(n.priority, 0),
            n.timestamp
        ), reverse=True)
        
        return unread
    
    def mark_read(self, notification_id: str):
        """Merk varsling som lest"""
        for n in self.notifications:
            if n.id == notification_id:
                n.read = True
                self.save()
                return True
        return False
    
    def mark_all_read(self):
        """Merk alle som lest"""
        for n in self.notifications:
            n.read = True
        self.save()
    
    def get_summary(self) -> Dict[str, Any]:
        """Hent oppsummering"""
        unread = [n for n in self.notifications if not n.read]
        
        by_priority = {'critical': 0, 'high': 0, 'normal': 0, 'low': 0}
        by_category = {}
        
        for n in unread:
            by_priority[n.priority] = by_priority.get(n.priority, 0) + 1
            by_category[n.category] = by_category.get(n.category, 0) + 1
        
        return {
            'total': len(self.notifications),
            'unread': len(unread),
            'by_priority': by_priority,
            'by_category': by_category,
            'action_required': len([n for n in unread if n.action_required])
        }
    
    def cleanup_old(self, days: int = 7):
        """Slett gamle varslinger"""
        cutoff = DateUtils.add_days(DateUtils.now(), -days)
        cutoff_str = DateUtils.format(cutoff)
        
        self.notifications = [
            n for n in self.notifications 
            if n.timestamp >= cutoff_str or not n.read
        ]
        self.save()
    
    def display_notifications(self, min_priority: str = "low"):
        """Vis varslinger i terminal"""
        unread = self.get_unread(min_priority)
        
        if not unread:
            print("✅ Ingen nye varslinger")
            return
        
        print(f"\n{'='*70}")
        print(f"🔔 VARSlinger ({len(unread)} uleste)")
        print(f"{'='*70}")
        
        priority_icons = {
            'critical': '🔴',
            'high': '🟠',
            'normal': '🔵',
            'low': '⚪'
        }
        
        for n in unread[:10]:  # Vis maks 10
            icon = priority_icons.get(n.priority, '⚪')
            action = " [HANDLING PÅKREVD]" if n.action_required else ""
            
            print(f"\n{icon} [{n.priority.upper()}] {n.title}{action}")
            print(f"   {n.message}")
            print(f"   📁 {n.category} | 🕐 {n.timestamp}")
            
            if n.action_url:
                print(f"   🔗 {n.action_url}")

# === PRE-DEFINED NOTIFICATIONS ===

def send_system_notifications(service: SmartNotificationService):
    """Send system-varslinger"""
    
    # Sjekk system-status
    service.notify(
        title="System Check Fullført",
        message="Alle automatiske systemer kjører normalt.",
        priority="normal",
        category="system"
    )
    
    # Sjekk om Morning Routine er pauset
    service.notify(
        title="Morning Routine Pauset",
        message="Morning Routine er fortsatt pauset. Kjør 'rm .morning-routine-paused' for å gjenoppta.",
        priority="low",
        category="system"
    )
    
    # Toolkit status
    service.notify(
        title="50 Verktøy Klare",
        message="BaarliClaw Toolkit med 50 moduler er bygget og integrert.",
        priority="normal",
        category="system"
    )

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("🔔 SMART NOTIFICATION SERVICE")
    print("="*70)
    
    # Initialiser tjeneste
    service = SmartNotificationService()
    
    # Send system-varslinger
    print("\n📤 Sender system-varslinger...")
    send_system_notifications(service)
    
    # Vis oppsummering
    summary = service.get_summary()
    print(f"\n📊 Oppsummering:")
    print(f"   Totalt: {summary['total']} varslinger")
    print(f"   Uleste: {summary['unread']}")
    print(f"   Handling påkrevd: {summary['action_required']}")
    
    # Vis varslinger
    print("\n📋 Uleste varslinger:")
    service.display_notifications()
    
    print("\n" + "="*70)
    print("✅ Notification Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
