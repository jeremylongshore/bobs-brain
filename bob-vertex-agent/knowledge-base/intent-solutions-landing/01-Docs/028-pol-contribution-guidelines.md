# Contributing to Intent Solutions Landing

Thank you for your interest in contributing! This document provides guidelines for contributing to the Intent Solutions landing page project.

## Development Setup

### Prerequisites
- **Bun** (latest version) - https://bun.sh
- **Git**
- **VS Code** (recommended) with extensions from `.vscode/extensions.json`

### Getting Started
```bash
# Clone repository
git clone https://github.com/jeremylongshore/intent-solutions-landing.git
cd intent-solutions-landing

# Install dependencies
bun install

# Start development server
bun run dev

# Open browser to http://localhost:8080
```

## Project Structure
See `00-CLAUDE.md` for complete project architecture.

## Code Style

### TypeScript/TSX
- Use TypeScript for all new code
- Prefer functional components with hooks
- Use explicit types (avoid `any`)
- Follow React best practices

### Styling
- Use Tailwind CSS utility classes
- Use `cn()` helper from `@/lib/utils` for conditional classes
- Follow mobile-first responsive design

### Naming Conventions
- Components: PascalCase (`Button.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)

## Commit Messages

Follow Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(ui): add contact form component
fix(nav): correct mobile menu toggle
docs: update architecture documentation
```

## Pull Request Process

1. **Create feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following code style guidelines

3. **Test your changes**:
   ```bash
   bun run build        # Verify production build
   bun run preview      # Test production build locally
   ```

4. **Commit with conventional commits**

5. **Push to GitHub**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open Pull Request** with:
   - Clear description of changes
   - Screenshots (for UI changes)
   - Related issue number (if applicable)

7. **Wait for review** - PRs require 1 approval

## Testing (Future)

When test infrastructure is added:
```bash
bun test             # Run all tests
bun test:watch       # Run tests in watch mode
bun test:coverage    # Generate coverage report
```

Target: 80% code coverage

## Documentation

- Update `00-CLAUDE.md` for architectural changes
- Update `01-README.md` for user-facing changes
- Add ADRs in `docs/ADRs/` for significant decisions
- Update `06-CHANGELOG.md` with notable changes

## Code Review Guidelines

### For Contributors
- Keep PRs small and focused (< 400 lines changed)
- Write clear PR descriptions
- Respond to feedback promptly
- Ensure CI passes (when implemented)

### For Reviewers
- Review within 48 hours
- Be constructive and kind
- Focus on code quality, not style (autoformat handles that)
- Approve when confident changes are safe

## Getting Help

- **Project Documentation**: See `00-CLAUDE.md`
- **Troubleshooting**: See `09-TROUBLESHOOTING.md`
- **Security Issues**: See `10-SECURITY.md` (DO NOT open public issues)
- **Questions**: Open a GitHub Discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see `03-LICENSE.md`).

---
**Last Updated**: October 4, 2025
