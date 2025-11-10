# Repository Guidelines

## Project Structure & Module Organization
- `src/app` contains Next.js routes, layouts, and route handlers; match new pages to existing segment folders.
- `src/components`, `src/lib`, and `src/hooks` hold shared UI, utilities, and client logic; prefer co-locating types in `src/types`.
- Unit specs live in `src/__tests__`; end-to-end scenarios and fixtures are staged under `03-Tests/e2e`.
- Static assets come from `public`; database schema, migrations, and seeding scripts stay in `prisma`.
- Automation, data movers, and release helpers sit in `05-Scripts`; reuse these instead of ad-hoc shell scripts.

## Build, Test, and Development Commands
- `npm run dev` starts the Next.js dev server with Turbopack; load `/` to verify landing flows.
- `npm run build` and `npm run start` compile and serve the production bundle.
- `npm run lint` enforces the Next.js + TypeScript ESLint ruleset.
- `npm run test:unit`, `npm run test:e2e`, and `npm run test:coverage` execute Vitest specs, Playwright suites, and coverage runs respectively.
- `npm run test:report` re-opens the last Playwright HTML report for UI triage.

## Coding Style & Naming Conventions
- TypeScript is required; keep 2-space indentation and single quotes for imports to match existing files.
- Export React components with `PascalCase` names (e.g., `TeamRosterCard`); helper functions stay `camelCase`.
- Tailwind CSS utility classes drive styling—compose using `cn` helpers in `src/lib`.
- Trust ESLint for lint fixes (`npm run lint -- --fix`) and run `npm run lint` before opening a PR.

## Testing Guidelines
- Extend Vitest suites in `src/__tests__`; name files `<subject>.test.ts(x)` to mirror the component or module.
- For Playwright, add scenarios under `03-Tests/e2e` and tag slow specs with `test.slow` to keep CI timing predictable.
- Before submitting a PR, run `npm run test` locally and attach key diffs from `test-results/` if failures need discussion.
- Use `npm run test:e2e:headed` when debugging flaky UI flows; capture screenshots for regressions in PRs.

## Commit & Pull Request Guidelines
- Follow the existing Conventional Commit pattern: `feat: ...`, `fix: ...`, `chore: ...`, `release: ...`.
- Squash small work-in-progress commits; each final commit should describe the change and the impacted surface area.
- PRs need a summary, linked Linear/GitHub issue (if present), test evidence (`npm run test` output or screenshots), and notes on env/seeding changes.
- Request review from the domain owner listed in `README.md` when touching compliance, auth, or data-model logic.

## Configuration & Secrets
- Maintain environment variables in `.env.local`; regenerate Prisma client with `npx prisma generate` after schema edits.
- Sentry configuration files (`sentry.client.config.ts`, `sentry.server.config.ts`) should include any new instrumentation.
- Never commit secrets; use the shared vault referenced in `06-Infrastructure` for API keys and OAuth credentials.
