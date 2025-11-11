# N8N Operations Runbook

Quick reference for n8n operations and troubleshooting.

## Service Management

### Start/Stop Services
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart specific service
docker compose restart n8n
```

### Health Checks
```bash
# Check service status
docker compose ps

# Check n8n health endpoint
curl -f https://your-domain.com/healthz

# View logs
docker compose logs n8n -f
docker compose logs n8n_db -f
docker compose logs n8n_proxy -f
```

## Common Issues

### N8N Won't Start
1. Check database connection:
   ```bash
   docker compose logs n8n_db
   ```
2. Verify encryption key is set in `.env`
3. Check disk space: `df -h`

### SSL/Proxy Issues
1. Check Caddy logs:
   ```bash
   docker compose logs n8n_proxy
   ```
2. Verify DNS points to server IP
3. Check firewall: `sudo ufw status`

### Webhooks Not Working
1. Verify `WEBHOOK_URL` in `.env`
2. Check proxy headers in `ops/Caddyfile`
3. Test with: `curl -X POST https://your-domain.com/webhook-test/test`

## Backup & Restore

### Create Backup
```bash
./ops/backup.sh
```

### Restore from Backup
```bash
./ops/restore.sh db_20231201_120000.sql.gz data_20231201_120000.tar.gz
```

### Emergency Recovery
1. Stop services: `docker compose down`
2. Restore from latest backup
3. Start services: `docker compose up -d`
4. Verify workflows load correctly

## Monitoring

### Key Metrics
- Service uptime
- Database connections
- Execution success rate
- Disk space usage

### Log Locations
- N8N: `docker compose logs n8n`
- Database: `docker compose logs n8n_db`
- Proxy: `docker compose logs n8n_proxy`

## Maintenance

### Updates
```bash
# Update images
docker compose pull
docker compose up -d

# Cleanup old images
docker image prune -f
```

### Daily Tasks
- Check service health
- Verify backup completed
- Monitor disk space

### Weekly Tasks
- Review execution failures
- Update system packages
- Test restore procedure