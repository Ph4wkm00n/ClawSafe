# Production Deployment Guide

This guide covers deploying ClawSafe to production environments.

## Pre-Deployment Checklist

- [ ] Set `CLAWSAFE_API_KEY` to a strong random value (min 32 chars)
- [ ] Set `CLAWSAFE_JWT_SECRET` to a strong random value
- [ ] Set `CLAWSAFE_DEMO_MODE=false`
- [ ] Set `CLAWSAFE_DEBUG=false`
- [ ] Configure SMTP for email notifications (optional)
- [ ] Review and customize the default security policy
- [ ] Test backup and restore procedures
- [ ] Configure monitoring (Prometheus/Grafana)

### Generate Secrets

```bash
# API Key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# JWT Secret
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Deployment Options

### Option 1: Docker Compose (Recommended for Small Teams)

```bash
cp .env.example .env
# Edit .env with production values
make prod  # Starts with Caddy HTTPS reverse proxy
```

### Option 2: Docker Compose with PostgreSQL

```bash
# In .env:
CLAWSAFE_DB_TYPE=postgresql
CLAWSAFE_DB_URL=postgresql://clawsafe:password@postgres:5432/clawsafe

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Option 3: Kubernetes with Helm

```bash
helm install clawsafe ./helm/clawsafe \
  --set secrets.apiKey=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))") \
  --set secrets.jwtSecret=$(python3 -c "import secrets; print(secrets.token_hex(32))") \
  --set config.demoMode=false \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=clawsafe.yourdomain.com
```

## HTTPS Configuration

### With Caddy (Automatic)

Edit `Caddyfile` — replace `:80` with your domain:

```
clawsafe.yourdomain.com {
    # ... (rest stays the same)
}
```

Caddy automatically obtains and renews Let's Encrypt certificates.

### With Kubernetes Ingress

```bash
helm install clawsafe ./helm/clawsafe \
  --set ingress.enabled=true \
  --set ingress.className=nginx \
  --set ingress.tls[0].secretName=clawsafe-tls \
  --set ingress.tls[0].hosts[0]=clawsafe.yourdomain.com
```

## Post-Deployment Verification

```bash
# Health check
curl https://clawsafe.yourdomain.com/api/v1/health

# Expected: {"status": "ok", "version": "2.0.0", "checks": {...}}

# Create first admin user
curl -X POST https://clawsafe.yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "secure-password", "role": "admin"}'
```

## Monitoring

Import the Grafana dashboard from `monitoring/grafana-dashboard.json`.

Configure Prometheus to scrape:
```yaml
scrape_configs:
  - job_name: clawsafe
    static_configs:
      - targets: ['clawsafe-backend:8000']
    metrics_path: /metrics
```

## Backup Strategy

### Automated Backups (via API)

```bash
# Trigger backup
curl -X POST https://clawsafe.yourdomain.com/api/v1/data/backup \
  -H "Authorization: Bearer YOUR_API_KEY"

# Schedule via cron:
0 2 * * * curl -s -X POST http://localhost:8000/api/v1/data/backup -H "Authorization: Bearer KEY"
```

### Manual Backup

```bash
docker compose cp backend:/data/clawsafe.db ./backup-$(date +%Y%m%d).db
```

## Upgrading

```bash
git pull
docker compose down
docker compose up --build -d
# Migrations run automatically on startup
```

## Rollback

```bash
docker compose down
git checkout v1.5.0  # Previous version tag
docker compose up --build -d
# Restore database if needed:
docker compose cp ./backup-YYYYMMDD.db backend:/data/clawsafe.db
```
