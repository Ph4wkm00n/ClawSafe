# Configuration Reference

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWSAFE_PORT` | `8000` | Backend API port |
| `CLAWSAFE_DATABASE_PATH` | `clawsafe.db` | SQLite database path |
| `CLAWSAFE_OPENCLAW_CONFIG_PATH` | `/etc/openclaw/config.yaml` | OpenClaw config file path |
| `CLAWSAFE_FRONTEND_URL` | `http://localhost:3000` | Frontend URL (for CORS) |
| `CLAWSAFE_DEBUG` | `false` | Enable debug mode |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend URL (frontend) |

## Policy YAML Format

Policies live in the `policies/` directory. The active policy can be managed via the API.

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
  default_action: ask              # "allow", "ask", or "block"
  rules:
    - name: web_search
      risk: low                    # "low", "medium", "high", "critical"
      action: allow                # "allow", "ask", or "block"
    - name: shell_exec
      risk: high
      action: block

data:
  allowed_mounts:
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

integrations:
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

## Safety Status Levels

| Level | Score Range | Meaning |
|-------|------------|---------|
| Safe | 0-29 | No significant risks detected |
| Needs Attention | 30-69 | Some issues that should be reviewed |
| At Risk | 70-100 | Critical security issues requiring immediate action |

## Risk Categories

- **Network:** Bind address, authentication, public exposure
- **Tools & Skills:** Dangerous skills like shell execution
- **Data & Files:** Overly broad file system mounts
- **Updates & Health:** Outdated versions with known issues
