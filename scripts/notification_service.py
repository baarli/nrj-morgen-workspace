#!/usr/bin/env python3
"""
🔔 Notification Service - Unified notification system
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("NotificationService")

@dataclass
class Notification:
    id: str
    title: str
    message: str
    level: str  # info, warning, error, critical
    source: str
    timestamp: str
    read: bool = False
    actions: List[Dict] = None
    
    def __post_init__(self):
        if self.actions is None:
            self.actions = []

class NotificationService:
    """Centralized notification management"""
    
    def __init__(self, storage_path='/root/.openclaw/workspace/brain/notifications.json'):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.notifications: List[Notification] = []
        self.load_notifications()
        
    def load_notifications(self):
        """Load notifications from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.notifications = [Notification(**n) for n in data]
            except Exception as e:
                logger.error(f"Error loading notifications: {e}")
    
    def save_notifications(self):
        """Save notifications to storage"""
        try:
            data = [asdict(n) for n in self.notifications]
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving notifications: {e}")
    
    def notify(self, title: str, message: str, level: str = 'info', 
               source: str = 'system', actions: List[Dict] = None) -> Notification:
        """Create and store a notification"""
        import uuid
        
        notification = Notification(
            id=str(uuid.uuid4())[:8],
            title=title,
            message=message,
            level=level,
            source=source,
            timestamp=datetime.now().isoformat(),
            actions=actions or []
        )
        
        self.notifications.append(notification)
        
        # Keep only last 100 notifications
        if len(self.notifications) > 100:
            self.notifications = self.notifications[-100:]
        
        self.save_notifications()
        
        # Log based on level
        if level == 'critical':
            logger.critical(f"{title}: {message}")
        elif level == 'error':
            logger.error(f"{title}: {message}")
        elif level == 'warning':
            logger.warning(f"{title}: {message}")
        else:
            logger.info(f"{title}: {message}")
        
        return notification
    
    def get_unread(self) -> List[Notification]:
        """Get all unread notifications"""
        return [n for n in self.notifications if not n.read]
    
    def mark_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        for n in self.notifications:
            if n.id == notification_id:
                n.read = True
                self.save_notifications()
                return True
        return False
    
    def mark_all_read(self):
        """Mark all notifications as read"""
        for n in self.notifications:
            n.read = True
        self.save_notifications()
    
    def clear_old(self, days: int = 7):
        """Clear notifications older than N days"""
        cutoff = datetime.now() - __import__('datetime').timedelta(days=days)
        
        self.notifications = [
            n for n in self.notifications 
            if datetime.fromisoformat(n.timestamp) > cutoff
        ]
        self.save_notifications()
    
    def get_stats(self) -> Dict:
        """Get notification statistics"""
        unread = len(self.get_unread())
        by_level = {}
        
        for n in self.notifications:
            by_level[n.level] = by_level.get(n.level, 0) + 1
        
        return {
            'total': len(self.notifications),
            'unread': unread,
            'by_level': by_level
        }
    
    def print_notifications(self, limit: int = 10):
        """Print recent notifications"""
        print("\n" + "=" * 70)
        print("🔔 NOTIFICATIONS")
        print("=" * 70)
        
        if not self.notifications:
            print("No notifications")
            return
        
        # Sort by timestamp (newest first)
        sorted_notifications = sorted(
            self.notifications, 
            key=lambda x: x.timestamp, 
            reverse=True
        )
        
        for n in sorted_notifications[:limit]:
            icon = {
                'critical': '🔴',
                'error': '❌',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(n.level, '•')
            
            read_status = " " if n.read else "[UNREAD]"
            time = datetime.fromisoformat(n.timestamp).strftime('%H:%M')
            
            print(f"\n{icon} {n.title} {read_status}")
            print(f"   {n.message[:60]}...")
            print(f"   Source: {n.source} | Time: {time}")
        
        print("=" * 70)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Notification Service')
    parser.add_argument('action', choices=['list', 'add', 'mark-read', 'stats'], 
                       help='Action to perform')
    parser.add_argument('--title', help='Notification title')
    parser.add_argument('--message', help='Notification message')
    parser.add_argument('--level', default='info', 
                       choices=['info', 'warning', 'error', 'critical'],
                       help='Notification level')
    parser.add_argument('--source', default='cli', help='Notification source')
    parser.add_argument('--id', help='Notification ID')
    
    args = parser.parse_args()
    
    service = NotificationService()
    
    if args.action == 'list':
        service.print_notifications()
    
    elif args.action == 'add':
        if not args.title or not args.message:
            print("Error: --title and --message required")
            sys.exit(1)
        notification = service.notify(args.title, args.message, args.level, args.source)
        print(f"Created notification: {notification.id}")
    
    elif args.action == 'mark-read':
        if not args.id:
            print("Error: --id required")
            sys.exit(1)
        if service.mark_read(args.id):
            print(f"Marked {args.id} as read")
        else:
            print(f"Notification {args.id} not found")
    
    elif args.action == 'stats':
        stats = service.get_stats()
        print(json.dumps(stats, indent=2))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
