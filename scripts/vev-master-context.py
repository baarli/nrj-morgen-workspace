#!/usr/bin/env python3
"""
Vev Master Context Loader
Laster alle kritiske dokumenter i riktig rekkefølge
"""
import os
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"

def load_file_summary(filepath, max_lines=10):
    """Load first few lines of a file"""
    try:
        if os.path.exists(filepath):
            content = Path(filepath).read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip()][:max_lines]
            return '\n   '.join(lines)
    except:
        pass
    return "   [Fil ikke funnet eller tom]"

def main():
    print("=" * 60)
    print("📚 VEV MASTER CONTEXT LOADING")
    print("=" * 60)
    print()
    
    # Step 0: SYSTEM_ARCHITECTURE.md (Master)
    print("📋 STEP 0: SYSTEM_ARCHITECTURE.md (Master Overview)")
    print("-" * 60)
    arch_summary = load_file_summary(f"{WORKSPACE}/SYSTEM_ARCHITECTURE.md", 5)
    print(f"   {arch_summary}")
    print()
    
    # Step 1: AGENTS.md (System Status)
    print("🤖 STEP 1: AGENTS.md (System Status)")
    print("-" * 60)
    agents_summary = load_file_summary(f"{WORKSPACE}/AGENTS.md", 5)
    print(f"   {agents_summary}")
    print()
    
    # Step 2: TOOLS.md (Verktøy)
    print("🛠️  STEP 2: TOOLS.md (Verktøy)")
    print("-" * 60)
    tools_summary = load_file_summary(f"{WORKSPACE}/TOOLS.md", 5)
    print(f"   {tools_summary}")
    print()
    
    # Step 3: MEMORY.md (Kunnskap)
    print("🧠 STEP 3: MEMORY.md (Kunnskap)")
    print("-" * 60)
    memory_summary = load_file_summary(f"{WORKSPACE}/MEMORY.md", 5)
    print(f"   {memory_summary}")
    print()
    
    # Step 4: SOUL.md (Personlighet)
    print("🎭 STEP 4: SOUL.md (Personlighet)")
    print("-" * 60)
    soul_summary = load_file_summary(f"{WORKSPACE}/SOUL.md", 5)
    print(f"   {soul_summary}")
    print()
    
    print("=" * 60)
    print("✅ ALL MASTER CONTEXT LOADED")
    print("=" * 60)

if __name__ == "__main__":
    main()
