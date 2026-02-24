# Contributing to Mission Control

Thank you for your interest in contributing to Mission Control! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- A code editor (VS Code recommended)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/baarliclaw/mission-control.git
cd mission-control

# Install Python dependencies
pip install -r api/requirements.txt

# Start the backend API
cd api
python3 total-control-api.py

# In a new terminal, start the frontend
cd public
python3 -m http.server 8888
```

## 📋 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add comments where necessary
- Update documentation

### 3. Test Your Changes
```bash
# Run API tests
cd api
python3 test-api.py

# Test frontend manually
open http://localhost:8888
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings
- Maximum line length: 100

### JavaScript
- Use ES6+ features
- Prefer const/let over var
- Use async/await for async operations
- Comment complex logic

### HTML/CSS
- Use semantic HTML
- BEM naming for CSS classes
- Mobile-first responsive design
- Dark theme consistency

## 🧪 Testing

### Unit Tests
```bash
cd api
python3 -m pytest test-api.py -v
```

### Integration Tests
```bash
# Test API endpoints
curl http://localhost:8081/api/status
curl http://localhost:8081/api/system/resources
```

### Manual Testing
- Test on different browsers
- Test on mobile devices
- Test offline mode
- Test WebSocket reconnection

## 📚 Documentation

- Update README.md if needed
- Add JSDoc comments for functions
- Update API documentation
- Add examples for new features

## 🐛 Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Browser/OS information

## 💡 Feature Requests

When requesting features:
- Describe the use case
- Explain the benefits
- Consider implementation complexity
- Be open to discussion

## 🏷️ Commit Message Format

We follow conventional commits:

```
feat: add new feature
fix: fix a bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

## 🎨 Design Guidelines

### Colors
- Primary: #667eea (purple)
- Secondary: #764ba2 (dark purple)
- Success: #10b981 (green)
- Warning: #f59e0b (orange)
- Danger: #ef4444 (red)
- Background: #0f172a (dark)

### Typography
- Headings: system-ui, sans-serif
- Body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- Monospace: 'Fira Code', monospace

### Icons
- Use Font Awesome 6
- Consistent sizing (16px, 20px, 24px)
- Meaningful icon choices

## 🔒 Security

- Never commit API keys
- Use environment variables
- Validate all inputs
- Sanitize user data
- Follow OWASP guidelines

## 📞 Contact

- GitHub Issues: [github.com/baarliclaw/mission-control/issues](https://github.com/baarliclaw/mission-control/issues)
- Email: niklasbaarli@gmail.com

## 🙏 Thank You!

Your contributions make Mission Control better for everyone!
