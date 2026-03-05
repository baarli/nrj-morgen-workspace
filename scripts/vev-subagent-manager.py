#!/usr/bin/env python3
"""
Vev Sub-Agent System v1.0
Enables parallel background work with continuous communication
"""
import os
import sys
import json
import time
import uuid
import signal
import multiprocessing as mp
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Callable, Dict, List
import queue

WORKSPACE = "/root/.openclaw/workspace"
TASKS_DIR = f"{WORKSPACE}/brain/subagent-tasks"
LOG_FILE = f"{WORKSPACE}/brain/logs/subagent.log"

@dataclass
class TaskProgress:
    task_id: str
    status: str  # 'pending', 'running', 'completed', 'failed', 'interrupted'
    progress_percent: int
    message: str
    timestamp: str
    result: Optional[dict] = None

class SubAgentManager:
    """Manages background sub-agents"""
    
    def __init__(self):
        self.active_tasks: Dict[str, mp.Process] = {}
        self.progress_queues: Dict[str, mp.Queue] = {}
        self.result_queues: Dict[str, mp.Queue] = {}
        self.interrupt_flags: Dict[str, mp.Value] = {}
        os.makedirs(TASKS_DIR, exist_ok=True)
        
    def log(self, msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        print(log_msg)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\n')
    
    def spawn_task(self, task_type: str, task_data: dict, 
                   progress_callback: Optional[Callable] = None) -> str:
        """Spawn a new background task"""
        task_id = str(uuid.uuid4())[:8]
        
        self.log(f"🚀 Spawning task {task_id}: {task_type}")
        
        # Create communication queues
        progress_queue = mp.Queue()
        result_queue = mp.Queue()
        interrupt_flag = mp.Value('b', False)
        
        self.progress_queues[task_id] = progress_queue
        self.result_queues[task_id] = result_queue
        self.interrupt_flags[task_id] = interrupt_flag
        
        # Start worker process
        process = mp.Process(
            target=self._worker_wrapper,
            args=(task_id, task_type, task_data, progress_queue, 
                  result_queue, interrupt_flag)
        )
        process.start()
        
        self.active_tasks[task_id] = process
        
        # Start progress monitor in main thread
        if progress_callback:
            import threading
            monitor = threading.Thread(
                target=self._monitor_progress,
                args=(task_id, progress_callback),
                daemon=True
            )
            monitor.start()
        
        return task_id
    
    def _worker_wrapper(self, task_id: str, task_type: str, task_data: dict,
                       progress_queue: mp.Queue, result_queue: mp.Queue,
                       interrupt_flag: mp.Value):
        """Wrapper that runs in subprocess"""
        try:
            # Import worker based on task type
            if task_type == "research":
                from vev_subagent_workers import research_worker
                result = research_worker(task_data, progress_queue, interrupt_flag)
            elif task_type == "analysis":
                from vev_subagent_workers import analysis_worker
                result = analysis_worker(task_data, progress_queue, interrupt_flag)
            elif task_type == "coding":
                from vev_subagent_workers import coding_worker
                result = coding_worker(task_data, progress_queue, interrupt_flag)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            result_queue.put({"status": "success", "result": result})
            
        except Exception as e:
            result_queue.put({"status": "error", "error": str(e)})
    
    def _monitor_progress(self, task_id: str, callback: Callable):
        """Monitor progress from main thread"""
        progress_queue = self.progress_queues.get(task_id)
        if not progress_queue:
            return
        
        while task_id in self.active_tasks:
            try:
                progress = progress_queue.get(timeout=1)
                callback(progress)
                
                if progress['status'] in ['completed', 'failed', 'interrupted']:
                    break
                    
            except queue.Empty:
                continue
    
    def get_progress(self, task_id: str) -> Optional[TaskProgress]:
        """Get current progress of a task"""
        if task_id not in self.active_tasks:
            return None
        
        # Check if there's progress in queue
        progress_queue = self.progress_queues.get(task_id)
        if progress_queue and not progress_queue.empty():
            try:
                progress_data = progress_queue.get_nowait()
                return TaskProgress(**progress_data)
            except:
                pass
        
        return None
    
    def interrupt_task(self, task_id: str) -> bool:
        """Interrupt a running task"""
        if task_id not in self.active_tasks:
            return False
        
        self.log(f"⏹️ Interrupting task {task_id}")
        
        # Set interrupt flag
        interrupt_flag = self.interrupt_flags.get(task_id)
        if interrupt_flag:
            interrupt_flag.value = True
        
        # Wait for graceful shutdown
        process = self.active_tasks[task_id]
        process.join(timeout=5)
        
        # Force kill if still running
        if process.is_alive():
            process.terminate()
            process.join(timeout=2)
            if process.is_alive():
                process.kill()
        
        # Cleanup
        self._cleanup_task(task_id)
        
        return True
    
    def get_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[dict]:
        """Get result of a completed task"""
        result_queue = self.result_queues.get(task_id)
        if not result_queue:
            return None
        
        try:
            result = result_queue.get(timeout=timeout)
            self._cleanup_task(task_id)
            return result
        except queue.Empty:
            return None
    
    def _cleanup_task(self, task_id: str):
        """Clean up task resources"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
        if task_id in self.progress_queues:
            del self.progress_queues[task_id]
        if task_id in self.result_queues:
            del self.result_queues[task_id]
        if task_id in self.interrupt_flags:
            del self.interrupt_flags[task_id]
    
    def list_active_tasks(self) -> List[dict]:
        """List all active tasks"""
        tasks = []
        for task_id, process in self.active_tasks.items():
            tasks.append({
                'task_id': task_id,
                'pid': process.pid,
                'is_alive': process.is_alive()
            })
        return tasks
    
    def shutdown_all(self):
        """Shutdown all sub-agents"""
        self.log("🛑 Shutting down all sub-agents...")
        
        for task_id in list(self.active_tasks.keys()):
            self.interrupt_task(task_id)

# Global manager instance
_manager = None

def get_manager() -> SubAgentManager:
    """Get or create global manager"""
    global _manager
    if _manager is None:
        _manager = SubAgentManager()
    return _manager

# Convenience functions
def spawn_background_task(task_type: str, task_data: dict, 
                          progress_callback: Optional[Callable] = None) -> str:
    """Spawn a background task"""
    return get_manager().spawn_task(task_type, task_data, progress_callback)

def get_task_progress(task_id: str) -> Optional[TaskProgress]:
    """Get task progress"""
    return get_manager().get_progress(task_id)

def interrupt_background_task(task_id: str) -> bool:
    """Interrupt a task"""
    return get_manager().interrupt_task(task_id)

def get_task_result(task_id: str, timeout: Optional[float] = None) -> Optional[dict]:
    """Get task result"""
    return get_manager().get_result(task_id, timeout)

if __name__ == "__main__":
    # Test
    manager = get_manager()
    
    def print_progress(progress):
        print(f"Progress: {progress['progress_percent']}% - {progress['message']}")
    
    # Spawn test task
    task_id = manager.spawn_task("test", {"duration": 5}, print_progress)
    print(f"Spawned task: {task_id}")
    
    # Wait for completion
    result = manager.get_result(task_id, timeout=10)
    print(f"Result: {result}")
