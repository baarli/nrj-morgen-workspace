---
name: code
description: General coding patterns, best practices, and language-specific guidance. Use when writing code in any language, debugging, refactoring, or optimizing. Includes patterns for JavaScript, Python, Bash, and more.
---

# Code Skill

**Master Principles:** [PRINCIPLES.md](/root/.openclaw/workspace/PRINCIPLES.md)  
*This skill embodies: "Software is craft" and "Do thoughtful work"*

## Philosophy

Code is not just logic. It is **structure, elegance, and intention**.

When I write code, I follow these principles from [SOUL.md](/root/.openclaw/workspace/SOUL.md):
- **Elegance > Functionality** - Working code is not enough; it must be clean
- **Clarity > Cleverness** - Code should be understandable in 6 months
- **Craftsmanship matters** - Quality is not accidental

## When to Use

- Writing new code
- Debugging existing code
- Refactoring
- Code review
- Optimization
- Learning a new language

## Universal Principles

### 1. DRY (Don't Repeat Yourself)
```javascript
// BAD: Repeated code
function getUserName(user) {
  if (user && user.profile && user.profile.name) {
    return user.profile.name;
  }
  return 'Anonymous';
}

function getUserEmail(user) {
  if (user && user.profile && user.profile.email) {
    return user.profile.email;
  }
  return 'no-email';
}

// GOOD: Reusable pattern
function getNested(obj, path, defaultValue) {
  return path.split('.').reduce((acc, part) => 
    acc && acc[part] ? acc[part] : defaultValue, obj);
}
```

### 2. Single Responsibility
```python
# BAD: Multiple responsibilities
def process_user_data(user):
    # Validate
    if not user.get('email'):
        raise ValueError('Email required')
    
    # Transform
    user['email'] = user['email'].lower()
    
    # Save
    db.save(user)
    
    # Notify
    send_email(user['email'], 'Welcome!')

# GOOD: Separated concerns
def validate_user(user):
    if not user.get('email'):
        raise ValueError('Email required')
    return user

def normalize_user(user):
    user['email'] = user['email'].lower()
    return user

def save_user(user):
    db.save(user)

def notify_user(user):
    send_email(user['email'], 'Welcome!')
```

### 3. Error Handling
```javascript
// BAD: Silent failure
function parseJSON(str) {
  return JSON.parse(str); // Can throw
}

// GOOD: Explicit handling
function parseJSON(str) {
  try {
    return { success: true, data: JSON.parse(str) };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

## Language-Specific Patterns

### JavaScript/TypeScript

#### Async/Await
```javascript
// BAD: Callback hell
fetchUser(id, (err, user) => {
  if (err) return handleError(err);
  fetchOrders(user.id, (err, orders) => {
    if (err) return handleError(err);
    processOrders(orders);
  });
});

// GOOD: Async/await
async function getUserOrders(userId) {
  try {
    const user = await fetchUser(userId);
    const orders = await fetchOrders(user.id);
    return processOrders(orders);
  } catch (error) {
    handleError(error);
  }
}
```

#### Destructuring
```javascript
// BAD
const name = user.name;
const email = user.email;

// GOOD
const { name, email } = user;

// With defaults
const { name = 'Anonymous', email = 'N/A' } = user;
```

### Python

#### List Comprehensions
```python
# BAD
squares = []
for x in range(10):
    squares.append(x ** 2)

# GOOD
squares = [x ** 2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
```

#### Context Managers
```python
# BAD
file = open('data.txt', 'r')
data = file.read()
file.close()  # Might not close if error

# GOOD
with open('data.txt', 'r') as file:
    data = file.read()
# Automatically closed
```

### Bash

#### Error Handling
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Check command success
if ! command -v git > /dev/null; then
    echo "Git not installed"
    exit 1
fi

# Or with &&
git pull || { echo "Pull failed"; exit 1; }
```

#### Functions
```bash
# GOOD: Defined before use
main() {
    local name="$1"
    echo "Hello, $name"
}

main "$@"
```

## Debugging Patterns

### JavaScript
```javascript
// Quick debug
console.log({ variable });  // Shows { variable: value }

// Conditional breakpoint
if (condition) debugger;

// Performance
console.time('operation');
// ... code ...
console.timeEnd('operation');
```

### Python
```python
# Quick debug
print(f"{variable=}")  # Python 3.8+

# PDB breakpoint
import pdb; pdb.set_trace()

# Or
breakpoint()  # Python 3.7+
```

## Testing Patterns

### Unit Test Structure
```javascript
describe('UserService', () => {
  beforeEach(() => {
    // Setup
  });
  
  afterEach(() => {
    // Cleanup
  });
  
  it('should create user', async () => {
    // Arrange
    const userData = { name: 'John', email: 'john@example.com' };
    
    // Act
    const user = await createUser(userData);
    
    // Assert
    expect(user.name).toBe('John');
    expect(user.email).toBe('john@example.com');
  });
});
```

## Code Review Checklist

- [ ] Does it work correctly?
- [ ] Is it readable?
- [ ] Are there tests?
- [ ] Is error handling adequate?
- [ ] Are there security issues?
- [ ] Is it performant enough?
- [ ] Is it maintainable?

## Related Skills

- `api-gateway` - Backend code patterns
- `frontend-design` - UI code patterns
- `skill-creator` - Creating reusable code
