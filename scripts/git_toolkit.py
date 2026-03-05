#!/usr/bin/env python3
"""
🔀 BAARLICLAW GIT TOOLKIT
Git-automatisering og -håndtering
"""

import os
import sys
import subprocess
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("GitToolkit")

@dataclass
class GitStatus:
    """Git repository status"""
    branch: str
    modified: List[str]
    staged: List[str]
    untracked: List[str]
    ahead: int
    behind: int
    clean: bool

class GitManager:
    """Manage Git repositories"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def _run(self, args: List[str], check: bool = True) -> Tuple[bool, str]:
        """Run git command"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except Exception as e:
            return False, str(e)
    
    def status(self) -> GitStatus:
        """Get repository status"""
        # Get branch
        success, branch = self._run(['rev-parse', '--abbrev-ref', 'HEAD'])
        branch = branch.strip() if success else "unknown"
        
        # Get status
        success, output = self._run(['status', '--porcelain', '-b'])
        
        modified = []
        staged = []
        untracked = []
        ahead = 0
        behind = 0
        
        if success:
            lines = output.strip().split('\n')
            for line in lines:
                if line.startswith('##'):
                    # Parse branch info
                    if '[' in line:
                        info = line[line.find('[')+1:line.find(']')]
                        if 'ahead' in info:
                            ahead = int(info.split('ahead ')[1].split(',')[0])
                        if 'behind' in info:
                            behind = int(info.split('behind ')[1].split(',')[0])
                elif len(line) >= 2:
                    status_code = line[:2]
                    filename = line[3:].strip()
                    
                    if status_code[0] != ' ' and status_code[0] != '?':
                        staged.append(filename)
                    if status_code[1] != ' ':
                        modified.append(filename)
                    if status_code == '??':
                        untracked.append(filename)
        
        return GitStatus(
            branch=branch,
            modified=modified,
            staged=staged,
            untracked=untracked,
            ahead=ahead,
            behind=behind,
            clean=len(modified) == 0 and len(staged) == 0 and len(untracked) == 0
        )
    
    def add(self, files: List[str]) -> bool:
        """Stage files"""
        success, _ = self._run(['add'] + files)
        if success:
            logger.info(f"Staged {len(files)} files")
        return success
    
    def commit(self, message: str) -> bool:
        """Commit staged changes"""
        success, output = self._run(['commit', '-m', message])
        if success:
            logger.info(f"Committed: {message}")
        return success
    
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """Push to remote"""
        if branch is None:
            success, branch = self._run(['rev-parse', '--abbrev-ref', 'HEAD'])
            branch = branch.strip()
        
        success, _ = self._run(['push', remote, branch])
        if success:
            logger.info(f"Pushed to {remote}/{branch}")
        return success
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """Pull from remote"""
        args = ['pull', remote]
        if branch:
            args.append(branch)
        
        success, _ = self._run(args)
        if success:
            logger.info(f"Pulled from {remote}")
        return success
    
    def log(self, n: int = 10) -> List[Dict]:
        """Get commit history"""
        format_str = '%H|%an|%ae|%ad|%s'
        success, output = self._run([
            'log', f'-n{n}',
            f'--format={format_str}',
            '--date=short'
        ])
        
        commits = []
        if success:
            for line in output.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|', 4)
                    if len(parts) == 5:
                        commits.append({
                            'hash': parts[0][:7],
                            'author': parts[1],
                            'email': parts[2],
                            'date': parts[3],
                            'message': parts[4]
                        })
        
        return commits
    
    def diff(self, staged: bool = False) -> str:
        """Get diff"""
        args = ['diff']
        if staged:
            args.append('--staged')
        
        success, output = self._run(args)
        return output if success else ""
    
    def branch_list(self) -> List[Dict]:
        """List branches"""
        success, output = self._run(['branch', '-a', '-v'])
        
        branches = []
        if success:
            for line in output.strip().split('\n'):
                if line:
                    current = line.startswith('*')
                    name = line[2:].split()[0]
                    branches.append({
                        'name': name,
                        'current': current
                    })
        
        return branches
    
    def create_branch(self, name: str, checkout: bool = True) -> bool:
        """Create new branch"""
        if checkout:
            success, _ = self._run(['checkout', '-b', name])
        else:
            success, _ = self._run(['branch', name])
        
        if success:
            logger.info(f"Created branch: {name}")
        return success
    
    def stash(self, message: Optional[str] = None) -> bool:
        """Stash changes"""
        args = ['stash']
        if message:
            args.extend(['push', '-m', message])
        else:
            args.append('push')
        
        success, _ = self._run(args)
        if success:
            logger.info("Changes stashed")
        return success
    
    def stash_pop(self) -> bool:
        """Pop stash"""
        success, _ = self._run(['stash', 'pop'])
        if success:
            logger.info("Stash popped")
        return success
    
    def get_stats(self) -> Dict:
        """Get repository statistics"""
        stats = {
            'commits': 0,
            'branches': 0,
            'contributors': set(),
            'files': 0
        }
        
        # Commit count
        success, output = self._run(['rev-list', '--count', 'HEAD'])
        if success:
            stats['commits'] = int(output.strip())
        
        # Branch count
        branches = self.branch_list()
        stats['branches'] = len(branches)
        
        # Contributors
        success, output = self._run(['log', '--format=%an'])
        if success:
            stats['contributors'] = set(output.strip().split('\n'))
        
        # File count
        success, output = self._run(['ls-files'])
        if success:
            stats['files'] = len(output.strip().split('\n'))
        
        stats['contributors'] = list(stats['contributors'])
        return stats

class GitAutoCommit:
    """Auto-commit changes"""
    
    def __init__(self, repo_path: str = "."):
        self.git = GitManager(repo_path)
    
    def auto_commit(self, message: Optional[str] = None) -> bool:
        """Auto-commit all changes"""
        status = self.git.status()
        
        if status.clean:
            logger.info("Nothing to commit")
            return True
        
        # Add all changes
        if status.modified or status.untracked:
            self.git.add(['.'])
        
        # Generate message if not provided
        if not message:
            files_changed = len(status.modified) + len(status.untracked)
            message = f"Auto-commit: {files_changed} files changed ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        # Commit
        return self.git.commit(message)
    
    def sync(self) -> bool:
        """Pull, commit, push"""
        # Pull first
        if not self.git.pull():
            logger.warning("Pull failed, continuing...")
        
        # Commit
        if not self.auto_commit():
            return False
        
        # Push
        return self.git.push()

# === CONVENIENCE FUNCTIONS ===
def quick_status(path: str = ".") -> GitStatus:
    """Quick status check"""
    git = GitManager(path)
    return git.status()

def quick_commit(message: str, path: str = ".") -> bool:
    """Quick commit"""
    git = GitManager(path)
    status = git.status()
    
    if status.clean:
        return True
    
    git.add(['.'])
    return git.commit(message)

def quick_sync(path: str = ".") -> bool:
    """Quick sync (pull, commit, push)"""
    auto = GitAutoCommit(path)
    return auto.sync()

# === TESTING ===
if __name__ == "__main__":
    print("🔀 BaarliClaw Git Toolkit - Testing")
    print("=" * 50)
    
    try:
        git = GitManager("/root/.openclaw/workspace")
        
        print("\n🧪 Testing status")
        status = git.status()
        print(f"✅ Branch: {status.branch}")
        print(f"✅ Clean: {status.clean}")
        print(f"✅ Modified: {len(status.modified)} files")
        
        print("\n🧪 Testing log")
        commits = git.log(5)
        print(f"✅ Last {len(commits)} commits:")
        for c in commits[:3]:
            print(f"   {c['hash']}: {c['message'][:50]}")
        
        print("\n🧪 Testing stats")
        stats = git.get_stats()
        print(f"✅ Total commits: {stats['commits']}")
        print(f"✅ Branches: {stats['branches']}")
        print(f"✅ Files: {stats['files']}")
        
    except ValueError as e:
        print(f"⚠️ {e}")
    
    print("\n✅ Git Toolkit ready!")
