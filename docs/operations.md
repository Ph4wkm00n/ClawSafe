# Operations Guide

## Starting and Stopping

```bash
# Start
make up          # Default mode
make home        # Home mode (localhost only)
make smb         # SMB mode (with Prometheus metrics)
make prod        # Production (Caddy HTTPS)

# Stop
make down        # or: docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f           # all services
```

## Deployment Modes

| Mode | Command | Ports Exposed | Notes |
|------|---------|--------------|-------|
| Default | `make up` | 8000, 3000 | Standard development/testing |
| Home | `make home` | 127.0.0.1:8000, 127.0.0.1:3000 | Localhost only, no LAN access |
| SMB | `make smb` | 8000, 3000, 9090 | Adds Prometheus metrics port |
| Production | `make prod` | 80, 443 | Caddy reverse proxy with auto HTTPS |

## Health Checks

Both containers have built-in Docker health checks:

- **Backend:** HTTP GET to `/api/v1/health` every 30s
- **Frontend:** wget to port 3000 every 30s

Check health manually:
```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "checks": {"database": "ok", "scheduler": "ok"}
}
```

- `"ok"` — all systems healthy (HTTP 200)
- `"degraded"` — a check failed (HTTP 503)

The frontend waits for backend health before starting (`depends_on: condition: service_healthy`).

## Backup and Restore

### Database Backup

```bash
# Copy the SQLite database out of the container
docker compose cp backend:/data/clawsafe.db ./backup-$(date +%Y%m%d).db
```

### Database Restore

```bash
docker compose down
docker compose cp ./backup-20260326.db backend:/data/clawsafe.db
docker compose up -d
```

### Config Backups (Auto-Fix)

ClawSafe automatically creates config backups before applying any fix. Backups are stored in `/data/backups/` inside the backend container. A maximum of 50 backups are retained — oldest are auto-deleted when the limit is exceeded.

To list backups via API:
```bash
curl http://localhost:8000/api/v1/backups
```

## Upgrading

```bash
git pull
docker compose down
docker compose up --build -d
```

The SQLite schema uses `CREATE TABLE IF NOT EXISTS`, so new tables are added automatically on startup. Check the [CHANGELOG](../CHANGELOG.md) for any manual migration steps between versions.

## Monitoring

### Prometheus

Scrape `http://localhost:8000/metrics` (or `http://backend:8000/metrics` from inside Docker).

| Metric | Type | Description |
|--------|------|-------------|
| `clawsafe_risk_score{category}` | Gauge | Risk score per category (0–100) |
| `clawsafe_overall_status` | Gauge | Overall status (0=safe, 1=attention, 2=risk) |
| `clawsafe_scan_count` | Counter | Total scans performed since startup |
| `clawsafe_fix_count` | Counter | Total fixes applied since startup |

Metrics are updated after each scheduled scan and each fix application.

### Scheduled Scans

- Default interval: 3600 seconds (1 hour), configurable via `CLAWSAFE_SCAN_INTERVAL`
- Uses exponential backoff on failures (2x, 4x, capped at 4x interval)
- Resets to normal interval on successful scan
- Logs status changes and triggers escalation notifications

### Logs

Backend outputs structured JSON logs to stdout:

```json
{"time":"2026-03-26T12:00:00","level":"INFO","logger":"app.services.scheduler","message":"Scan complete: status=safe score=10"}
```

Configure verbosity with `CLAWSAFE_LOG_LEVEL`:
- `DEBUG` — verbose, includes scan details
- `INFO` — default, scans + fixes + status changes
- `WARNING` — only issues
- `ERROR` — only failures

View live logs:
```bash
docker compose logs -f backend --since 1h
```

### Webhook Notifications

Configure webhooks to receive alerts on risk escalation:

```bash
curl -X PUT http://localhost:8000/api/v1/settings/notifications \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhooks": [{"url": "https://hooks.slack.com/...", "events": ["escalation"]}],
    "events": ["escalation"]
  }'
```

Test a webhook:
```bash
curl -X POST http://localhost:8000/api/v1/settings/notifications/test \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://hooks.slack.com/..."}'
```

Webhook payloads include `source`, `type`, `message`, and status change details. Webhooks retry up to 3 times with a 10-second timeout.

## Resource Limits

Default Docker resource limits per service:
- **Memory:** 512 MB
- **CPU:** 0.5 cores

Adjust in `docker-compose.yml` under `deploy.resources.limits` if needed.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | `docker compose logs backend` — check for import or DB errors |
| Frontend can't reach backend | Verify `NEXT_PUBLIC_API_URL` matches backend address |
| Health check failing | Ensure database path (`/data`) is writable by the `appuser` |
| Scheduler not running | Check logs for scan errors; backoff increases sleep time |
| Settings not saving | Verify `CLAWSAFE_API_KEY` matches `NEXT_PUBLIC_API_KEY` |
| Theme not persisting | Clear browser localStorage, re-select theme |
| 401 on write endpoints | Set `Authorization: Bearer <key>` header matching `CLAWSAFE_API_KEY` |
| Webhook fails validation | URL must be HTTPS and not target private/loopback IPs |
| Container OOM killed | Increase `mem_limit` in docker-compose.yml |
| Scan results empty | Check `CLAWSAFE_DEMO_MODE=true` for demo data, or connect real OpenClaw |
