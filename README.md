# ClawSafe

> Keeps your AI helper safe at home, no IT degree needed.

ClawSafe is a self-hosted security sidecar for [OpenClaw](https://openclaw.ai) that helps home users and small businesses **secure, monitor, and understand** their OpenClaw instances. It gives you friendly, plain-language guidance by default, plus powerful **Advanced Settings** for tech-savvy users.

---

## Features

- **Friendly safety dashboard** — Clear status (Safe / Needs Attention / At Risk) with category cards for Network, Tools & Skills, Data & Files, and Updates.

- **One-click fixes & guides** — Auto-fix common issues or follow step-by-step instructions with copy-pastable commands. All changes are backed up and undoable.

- **Advanced Settings** — Configure network rules, per-skill policies, data mounts, logging, and webhooks using a tabbed UI and YAML-based policy-as-code.

- **Monitoring & alerts** — Scheduled security scans, Prometheus metrics, webhook notifications (Slack, Discord), and email alerts on risk escalation.

- **OpenClaw skill integration** — Ask your agent "Is it safe?" and get a plain-language security summary.

- **Playful & minimal themes** — Choose a cozy mascot-driven look or a clean utility style, both with light/dark mode.

---

## Quick Start

### Requirements

- Linux host (Debian/Ubuntu recommended)
- Docker + Docker Compose
- An existing OpenClaw instance (optional)

### Install

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
cp .env.example .env
docker compose up --build -d
```

Open [http://localhost:3000](http://localhost:3000) — the onboarding wizard will guide you.

**Home user (localhost only):**
```bash
docker compose -f docker-compose.yml -f docker-compose.home.yml up --build -d
```

**Small business (with metrics):**
```bash
docker compose -f docker-compose.yml -f docker-compose.smb.yml up --build -d
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python (FastAPI) + SQLite |
| Frontend | Next.js (React) + TypeScript + Tailwind CSS |
| Packaging | Docker + Docker Compose |
| Config | YAML policy files |
| Monitoring | Prometheus metrics, structured JSON logging |

---

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Reference](docs/api-reference.md)
- [Security Guide](docs/security.md)
- [Operations Guide](docs/operations.md)
- [Contributing](docs/contributing.md)

---

## Development

```bash
make install   # Install all dependencies
make dev       # Start backend + frontend in dev mode
make test      # Run all tests
make lint      # Run linters
make build     # Build Docker images
make up        # Start with Docker Compose
```

---

## License

Open source. See LICENSE for details.
