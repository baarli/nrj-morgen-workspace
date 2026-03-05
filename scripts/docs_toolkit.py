#!/usr/bin/env python3
"""
📝 BAARLICLAW DOCS TOOLKIT
Automatisk dokumentasjons-generering
"""

import os
import sys
import re
import ast
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("DocsToolkit")

@dataclass
class FunctionDoc:
    """Function documentation"""
    name: str
    signature: str
    docstring: str
    params: List[Dict[str, str]]
    returns: Optional[str]
    examples: List[str]

@dataclass
class ClassDoc:
    """Class documentation"""
    name: str
    docstring: str
    methods: List[FunctionDoc]
    attributes: List[Dict[str, str]]

@dataclass
class ModuleDoc:
    """Module documentation"""
    name: str
    description: str
    functions: List[FunctionDoc]
    classes: List[ClassDoc]
    constants: List[Dict[str, Any]]

class PythonDocParser:
    """Parse Python files for documentation"""
    
    def parse_file(self, filepath: str) -> Optional[ModuleDoc]:
        """Parse a Python file"""
        try:
            with open(filepath, 'r') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            module_name = Path(filepath).stem
            module_doc = self._get_docstring(tree)
            
            functions = []
            classes = []
            constants = []
            
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    func_doc = self._parse_function(node)
                    if func_doc:
                        functions.append(func_doc)
                
                elif isinstance(node, ast.ClassDef):
                    class_doc = self._parse_class(node)
                    if class_doc:
                        classes.append(class_doc)
                
                elif isinstance(node, ast.Assign):
                    # Constants
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id.isupper():
                                value = self._get_value(node.value)
                                constants.append({
                                    'name': target.id,
                                    'value': value
                                })
            
            return ModuleDoc(
                name=module_name,
                description=module_doc or "",
                functions=functions,
                classes=classes,
                constants=constants
            )
            
        except Exception as e:
            logger.error(f"Failed to parse {filepath}: {e}")
            return None
    
    def _get_docstring(self, node) -> str:
        """Extract docstring from node"""
        docstring = ast.get_docstring(node)
        return docstring or ""
    
    def _parse_function(self, node: ast.FunctionDef) -> Optional[FunctionDoc]:
        """Parse function definition"""
        name = node.name
        if name.startswith('_'):
            return None  # Skip private functions
        
        docstring = self._get_docstring(node)
        signature = self._get_signature(node)
        params = self._get_params(node)
        returns = self._get_return_type(node)
        examples = self._extract_examples(docstring)
        
        return FunctionDoc(
            name=name,
            signature=signature,
            docstring=docstring,
            params=params,
            returns=returns,
            examples=examples
        )
    
    def _parse_class(self, node: ast.ClassDef) -> Optional[ClassDoc]:
        """Parse class definition"""
        name = node.name
        docstring = self._get_docstring(node)
        
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith('_') or item.name == '__init__':
                    func_doc = self._parse_function(item)
                    if func_doc:
                        methods.append(func_doc)
            
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    attr_type = self._get_annotation(item.annotation)
                    attributes.append({
                        'name': item.target.id,
                        'type': attr_type
                    })
        
        return ClassDoc(
            name=name,
            docstring=docstring,
            methods=methods,
            attributes=attributes
        )
    
    def _get_signature(self, node: ast.FunctionDef) -> str:
        """Get function signature"""
        args = []
        
        # Regular args
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._get_annotation(arg.annotation)}"
            args.append(arg_str)
        
        # Defaults
        defaults_start = len(node.args.args) - len(node.args.defaults)
        for i, default in enumerate(node.args.defaults):
            arg_idx = defaults_start + i
            args[arg_idx] += f" = {self._get_value(default)}"
        
        # Return type
        returns = ""
        if node.returns:
            returns = f" -> {self._get_annotation(node.returns)}"
        
        return f"{node.name}({', '.join(args)}){returns}"
    
    def _get_params(self, node: ast.FunctionDef) -> List[Dict[str, str]]:
        """Extract parameter info"""
        params = []
        
        for arg in node.args.args:
            if arg.arg == 'self':
                continue
            
            param_info = {
                'name': arg.arg,
                'type': self._get_annotation(arg.annotation) if arg.annotation else 'Any',
                'description': ''
            }
            params.append(param_info)
        
        return params
    
    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Get return type annotation"""
        if node.returns:
            return self._get_annotation(node.returns)
        return None
    
    def _get_annotation(self, annotation) -> str:
        """Convert annotation to string"""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            value = self._get_annotation(annotation.value)
            slice_val = self._get_annotation(annotation.slice)
            return f"{value}[{slice_val}]"
        elif isinstance(annotation, ast.Constant):
            return repr(annotation.value)
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_annotation(annotation.value)}.{annotation.attr}"
        return str(annotation)
    
    def _get_value(self, node) -> str:
        """Get value from AST node"""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.List):
            return "[]"
        elif isinstance(node, ast.Dict):
            return "{}"
        return "..."
    
    def _extract_examples(self, docstring: str) -> List[str]:
        """Extract examples from docstring"""
        examples = []
        lines = docstring.split('\n')
        in_example = False
        current_example = []
        
        for line in lines:
            if 'example' in line.lower() or '```' in line:
                if in_example and current_example:
                    examples.append('\n'.join(current_example))
                    current_example = []
                in_example = not in_example
            elif in_example:
                current_example.append(line.strip())
        
        if current_example:
            examples.append('\n'.join(current_example))
        
        return examples

class MarkdownGenerator:
    """Generate Markdown documentation"""
    
    def generate_module_doc(self, module: ModuleDoc) -> str:
        """Generate Markdown for module"""
        lines = [
            f"# {module.name}",
            "",
            module.description,
            "",
        ]
        
        # Constants
        if module.constants:
            lines.extend([
                "## Constants",
                "",
            ])
            for const in module.constants:
                lines.append(f"- `{const['name']}` = `{const['value']}`")
            lines.append("")
        
        # Functions
        if module.functions:
            lines.extend([
                "## Functions",
                "",
            ])
            for func in module.functions:
                lines.extend(self._generate_function_doc(func))
            lines.append("")
        
        # Classes
        if module.classes:
            lines.extend([
                "## Classes",
                "",
            ])
            for cls in module.classes:
                lines.extend(self._generate_class_doc(cls))
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_function_doc(self, func: FunctionDoc) -> List[str]:
        """Generate function documentation"""
        lines = [
            f"### `{func.signature}`",
            "",
        ]
        
        if func.docstring:
            lines.extend([func.docstring, ""])
        
        if func.params:
            lines.extend([
                "**Parameters:**",
                "",
            ])
            for param in func.params:
                lines.append(f"- `{param['name']}` ({param['type']}) - {param['description']}")
            lines.append("")
        
        if func.returns:
            lines.extend([
                f"**Returns:** `{func.returns}`",
                "",
            ])
        
        if func.examples:
            lines.extend([
                "**Examples:**",
                "",
                "```python",
            ])
            for example in func.examples:
                lines.append(example)
            lines.extend([
                "```",
                "",
            ])
        
        return lines
    
    def _generate_class_doc(self, cls: ClassDoc) -> List[str]:
        """Generate class documentation"""
        lines = [
            f"### class `{cls.name}`",
            "",
        ]
        
        if cls.docstring:
            lines.extend([cls.docstring, ""])
        
        if cls.attributes:
            lines.extend([
                "**Attributes:**",
                "",
            ])
            for attr in cls.attributes:
                lines.append(f"- `{attr['name']}: {attr['type']}`")
            lines.append("")
        
        if cls.methods:
            lines.extend([
                "**Methods:**",
                "",
            ])
            for method in cls.methods:
                lines.append(f"#### `{method.signature}`")
                lines.append("")
                if method.docstring:
                    lines.append(method.docstring)
                    lines.append("")
        
        return lines

class DocsBuilder:
    """Build documentation for a project"""
    
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.parser = PythonDocParser()
        self.generator = MarkdownGenerator()
    
    def build(self):
        """Build all documentation"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Find all Python files
        python_files = list(Path(self.source_dir).rglob("*.py"))
        
        modules = []
        for filepath in python_files:
            if '__pycache__' in str(filepath):
                continue
            
            module = self.parser.parse_file(str(filepath))
            if module:
                modules.append(module)
                
                # Generate individual file doc
                rel_path = filepath.relative_to(self.source_dir)
                doc_path = Path(self.output_dir) / rel_path.with_suffix('.md')
                doc_path.parent.mkdir(parents=True, exist_ok=True)
                
                markdown = self.generator.generate_module_doc(module)
                with open(doc_path, 'w') as f:
                    f.write(markdown)
                
                logger.info(f"Generated: {doc_path}")
        
        # Generate index
        self._generate_index(modules)
        
        logger.info(f"Documentation built: {len(modules)} modules")
    
    def _generate_index(self, modules: List[ModuleDoc]):
        """Generate index file"""
        lines = [
            "# API Documentation",
            "",
            f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Modules",
            "",
        ]
        
        for module in sorted(modules, key=lambda m: m.name):
            lines.append(f"- [{module.name}]({module.name}.md)")
        
        index_path = Path(self.output_dir) / "README.md"
        with open(index_path, 'w') as f:
            f.write('\n'.join(lines))

# === CONVENIENCE FUNCTIONS ===
def quick_doc(filepath: str) -> str:
    """Quick documentation for a file"""
    parser = PythonDocParser()
    module = parser.parse_file(filepath)
    if module:
        generator = MarkdownGenerator()
        return generator.generate_module_doc(module)
    return ""

def generate_project_docs(source: str = ".", output: str = "./docs"):
    """Generate docs for entire project"""
    builder = DocsBuilder(source, output)
    builder.build()

# === TESTING ===
if __name__ == "__main__":
    print("📝 BaarliClaw Docs Toolkit - Testing")
    print("=" * 50)
    
    # Test parsing
    print("\n🧪 Testing parser")
    parser = PythonDocParser()
    
    # Create test file
    test_code = '''
"""Test module for documentation."""

MAX_SIZE = 100

class Calculator:
    """A simple calculator class."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers.
        
        Example:
            calc = Calculator()
            result = calc.add(1, 2)
        """
        return a + b

def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"
'''
    
    test_file = "/tmp/test_module.py"
    with open(test_file, 'w') as f:
        f.write(test_code)
    
    module = parser.parse_file(test_file)
    
    if module:
        print(f"✅ Parsed: {module.name}")
        print(f"✅ Functions: {len(module.functions)}")
        print(f"✅ Classes: {len(module.classes)}")
        print(f"✅ Constants: {len(module.constants)}")
        
        # Generate markdown
        print("\n🧪 Testing markdown generation")
        generator = MarkdownGenerator()
        markdown = generator.generate_module_doc(module)
        print("✅ Generated markdown:")
        print(markdown[:500])
    
    # Cleanup
    os.remove(test_file)
    
    print("\n✅ Docs Toolkit ready!")
