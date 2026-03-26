# User Guide

## Getting Started

### First Visit — Onboarding

When you first open ClawSafe, the onboarding wizard walks you through setup:

1. **Welcome** — Introduction to ClawSafe
2. **Detection** — ClawSafe checks if OpenClaw is running
3. **Questions** — Home or business? Private or public?
4. **Summary** — Review what ClawSafe will configure

After completing onboarding, you'll see the main dashboard.

### Dashboard

The dashboard shows your overall security status:

- **Status Header** — Safe (green), Needs Attention (amber), or At Risk (red)
- **Category Cards** — Network, Tools & Skills, Data & Files, Updates & Health
- **Recent Activity** — Latest security events

Each card shows a summary and an action button:
- **"Fix this for me"** — Auto-fix the issue with one click
- **"Show me how"** — Step-by-step manual instructions

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Refresh dashboard |
| `D` | Go to Dashboard |
| `I` | Go to Instances |
| `A` | Go to Activity |
| `S` | Go to Settings |

## Features

### Fixing Security Issues

Click "Fix this for me" on any card to open the fix panel:

1. **Auto-fix** — ClawSafe applies the fix automatically. A backup is created first.
2. **Show me how** — Step-by-step instructions with copy-pastable commands.
3. **Undo** — If the fix causes issues, click "Undo" to restore the previous config.

### Advanced Settings

Navigate to **Settings** for detailed configuration:

| Tab | What You Can Configure |
|-----|----------------------|
| **Network** | Bind address, allowed IP ranges, VPN-only mode |
| **Tools & Skills** | Enable/disable individual skills, set risk-based policies |
| **Data & Files** | Review mount paths, configure backups |
| **Integrations** | Webhook URLs, email notifications, Prometheus metrics |

Settings auto-save when you make changes.

### Multi-Instance Management

Navigate to **Instances** to manage multiple OpenClaw deployments:

- **Add Instance** — Register a new OpenClaw with its config path
- **Remove Instance** — Deregister an instance (default instance can't be removed)
- **Aggregated View** — See overall risk across all instances

### Vulnerability Scanning

Navigate to **Vulnerabilities** to see container security:

- **Container List** — All running Docker containers
- **CVE Details** — Known vulnerabilities per image (requires Trivy)
- **Severity Levels** — Critical, High, Medium, Low

### Audit Trail

Navigate to **Audit Trail** to see who changed what:

- **Timeline** — Chronological list of all changes
- **User Attribution** — Who made each change
- **Resource Tracking** — What was changed (settings, policy, fix, etc.)

### Appearance

Customize the look and feel:

- **Playful Theme** — Mascot, soft colors, rounded shapes
- **Minimal Theme** — Clean, flat, utility-focused
- **Light/Dark Mode** — Matches system preference or manual override

Theme preferences persist across browser sessions.

### Notifications

Configure alerts in **Settings > Integrations**:

- **Webhooks** — Slack, Discord, Microsoft Teams, or generic HTTP
- **Email** — SMTP-based email alerts for risk escalation
- **Do Not Disturb** — Set quiet hours for notifications

### Security Intelligence

Advanced security analysis available via API:

- **Secrets Scanner** — Detects leaked credentials in config files
- **Compliance** — CIS Benchmark and SOC 2 control mapping
- **CVSS Scoring** — Industry-standard vulnerability scoring
- **Blast Radius** — Estimates impact of a potential compromise
- **Custom Rules** — Define YAML-based detection rules

## API Access

All features are available via REST API at `/api/v1/`. See the [API Reference](api-reference.md) for endpoints.

Interactive API docs: `http://your-server:8000/docs` (Swagger UI)
