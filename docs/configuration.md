# Configuration Reference

## Environment Variables

All backend variables use the `CLAWSAFE_` prefix.

### Backend

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWSAFE_PORT` | `8000` | Backend API port |
| `CLAWSAFE_HOST` | `0.0.0.0` | Backend bind address |
| `CLAWSAFE_DATABASE_PATH` | `clawsafe.db` | SQLite database file path |
| `CLAWSAFE_OPENCLAW_CONFIG_PATH` | `/etc/openclaw/config.yaml` | Path to OpenClaw config file |
| `CLAWSAFE_FRONTEND_URL` | `http://localhost:3000` | Frontend URL (used for CORS) |
| `CLAWSAFE_API_KEY` | _(empty)_ | API key for write endpoints. **Leave empty to disable auth (dev only).** Set in production. |
| `CLAWSAFE_SCAN_INTERVAL` | `3600` | Seconds between background scans (default: 1 hour) |
| `CLAWSAFE_DEMO_MODE` | `true` | Seed demo activity data on first start. Set `false` in production. |
| `CLAWSAFE_LOG_LEVEL` | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `CLAWSAFE_DEBUG` | `false` | Enable FastAPI debug mode |

### Frontend

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL for the frontend to connect to |
| `NEXT_PUBLIC_API_KEY` | _(empty)_ | API key sent with all requests. Must match `CLAWSAFE_API_KEY`. |

### Docker Compose (overlay-specific)

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWSAFE_METRICS_PORT` | `9090` | Prometheus metrics port (SMB overlay) |

## Authentication

When `CLAWSAFE_API_KEY` is set:
- **Read endpoints** (GET) — no auth required
- **Write endpoints** (PUT, POST for fixes/settings/policy/notifications) — require `Authorization: Bearer <key>` header

When `CLAWSAFE_API_KEY` is empty (default):
- All endpoints are open (development mode)

The frontend automatically sends the key if `NEXT_PUBLIC_API_KEY` is set.

## Policy YAML Format

Policies live in the `policies/` directory. The active policy can be managed via the API (`GET/PUT /api/v1/policy`) and affects risk scoring in real-time.

### Required Fields

Every policy must have `version`, `name`, `network`, `tools`, `data`, and `auth` sections.

### Full Example

```yaml
version: "1"
name: my-policy

network:
  bind_address: "127.0.0.1"       # "127.0.0.1" or "0.0.0.0"
  allowed_cidrs:                   # IP ranges allowed to connect
    - "127.0.0.0/8"
    - "192.168.0.0/16"
  vpn_only: false                  # Require VPN for connections

tools:
  default_action: ask              # Default for unlisted tools: "allow", "ask", or "block"
  rules:                           # Per-tool overrides
    - name: web_search
      risk: low                    # "low", "medium", "high", "critical"
      action: allow                # "allow", "ask", or "block"
    - name: shell_exec
      risk: high
      action: block

data:
  allowed_mounts:                  # Directories OpenClaw can access
    - "/app/data"
  backup:
    enabled: true
    frequency: daily               # "hourly", "daily", "weekly"
    destination: "/data/backups"

auth:
  enabled: true
  method: token                    # "token" or "password"

monitoring:
  scan_interval: 3600              # Seconds between scans
  log_format: json                 # "json" or "text"

integrations:                      # Optional (SMB/advanced setups)
  metrics:
    enabled: true
    port: 9090
  webhooks:
    - url: "https://hooks.slack.com/services/..."
      events: ["escalation"]
  email:
    enabled: false
    address: "alerts@example.com"
```

### Policy Validation

Validate a policy without applying:
```bash
curl -X POST http://localhost:8000/api/v1/policy/validate \
  -H "Content-Type: application/json" \
  -d @policies/default.yaml
```

### Policy Enforcement

The active policy affects risk scoring:
- If policy says `shell_exec: block` but the tool is enabled, the tools score increases
- If `vpn_only: true` but VPN isn't enforced, the network score increases
- Scoring adjustments happen in real-time when the status endpoint is called

## Safety Status Levels

| Level | Score Range | Meaning |
|-------|------------|---------|
| Safe | 0–29 | No significant risks detected |
| Needs Attention | 30–69 | Some issues that should be reviewed |
| At Risk | 70–100 | Critical security issues requiring immediate action |

The overall score is the maximum of all category scores.

## Risk Categories

| Category | What It Checks |
|----------|---------------|
| **Network** | Bind address, public exposure, authentication status |
| **Tools & Skills** | High-risk skills enabled (shell, file write, etc.) |
| **Data & Files** | Sensitive mount paths (`/`, `/etc`, `/root`, `/home`) |
| **Updates & Health** | Version currency, available updates |

## Prometheus Metrics

Available at `GET /metrics` (Prometheus text format):

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `clawsafe_risk_score` | Gauge | `category` | Risk score per category (0–100) |
| `clawsafe_overall_status` | Gauge | — | Overall status (0=safe, 1=attention, 2=risk) |
| `clawsafe_scan_count` | Counter | — | Total scans performed |
| `clawsafe_fix_count` | Counter | — | Total fixes applied |

## Docker Deployment Modes

| Mode | Command | Description |
|------|---------|-------------|
| Default | `make up` | Standard deployment |
| Home | `make home` | Localhost only, no external access |
| SMB | `make smb` | Adds metrics port and log volume |
| Production | `make prod` | Caddy reverse proxy with automatic HTTPS |

All modes include Docker health checks (backend: HTTP, frontend: wget) and resource limits (512MB RAM, 0.5 CPU per service).
