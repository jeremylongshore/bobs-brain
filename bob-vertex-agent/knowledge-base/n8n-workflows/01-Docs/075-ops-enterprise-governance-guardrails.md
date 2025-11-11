# N8N Enterprise Governance & Guardrails

Short answer: you've got creation and basic sync. Missing are guardrails, promotion, and runtime safety. Add these.

## Gaps to close

### Governance & catalog
- **Ownership map**: `/catalog/index.yml` with workflow → owners, Slack channel, SLA, data sensitivity.
- **CODEOWNERS per folder**: `workflows/<name>/` → responsible team.
- **Lifecycle states**: draft → staging → prod. Label in meta.yml.

### Build & test
- **Schema + lint rules**: custom JSON Schema for nodes you allow; fail on disallowed ones.
- **Fixtures & mocks**: `tests/fixtures/*.json` for sample payloads; `tests/mock-http.sh` to stub APIs.
- **Smoke runner**: `ops/smoke.sh workflows/<name>` loads + dry-runs critical paths.
- **Chaos/rate-limit check**: `ops/chaos.sh` simulates 429/500 and asserts graceful failure.

### Promotion (dev → staging → prod)
- **Env overlays**: `env/dev.env`, `env/stage.env`, `env/prod.env` with credential IDs and URLs.
- **Promote script**: `ops/promote.sh <name> <env>` swaps env vars and imports to target.
- **Change approval**: required review on folders via CODEOWNERS; PR label ready-for-prod gate.

### Secrets & credentials
- **Credential map**: `/catalog/credentials.yml` listing required keys per workflow and least-priv scopes.
- **Rotation runbook**: `/docs/ROTATION.md` with rotate/test/rollback steps.
- **Secret checks**: CI job that blocks if placeholders like sk-live appear in JSON.

### Deploy & rollback
- **Tag + artifact**: `ops/package.sh <name>` → `dist/<name>-<version>.zip` of the workflow folder.
- **Selective rollback**: `ops/rollback.sh <name> <tag>` re-imports prior packaged version.
- **Diff deploy**: you have this; extend to support per-env diffs (`--env prod`).

### Runtime safety
- **Idempotency keys**: convention in nodes writing externally; document in each meta.yml.
- **Dedup filter**: pre-step node pattern to drop duplicates on a stable key.
- **Timeouts/retries**: standardized retry/timeout defaults; CI fails if unset.

### Observability
- **Run logs export**: ship n8n logs to Loki/ELK; per-workflow labels.
- **Healthchecks**: synthetic pings for key webhooks; alerting thresholds.
- **Error budgets**: per workflow SLA in index.yml; alert when burning too fast.

### Cost & quotas
- **Rate-limit policy**: `docs/RATE_LIMITS.md` with provider caps and safe concurrency.
- **Kill switches**: env-driven flags to disable flows during incidents.

### Docs & DX
- **Per-workflow README.md**: input → process → output, dependencies, sample event.
- **Scaffold command**: `ops/new-workflow.sh <name>` creates folder with templates.
- **Human CLI**: `ops/cli.sh` with subcommands: new, test, package, promote, rollback.

## Minimal files to add

```
catalog/index.yml
catalog/credentials.yml
env/dev.env
env/stage.env
env/prod.env
ops/new-workflow.sh
ops/promote.sh
ops/package.sh
ops/rollback.sh
ops/smoke.sh
ops/chaos.sh
tests/fixtures/*.json
docs/ROTATION.md
docs/RATE_LIMITS.md
```

## CI upgrades
- **ci-schema.yml**: validate against your JSON Schema.
- **ci-secrets.yml**: grep ban for tokens.
- **ci-smoke.yml**: run `ops/smoke.sh` on changed workflows.
- **ci-release.yml**: on tag, build `dist/*.zip` and attach to GitHub Release.

If you want, I'll output these files' exact contents in one shot so you can drop them into the factory.