#!/usr/bin/env python3
"""
🤖 BAARLICLAW AUTOMATION ENGINE
Automatiseringsmotor som binder alt sammen
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading

# Legg til toolkit i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("AutomationEngine")

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Represents a single automation task"""
    id: str
    name: str
    command: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    depends_on: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.depends_on is None:
            self.depends_on = []
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'command': self.command,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error': self.error,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries
        }

class AutomationEngine:
    """
    Central automation engine
    
    Features:
    - Task queue with priorities
    - Dependency management
    - Retry logic
    - Parallel execution
    - Progress tracking
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.running = False
        self.lock = threading.Lock()
        self.workers: List[threading.Thread] = []
        self.history: List[Dict] = []
        self.callbacks: Dict[str, List[Callable]] = {
            'on_task_complete': [],
            'on_task_fail': [],
            'on_all_complete': []
        }
        
    def register_callback(self, event: str, callback: Callable):
        """Register a callback for an event"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any):
        """Trigger all callbacks for an event"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def add_task(self, name: str, command: str, 
                 depends_on: Optional[List[str]] = None,
                 max_retries: int = 3) -> str:
        """
        Add a new task to the queue
        
        Args:
            name: Task name
            command: Shell command or Python function reference
            depends_on: List of task IDs that must complete first
            max_retries: Number of retries on failure
        """
        task_id = f"task_{int(time.time() * 1000)}_{len(self.tasks)}"
        
        task = Task(
            id=task_id,
            name=name,
            command=command,
            max_retries=max_retries,
            depends_on=depends_on or []
        )
        
        with self.lock:
            self.tasks[task_id] = task
            self.task_queue.append(task_id)
        
        logger.info(f"Added task: {name} ({task_id})")
        return task_id
    
    def add_python_task(self, name: str, func: Callable, 
                       args: tuple = (), kwargs: Optional[Dict] = None,
                       depends_on: Optional[List[str]] = None) -> str:
        """Add a Python function as a task"""
        # Store function reference for later execution
        task_id = self.add_task(
            name=name,
            command=f"__python__:{func.__name__}",
            depends_on=depends_on
        )
        
        # Store function and args
        self.tasks[task_id]._func = func
        self.tasks[task_id]._args = args
        self.tasks[task_id]._kwargs = kwargs or {}
        
        return task_id
    
    def _can_run(self, task: Task) -> bool:
        """Check if task can run (dependencies satisfied)"""
        for dep_id in task.depends_on:
            if dep_id not in self.tasks:
                return False
            dep_task = self.tasks[dep_id]
            if dep_task.status != TaskStatus.SUCCESS:
                return False
        return True
    
    def _execute_task(self, task: Task) -> bool:
        """Execute a single task"""
        task.started_at = datetime.now()
        task.status = TaskStatus.RUNNING
        
        logger.info(f"Executing: {task.name}")
        
        try:
            if task.command.startswith("__python__:"):
                # Execute Python function
                if hasattr(task, '_func'):
                    result = task._func(*task._args, **task._kwargs)
                    task.result = result
                else:
                    raise ValueError("Python function not found")
            else:
                # Execute shell command
                result = subprocess.run(
                    task.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    task.result = {
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    }
                else:
                    raise subprocess.CalledProcessError(
                        result.returncode, task.command,
                        output=result.stdout, stderr=result.stderr
                    )
            
            task.status = TaskStatus.SUCCESS
            task.completed_at = datetime.now()
            logger.info(f"✅ Completed: {task.name}")
            self._trigger_callbacks('on_task_complete', task)
            return True
            
        except Exception as e:
            task.error = str(e)
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                task.status = TaskStatus.RETRYING
                logger.warning(f"⚠️ Retrying {task.name} ({task.retry_count}/{task.max_retries})")
                return False
            else:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                logger.error(f"❌ Failed: {task.name} - {e}")
                self._trigger_callbacks('on_task_fail', task)
                return False
    
    def _worker_loop(self):
        """Worker thread loop"""
        while self.running:
            task_to_run = None
            
            with self.lock:
                for task_id in self.task_queue:
                    task = self.tasks[task_id]
                    if task.status in [TaskStatus.PENDING, TaskStatus.RETRYING]:
                        if self._can_run(task):
                            task_to_run = task
                            break
            
            if task_to_run:
                self._execute_task(task_to_run)
            else:
                time.sleep(0.5)
    
    def start(self):
        """Start the automation engine"""
        self.running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"🚀 Automation engine started with {self.max_workers} workers")
    
    def stop(self):
        """Stop the automation engine"""
        self.running = False
        for worker in self.workers:
            worker.join(timeout=5)
        logger.info("🛑 Automation engine stopped")
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """Wait for all tasks to complete"""
        start_time = time.time()
        
        while True:
            with self.lock:
                pending = [
                    t for t in self.tasks.values()
                    if t.status in [TaskStatus.PENDING, TaskStatus.RUNNING, TaskStatus.RETRYING]
                ]
            
            if not pending:
                self._trigger_callbacks('on_all_complete', self.get_summary())
                return True
            
            if timeout and (time.time() - start_time) > timeout:
                logger.warning("⏱️ Timeout waiting for tasks")
                return False
            
            time.sleep(0.5)
    
    def get_summary(self) -> Dict:
        """Get summary of all tasks"""
        with self.lock:
            statuses = {}
            for task in self.tasks.values():
                status = task.status.value
                statuses[status] = statuses.get(status, 0) + 1
            
            return {
                'total': len(self.tasks),
                'by_status': statuses,
                'success_rate': (
                    statuses.get('success', 0) / len(self.tasks) * 100
                    if self.tasks else 0
                )
            }
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def export_report(self, filepath: str):
        """Export task report to JSON"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': self.get_summary(),
            'tasks': [task.to_dict() for task in self.tasks.values()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Report exported to {filepath}")

# === WORKFLOW BUILDER ===
class WorkflowBuilder:
    """Build complex workflows with the automation engine"""
    
    def __init__(self, engine: AutomationEngine):
        self.engine = engine
        self.steps: List[Dict] = []
    
    def add_step(self, name: str, action: str, 
                 depends_on: Optional[List[str]] = None) -> 'WorkflowBuilder':
        """Add a step to the workflow"""
        self.steps.append({
            'name': name,
            'action': action,
            'depends_on': depends_on or [],
            'id': None
        })
        return self
    
    def add_python_step(self, name: str, func: Callable,
                       args: tuple = (), kwargs: Optional[Dict] = None,
                       depends_on: Optional[List[str]] = None) -> 'WorkflowBuilder':
        """Add a Python function step"""
        self.steps.append({
            'name': name,
            'action': '__python__',
            'func': func,
            'args': args,
            'kwargs': kwargs or {},
            'depends_on': depends_on or [],
            'id': None
        })
        return self
    
    def build(self) -> List[str]:
        """Build and return task IDs"""
        task_ids = []
        
        for step in self.steps:
            # Map dependency names to IDs
            dep_ids = []
            for dep_name in step['depends_on']:
                for s in self.steps:
                    if s['name'] == dep_name and s['id']:
                        dep_ids.append(s['id'])
                        break
            
            if step['action'] == '__python__':
                task_id = self.engine.add_python_task(
                    name=step['name'],
                    func=step['func'],
                    args=step['args'],
                    kwargs=step['kwargs'],
                    depends_on=dep_ids
                )
            else:
                task_id = self.engine.add_task(
                    name=step['name'],
                    command=step['action'],
                    depends_on=dep_ids
                )
            
            step['id'] = task_id
            task_ids.append(task_id)
        
        return task_ids

# === PRE-BUILT WORKFLOWS ===
def create_morning_routine_workflow(engine: AutomationEngine) -> WorkflowBuilder:
    """Create the NRJ Morgen morning routine workflow"""
    workflow = WorkflowBuilder(engine)
    
    workflow \
        .add_step("check_api_status", "curl -s https://api.search.brave.com/status") \
        .add_step("fetch_news", "python3 /root/.openclaw/workspace/scripts/morning-routine-v2.1.py",
                 depends_on=["check_api_status"]) \
        .add_step("update_images", "python3 /root/.openclaw/workspace/scripts/update_article_images.py",
                 depends_on=["fetch_news"]) \
        .add_step("verify_database", "python3 -c \"print('DB check')\"",
                 depends_on=["update_images"])
    
    return workflow

# === TESTING ===
if __name__ == "__main__":
    print("🤖 BaarliClaw Automation Engine - Testing")
    print("=" * 50)
    
    # Create engine
    engine = AutomationEngine(max_workers=2)
    
    # Test Python function task
    def test_func(name: str) -> str:
        time.sleep(0.5)
        return f"Hello, {name}!"
    
    # Add tasks
    task1 = engine.add_python_task("greet", test_func, args=("World",))
    task2 = engine.add_task("list_files", "ls -la /tmp")
    task3 = engine.add_task("echo_test", "echo 'Automation works!'")
    
    # Add callback
    def on_complete(task):
        print(f"✅ Task completed: {task.name}")
    
    engine.register_callback('on_task_complete', on_complete)
    
    # Start and run
    engine.start()
    
    print("\n⏳ Running tasks...")
    engine.wait_for_completion(timeout=30)
    
    # Show summary
    summary = engine.get_summary()
    print(f"\n📊 Summary: {summary}")
    
    # Stop
    engine.stop()
    
    print("\n✅ Automation Engine ready!")
