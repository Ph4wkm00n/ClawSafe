# ClawSafe

> Keeps your AI helper safe at home, no IT degree needed.

ClawSafe is a self-hosted security sidecar for [OpenClaw](https://openclaw.ai) that helps home users and small businesses **secure, monitor, and understand** their OpenClaw instances. It gives you friendly, plain-language guidance by default, plus powerful **Advanced Settings** for tech-savvy users.

---

## Features

- **Friendly safety dashboard** — Clear status (Safe / Needs Attention / At Risk) with category cards for Network, Tools & Skills, Data & Files, and Updates.

- **One-click fixes & guides** — Auto-fix common issues or follow step-by-step instructions with copy-pastable commands. All changes are backed up with one-click undo.

- **Advanced Settings** — Configure network rules, per-skill policies, data mounts, logging, and webhooks using a tabbed UI with auto-save. YAML-based policy-as-code with policy-aware risk scoring.

- **Monitoring & alerts** — Scheduled background scans with drift detection, Prometheus metrics endpoint, webhook notifications (Slack, Discord) with retry logic, and risk escalation alerts.

- **API key authentication** — All write endpoints protected by API key. Read endpoints remain open. Configurable per deployment.

- **OpenClaw skill integration** — Ask your agent "Is it safe?" and get a plain-language security summary powered by ClawSafe's API.

- **Playful & minimal themes** — Choose a cozy mascot-driven look or a clean utility style, both with light/dark mode. Theme persists across reloads.

- **Production-ready Docker** — Health checks, resource limits, non-root containers, Caddy reverse proxy overlay for automatic HTTPS.

---

## Architecture

```
┌─────────────────┐     ┌────────────────────┐     ┌──────────────┐
│   Next.js UI    │────▶│   FastAPI Backend   │────▶│   OpenClaw   │
│   (port 3000)   │◀────│   (port 8000)      │◀────│   Instance   │
└─────────────────┘     └────────────────────┘     └──────────────┘
                               │         │
                        ┌──────┘         └──────┐
                        │   SQLite DB   │  Prometheus  │
                        │   (5 tables)  │  /metrics    │
                        └───────────────┴──────────────┘
```

---

## Quick Start

### Requirements

- Linux host (Debian/Ubuntu recommended)
- Docker + Docker Compose
- An existing OpenClaw instance (optional — ClawSafe works in demo mode)

### Install

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
cp .env.example .env
# Optional: set CLAWSAFE_API_KEY in .env for production
docker compose up --build -d
```

Open [http://localhost:3000](http://localhost:3000) — the onboarding wizard will guide you through initial setup.

### Deployment Modes

```bash
# Default
make up

# Home user (localhost only, no external access)
make home

# Small business (with Prometheus metrics)
make smb

# Production (Caddy reverse proxy with automatic HTTPS)
make prod
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 (FastAPI) + SQLite + Pydantic |
| Frontend | Next.js 15 (React 19) + TypeScript + Tailwind CSS |
| Auth | API key (Bearer token) on write endpoints |
| Packaging | Docker + Docker Compose (4 overlay modes) |
| Config | YAML policy files + environment variables |
| Monitoring | Prometheus metrics, structured JSON logging |
| Testing | pytest (41 tests) + Vitest (24 tests) |
| CI/CD | GitHub Actions (lint, test, coverage, Trivy scan) |

---

## Documentation

- [Installation Guide](docs/installation.md) — Docker & development setup
- [Configuration Reference](docs/configuration.md) — All env vars and policy YAML
- [API Reference](docs/api-reference.md) — All endpoints with auth requirements
- [Security Guide](docs/security.md) — Auth, HTTPS, SSRF protection, container security
- [Operations Guide](docs/operations.md) — Backup, upgrade, monitoring, troubleshooting
- [Contributing](docs/contributing.md) — Development setup, code style, PR guidelines

---

## Development

```bash
make install   # Install all dependencies
make dev       # Start backend + frontend in dev mode (hot reload)
make test      # Run all tests (65 total)
make lint      # Run linters (ruff + eslint)
make build     # Build Docker images
make clean     # Remove containers and build artifacts
```

---

## License

Open source. See LICENSE for details.
