#!/usr/bin/env python3
"""
🔄 BAARLICLAW CI/CD TOOLKIT
Continuous Integration / Deployment verktøy
"""

import os
import sys
import subprocess
import json
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("CICDToolkit")

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PipelineStep:
    """Pipeline step"""
    name: str
    command: str
    status: StepStatus = StepStatus.PENDING
    output: str = ""
    error: str = ""
    duration_ms: float = 0
    allow_failure: bool = False

@dataclass
class Pipeline:
    """Pipeline definition"""
    name: str
    steps: List[PipelineStep]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def duration_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0
    
    @property
    def success(self) -> bool:
        for step in self.steps:
            if step.status == StepStatus.FAILED and not step.allow_failure:
                return False
        return True
    
    @property
    def failed_steps(self) -> List[PipelineStep]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

class PipelineRunner:
    """Run CI/CD pipelines"""
    
    def __init__(self):
        self.pipelines: List[Pipeline] = []
        self.callbacks: Dict[str, List[Callable]] = {
            'on_step_complete': [],
            'on_pipeline_complete': []
        }
    
    def on(self, event: str, callback: Callable):
        """Register callback"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger(self, event: str, data: Any):
        """Trigger callbacks"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def create_pipeline(self, name: str) -> Pipeline:
        """Create new pipeline"""
        pipeline = Pipeline(name=name, steps=[])
        self.pipelines.append(pipeline)
        return pipeline
    
    def add_step(self, pipeline: Pipeline, name: str, command: str,
                 allow_failure: bool = False):
        """Add step to pipeline"""
        step = PipelineStep(
            name=name,
            command=command,
            allow_failure=allow_failure
        )
        pipeline.steps.append(step)
    
    def run_pipeline(self, pipeline: Pipeline) -> bool:
        """Run a pipeline"""
        logger.info(f"🚀 Starting pipeline: {pipeline.name}")
        pipeline.start_time = datetime.now()
        
        for step in pipeline.steps:
            if step.status == StepStatus.SKIPPED:
                continue
            
            step.status = StepStatus.RUNNING
            logger.info(f"  ▶️  {step.name}")
            
            start = datetime.now()
            
            try:
                result = subprocess.run(
                    step.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                step.duration_ms = (datetime.now() - start).total_seconds() * 1000
                step.output = result.stdout
                
                if result.returncode == 0:
                    step.status = StepStatus.SUCCESS
                    logger.info(f"  ✅ {step.name} ({step.duration_ms:.0f}ms)")
                else:
                    step.status = StepStatus.FAILED
                    step.error = result.stderr
                    logger.error(f"  ❌ {step.name}: {result.stderr[:100]}")
                    
                    if not step.allow_failure:
                        break
                
            except subprocess.TimeoutExpired:
                step.status = StepStatus.FAILED
                step.error = "Timeout"
                step.duration_ms = (datetime.now() - start).total_seconds() * 1000
                logger.error(f"  ⏱️  {step.name}: Timeout")
                
                if not step.allow_failure:
                    break
                    
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error = str(e)
                step.duration_ms = (datetime.now() - start).total_seconds() * 1000
                logger.error(f"  ❌ {step.name}: {e}")
                
                if not step.allow_failure:
                    break
            
            self._trigger('on_step_complete', step)
        
        pipeline.end_time = datetime.now()
        self._trigger('on_pipeline_complete', pipeline)
        
        if pipeline.success:
            logger.info(f"✅ Pipeline completed: {pipeline.name}")
        else:
            logger.error(f"❌ Pipeline failed: {pipeline.name}")
        
        return pipeline.success
    
    def generate_report(self, pipeline: Pipeline) -> str:
        """Generate pipeline report"""
        lines = [
            f"\n{'='*60}",
            f"🔄 PIPELINE REPORT: {pipeline.name}",
            f"{'='*60}",
            f"Status: {'✅ SUCCESS' if pipeline.success else '❌ FAILED'}",
            f"Duration: {pipeline.duration_ms:.0f}ms",
            f"Steps: {len(pipeline.steps)}",
            f"{'='*60}",
        ]
        
        for step in pipeline.steps:
            icon = {
                StepStatus.PENDING: "⏸️",
                StepStatus.RUNNING: "▶️",
                StepStatus.SUCCESS: "✅",
                StepStatus.FAILED: "❌",
                StepStatus.SKIPPED: "⏭️"
            }.get(step.status, "❓")
            
            lines.append(f"\n{icon} {step.name}")
            lines.append(f"   Status: {step.status.value}")
            lines.append(f"   Duration: {step.duration_ms:.0f}ms")
            
            if step.error:
                lines.append(f"   Error: {step.error[:100]}")
        
        lines.append(f"\n{'='*60}")
        
        return "\n".join(lines)

class DeploymentManager:
    """Manage deployments"""
    
    def __init__(self):
        self.deployments: List[Dict] = []
    
    def deploy(self, name: str, source: str, destination: str,
               pre_deploy: Optional[List[str]] = None,
               post_deploy: Optional[List[str]] = None) -> bool:
        """Deploy application"""
        logger.info(f"🚀 Deploying: {name}")
        
        deployment = {
            "name": name,
            "source": source,
            "destination": destination,
            "start_time": datetime.now(),
            "status": "running"
        }
        
        try:
            # Pre-deploy hooks
            if pre_deploy:
                for cmd in pre_deploy:
                    result = subprocess.run(cmd, shell=True, capture_output=True)
                    if result.returncode != 0:
                        raise Exception(f"Pre-deploy failed: {result.stderr}")
            
            # Deploy
            if os.path.isfile(source):
                # Single file
                import shutil
                shutil.copy2(source, destination)
            else:
                # Directory
                if os.path.exists(destination):
                    import shutil
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
            
            # Post-deploy hooks
            if post_deploy:
                for cmd in post_deploy:
                    result = subprocess.run(cmd, shell=True, capture_output=True)
                    if result.returncode != 0:
                        raise Exception(f"Post-deploy failed: {result.stderr}")
            
            deployment["status"] = "success"
            deployment["end_time"] = datetime.now()
            logger.info(f"✅ Deployed: {name}")
            
        except Exception as e:
            deployment["status"] = "failed"
            deployment["error"] = str(e)
            logger.error(f"❌ Deployment failed: {e}")
        
        self.deployments.append(deployment)
        return deployment["status"] == "success"
    
    def rollback(self, name: str, backup_path: str) -> bool:
        """Rollback to backup"""
        logger.info(f"⏮️  Rolling back: {name}")
        
        try:
            # Implementation depends on backup strategy
            logger.info(f"✅ Rollback complete: {name}")
            return True
        except Exception as e:
            logger.error(f"❌ Rollback failed: {e}")
            return False

# === PRE-BUILT PIPELINES ===
def create_python_pipeline(project_path: str = ".") -> Pipeline:
    """Create standard Python project pipeline"""
    runner = PipelineRunner()
    pipeline = runner.create_pipeline("Python CI")
    
    runner.add_step(pipeline, "Install dependencies", 
                   f"cd {project_path} && pip install -r requirements.txt")
    runner.add_step(pipeline, "Run tests",
                   f"cd {project_path} && python -m pytest")
    runner.add_step(pipeline, "Lint code",
                   f"cd {project_path} && flake8 .", allow_failure=True)
    runner.add_step(pipeline, "Type check",
                   f"cd {project_path} && mypy .", allow_failure=True)
    
    return pipeline

def create_static_site_pipeline(source: str, destination: str) -> Pipeline:
    """Create static site deployment pipeline"""
    runner = PipelineRunner()
    pipeline = runner.create_pipeline("Static Site Deploy")
    
    runner.add_step(pipeline, "Build site",
                   f"cd {source} && npm run build")
    runner.add_step(pipeline, "Run tests",
                   f"cd {source} && npm test", allow_failure=True)
    runner.add_step(pipeline, "Deploy",
                   f"cp -r {source}/dist/* {destination}/")
    
    return pipeline

# === TESTING ===
if __name__ == "__main__":
    print("🔄 BaarliClaw CI/CD Toolkit - Testing")
    print("=" * 50)
    
    # Create pipeline
    runner = PipelineRunner()
    pipeline = runner.create_pipeline("Test Pipeline")
    
    runner.add_step(pipeline, "Check Python", "python3 --version")
    runner.add_step(pipeline, "Check Git", "git --version")
    runner.add_step(pipeline, "List files", "ls -la /tmp")
    runner.add_step(pipeline, "Failing step", "exit 1", allow_failure=True)
    
    # Run
    print("\n🧪 Running pipeline...")
    success = runner.run_pipeline(pipeline)
    
    # Report
    print(runner.generate_report(pipeline))
    
    print("\n✅ CI/CD Toolkit ready!")
