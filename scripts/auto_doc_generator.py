#!/usr/bin/env python3
"""
Auto-Documentation Generator - Automatically generates docs from code
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class AutoDocGenerator:
    """Automatically generates documentation from code files"""
    
    def __init__(self, workspace_path='/root/.openclaw/workspace'):
        self.workspace = Path(workspace_path)
        self.docs_dir = self.workspace / 'docs' / 'auto-generated'
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_python_docstrings(self, file_path):
        """Extract docstrings and function signatures from Python files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            docs = {
                'file': str(file_path),
                'module_docstring': '',
                'functions': [],
                'classes': []
            }
            
            # Extract module docstring
            module_match = re.match(r'^[\'\"]{3}(.+?)[\'\"]{3}', content, re.DOTALL)
            if module_match:
                docs['module_docstring'] = module_match.group(1).strip()
            
            # Extract functions
            func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*([^:]+))?:\s*(?:[\'\"]{3}(.+?)[\'\"]{3})?'
            for match in re.finditer(func_pattern, content, re.DOTALL):
                func_name = match.group(1)
                params = match.group(2).strip()
                return_type = match.group(3) if match.group(3) else 'None'
                docstring = match.group(4) if match.group(4) else ''
                
                docs['functions'].append({
                    'name': func_name,
                    'params': params,
                    'return_type': return_type,
                    'docstring': docstring.strip()[:200] if docstring else ''
                })
            
            # Extract classes
            class_pattern = r'class\s+(\w+)(?:\(([^)]+)\))?:\s*(?:[\'\"]{3}(.+?)[\'\"]{3})?'
            for match in re.finditer(class_pattern, content, re.DOTALL):
                class_name = match.group(1)
                parent = match.group(2) if match.group(2) else 'object'
                docstring = match.group(3) if match.group(3) else ''
                
                docs['classes'].append({
                    'name': class_name,
                    'parent': parent,
                    'docstring': docstring.strip()[:200] if docstring else ''
                })
            
            return docs
        except Exception as e:
            return {'file': str(file_path), 'error': str(e)}
    
    def extract_shell_comments(self, file_path):
        """Extract comments from shell scripts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            docs = {
                'file': str(file_path),
                'description': '',
                'functions': []
            }
            
            # Extract header comments
            lines = content.split('\n')
            header_lines = []
            for line in lines:
                if line.startswith('#') and not line.startswith('#!/') and not line.startswith('# -*-'):
                    header_lines.append(line.lstrip('# '))
                elif line.strip() and not line.startswith('#'):
                    break
            
            docs['description'] = '\n'.join(header_lines[:10])
            
            # Extract function definitions with comments
            func_pattern = r'(?:#\s*(.+?)\n)?^(\w+)\s*\(\)\s*\{'
            for match in re.finditer(func_pattern, content, re.MULTILINE):
                comment = match.group(1) if match.group(1) else ''
                func_name = match.group(2)
                
                docs['functions'].append({
                    'name': func_name,
                    'description': comment
                })
            
            return docs
        except Exception as e:
            return {'file': str(file_path), 'error': str(e)}
    
    def scan_workspace(self):
        """Scan entire workspace for code files"""
        results = {
            'python': [],
            'shell': [],
            'timestamp': datetime.now().isoformat()
        }
        
        scripts_dir = self.workspace / 'scripts'
        if scripts_dir.exists():
            for py_file in scripts_dir.glob('*.py'):
                if not py_file.name.startswith('test_'):
                    docs = self.extract_python_docstrings(py_file)
                    if docs.get('functions') or docs.get('classes'):
                        results['python'].append(docs)
            
            for sh_file in scripts_dir.glob('*.sh'):
                docs = self.extract_shell_comments(sh_file)
                if docs.get('functions') or docs.get('description'):
                    results['shell'].append(docs)
        
        return results
    
    def generate_markdown_docs(self, scan_results):
        """Generate markdown documentation from scan results"""
        output = []
        
        output.append("# Auto-Generated Documentation\n")
        output.append(f"*Generated: {scan_results['timestamp']}*\n")
        output.append(f"*Total Python modules: {len(scan_results['python'])}*\n")
        output.append(f"*Total Shell scripts: {len(scan_results['shell'])}*\n\n")
        
        # Python modules
        output.append("## Python Modules\n")
        for module in sorted(scan_results['python'], key=lambda x: x['file']):
            file_name = Path(module['file']).name
            output.append(f"### {file_name}\n")
            
            if module.get('module_docstring'):
                output.append(f"{module['module_docstring']}\n")
            
            if module.get('classes'):
                output.append("\n**Classes:**\n")
                for cls in module['classes']:
                    output.append(f"- `{cls['name']}` (extends {cls['parent']})\n")
                    if cls['docstring']:
                        output.append(f"  - {cls['docstring']}\n")
            
            if module.get('functions'):
                output.append("\n**Functions:**\n")
                for func in module['functions'][:10]:  # Limit to first 10
                    output.append(f"- `{func['name']}({func['params']}) -> {func['return_type']}`\n")
                    if func['docstring']:
                        output.append(f"  - {func['docstring'][:100]}...\n")
                
                if len(module['functions']) > 10:
                    output.append(f"- ... and {len(module['functions']) - 10} more functions\n")
            
            output.append("\n---\n\n")
        
        # Shell scripts
        output.append("## Shell Scripts\n")
        for script in sorted(scan_results['shell'], key=lambda x: x['file']):
            file_name = Path(script['file']).name
            output.append(f"### {file_name}\n")
            
            if script.get('description'):
                output.append(f"{script['description'][:200]}...\n")
            
            if script.get('functions'):
                output.append("\n**Functions:**\n")
                for func in script['functions'][:5]:
                    output.append(f"- `{func['name']}()`\n")
                    if func['description']:
                        output.append(f"  - {func['description']}\n")
            
            output.append("\n---\n\n")
        
        return ''.join(output)
    
    def generate_json_index(self, scan_results):
        """Generate searchable JSON index"""
        index = {
            'timestamp': scan_results['timestamp'],
            'modules': {},
            'functions': [],
            'classes': []
        }
        
        for module in scan_results['python']:
            file_name = Path(module['file']).stem
            index['modules'][file_name] = {
                'file': module['file'],
                'function_count': len(module.get('functions', [])),
                'class_count': len(module.get('classes', []))
            }
            
            for func in module.get('functions', []):
                index['functions'].append({
                    'name': func['name'],
                    'module': file_name,
                    'params': func['params'],
                    'docstring': func['docstring'][:100]
                })
            
            for cls in module.get('classes', []):
                index['classes'].append({
                    'name': cls['name'],
                    'module': file_name,
                    'parent': cls['parent']
                })
        
        return index
    
    def run(self):
        """Run full documentation generation"""
        print("🔍 Scanning workspace for code files...")
        scan_results = self.scan_workspace()
        
        print(f"📊 Found {len(scan_results['python'])} Python modules")
        print(f"📊 Found {len(scan_results['shell'])} Shell scripts")
        
        print("📝 Generating markdown documentation...")
        markdown = self.generate_markdown_docs(scan_results)
        
        md_file = self.docs_dir / 'code-reference.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"💾 Saved: {md_file}")
        
        print("📇 Generating JSON index...")
        json_index = self.generate_json_index(scan_results)
        
        json_file = self.docs_dir / 'code-index.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_index, f, indent=2)
        print(f"💾 Saved: {json_file}")
        
        # Print summary
        total_funcs = len(json_index['functions'])
        total_classes = len(json_index['classes'])
        
        print("\n" + "=" * 50)
        print("✅ Documentation generation complete!")
        print(f"📚 Total functions documented: {total_funcs}")
        print(f"📚 Total classes documented: {total_classes}")
        print("=" * 50)
        
        return {
            'markdown_file': str(md_file),
            'json_file': str(json_file),
            'stats': {
                'python_modules': len(scan_results['python']),
                'shell_scripts': len(scan_results['shell']),
                'functions': total_funcs,
                'classes': total_classes
            }
        }


def main():
    """Main entry point"""
    generator = AutoDocGenerator()
    result = generator.run()
    return 0


if __name__ == '__main__':
    exit(main())
