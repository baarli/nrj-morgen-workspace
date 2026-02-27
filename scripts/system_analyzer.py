#!/usr/bin/env python3
"""
System-wide Code Quality Analyzer
Analyzes all Python and Shell scripts in the workspace for:
1. Code quality issues (duplication, complexity, dead code)
2. Missing error handling
3. Security vulnerabilities
4. Performance bottlenecks
5. Documentation gaps
"""

import os
import re
import ast
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Set

class CodeAnalyzer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues = defaultdict(list)
        self.file_stats = {}
        self.duplicate_patterns = defaultdict(list)
        self.security_issues = []
        self.performance_issues = []
        self.documentation_gaps = []
        self.error_handling_issues = []
        
    def analyze_all(self):
        """Run complete analysis on all files."""
        python_files = list(self.base_path.rglob("*.py"))
        shell_files = list(self.base_path.rglob("*.sh"))
        
        # Filter out node_modules, .netlify, dist directories
        python_files = [f for f in python_files if not any(x in str(f) for x in ['node_modules', '.netlify', 'dist'])]
        shell_files = [f for f in shell_files if not any(x in str(f) for x in ['node_modules', '.netlify', 'dist'])]
        
        print(f"Found {len(python_files)} Python files and {len(shell_files)} shell scripts")
        
        for f in python_files:
            self.analyze_python_file(f)
        
        for f in shell_files:
            self.analyze_shell_file(f)
        
        self.detect_duplicates()
        self.generate_report()
    
    def analyze_python_file(self, filepath: Path):
        """Analyze a single Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.issues[str(filepath)].append(f"Could not read file: {e}")
            return
        
        lines = content.split('\n')
        stats = {
            'lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'functions': 0,
            'classes': 0,
            'imports': [],
            'complexity_score': 0,
            'issues': []
        }
        
        # Parse AST for deeper analysis
        try:
            tree = ast.parse(content)
            self.analyze_ast(tree, stats, filepath, content)
        except SyntaxError as e:
            stats['issues'].append(f"Syntax error: {e}")
        except Exception as e:
            stats['issues'].append(f"Parse error: {e}")
        
        # Check for security issues
        self.check_python_security(filepath, content, stats)
        
        # Check for performance issues
        self.check_python_performance(filepath, content, stats)
        
        # Check documentation
        self.check_python_documentation(filepath, content, stats)
        
        # Check error handling
        self.check_python_error_handling(filepath, content, stats)
        
        self.file_stats[str(filepath)] = stats
    
    def analyze_ast(self, tree: ast.AST, stats: Dict, filepath: Path, content: str):
        """Analyze Python AST for code quality metrics."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stats['functions'] += 1
                # Calculate cyclomatic complexity
                complexity = self.calculate_complexity(node)
                stats['complexity_score'] += complexity
                if complexity > 10:
                    stats['issues'].append(f"High complexity function '{node.name}' (score: {complexity})")
                
                # Check for missing docstrings
                if not ast.get_docstring(node):
                    stats['issues'].append(f"Function '{node.name}' missing docstring")
                    
            elif isinstance(node, ast.ClassDef):
                stats['classes'] += 1
                if not ast.get_docstring(node):
                    stats['issues'].append(f"Class '{node.name}' missing docstring")
                    
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    stats['imports'].append(alias.name)
            
            elif isinstance(node, ast.Try):
                # Check for bare except clauses
                for handler in node.handlers:
                    if handler.type is None:
                        stats['issues'].append("Bare 'except:' clause found - should catch specific exceptions")
    
    def calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler,
                                ast.With, ast.Assert, ast.comprehension)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def check_python_security(self, filepath: Path, content: str, stats: Dict):
        """Check for security vulnerabilities in Python code."""
        security_patterns = [
            (r'eval\s*\(', "Use of eval() - dangerous code execution"),
            (r'exec\s*\(', "Use of exec() - dangerous code execution"),
            (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "subprocess with shell=True - injection risk"),
            (r'os\.system\s*\(', "os.system() - command injection risk"),
            (r'input\s*\(', "Use of input() - consider security implications"),
            (r'\.format\s*\([^)]*%', "String formatting with % - potential injection"),
            (r'f["\'].*\{.*\}.*["\'].*\.format', "Possible format string confusion"),
            (r'tempfile\.(mktemp|TemporaryFile)', "Insecure temporary file usage"),
            (r'pickle\.(loads|load)', "pickle usage - can execute arbitrary code"),
            (r'yaml\.load\s*\([^)]*\)', "yaml.load without Loader - unsafe"),
            (r'hashlib\.md5', "MD5 is cryptographically broken"),
            (r'hashlib\.sha1', "SHA1 is cryptographically weak"),
            (r'ssl\.PROTOCOL_SSLv[23]', "Outdated SSL protocol"),
            (r'urllib\.urlopen', "urllib without verification - use requests with verify"),
            (r'requests\.(get|post)\s*\([^)]*verify\s*=\s*False', "SSL verification disabled"),
            (r'debug\s*=\s*True', "Debug mode enabled - security risk in production"),
            (r'secret[_\s]*=\s*["\'][^"\']+["\']', "Hardcoded secret detected"),
            (r'password[_\s]*=\s*["\'][^"\']+["\']', "Hardcoded password detected"),
            (r'api[_\s]*key[_\s]*=\s*["\'][^"\']+["\']', "Hardcoded API key detected"),
            (r'token[_\s]*=\s*["\'][^"\']+["\']', "Hardcoded token detected"),
        ]
        
        for pattern, message in security_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issue = f"SECURITY: {message}"
                stats['issues'].append(issue)
                self.security_issues.append({
                    'file': str(filepath),
                    'issue': message,
                    'severity': 'HIGH' if 'eval' in message or 'exec' in message or 'shell=True' in message else 'MEDIUM'
                })
    
    def check_python_performance(self, filepath: Path, content: str, stats: Dict):
        """Check for performance issues in Python code."""
        performance_patterns = [
            (r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', "Using range(len()) - use enumerate() instead"),
            (r'\.append\s*\([^)]+\)\s*\n\s*for\s+', "List building in loop - use list comprehension"),
            (r'str\s*\(\s*\)\s*\.join\s*\(', "String concatenation in loop - inefficient"),
            (r'readlines\s*\(\s*\)', "readlines() loads entire file - consider iteration"),
            (r'\.read\s*\(\s*\)', "read() loads entire file - consider chunked reading"),
            (r'sqlite3.*execute\s*\([^)]+\)\s*\n\s*for\s+', "SQL in loop - use executemany()"),
            (r'requests\.(get|post).*for\s+', "HTTP requests in loop - consider batching/async"),
            (r'time\.sleep\s*\(\s*0\.001', "Very short sleep - busy waiting pattern"),
            (r'while\s+True\s*:\s*\n\s*if', "Busy loop pattern - consider events"),
            (r'global\s+\w+', "Global variable usage - consider encapsulation"),
            (r'\.sort\s*\(\s*\).*\.sort\s*\(\s*\)', "Multiple sorts - inefficient"),
            (r're\.compile.*inside.*def', "Regex compilation inside function - compile once outside"),
        ]
        
        for pattern, message in performance_patterns:
            if re.search(pattern, content):
                stats['issues'].append(f"PERFORMANCE: {message}")
                self.performance_issues.append({
                    'file': str(filepath),
                    'issue': message
                })
    
    def check_python_documentation(self, filepath: Path, content: str, stats: Dict):
        """Check for documentation gaps in Python code."""
        lines = content.split('\n')
        
        # Check module docstring
        if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
            if len(lines) > 20:  # Only flag larger files
                stats['issues'].append("DOCUMENTATION: Missing module docstring")
                self.documentation_gaps.append({
                    'file': str(filepath),
                    'type': 'Missing module docstring'
                })
        
        # Check for TODO/FIXME comments (might indicate incomplete work)
        todo_count = len(re.findall(r'#\s*(TODO|FIXME|XXX|HACK)', content, re.IGNORECASE))
        if todo_count > 0:
            stats['issues'].append(f"DOCUMENTATION: {todo_count} TODO/FIXME comments found")
    
    def check_python_error_handling(self, filepath: Path, content: str, stats: Dict):
        """Check for missing error handling in Python code."""
        # Check for file operations without try/except
        file_patterns = [
            r'open\s*\([^)]+\)\s*\n(?!\s*try)',
            r'\.read\s*\(\s*\)(?!\s*except)',
            r'\.write\s*\([^)]+\)(?!\s*except)',
        ]
        
        # Check for network operations without error handling
        network_patterns = [
            r'requests\.(get|post|put|delete)',
            r'urllib\.request\.urlopen',
            r'http\.client\.HTTPConnection',
        ]
        
        # Check for database operations without error handling
        db_patterns = [
            r'\.execute\s*\(',
            r'\.commit\s*\(',
        ]
        
        # Simple heuristic: check if file has try/except blocks
        has_try_except = 'try:' in content and 'except' in content
        
        for pattern in file_patterns + network_patterns + db_patterns:
            if re.search(pattern, content) and not has_try_except:
                if len(content.split('\n')) > 30:  # Only flag substantial files
                    issue = f"Missing error handling for I/O or network operations"
                    if issue not in stats['issues']:
                        stats['issues'].append(f"ERROR HANDLING: {issue}")
                        self.error_handling_issues.append({
                            'file': str(filepath),
                            'issue': 'Missing try/except for I/O or network operations'
                        })
                    break
    
    def analyze_shell_file(self, filepath: Path):
        """Analyze a shell script file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.issues[str(filepath)].append(f"Could not read file: {e}")
            return
        
        lines = content.split('\n')
        stats = {
            'lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'functions': len(re.findall(r'^[\w_]+\s*\(\s*\)\s*\{', content, re.MULTILINE)),
            'issues': []
        }
        
        # Check for security issues
        self.check_shell_security(filepath, content, stats)
        
        # Check for error handling
        self.check_shell_error_handling(filepath, content, stats)
        
        # Check for best practices
        self.check_shell_best_practices(filepath, content, stats)
        
        self.file_stats[str(filepath)] = stats
    
    def check_shell_security(self, filepath: Path, content: str, stats: Dict):
        """Check for security issues in shell scripts."""
        security_patterns = [
            (r'eval\s+', "Use of eval - dangerous"),
            (r'\$\([^)]*\`', "Command substitution with backticks - use $() instead"),
            (r'rm\s+-rf\s+/', "Dangerous rm -rf / pattern"),
            (r'curl\s+[^|]*\|\s*(ba)?sh', "Piping curl to shell - dangerous"),
            (r'wget\s+[^|]*\|\s*(ba)?sh', "Piping wget to shell - dangerous"),
            (r'chmod\s+777', "Overly permissive chmod 777"),
            (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
            (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
            (r'api[_\s]*key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        ]
        
        for pattern, message in security_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                stats['issues'].append(f"SECURITY: {message}")
                self.security_issues.append({
                    'file': str(filepath),
                    'issue': message,
                    'severity': 'HIGH' if 'eval' in message or 'rm -rf' in message else 'MEDIUM'
                })
    
    def check_shell_error_handling(self, filepath: Path, content: str, stats: Dict):
        """Check for error handling in shell scripts."""
        # Check for set -e or set -o errexit
        if not re.search(r'set\s+-[euo]+', content) and not re.search(r'set\s+-o\s+(errexit|nounset|pipefail)', content):
            stats['issues'].append("ERROR HANDLING: Missing 'set -e' or error handling options")
            self.error_handling_issues.append({
                'file': str(filepath),
                'issue': "Missing 'set -e' for error handling"
            })
        
        # Check for command error checking
        if not re.search(r'if\s+\[\s*\$\?\s*-ne\s*0', content) and not re.search(r'\|\|\s*exit', content):
            if len(content.split('\n')) > 20:  # Only flag substantial scripts
                stats['issues'].append("ERROR HANDLING: No explicit command error checking")
    
    def check_shell_best_practices(self, filepath: Path, content: str, stats: Dict):
        """Check for shell best practices."""
        # Check for shebang
        if not content.startswith('#!'):
            stats['issues'].append("DOCUMENTATION: Missing shebang line")
        
        # Check for unquoted variables
        unquoted_vars = re.findall(r'\$\w+(?!\w|[^\s"])', content)
        if len(unquoted_vars) > 5:
            stats['issues'].append(f"BEST PRACTICE: {len(unquoted_vars)} potentially unquoted variable usages")
        
        # Check for documentation
        if len(content.split('\n')) > 30:
            comment_lines = len([l for l in content.split('\n') if l.strip().startswith('#')])
            if comment_lines < 3:
                stats['issues'].append("DOCUMENTATION: Script lacks comments")
                self.documentation_gaps.append({
                    'file': str(filepath),
                    'type': 'Insufficient comments'
                })
    
    def detect_duplicates(self):
        """Detect duplicate code patterns across files."""
        # Simple duplicate detection based on function signatures and imports
        function_sigs = defaultdict(list)
        import_patterns = defaultdict(list)
        
        for filepath, stats in self.file_stats.items():
            if filepath.endswith('.py'):
                # Track import patterns
                for imp in stats.get('imports', []):
                    import_patterns[imp].append(filepath)
        
        # Find files with identical import patterns (potential duplication)
        for imp, files in import_patterns.items():
            if len(files) > 3:  # Same import in many files
                self.duplicate_patterns[f"Common import: {imp}"] = files[:5]
    
    def generate_report(self):
        """Generate comprehensive analysis report."""
        report = []
        report.append("# System-Wide Code Quality Analysis Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Workspace:** {self.base_path}")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        report.append("")
        
        total_files = len(self.file_stats)
        total_issues = sum(len(s['issues']) for s in self.file_stats.values())
        files_with_issues = sum(1 for s in self.file_stats.values() if s['issues'])
        
        report.append(f"- **Total files analyzed:** {total_files}")
        report.append(f"- **Files with issues:** {files_with_issues} ({files_with_issues/total_files*100:.1f}%)")
        report.append(f"- **Total issues found:** {total_issues}")
        report.append(f"- **Security issues:** {len(self.security_issues)}")
        report.append(f"- **Performance issues:** {len(self.performance_issues)}")
        report.append(f"- **Documentation gaps:** {len(self.documentation_gaps)}")
        report.append(f"- **Error handling issues:** {len(self.error_handling_issues)}")
        report.append("")
        
        # Priority Matrix
        report.append("## Priority Matrix")
        report.append("")
        report.append("| Priority | Category | Count | Action Required |")
        report.append("|----------|----------|-------|-----------------|")
        report.append(f"| 🔴 CRITICAL | Security Vulnerabilities | {len([i for i in self.security_issues if i.get('severity') == 'HIGH'])} | Immediate fix required |")
        report.append(f"| 🟠 HIGH | Error Handling | {len(self.error_handling_issues)} | Fix within 1 week |")
        report.append(f"| 🟡 MEDIUM | Performance Issues | {len(self.performance_issues)} | Address in next sprint |")
        report.append(f"| 🟢 LOW | Documentation Gaps | {len(self.documentation_gaps)} | Address when convenient |")
        report.append("")
        
        # Security Issues
        if self.security_issues:
            report.append("## 🔴 Security Vulnerabilities")
            report.append("")
            report.append("| File | Issue | Severity |")
            report.append("|------|-------|----------|")
            for issue in sorted(self.security_issues, key=lambda x: x['severity'], reverse=True)[:30]:
                file_short = issue['file'].replace(str(self.base_path), '')
                report.append(f"| {file_short} | {issue['issue']} | {issue.get('severity', 'MEDIUM')} |")
            report.append("")
        
        # Error Handling Issues
        if self.error_handling_issues:
            report.append("## 🟠 Error Handling Issues")
            report.append("")
            report.append("| File | Issue |")
            report.append("|------|-------|")
            for issue in self.error_handling_issues[:30]:
                file_short = issue['file'].replace(str(self.base_path), '')
                report.append(f"| {file_short} | {issue['issue']} |")
            report.append("")
        
        # Performance Issues
        if self.performance_issues:
            report.append("## 🟡 Performance Bottlenecks")
            report.append("")
            report.append("| File | Issue |")
            report.append("|------|-------|")
            for issue in self.performance_issues[:30]:
                file_short = issue['file'].replace(str(self.base_path), '')
                report.append(f"| {file_short} | {issue['issue']} |")
            report.append("")
        
        # Documentation Gaps
        if self.documentation_gaps:
            report.append("## 🟢 Documentation Gaps")
            report.append("")
            report.append("| File | Type |")
            report.append("|------|------|")
            for issue in self.documentation_gaps[:30]:
                file_short = issue['file'].replace(str(self.base_path), '')
                report.append(f"| {file_short} | {issue['type']} |")
            report.append("")
        
        # Code Quality Statistics
        report.append("## Code Quality Statistics")
        report.append("")
        
        # Most complex files
        complex_files = sorted(
            [(f, s) for f, s in self.file_stats.items() if s.get('complexity_score', 0) > 0],
            key=lambda x: x[1].get('complexity_score', 0),
            reverse=True
        )[:15]
        
        if complex_files:
            report.append("### Most Complex Files")
            report.append("")
            report.append("| File | Complexity | Functions | Classes | Lines |")
            report.append("|------|------------|-----------|---------|-------|")
            for filepath, stats in complex_files:
                file_short = filepath.replace(str(self.base_path), '')
                report.append(f"| {file_short} | {stats['complexity_score']} | {stats['functions']} | {stats['classes']} | {stats['lines']} |")
            report.append("")
        
        # Largest files
        largest_files = sorted(
            self.file_stats.items(),
            key=lambda x: x[1]['lines'],
            reverse=True
        )[:15]
        
        report.append("### Largest Files")
        report.append("")
        report.append("| File | Lines | Code | Comments | Blank |")
        report.append("|------|-------|------|----------|-------|")
        for filepath, stats in largest_files:
            file_short = filepath.replace(str(self.base_path), '')
            report.append(f"| {file_short} | {stats['lines']} | {stats['code_lines']} | {stats['comment_lines']} | {stats['blank_lines']} |")
        report.append("")
        
        # Files with most issues
        files_by_issues = sorted(
            [(f, s) for f, s in self.file_stats.items() if s['issues']],
            key=lambda x: len(x[1]['issues']),
            reverse=True
        )[:15]
        
        if files_by_issues:
            report.append("### Files with Most Issues")
            report.append("")
            report.append("| File | Issues |")
            report.append("|------|--------|")
            for filepath, stats in files_by_issues:
                file_short = filepath.replace(str(self.base_path), '')
                report.append(f"| {file_short} | {len(stats['issues'])} |")
            report.append("")
        
        # Duplicate Patterns
        if self.duplicate_patterns:
            report.append("## Potential Code Duplication")
            report.append("")
            for pattern, files in self.duplicate_patterns.items():
                report.append(f"### {pattern}")
                report.append(f"Found in {len(files)} files:")
                for f in files[:5]:
                    report.append(f"- {f.replace(str(self.base_path), '')}")
                report.append("")
        
        # Detailed Issues by File
        report.append("## Detailed Issues by File")
        report.append("")
        
        for filepath, stats in sorted(self.file_stats.items()):
            if stats['issues']:
                file_short = filepath.replace(str(self.base_path), '')
                report.append(f"### {file_short}")
                report.append("")
                for issue in stats['issues'][:10]:  # Limit to 10 issues per file
                    report.append(f"- {issue}")
                if len(stats['issues']) > 10:
                    report.append(f"- ... and {len(stats['issues']) - 10} more issues")
                report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        report.append("")
        report.append("### Immediate Actions (This Week)")
        report.append("")
        report.append("1. **Fix Critical Security Issues**")
        report.append("   - Replace eval()/exec() with safer alternatives")
        report.append("   - Remove hardcoded credentials")
        report.append("   - Enable SSL verification for all HTTP requests")
        report.append("")
        report.append("2. **Add Error Handling**")
        report.append("   - Add try/except blocks around file I/O operations")
        report.append("   - Add 'set -e' to shell scripts")
        report.append("   - Implement proper error logging")
        report.append("")
        report.append("### Short-term Improvements (Next 2 Weeks)")
        report.append("")
        report.append("1. **Refactor Complex Functions**")
        report.append("   - Break down functions with complexity > 10")
        report.append("   - Extract common patterns into reusable functions")
        report.append("")
        report.append("2. **Performance Optimization**")
        report.append("   - Replace string concatenation with join()")
        report.append("   - Use list comprehensions where appropriate")
        report.append("   - Compile regex patterns outside loops")
        report.append("")
        report.append("### Long-term Improvements (Next Month)")
        report.append("")
        report.append("1. **Documentation**")
        report.append("   - Add module docstrings to all files")
        report.append("   - Document all public functions and classes")
        report.append("   - Create README files for complex modules")
        report.append("")
        report.append("2. **Code Organization**")
        report.append("   - Consolidate duplicate code patterns")
        report.append("   - Create shared utility modules")
        report.append("   - Implement consistent coding standards")
        report.append("")
        report.append("3. **Testing**")
        report.append("   - Add unit tests for critical functions")
        report.append("   - Implement integration tests for APIs")
        report.append("   - Set up automated code quality checks")
        report.append("")
        
        # Write report
        report_path = self.base_path / 'brain' / 'reports' / 'system-analysis-2026-02-28.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\nReport saved to: {report_path}")
        return '\n'.join(report)

if __name__ == "__main__":
    analyzer = CodeAnalyzer("/root/.openclaw/workspace")
    analyzer.analyze_all()
