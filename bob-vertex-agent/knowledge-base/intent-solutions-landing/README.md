# Test Suite

## Structure
- `unit/` - Unit tests for individual functions/components
- `integration/` - Integration tests for feature workflows
- `e2e/` - End-to-end tests for critical user journeys

## Running Tests
```bash
bun test           # All tests
bun test:unit      # Unit tests only
bun test:e2e       # E2E tests only
```

## Coverage Goals
- Unit tests: 80% coverage
- Integration tests: Key workflows covered
- E2E tests: Critical user paths covered

## Future Setup
When ready to implement:
1. Install Vitest: `bun add -d vitest @testing-library/react @testing-library/jest-dom jsdom`
2. Create `vitest.config.ts`
3. Write first test in `unit/`
