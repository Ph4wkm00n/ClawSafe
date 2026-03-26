# ClawSafe

> Keeps your AI helper safe at home, no IT degree needed.

ClawSafe is a self-hosted security sidecar for [OpenClaw](https://openclaw.ai) that helps home users and small businesses **secure, monitor, and understand** their OpenClaw instances. It gives you friendly, plain-language guidance by default, plus powerful **Advanced Settings** for tech-savvy users.

---

## Features

**Security Dashboard**
- Clear status (Safe / Needs Attention / At Risk) with 4 category cards
- One-click auto-fix with backup/undo, or step-by-step manual instructions
- Background scanning with drift detection and risk escalation alerts

**Advanced Security Intelligence** (v2.0)
- Secrets scanning (10 patterns: AWS keys, GitHub tokens, private keys, DB URLs)
- Container/CVE scanning via Trivy integration
- CIS Benchmark + SOC 2 compliance mapping with gap analysis
- CVSS 3.1-style scoring, combined risk analysis, blast radius estimation
- Custom YAML rule engine for organization-specific detection

**Multi-Instance & Team Management**
- Register and monitor multiple OpenClaw instances from one dashboard
- Cross-instance risk aggregation and per-instance status
- User accounts with JWT auth (Admin / Security Officer / Viewer roles)
- Audit trail tracking who changed what, when

**Integrations & Monitoring**
- Prometheus metrics (risk scores, scan duration, error rates, latency histograms)
- Webhook notifications: Slack (Block Kit), Microsoft Teams (Adaptive Cards), generic JSON
- HMAC-SHA256 signed webhooks, do-not-disturb hours, digest mode
- Email alerts via SMTP for risk escalation
- Grafana dashboard included (`monitoring/grafana-dashboard.json`)

**Developer & DevOps**
- Plugin SDK (Python) for custom scanners, fixers, and notifiers
- Policy-as-code with version history, YAML export, validation API
- PostgreSQL support for production (SQLite default for development)
- Helm chart for Kubernetes deployment
- Docker Compose with 4 modes (default, home, SMB, production with Caddy HTTPS)
- WebSocket real-time updates with auto-reconnect

---

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────┐
│   Next.js UI    │────▶│   FastAPI Backend     │────▶│   OpenClaw   │
│   (port 3000)   │◀────│   (port 8000)        │◀────│  Instance(s) │
└─────────────────┘     └──────────────────────┘     └──────────────┘
                              │           │
                       ┌──────┘           └──────┐
                       │ SQLite/PostgreSQL │ Prometheus │
                       │ (6 tables)       │ /metrics   │
                       └──────────────────┴────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
cp .env.example .env
# Set CLAWSAFE_API_KEY for production security
docker compose up --build -d
```

Open [http://localhost:3000](http://localhost:3000) — the onboarding wizard guides you through setup.

### Deployment Modes

| Command | Mode | Description |
|---------|------|-------------|
| `make up` | Default | Standard deployment |
| `make home` | Home | Localhost only, no LAN access |
| `make smb` | SMB | Adds Prometheus metrics port |
| `make prod` | Production | Caddy reverse proxy with automatic HTTPS |
| `make helm-install` | Kubernetes | Helm chart deployment |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 (FastAPI) + SQLite/PostgreSQL + Pydantic |
| Frontend | Next.js 15 (React 19) + TypeScript + Tailwind CSS |
| Auth | API key + JWT tokens (3 roles) |
| Packaging | Docker + Docker Compose + Helm chart |
| Monitoring | Prometheus + Grafana + structured JSON logging |
| Testing | pytest (92 tests) + Vitest (24 tests) |
| CI/CD | GitHub Actions (lint, test, coverage, Trivy scan) |

---

## Documentation

- [User Guide](docs/user-guide.md) — Dashboard walkthrough, features, keyboard shortcuts
- [Installation Guide](docs/installation.md) — Docker, Kubernetes, and manual setup
- [Deployment Guide](docs/deployment-guide.md) — Production checklist, HTTPS, monitoring
- [Configuration Reference](docs/configuration.md) — All env vars, policy YAML, metrics
- [API Reference](docs/api-reference.md) — All endpoints with auth and examples
- [Security Guide](docs/security.md) — Auth, HTTPS, SSRF protection, production checklist
- [Operations Guide](docs/operations.md) — Backup, upgrade, monitoring, troubleshooting
- [Contributing](docs/contributing.md) — Development setup, code style, PR guidelines
- [Future Roadmap](docs/ROADMAP.md) — v2.5 through v3.0 planned features

---

## Development

```bash
make install   # Install all dependencies
make dev       # Start backend + frontend (hot reload)
make test      # Run all tests (116 total)
make lint      # Run linters (ruff + eslint)
make migrate   # Run database migrations
make seed      # Seed demo data
```

---

## Security

ClawSafe follows security best practices:

- **Authentication** — API key + JWT on all write endpoints; PBKDF2-SHA256 password hashing
- **Input validation** — Action ID whitelist, config path validation, SSRF-protected webhooks
- **Container security** — Non-root users, resource limits, health checks
- **Infrastructure** — Caddy with security headers (HSTS, CSP, X-Frame-Options)
- **Supply chain** — Trivy image scanning in CI, pre-commit hooks

See the [Security Guide](docs/security.md) for details and production checklist.

---

## License

[MIT License](LICENSE) — free to use, modify, and distribute.
