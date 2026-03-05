---
name: javascript-syntax-validator
version: 1.0.0
description: Validate JavaScript syntax in HTML files before deploying. Prevents broken deployments due to syntax errors.
triggers:
  - Before deploying HTML with JavaScript
  - After editing JavaScript in HTML files
  - When user reports "login not working" or similar
  - Before git commit of HTML files
---

# JavaScript Syntax Validator Skill

## Purpose
Prevent deployment of broken JavaScript by validating syntax before committing.

## When to Use
- Before deploying any HTML file containing JavaScript
- After making changes to JavaScript code
- When user reports functionality not working
- Before git commit of HTML/JS files

## Validation Steps

### Step 1: Check Brace Balance
```python
import re

def check_js_syntax(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract JavaScript
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if not script_match:
        return False, "No JavaScript found"
    
    js = script_match.group(1)
    
    # Check braces
    open_braces = js.count('{')
    close_braces = js.count('}')
    
    if open_braces != close_braces:
        return False, f"Unbalanced braces: {open_braces} open, {close_braces} close"
    
    # Check parentheses
    open_parens = js.count('(')
    close_parens = js.count(')')
    
    if open_parens != close_parens:
        return False, f"Unbalanced parentheses: {open_parens} open, {close_parens} close"
    
    return True, "Syntax OK"

# Usage
ok, msg = check_js_syntax('index.html')
print(msg)
```

### Step 2: Verify Key Functions Exist
```python
def verify_functions(file_path, required_functions):
    with open(file_path, 'r') as f:
        content = f.read()
    
    missing = []
    for func in required_functions:
        if f'function {func}' not in content and f'async function {func}' not in content:
            missing.append(func)
    
    return missing

# Usage for Mission Control
required = ['doLogin', 'showApp', 'loadSaker', 'doSearch', 'showToast']
missing = verify_functions('index.html', required)
if missing:
    print(f"Missing functions: {missing}")
```

### Step 3: Test in Browser (Manual)
1. Open browser console (F12)
2. Check for red errors
3. Test key functionality
4. Verify no "is not defined" errors

## Common Mistakes to Avoid

### ❌ Wrong: Empty Function
```javascript
async function doSearch() {

// Next function...
```

### ✅ Right: Complete Function
```javascript
async function doSearch() {
  // Implementation here
  const query = document.getElementById('search-query').value;
  // ... more code
}

// Next function...
```

### ❌ Wrong: Extra Closing Brace
```javascript
function test() {
  if (true) {
    console.log('test');
  }
}  // <-- This closes test()
}  // <-- EXTRA BRACE!
```

### ✅ Right: Balanced Braces
```javascript
function test() {
  if (true) {
    console.log('test');
  }
}  // <-- Only one closing brace
```

## Pre-Deploy Checklist

- [ ] Run brace balance check
- [ ] Verify all required functions exist
- [ ] Check git diff for unexpected changes
- [ ] Test in browser locally if possible
- [ ] Have rollback plan (know which commit to revert to)

## Emergency Fix

If deployment breaks:

```bash
# Immediate rollback
git log --oneline -5  # Find last working commit
git show <commit>:index.html > index.html
git add index.html
git commit -m "Emergency rollback - fix syntax error"
git push origin master
```

## Integration with Workflow

### Before Any JS Edit:
1. `cp index.html index.html.backup.$(date +%Y%m%d_%H%M%S)`

### After Any JS Edit:
1. Run syntax validator
2. Check git diff
3. Deploy
4. Test in browser

### If Syntax Error Found:
1. Don't panic
2. Restore from backup or git
3. Re-apply changes more carefully
4. Validate again
5. Deploy

## Success Criteria

- Zero syntax errors in production
- All key functions working
- No "is not defined" console errors
- Balanced braces and parentheses

## Documentation

- Mission Control: `/root/.openclaw/workspace/mission-control-gh-pages/`
- Backup location: Same directory with `.backup.YYYYMMDD_HHMMSS` suffix
- Git history: `git log --oneline` for rollback