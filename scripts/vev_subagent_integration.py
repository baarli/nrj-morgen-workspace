#!/usr/bin/env python3
"""
Vev Sub-Agent Integration
Enables using sub-agents during conversation
"""
import sys
import os

# Fix imports
try:
    from vev_subagent_manager import (
        spawn_background_task, 
        get_task_progress, 
        interrupt_background_task,
        get_task_result,
        get_manager
    )
except ImportError:
    # Try with dash instead of underscore
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vev_subagent_manager", 
        os.path.join(os.path.dirname(__file__), "vev-subagent-manager.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    spawn_background_task = module.spawn_background_task
    get_task_progress = module.get_task_progress
    interrupt_background_task = module.interrupt_background_task
    get_task_result = module.get_task_result
    get_manager = module.get_manager

class VevWithSubAgents:
    """Vev enhanced with sub-agent capabilities"""
    
    def __init__(self):
        self.manager = get_manager()
        self.active_conversation_tasks = {}
    
    def spawn_research(self, query: str, sources=None, depth=3) -> str:
        """Spawn a research task"""
        task_data = {
            'query': query,
            'sources': sources or ['web'],
            'depth': depth
        }
        
        def on_progress(progress):
            # In real implementation, this would update the conversation
            print(f"[Research Progress] {progress['progress_percent']}%: {progress['message']}")
        
        task_id = spawn_background_task('research', task_data, on_progress)
        self.active_conversation_tasks[task_id] = {
            'type': 'research',
            'query': query,
            'started': True
        }
        
        return task_id
    
    def spawn_analysis(self, data: list, analysis_type='general') -> str:
        """Spawn an analysis task"""
        task_data = {
            'data': data,
            'analysis_type': analysis_type
        }
        
        def on_progress(progress):
            print(f"[Analysis Progress] {progress['progress_percent']}%: {progress['message']}")
        
        task_id = spawn_background_task('analysis', task_data, on_progress)
        self.active_conversation_tasks[task_id] = {
            'type': 'analysis',
            'items': len(data),
            'started': True
        }
        
        return task_id
    
    def spawn_coding(self, task: str, language='python', requirements=None) -> str:
        """Spawn a coding task"""
        task_data = {
            'task': task,
            'language': language,
            'requirements': requirements or []
        }
        
        def on_progress(progress):
            print(f"[Coding Progress] {progress['progress_percent']}%: {progress['message']}")
        
        task_id = spawn_background_task('coding', task_data, on_progress)
        self.active_conversation_tasks[task_id] = {
            'type': 'coding',
            'task': task,
            'started': True
        }
        
        return task_id
    
    def check_progress(self, task_id: str) -> dict:
        """Check progress of a task"""
        progress = get_task_progress(task_id)
        if progress:
            return {
                'status': progress.status,
                'percent': progress.progress_percent,
                'message': progress.message
            }
        
        # Check if completed
        result = get_task_result(task_id, timeout=0.1)
        if result:
            return {
                'status': 'completed',
                'result': result
            }
        
        return {'status': 'unknown', 'message': 'Task not found or not started'}
    
    def interrupt_task(self, task_id: str) -> bool:
        """Interrupt a running task"""
        return interrupt_background_task(task_id)
    
    def wait_for_result(self, task_id: str, timeout=None) -> dict:
        """Wait for and return task result"""
        return get_task_result(task_id, timeout)
    
    def list_active_tasks(self) -> list:
        """List all active tasks in this conversation"""
        return [
            {
                'task_id': tid,
                'type': info['type'],
                'status': self.check_progress(tid)['status']
            }
            for tid, info in self.active_conversation_tasks.items()
        ]

# Global instance for this conversation
_vev_subagent = None

def get_vev_with_subagents() -> VevWithSubAgents:
    """Get or create global instance"""
    global _vev_subagent
    if _vev_subagent is None:
        _vev_subagent = VevWithSubAgents()
    return _vev_subagent

# Example usage in conversation
def example_conversation():
    """Example of how sub-agents work in conversation"""
    vev = get_vev_with_subagents()
    
    print("🤖 Vev: Jeg kan hjelpe deg med flere ting samtidig!")
    print()
    
    # User asks for research
    print("👤 Bruker: Kan du researche NRJ Morgen konkurrenter?")
    print()
    
    # Spawn background research
    task_id = vev.spawn_research(
        query="NRJ Morgen radio konkurrenter",
        sources=['web', 'podcast'],
        depth=3
    )
    
    print(f"🤖 Vev: Jeg starter research nå (task: {task_id})")
    print("🤖 Vev: Mens jeg researcer, hva annet kan jeg hjelpe deg med?")
    print()
    
    # Continue conversation while research runs
    print("👤 Bruker: Kan du også analysere våre podcast-episoder?")
    print()
    
    # Spawn parallel analysis
    analysis_id = vev.spawn_analysis(
        data=['episode1', 'episode2', 'episode3', 'episode4', 'episode5'],
        analysis_type='engagement'
    )
    
    print(f"🤖 Vev: Starter analyse også (task: {analysis_id})")
    print("🤖 Vev: Nå kjører begge oppgavene i bakgrunnen!")
    print()
    
    # Check progress
    import time
    time.sleep(2)
    
    progress = vev.check_progress(task_id)
    print(f"📊 Research progress: {progress.get('percent', 0)}% - {progress.get('message', 'Unknown')}")
    
    analysis_progress = vev.check_progress(analysis_id)
    print(f"📊 Analysis progress: {analysis_progress.get('percent', 0)}% - {analysis_progress.get('message', 'Unknown')}")
    print()
    
    # Wait for results
    print("🤖 Vev: Venter på resultater...")
    research_result = vev.wait_for_result(task_id, timeout=30)
    analysis_result = vev.wait_for_result(analysis_id, timeout=30)
    
    print()
    print("✅ Research ferdig!")
    print(f"   Funnet: {research_result['result']['total_items']} kilder")
    print()
    print("✅ Analyse ferdig!")
    print(f"   Generert: {len(analysis_result['result']['insights'])} innsikter")

if __name__ == "__main__":
    example_conversation()
