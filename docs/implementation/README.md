# Implementation Plan

ClawSafe implementation is organized into four milestones matching the product roadmap.
Each phase has its own document with detailed tasks.

| Phase | Document | Focus | Target |
|-------|----------|-------|--------|
| 0 | [00-project-setup.md](./00-project-setup.md) | Scaffolding, CI, Docker | Week 1-2 |
| 1 | [01-core-dashboard.md](./01-core-dashboard.md) | Risk detection, dashboard, manual fixes | v0.1 |
| 2 | [02-autofix-and-themes.md](./02-autofix-and-themes.md) | Auto-fix, themes, advanced settings | v0.2 |
| 3 | [03-integrations.md](./03-integrations.md) | OpenClaw skill, alerts, webhooks | v0.3 |
| 4 | [04-polish-and-release.md](./04-polish-and-release.md) | UX polish, docs, stable release | v1.0 |

## Architecture Overview

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Next.js UI  │────▶│  FastAPI Backend  │────▶│   OpenClaw    │
│  (port 3000) │◀────│  (port 8000)     │◀────│   Instance    │
└─────────────┘     └──────────────────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │   SQLite    │
                    │  (local DB) │
                    └─────────────┘
```

- **Frontend** calls backend REST API (`/api/v1/...`)
- **Backend** scans OpenClaw config, computes risk scores, applies fixes
- **SQLite** stores activity logs, scan history, user preferences
- **Docker Compose** orchestrates all services
