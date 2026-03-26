# Security Guide

## Authentication

ClawSafe uses API key authentication to protect all write endpoints.

### Endpoint Protection

| Endpoint Type | Auth Required | Examples |
|---------------|--------------|---------|
| Read (GET) | No | `/status`, `/health`, `/activity`, `/recommendations` |
| Write (PUT/POST) | Yes | `/fix/*`, `/settings`, `/policy`, `/notifications` |
| Metrics | No | `/metrics` (restrict via firewall in production) |

### Setup

Set an API key in your environment:

```bash
# In .env
CLAWSAFE_API_KEY=your-secure-random-key-here
NEXT_PUBLIC_API_KEY=your-secure-random-key-here  # Same key for frontend
```

Generate a secure key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### How It Works

When `CLAWSAFE_API_KEY` is set:
- Write endpoints require `Authorization: Bearer <key>` header
- Invalid or missing keys return HTTP 401
- Read endpoints remain open (no auth needed)

When `CLAWSAFE_API_KEY` is empty (default):
- All endpoints are open — **for development only**

The frontend sends the key automatically when `NEXT_PUBLIC_API_KEY` is configured.

## HTTPS / TLS

ClawSafe should always be deployed behind HTTPS in production.

### Using the Caddy Overlay (Recommended)

```bash
make prod
# or: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

This adds a Caddy reverse proxy with automatic HTTPS. Edit `Caddyfile` to set your domain:

```
clawsafe.yourdomain.com {
    reverse_proxy frontend:3000
    handle_path /api/* {
        reverse_proxy backend:8000
    }
    handle_path /metrics {
        reverse_proxy backend:8000
    }
}
```

Caddy automatically obtains and renews Let's Encrypt certificates.

### Manual Reverse Proxy (nginx)

If using nginx, forward:
- `/` → `frontend:3000`
- `/api/*` → `backend:8000`
- `/metrics` → `backend:8000`

## Input Validation

### Action IDs
- Pattern: `^[a-z][a-z0-9_]{0,63}$`
- Prevents path traversal attacks (e.g., `../../etc/passwd`)
- Invalid IDs return HTTP 400

### Webhook URLs
- Must use `http://` or `https://` scheme
- Must have a hostname
- **Blocked targets:** private IPs (10.x, 172.16.x, 192.168.x), loopback (127.0.0.1, ::1, localhost), reserved ranges
- Prevents Server-Side Request Forgery (SSRF)

### Policy Validation
- Required fields checked: `version`, `name`, `network`, `tools`, `data`, `auth`
- Tool actions must be `allow`, `ask`, or `block`
- Invalid policies return detailed error messages

## Data Security

- **SQLite database** is stored unencrypted. Restrict file permissions (`chmod 600`).
- **Config backups** are stored in `/data/backups/`. Auto-cleaned at 50 maximum.
- **Webhook URLs** and notification config are stored in the database — treat the DB file as sensitive.
- **No telemetry** — ClawSafe sends no data externally unless you configure webhooks.

## Container Security

- Both backend and frontend run as **non-root users** (`appuser`) in Docker
- **Resource limits:** 512MB RAM, 0.5 CPU per service (configurable in docker-compose.yml)
- **Health checks:** Backend verifies DB + scheduler; frontend checks HTTP port
- **Frontend depends on backend health** before starting (`condition: service_healthy`)
- Backend image includes `HEALTHCHECK` instruction for Docker orchestration

## Network Security

- **Home mode** (`make home`) binds all ports to `127.0.0.1` — no LAN access
- **CORS** restricted to configured `CLAWSAFE_FRONTEND_URL` with explicit method/header lists
- **Metrics endpoint** (`/metrics`) is unauthenticated — restrict via firewall or Caddy config in production
- **Webhook retry:** Failed webhooks retry up to 3 times with 10-second timeout

## Production Checklist

Before deploying to production:

- [ ] Set `CLAWSAFE_API_KEY` to a strong random value
- [ ] Set `NEXT_PUBLIC_API_KEY` to the same value
- [ ] Set `CLAWSAFE_DEMO_MODE=false`
- [ ] Use `make prod` or configure HTTPS via reverse proxy
- [ ] Restrict `/metrics` endpoint access (firewall or Caddy rules)
- [ ] Set appropriate file permissions on the database directory
- [ ] Review and customize the active policy via the Settings page
- [ ] Configure webhook notifications for risk escalation alerts
- [ ] Set `CLAWSAFE_LOG_LEVEL=WARNING` for quieter logs in production
