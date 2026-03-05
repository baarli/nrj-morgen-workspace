#!/usr/bin/env python3
"""
🔒 Security Fixer - Automated security vulnerability remediation
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

class SecurityFixer:
    """Automatically fix common security vulnerabilities"""
    
    def __init__(self, workspace_path='/root/.openclaw/workspace'):
        self.workspace = Path(workspace_path)
        self.fixes_applied = []
        
    def fix_shell_scripts_set_e(self):
        """Add set -e to shell scripts missing error handling"""
        scripts_dir = self.workspace / 'scripts'
        
        for sh_file in scripts_dir.glob('*.sh'):
            try:
                with open(sh_file, 'r') as f:
                    content = f.read()
                
                # Check if already has set -e
                if 'set -e' in content or 'set -o errexit' in content:
                    continue
                
                # Find shebang line
                lines = content.split('\n')
                shebang_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith('#!'):
                        shebang_idx = i
                        break
                
                if shebang_idx >= 0:
                    # Insert set -e after shebang and empty line
                    insert_idx = shebang_idx + 1
                    if insert_idx < len(lines) and lines[insert_idx].strip() == '':
                        insert_idx += 1
                    
                    lines.insert(insert_idx, 'set -e  # Exit on error')
                    
                    with open(sh_file, 'w') as f:
                        f.write('\n'.join(lines))
                    
                    self.fixes_applied.append(f"Added 'set -e' to {sh_file.name}")
                    
            except Exception as e:
                print(f"Error fixing {sh_file}: {e}")
    
    def fix_md5_to_sha256(self):
        """Replace MD5 with SHA-256 in toolkit files"""
        toolkit_files = [
            self.workspace / 'scripts' / 'baarliclaw_toolkit.py',
            self.workspace / 'scripts' / 'uuid_toolkit.py',
            self.workspace / 'scripts' / 'file_toolkit.py',
            self.workspace / 'scripts' / 'cache_toolkit.py',
        ]
        
        for file_path in toolkit_files:
            if not file_path.exists():
                continue
                
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace MD5 with SHA-256
                original = content
                content = re.sub(r'hashlib\.md5', 'hashlib.sha256', content)
                
                if content != original:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    self.fixes_applied.append(f"Replaced MD5 with SHA-256 in {file_path.name}")
                    
            except Exception as e:
                print(f"Error fixing {file_path}: {e}")
    
    def generate_report(self):
        """Generate fix report"""
        report_path = self.workspace / 'brain' / 'reports' / 'security-auto-fixes-2026-02-28.md'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# Security Auto-Fixes Report\n\n")
            f.write(f"**Date:** 2026-02-28\n\n")
            f.write(f"**Total Fixes Applied:** {len(self.fixes_applied)}\n\n")
            
            if self.fixes_applied:
                f.write("## Fixes Applied\n\n")
                for fix in self.fixes_applied:
                    f.write(f"- ✅ {fix}\n")
            else:
                f.write("No automatic fixes were applied.\n")
        
        return report_path
    
    def run(self):
        """Run all security fixes"""
        print("🔒 Running security fixes...")
        
        self.fix_shell_scripts_set_e()
        self.fix_md5_to_sha256()
        
        report_path = self.generate_report()
        
        print(f"\n✅ Security fixes complete!")
        print(f"📊 {len(self.fixes_applied)} fixes applied")
        print(f"💾 Report saved to: {report_path}")
        
        return self.fixes_applied


if __name__ == '__main__':
    fixer = SecurityFixer()
    fixer.run()
