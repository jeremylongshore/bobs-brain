# N8N Self-Host Setup Prompt

Short path: run n8n in Docker on your VM behind a reverse proxy, use Postgres, set an encryption key, wire backups, and lock the box.

## 0) Prereqs
- **VM**: 2 vCPU, 4GB RAM, 20GB+ disk.
- **DNS**: n8n.yourdomain.com → VM IP.
- **Ports**: 80/443 open. SSH limited.
- **Install**: Docker, Docker Compose, ufw (or firewalld).

## 1) One-file deploy (Docker Compose)

Create docker-compose.yml and .env in /opt/n8n.

### .env

```bash
# core
N8N_HOST=n8n.yourdomain.com
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_ENCRYPTION_KEY=CHANGE_ME_32+_chars
WEBHOOK_URL=https://n8n.yourdomain.com/
N8N_EDITOR_BASE_URL=https://n8n.yourdomain.com/
N8N_DIAGNOSTICS_ENABLED=false

# executions + logs
EXECUTIONS_MODE=regular          # or queue (needs Redis)
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168      # hours

# db
POSTGRES_USER=n8n
POSTGRES_PASSWORD=strongpass
POSTGRES_DB=n8n
POSTGRES_NON_ROOT_USER=n8n
POSTGRES_NON_ROOT_PASSWORD=strongpass

# timezone
GENERIC_TIMEZONE=America/Chicago
```

### docker-compose.yml

```yaml
version: "3.8"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - n8n_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 10

  n8n:
    image: n8nio/n8n:latest
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=db
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=${N8N_PORT}
      - N8N_PROTOCOL=${N8N_PROTOCOL}
      - N8N_EDITOR_BASE_URL=${N8N_EDITOR_BASE_URL}
      - WEBHOOK_URL=${WEBHOOK_URL}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - EXECUTIONS_MODE=${EXECUTIONS_MODE}
      - EXECUTIONS_DATA_SAVE_ON_SUCCESS=${EXECUTIONS_DATA_SAVE_ON_SUCCESS}
      - EXECUTIONS_DATA_PRUNE=${EXECUTIONS_DATA_PRUNE}
      - EXECUTIONS_DATA_MAX_AGE=${EXECUTIONS_DATA_MAX_AGE}
      - GENERIC_TIMEZONE=${GENERIC_TIMEZONE}
    volumes:
      - n8n_data:/home/node/.n8n
    ports:
      - "127.0.0.1:5678:5678"   # bind local; proxy handles public
    restart: unless-stopped

  proxy:
    image: caddy:2
    ports:
      - "80:80"
      - "443:443"
    environment:
      - ACME_AGREE=true
    volumes:
      - caddy_data:/data
      - caddy_config:/config
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
    restart: unless-stopped

volumes:
  n8n_db:
  n8n_data:
  caddy_data:
  caddy_config:
```

### Caddyfile

```
${N8N_HOST} {
  encode gzip
  reverse_proxy n8n:5678
}
```

### Bring it up:

```bash
sudo ufw allow 80,443/tcp
sudo ufw allow from <your-ip> to any port 22 proto tcp
sudo ufw enable
docker compose up -d
```

## 2) First-run checklist
- Visit https://n8n.yourdomain.com → create owner account.
- Set up SMTP (Settings → Email) if you want notifications.
- Create first credential and one workflow. Trigger test.

**Pro-tip**: set N8N_ENCRYPTION_KEY before creating any credentials. Changing it later makes stored creds unreadable.

## 3) Webhooks and callbacks
- Use WEBHOOK_URL=https://n8n.yourdomain.com/.
- OAuth apps (Google, Slack, etc.): set callback to your n8n URL per node docs.
- If testing behind NAT without DNS, use Cloudflare Tunnel or ssh -R for a temporary public URL.

## 4) Backups
- **Postgres**: nightly dump.

```bash
docker exec -t $(docker ps -qf name=_db_) pg_dump -U n8n n8n | gzip > /opt/n8n/backups/db-$(date +%F).sql.gz
```

- **App data**: /home/node/.n8n volume. Snapshot it weekly.
- Keep 7–14 days. Test restore quarterly. Future you will send a fruit basket.

## 5) Updates / rollback

```bash
docker compose pull n8n
docker compose up -d
# rollback if needed
docker compose pull n8n:previous && docker compose up -d
```

Pin to a tag if you want slower change: n8nio/n8n:1.64.0 for example.

## 6) Hardening
- Create a non-root deploy user. Limit sudo.
- Fail2ban or CrowdSec for SSH.
- ufw default deny inbound. Only 80/443 open.
- Turn on automatic security updates (Ubuntu: unattended-upgrades).
- Keep VM time in sync (chrony). Schedules hate drift.

## 7) Scaling knobs
- Heavy workloads → switch to EXECUTIONS_MODE=queue and add Redis + a separate n8n-worker service.
- Push long tasks to worker; keep editor responsive.
- Use Postgres outside the VM if you need HA later.

### Compose diff for queue mode:

```yaml
  redis:
    image: redis:7
    restart: unless-stopped

  n8n:
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis

  n8n-worker:
    image: n8nio/n8n:latest
    depends_on: [redis, db]
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      # repeat DB + N8N_* envs same as n8n
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped
```

## 8) Logging and metrics
- `docker logs n8n -f` for quick triage.
- Ship logs: Vector/Fluent Bit → Loki or CloudWatch.
- Health: add Uptime-Kuma/Healthchecks to ping /healthz via proxy route:
- Caddy snippet: `handle_path /healthz { reverse_proxy n8n:5678 }`

## 9) Cost/ops tips
- Postgres on same VM is fine up to a few million executions.
- SSD > HDD. IOPS matter more than raw CPU for bursts.
- Snapshots before upgrades. Rollbacks are cheap insurance.

## 10) Common pitfalls
- **502/SSL loop**: proxy points to http://n8n:5678; do not use HTTPS upstream.
- **Creds don't save**: missing N8N_ENCRYPTION_KEY.
- **Webhooks 404**: wrong WEBHOOK_URL or proxy not forwarding.
- **Large JSON bodies**: add `reverse_proxy … { header_up Host {host} }` if your proxy strips headers.

---

If you want, I can output a one-shot bash script that installs Docker, writes these files, and brings the stack up in one command.