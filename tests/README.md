# Test Suite for Mission Control

Automated testing for all Mission Control features.

## Structure

```
tests/
├── unit/              # Unit tests for individual functions
├── integration/       # Integration tests for workflows
├── e2e/              # End-to-end tests
├── performance/      # Performance tests
└── coverage/         # Coverage reports
```

## Running Tests

```bash
# Run all tests
npm test

# Run specific test suite
npm run test:unit
npm run test:integration
npm run test:e2e

# Run with coverage
npm run test:coverage
```

## Test Framework

- **Jest**: Unit and integration testing
- **Playwright**: E2E browser testing
- **Lighthouse**: Performance auditing

## CI/CD Integration

Tests run automatically on:
- Every commit
- Pull requests
- Daily at 02:00 UTC
