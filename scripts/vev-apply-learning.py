#!/usr/bin/env python3
"""
Vev Learning Application System
Applies previous learning to current tasks
"""
import os
import json
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DB = f"{WORKSPACE}/brain/learning-database.json"

def load_learning_db():
    if os.path.exists(LEARNING_DB):
        with open(LEARNING_DB) as f:
            return json.load(f)
    return {"sessions": [], "learnings": []}

def get_relevant_learning(task_description):
    """Find relevant previous learning for current task"""
    db = load_learning_db()
    
    if not db["learnings"]:
        return None
    
    # Simple keyword matching
    keywords = task_description.lower().split()
    relevant = []
    
    for learning in db["learnings"][-20:]:  # Last 20 learnings
        learning_text = learning.get("text", "").lower()
        score = sum(1 for kw in keywords if kw in learning_text)
        if score > 0:
            relevant.append((learning, score))
    
    # Sort by relevance score
    relevant.sort(key=lambda x: x[1], reverse=True)
    
    return [l[0] for l in relevant[:3]]  # Top 3 most relevant

def apply_learning_before_task(task_description):
    """Check for relevant learning before starting a task"""
    print("=" * 60)
    print("🧠 CHECKING PREVIOUS LEARNING")
    print("=" * 60)
    print()
    
    relevant = get_relevant_learning(task_description)
    
    if not relevant:
        print("   No previous learning found for this type of task.")
        print("   This might be new - I'll learn from this experience!")
        return None
    
    print(f"   Found {len(relevant)} relevant previous learnings:")
    print()
    
    for i, learning in enumerate(relevant, 1):
        print(f"   {i}. {learning['text']}")
        print(f"      From: {learning.get('date', 'unknown')}")
        print()
    
    return relevant

def suggest_best_practice(task_description):
    """Suggest best practices based on previous learning"""
    db = load_learning_db()
    
    # Count task types
    task_counts = {}
    for session in db.get("sessions", []):
        for task_type in session.get("task_types", []):
            task_counts[task_type] = task_counts.get(task_type, 0) + 1
    
    # If we've done this task type before, suggest what worked
    for task_type in task_counts:
        if task_type in task_description.lower():
            return f"You've worked on {task_type} {task_counts[task_type]} times before. Consider what worked previously."
    
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task = sys.argv[1]
        apply_learning_before_task(task)
    else:
        print("Usage: python3 vev-apply-learning.py 'task description'")
