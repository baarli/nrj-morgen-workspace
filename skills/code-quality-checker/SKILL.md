# Code Quality Checker

## Overview
Systematisk kodekvalitetsjekk for alle scripts i workspace. Sikrer konsistent kodekvalitet, dokumentasjon og vedlikeholdbarhet.

## Capabilities

### 1. Python Code Analysis
- Syntax checking
- Import validation
- Function documentation check
- Variable naming conventions
- Code complexity analysis

### 2. Shell Script Analysis
- Syntax validation
- Best practice checking
- Error handling verification
- Portability checks

### 3. HTML/CSS Analysis
- Valid HTML structure
- CSS best practices
- Accessibility checks
- Performance hints

### 4. Reporting
- Quality score per file
- Issue categorization (critical/warning/info)
- Trend tracking over time
- Recommendations for improvement

## Usage

### Check Single File
```bash
./skills/code-quality-checker/check-quality.sh path/to/file.py
```

### Check All Scripts
```bash
./skills/code-quality-checker/check-quality.sh --all
```

### Generate Report
```bash
./skills/code-quality-checker/check-quality.sh --report
```

### Check Specific Type
```bash
./skills/code-quality-checker/check-quality.sh --type python
./skills/code-quality-checker/check-quality.sh --type bash
./skills/code-quality-checker/check-quality.sh --type html
```

## Quality Rules

### Python Rules (rules/python.rules)
- Functions must have docstrings
- Maximum 50 lines per function
- No unused imports
- Variable names: snake_case
- Class names: PascalCase
- Maximum file length: 500 lines

### Bash Rules (rules/bash.rules)
- Use `#!/bin/bash` shebang
- Quote all variables
- Check for `set -e` or error handling
- No hardcoded paths
- Functions should have comments

### HTML Rules (rules/html.rules)
- Valid DOCTYPE
- Proper nesting
- Alt attributes on images
- Semantic HTML elements

## Output Format

```
╔════════════════════════════════════════════════════════╗
║           CODE QUALITY REPORT - 2026-02-27            ║
╠════════════════════════════════════════════════════════╣
║ Files Checked: 47                                      ║
║ Overall Score: 87/100                                  ║
║ Critical Issues: 2                                     ║
║ Warnings: 12                                           ║
║ Info: 23                                               ║
╠════════════════════════════════════════════════════════╣
║ Top Issues:                                            ║
║ 1. Missing docstrings (8 files)                        ║
║ 2. Lines too long (5 files)                            ║
║ 3. Unused imports (2 files)                            ║
╚════════════════════════════════════════════════════════╝
```

## Integration

### Pre-commit Hook
Add to git hooks for automatic checking before commits.

### CI/CD Integration
Run as part of automated testing pipeline.

### Scheduled Checks
Run weekly via cron to track quality trends.

## Success Metrics

- Average quality score > 85/100
- Zero critical issues
- < 10 warnings per 1000 lines
- 100% of new code passes checks
