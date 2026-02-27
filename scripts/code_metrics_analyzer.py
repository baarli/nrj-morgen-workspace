#!/usr/bin/env python3
"""
Code Metrics Analyzer - Calculate code complexity and quality metrics
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CodeMetricsAnalyzer:
    """Analyze code metrics for quality assessment"""
    
    def __init__(self, workspace_path='/root/.openclaw/workspace'):
        self.workspace = Path(workspace_path)
        self.metrics = defaultdict(dict)
        
    def analyze_python_file(self, file_path):
        """Analyze a Python file for metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            metrics = {
                'total_lines': len(lines),
                'code_lines': 0,
                'blank_lines': 0,
                'comment_lines': 0,
                'functions': 0,
                'classes': 0,
                'imports': 0,
                'complexity_score': 0
            }
            
            for line in lines:
                stripped = line.strip()
                
                if not stripped:
                    metrics['blank_lines'] += 1
                elif stripped.startswith('#'):
                    metrics['comment_lines'] += 1
                else:
                    metrics['code_lines'] += 1
                    
                    # Count functions and classes
                    if re.match(r'^def\s+\w+', stripped):
                        metrics['functions'] += 1
                    elif re.match(r'^class\s+\w+', stripped):
                        metrics['classes'] += 1
                    elif re.match(r'^(import|from)\s+', stripped):
                        metrics['imports'] += 1
            
            # Calculate complexity score (simple heuristic)
            # Based on: lines of code, functions, nesting depth
            nesting_depth = content.count('    ') + content.count('\t')
            metrics['complexity_score'] = (
                metrics['code_lines'] * 0.1 +
                metrics['functions'] * 2 +
                nesting_depth * 0.01
            )
            
            return metrics
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_shell_file(self, file_path):
        """Analyze a shell script for metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            metrics = {
                'total_lines': len(lines),
                'code_lines': 0,
                'blank_lines': 0,
                'comment_lines': 0,
                'functions': 0,
                'complexity_score': 0
            }
            
            for line in lines:
                stripped = line.strip()
                
                if not stripped:
                    metrics['blank_lines'] += 1
                elif stripped.startswith('#'):
                    metrics['comment_lines'] += 1
                else:
                    metrics['code_lines'] += 1
                    
                    # Count functions
                    if re.match(r'^\w+\s*\(\)\s*\{', stripped):
                        metrics['functions'] += 1
            
            # Calculate complexity
            conditionals = content.count('if ') + content.count('elif ') + content.count('case ')
            loops = content.count('for ') + content.count('while ')
            metrics['complexity_score'] = metrics['code_lines'] * 0.1 + conditionals + loops
            
            return metrics
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_workspace(self):
        """Analyze entire workspace"""
        scripts_dir = self.workspace / 'scripts'
        
        if scripts_dir.exists():
            # Python files
            for py_file in scripts_dir.glob('*.py'):
                if not py_file.name.startswith('test_'):
                    self.metrics[str(py_file)] = self.analyze_python_file(py_file)
            
            # Shell files
            for sh_file in scripts_dir.glob('*.sh'):
                self.metrics[str(sh_file)] = self.analyze_shell_file(sh_file)
        
        return self.metrics
    
    def calculate_summary(self):
        """Calculate summary statistics"""
        total_files = len(self.metrics)
        total_lines = sum(m.get('total_lines', 0) for m in self.metrics.values())
        total_code = sum(m.get('code_lines', 0) for m in self.metrics.values())
        total_comments = sum(m.get('comment_lines', 0) for m in self.metrics.values())
        total_functions = sum(m.get('functions', 0) for m in self.metrics.values())
        total_classes = sum(m.get('classes', 0) for m in self.metrics.values() if 'classes' in m)
        
        avg_complexity = sum(m.get('complexity_score', 0) for m in self.metrics.values()) / total_files if total_files > 0 else 0
        
        # Find most complex files
        complex_files = sorted(
            [(f, m.get('complexity_score', 0)) for f, m in self.metrics.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'total_code_lines': total_code,
            'total_comment_lines': total_comments,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'avg_complexity': round(avg_complexity, 2),
            'comment_ratio': round(total_comments / total_code * 100, 2) if total_code > 0 else 0,
            'most_complex_files': complex_files
        }
    
    def generate_report(self):
        """Generate full report"""
        self.analyze_workspace()
        summary = self.calculate_summary()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'files': dict(self.metrics)
        }
        
        return report
    
    def print_report(self, report):
        """Print formatted report"""
        summary = report['summary']
        
        print("\n" + "=" * 70)
        print("📊 CODE METRICS ANALYSIS")
        print("=" * 70)
        
        print(f"\n📁 Summary:")
        print(f"  Total files analyzed: {summary['total_files']}")
        print(f"  Total lines: {summary['total_lines']:,}")
        print(f"  Code lines: {summary['total_code_lines']:,}")
        print(f"  Comment lines: {summary['total_comment_lines']:,}")
        print(f"  Comment ratio: {summary['comment_ratio']}%")
        print(f"  Total functions: {summary['total_functions']}")
        print(f"  Total classes: {summary['total_classes']}")
        print(f"  Average complexity: {summary['avg_complexity']}")
        
        print(f"\n🔥 Most Complex Files:")
        for file_path, complexity in summary['most_complex_files']:
            file_name = Path(file_path).name
            print(f"  {complexity:.1f} - {file_name}")
        
        print("=" * 70)
    
    def save_report(self, report, output_dir='/root/.openclaw/workspace/brain/reports'):
        """Save report to JSON"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = Path(output_dir) / f'code-metrics-{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    analyzer = CodeMetricsAnalyzer()
    
    print("🔍 Analyzing code metrics...")
    report = analyzer.generate_report()
    
    analyzer.print_report(report)
    
    report_file = analyzer.save_report(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0


if __name__ == '__main__':
    exit(main())
