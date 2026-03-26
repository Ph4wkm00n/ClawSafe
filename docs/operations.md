# Operations Guide

## Starting and Stopping

```bash
# Start
make up      # or: docker compose up -d

# Stop
make down    # or: docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

## Backup and Restore

### Database Backup

```bash
# Copy the SQLite database
docker compose cp backend:/data/clawsafe.db ./backup-$(date +%Y%m%d).db
```

### Database Restore

```bash
docker compose down
docker compose cp ./backup-20260326.db backend:/data/clawsafe.db
docker compose up -d
```

### Config Backups

ClawSafe automatically creates config backups before applying fixes. These are stored in `/data/backups/` inside the backend container. A maximum of 50 backups are retained (oldest are auto-deleted).

## Upgrading

```bash
git pull
docker compose down
docker compose up --build -d
```

The SQLite schema uses `CREATE TABLE IF NOT EXISTS`, so new tables are added automatically. For schema changes to existing tables, manual migration may be needed — check the CHANGELOG for migration notes.

## Monitoring

### Prometheus

Scrape `http://backend:8000/metrics` for:
- `clawsafe_risk_score{category}` — risk score per category
- `clawsafe_overall_status` — overall status (0=safe, 1=attention, 2=risk)
- `clawsafe_scan_count` — total scans performed
- `clawsafe_fix_count` — total fixes applied

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Returns:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "checks": {"database": "ok", "scheduler": "ok"}
}
```

Status is `"degraded"` if any check fails (returns 503).

### Logs

Backend outputs structured JSON logs to stdout. Configure `CLAWSAFE_LOG_LEVEL` for verbosity (DEBUG, INFO, WARNING, ERROR).

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check `docker compose logs backend` for errors |
| Frontend can't reach backend | Verify `NEXT_PUBLIC_API_URL` matches backend address |
| Health check failing | Ensure database path is writable |
| Scheduler not running | Check logs for scan errors; it uses exponential backoff |
| Settings not saving | Verify API key matches between frontend and backend |
| Theme not persisting | Clear localStorage and re-select theme |
