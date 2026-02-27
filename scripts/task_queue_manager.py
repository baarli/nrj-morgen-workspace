#!/usr/bin/env python3
"""
🎯 Task Queue Manager - Manage and monitor background tasks
"""

import os
import sys
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("TaskQueueManager")

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    name: str
    command: str
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    priority: int = 5  # 1-10, lower is higher priority

class TaskQueueManager:
    """Manage background task queue"""
    
    def __init__(self, queue_file='/root/.openclaw/workspace/brain/task-queue.json'):
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks: Dict[str, Task] = {}
        self.load_queue()
        
    def load_queue(self):
        """Load task queue from file"""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    for task_id, task_data in data.items():
                        self.tasks[task_id] = Task(**task_data)
            except Exception as e:
                logger.error(f"Error loading queue: {e}")
    
    def save_queue(self):
        """Save task queue to file"""
        data = {task_id: asdict(task) for task_id, task in self.tasks.items()}
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_task(self, name: str, command: str, priority: int = 5) -> str:
        """Add a new task to the queue"""
        task_id = str(uuid.uuid4())[:8]
        task = Task(
            id=task_id,
            name=name,
            command=command,
            status=TaskStatus.PENDING.value,
            created_at=datetime.now().isoformat(),
            priority=priority
        )
        self.tasks[task_id] = task
        self.save_queue()
        logger.info(f"Added task: {name} (ID: {task_id})")
        return task_id
    
    def get_next_task(self) -> Optional[Task]:
        """Get next pending task by priority"""
        pending = [
            task for task in self.tasks.values()
            if task.status == TaskStatus.PENDING.value
        ]
        
        if not pending:
            return None
        
        # Sort by priority (lower number = higher priority)
        pending.sort(key=lambda t: t.priority)
        return pending[0]
    
    def start_task(self, task_id: str):
        """Mark task as running"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.RUNNING.value
            self.tasks[task_id].started_at = datetime.now().isoformat()
            self.save_queue()
    
    def complete_task(self, task_id: str, result: str):
        """Mark task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED.value
            self.tasks[task_id].completed_at = datetime.now().isoformat()
            self.tasks[task_id].result = result
            self.save_queue()
    
    def fail_task(self, task_id: str, error: str):
        """Mark task as failed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED.value
            self.tasks[task_id].completed_at = datetime.now().isoformat()
            self.tasks[task_id].error = error
            self.save_queue()
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.status == TaskStatus.PENDING.value:
                task.status = TaskStatus.CANCELLED.value
                self.save_queue()
                return True
        return False
    
    def get_status(self) -> Dict:
        """Get queue status summary"""
        status_counts = {
            'pending': 0,
            'running': 0,
            'completed': 0,
            'failed': 0,
            'cancelled': 0
        }
        
        for task in self.tasks.values():
            if task.status in status_counts:
                status_counts[task.status] += 1
        
        return {
            'total': len(self.tasks),
            'by_status': status_counts,
            'timestamp': datetime.now().isoformat()
        }
    
    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """List tasks, optionally filtered by status"""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # Sort by creation time (newest first)
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks
    
    def print_queue(self):
        """Print formatted queue status"""
        status = self.get_status()
        
        print("\n" + "=" * 60)
        print("🎯 TASK QUEUE STATUS")
        print("=" * 60)
        
        print(f"\n📊 Summary:")
        print(f"   Total tasks: {status['total']}")
        print(f"   Pending: {status['by_status']['pending']}")
        print(f"   Running: {status['by_status']['running']}")
        print(f"   Completed: {status['by_status']['completed']}")
        print(f"   Failed: {status['by_status']['failed']}")
        
        pending = self.list_tasks(TaskStatus.PENDING.value)
        if pending:
            print(f"\n⏳ Pending Tasks:")
            for task in pending[:5]:
                print(f"   [{task.priority}] {task.name} (ID: {task.id})")
        
        running = self.list_tasks(TaskStatus.RUNNING.value)
        if running:
            print(f"\n🔄 Running Tasks:")
            for task in running:
                print(f"   {task.name} (ID: {task.id})")
        
        print("=" * 60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Task Queue Manager')
    parser.add_argument('action', choices=['add', 'list', 'status', 'cancel'], help='Action')
    parser.add_argument('--name', help='Task name')
    parser.add_argument('--command', help='Task command')
    parser.add_argument('--priority', type=int, default=5, help='Task priority (1-10)')
    parser.add_argument('--id', help='Task ID')
    
    args = parser.parse_args()
    
    manager = TaskQueueManager()
    
    if args.action == 'add':
        if not args.name or not args.command:
            print("Error: --name and --command required")
            sys.exit(1)
        task_id = manager.add_task(args.name, args.command, args.priority)
        print(f"Added task: {task_id}")
    
    elif args.action == 'list':
        manager.print_queue()
    
    elif args.action == 'status':
        status = manager.get_status()
        print(json.dumps(status, indent=2))
    
    elif args.action == 'cancel':
        if not args.id:
            print("Error: --id required")
            sys.exit(1)
        if manager.cancel_task(args.id):
            print(f"Cancelled task: {args.id}")
        else:
            print(f"Could not cancel task: {args.id}")


if __name__ == '__main__':
    main()
