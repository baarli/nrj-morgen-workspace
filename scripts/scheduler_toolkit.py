#!/usr/bin/env python3
"""
⏰ BAARLICLAW SCHEDULER TOOLKIT
Tidsplanlegging og påminnelser
"""

import os
import sys
import time
import threading
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("SchedulerToolkit")

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ScheduledTask:
    """Scheduled task"""
    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: Dict
    scheduled_time: datetime
    priority: TaskPriority
    recurring: bool = False
    interval_seconds: Optional[int] = None
    completed: bool = False
    cancelled: bool = False

class TaskScheduler:
    """Schedule and run tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def schedule(self, name: str, func: Callable,
                 scheduled_time: datetime,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 args: tuple = None,
                 kwargs: Dict = None,
                 recurring: bool = False,
                 interval_seconds: Optional[int] = None) -> str:
        """Schedule a task"""
        task_id = f"task_{int(time.time() * 1000)}"
        
        task = ScheduledTask(
            id=task_id,
            name=name,
            func=func,
            args=args or (),
            kwargs=kwargs or {},
            scheduled_time=scheduled_time,
            priority=priority,
            recurring=recurring,
            interval_seconds=interval_seconds
        )
        
        with self._lock:
            self.tasks[task_id] = task
        
        logger.info(f"Scheduled: {name} at {scheduled_time}")
        return task_id
    
    def schedule_in(self, name: str, func: Callable,
                   seconds: int,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   **kwargs) -> str:
        """Schedule task to run in X seconds"""
        scheduled_time = datetime.now() + timedelta(seconds=seconds)
        return self.schedule(name, func, scheduled_time, priority, kwargs=kwargs)
    
    def start(self):
        """Start the scheduler"""
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def _run_loop(self):
        """Main scheduler loop"""
        while self.running:
            now = datetime.now()
            
            with self._lock:
                to_run = []
                for task in self.tasks.values():
                    if not task.completed and not task.cancelled:
                        if task.scheduled_time <= now:
                            to_run.append(task)
                
                to_run.sort(key=lambda t: t.priority.value, reverse=True)
            
            for task in to_run:
                try:
                    logger.info(f"Running: {task.name}")
                    task.func(*task.args, **task.kwargs)
                    
                    if task.recurring and task.interval_seconds:
                        task.scheduled_time = now + timedelta(seconds=task.interval_seconds)
                    else:
                        task.completed = True
                        
                except Exception as e:
                    logger.error(f"Task failed: {task.name} - {e}")
                    task.completed = True
            
            time.sleep(1)

# === TESTING ===
if __name__ == "__main__":
    print("⏰ BaarliClaw Scheduler Toolkit - Testing")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    def test_task():
        print("Task executed!")
    
    scheduler.schedule_in("Test", test_task, 1)
    scheduler.start()
    time.sleep(2)
    scheduler.stop()
    
    print("\n✅ Scheduler Toolkit ready!")
