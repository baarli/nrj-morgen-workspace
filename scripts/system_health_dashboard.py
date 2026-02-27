#!/usr/bin/env python3
"""
System Health Dashboard - Real-time monitoring of all BaarliClaw systems
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts to path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

class SystemHealthDashboard:
    """Real-time system health monitoring"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.reports_dir = self.workspace / 'brain' / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def check_disk_usage(self):
        """Check disk usage for workspace"""
        try:
            result = subprocess.run(
                ['du', '-sh', str(self.workspace)],
                capture_output=True, text=True
            )
            size = result.stdout.split()[0]
            
            # Check available space
            df = subprocess.run(
                ['df', '-h', str(self.workspace)],
                capture_output=True, text=True
            )
            lines = df.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                available = parts[3] if len(parts) > 3 else 'N/A'
                percent = parts[4] if len(parts) > 4 else 'N/A'
            else:
                available = percent = 'N/A'
                
            return {
                'status': 'healthy' if percent == 'N/A' or int(percent.replace('%', '')) < 80 else 'warning',
                'used': size,
                'available': available,
                'percent': percent
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def count_files(self):
        """Count various file types"""
        stats = {
            'python': 0,
            'shell': 0,
            'markdown': 0,
            'json': 0,
            'html': 0,
            'total': 0
        }
        
        for root, dirs, files in os.walk(self.workspace):
            # Skip node_modules and hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                stats['total'] += 1
                if file.endswith('.py'):
                    stats['python'] += 1
                elif file.endswith('.sh'):
                    stats['shell'] += 1
                elif file.endswith('.md'):
                    stats['markdown'] += 1
                elif file.endswith('.json'):
                    stats['json'] += 1
                elif file.endswith('.html'):
                    stats['html'] += 1
                    
        return stats
    
    def check_git_status(self):
        """Check git repository status"""
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace,
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                return {'status': 'not_git', 'message': 'Not a git repository'}
            
            lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            modified = len([l for l in lines if l.startswith(' M')])
            added = len([l for l in lines if l.startswith('??')])
            deleted = len([l for l in lines if l.startswith(' D')])
            
            return {
                'status': 'clean' if not lines else 'dirty',
                'modified': modified,
                'added': added,
                'deleted': deleted,
                'total_changes': len(lines)
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def check_cron_jobs(self):
        """Check cron job status"""
        try:
            result = subprocess.run(
                ['openclaw', 'cron', 'list'],
                capture_output=True, text=True
            )
            
            # Parse output to count jobs
            lines = result.stdout.split('\n')
            enabled = sum(1 for l in lines if '✅' in l)
            disabled = sum(1 for l in lines if '⏸️' in l)
            errors = sum(1 for l in lines if 'error' in l.lower() or '❌' in l)
            
            return {
                'status': 'healthy' if errors == 0 else 'warning',
                'enabled': enabled,
                'disabled': disabled,
                'errors': errors
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def check_skills(self):
        """Check skills directory"""
        skills_dir = self.workspace / 'skills'
        if not skills_dir.exists():
            return {'status': 'missing', 'count': 0}
        
        skills = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        # Check for SKILL.md in each
        complete = sum(1 for s in skills if (s / 'SKILL.md').exists())
        
        return {
            'status': 'healthy',
            'total': len(skills),
            'complete': complete,
            'incomplete': len(skills) - complete
        }
    
    def check_memory_files(self):
        """Check memory files"""
        memory_dir = self.workspace / 'memory'
        if not memory_dir.exists():
            return {'status': 'missing', 'count': 0}
        
        files = list(memory_dir.glob('*.md'))
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = memory_dir / f'{today}.md'
        
        return {
            'status': 'healthy',
            'total': len(files),
            'today_exists': today_file.exists(),
            'latest': max((f.stat().st_mtime for f in files), default=0)
        }
    
    def generate_report(self):
        """Generate comprehensive health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'details': {}
        }
        
        # Collect all metrics
        report['details']['disk'] = self.check_disk_usage()
        report['details']['files'] = self.count_files()
        report['details']['git'] = self.check_git_status()
        report['details']['cron'] = self.check_cron_jobs()
        report['details']['skills'] = self.check_skills()
        report['details']['memory'] = self.check_memory_files()
        
        # Calculate overall health score
        health_score = 100
        issues = []
        
        if report['details']['disk'].get('status') == 'warning':
            health_score -= 20
            issues.append('Disk usage high')
        
        if report['details']['git'].get('status') == 'dirty':
            health_score -= 10
            issues.append(f"{report['details']['git'].get('total_changes', 0)} uncommitted changes")
        
        if report['details']['cron'].get('errors', 0) > 0:
            health_score -= 15
            issues.append(f"{report['details']['cron']['errors']} cron errors")
        
        if not report['details']['memory'].get('today_exists'):
            health_score -= 5
            issues.append('No memory file for today')
        
        report['summary'] = {
            'health_score': max(0, health_score),
            'status': 'healthy' if health_score >= 80 else 'warning' if health_score >= 50 else 'critical',
            'issues': issues
        }
        
        return report
    
    def save_report(self, report):
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = self.reports_dir / f'system-health-{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def print_report(self, report):
        """Print formatted report"""
        print("=" * 60)
        print("🩺 SYSTEM HEALTH DASHBOARD")
        print("=" * 60)
        print(f"Generated: {report['timestamp']}")
        print()
        
        summary = report['summary']
        status_emoji = {'healthy': '✅', 'warning': '⚠️', 'critical': '🔴'}
        emoji = status_emoji.get(summary['status'], '❓')
        
        print(f"{emoji} Overall Health: {summary['health_score']}/100 ({summary['status'].upper()})")
        
        if summary['issues']:
            print("\n⚠️ Issues Found:")
            for issue in summary['issues']:
                print(f"  • {issue}")
        else:
            print("\n✨ No issues found!")
        
        print("\n📊 Details:")
        print(f"  Disk: {report['details']['disk'].get('used', 'N/A')} used ({report['details']['disk'].get('percent', 'N/A')})")
        print(f"  Files: {report['details']['files']['total']} total ({report['details']['files']['python']} Python, {report['details']['files']['shell']} Shell)")
        print(f"  Git: {report['details']['git'].get('total_changes', 0)} uncommitted changes")
        print(f"  Cron: {report['details']['cron'].get('enabled', 0)} enabled, {report['details']['cron'].get('errors', 0)} errors")
        print(f"  Skills: {report['details']['skills'].get('total', 0)} total")
        print(f"  Memory: {report['details']['memory'].get('total', 0)} files")
        
        print("\n" + "=" * 60)


def main():
    """Main entry point"""
    dashboard = SystemHealthDashboard()
    report = dashboard.generate_report()
    dashboard.print_report(report)
    
    report_file = dashboard.save_report(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    return report['summary']['health_score']


if __name__ == '__main__':
    sys.exit(0 if main() >= 80 else 1)
