# Security Guide

## Authentication

ClawSafe supports API key authentication for all write endpoints (fix, settings, policy, notifications).

### Setup

Set an API key in your environment:

```bash
CLAWSAFE_API_KEY=your-secret-key-here
```

When set, all write endpoints require `Authorization: Bearer <key>` header. Read endpoints (status, health, activity) remain open.

For the frontend to send the key automatically, also set:

```bash
NEXT_PUBLIC_API_KEY=your-secret-key-here
```

### Development Mode

When `CLAWSAFE_API_KEY` is empty (default), authentication is disabled. This is intended only for local development.

## HTTPS / TLS

ClawSafe should always be deployed behind HTTPS in production.

### Using the Caddy Overlay

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

This adds a Caddy reverse proxy that handles TLS automatically. Edit `Caddyfile` to set your domain.

### Manual Reverse Proxy

If using nginx or another proxy, forward:
- `/` → `frontend:3000`
- `/api/*` → `backend:8000`
- `/metrics` → `backend:8000`

## Input Validation

- **Action IDs** must match `^[a-z][a-z0-9_]+$` to prevent path traversal
- **Webhook URLs** are validated against private/loopback IPs to prevent SSRF
- **Policy YAML** is validated before application (required fields, valid actions)

## Data Security

- SQLite database is stored unencrypted on disk. Restrict file permissions.
- Config backups are stored in `/data/backups/`. Set appropriate permissions.
- Webhook URLs and notification config are stored in the database.

## Container Security

- Both backend and frontend run as non-root users in Docker.
- Resource limits (512MB RAM, 0.5 CPU) are set in docker-compose.yml.
- Health checks verify service availability.

## Network Security

- Default configuration binds to localhost only (docker-compose.home.yml).
- CORS is restricted to configured frontend URL.
- The `/metrics` endpoint is accessible without auth — restrict access via firewall or reverse proxy in production.
