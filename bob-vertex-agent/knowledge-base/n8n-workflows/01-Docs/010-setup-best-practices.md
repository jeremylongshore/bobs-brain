# N8N VM Best Practices

Here's a single, opinionated best-practices list for self-hosting n8n on a VM. No options. Just what to do.

## 1) Architecture
- Run Docker Compose: n8n, postgres, reverse proxy (Caddy/Nginx), optional redis for queue mode.
- Bind n8n to localhost only. Internet traffic hits the proxy, not port 5678.
- Use a real domain with TLS. Set N8N_HOST, WEBHOOK_URL, N8N_PROTOCOL=https.

## 2) Secrets & Keys
- Set a strong N8N_ENCRYPTION_KEY before creating credentials. Never rotate casually.
- Store secrets in .env (local only) or your platform's secret store. Never in Git.
- Maintain a .env.example with placeholders. Keep it in the repo.

## 3) Network & OS hardening
- ufw: allow 80/443, restrict SSH to your IPs, disable password SSH.
- Keep the VM lean: auto security updates, fail2ban, time sync (chrony).
- No public 5678. Ever.

## 4) Reverse proxy
- Terminate TLS at the proxy. Upstream to http://n8n:5678.
- Set headers: Host, X-Forwarded-Proto so webhooks and OAuth work.
- Health route: expose /healthz through proxy for uptime checks.

## 5) Database
- Use Postgres with a dedicated volume. Enable daily pg_dump + retention.
- Tune basics: shared_buffers ~25% RAM, max_connections sane (e.g., 100), and SSD storage.

## 6) Backups (test restores)
- Nightly DB dump + weekly n8n data volume snapshot.
- Keep 7–14 days of rotations off-box (object storage).
- Quarterly restore drill. A backup untested is a rumor.

## 7) Workflow lifecycle
- Build in dev (local Docker), export JSON → Git → PR review → import into prod via CLI/API.
- Tag "golden" JSON bundles per release.
- Never edit critical prod workflows live; treat UI edits as hotfixes only.

## 8) CI/CD for workflows
- Lint JSON with jq -e.
- Basic schema check: require .nodes and .connections.
- Optional dry-import stage in CI (spin a temp n8n container, validate import).

## 9) Executions
- Start with EXECUTIONS_MODE=regular.
- Move to queue mode + Redis when: long jobs, concurrency, or UI lag shows up.
- Prune old execution data: EXECUTIONS_DATA_PRUNE=true, EXECUTIONS_DATA_MAX_AGE=168 (hours).

## 10) Observability
- Centralize logs (Vector/Fluent Bit → Loki/CloudWatch). Include proxy + n8n.
- Uptime checks hit /healthz and a sample webhook. Alerts on failures, not vibes.
- Track execution failures rate; alert on trend, not single spikes.

## 11) Upgrades & rollback
- Pin image tags (e.g., n8nio/n8n:1.xx.y) and changelog each upgrade.
- docker compose pull && up -d. Snapshot before. Roll back by previous tag if needed.
- Post-upgrade smoke test: import a small known-good workflow and run it.

## 12) Credentials hygiene
- One service account per integration with least privilege scopes.
- Rotate keys on a schedule. Document rotation runbook (who, where, rollback).

## 13) Performance hygiene
- Prefer fewer, clearer workflows over one mega-graph.
- Externalize heavy compute to dedicated services (functions, workers).
- Cache repeated API calls where safe. Rate-limit defensively.

## 14) Documentation (short, living)
- Root README stays thin: Quickstart, Deploy, Secrets, Support.
- Per-workflow README (3 bullets): input → process → output.
- A RUNBOOK.md for on-call: restart, logs, restore, common errors.

## 15) Security scanning
- Enable image and dependency scans monthly.
- Secret scanning + push protection on your repos.
- Never expose admin endpoints; keep TLS modern, disable weak ciphers.

## 16) Cost and safety rails
- Right-size VM (2 vCPU/4–8 GB RAM is typical start). SSD > CPU for bursty IO.
- Auto-prune Docker images/volumes monthly.
- Quotas on external APIs to prevent bill shock.

## 17) Change control
- One Issue → one PR → one release note.
- Require CI green + reviewer for prod changes.
- Keep a CHANGELOG.md; publish brief notes to /docs or your wiki.

## 18) Disaster recovery target
- RTO: < 60 min, RPO: < 24 hrs (set your own, then test).
- Scripted rebuild: install Docker, pull Compose, restore DB + data, import workflows, validate.

## 19) Access control
- Non-root deploy user. SSH keys only. Short-lived sudo.
- Separate prod and dev credentials; never reuse tokens.

## 20) Learning loop
- Rebuild small public demos: webhook → transform → Slack/Notion.
- After each, write a 5-line debrief: what broke, why, the guard you added.
- Teach once a month: explaining forces clarity.

---

If you want, I can output a starter repo layout (/ops, /workflows, /docs, scripts) with CI, backup scripts, and import/deploy tooling prewired.