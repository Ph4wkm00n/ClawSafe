# Implementation Plan

All phases are complete. ClawSafe is at v1.1.0 with production hardening.

| Phase | Document | Focus | Status |
|-------|----------|-------|--------|
| 0 | [00-project-setup.md](./00-project-setup.md) | Scaffolding, CI, Docker | Complete |
| 1 | [01-core-dashboard.md](./01-core-dashboard.md) | Risk detection, dashboard, manual fixes | Complete |
| 2 | [02-autofix-and-themes.md](./02-autofix-and-themes.md) | Auto-fix, themes, advanced settings | Complete |
| 3 | [03-integrations.md](./03-integrations.md) | Scheduler, notifications, metrics, skill | Complete |
| 4 | [04-polish-and-release.md](./04-polish-and-release.md) | UX polish, docs, testing, release | Complete |

## Post-Release Enhancements (v1.1.0)

Beyond the original plan, the following production hardening was added:

- API key authentication on all write endpoints
- Input validation (action IDs, webhook URLs) preventing path traversal and SSRF
- Structured JSON logging with configurable levels
- Real health checks (DB connectivity + scheduler status)
- Policy-aware risk scoring (active policy affects scores)
- Prometheus metrics populated during scans and fixes
- Scheduler exponential backoff on failures
- Onboarding wizard connected to dashboard and backend
- Theme flash prevention via localStorage
- Settings tabs save to policy API with auto-save and toast feedback
- Focus trap and ARIA improvements for accessibility
- Non-root Docker containers with health checks and resource limits
- Production Caddy overlay for automatic HTTPS
- Makefile for one-command operations
- Security and operations documentation

## Architecture

```
┌───────────────────┐     ┌─────────────────────────┐     ┌──────────────┐
│   Next.js UI      │────▶│    FastAPI Backend       │────▶│   OpenClaw   │
│   (port 3000)     │◀────│    (port 8000)           │◀────│   Instance   │
│                   │     │                           │     └──────────────┘
│  - Dashboard      │     │  - Auth middleware        │
│  - Onboarding     │     │  - Scanner + Scoring      │
│  - Settings       │     │  - Fixer + Backup         │
│  - Appearance     │     │  - Scheduler (background)  │
│  - Activity       │     │  - Notifications           │
│  - Error boundary │     │  - Policy enforcement      │
└───────────────────┘     └─────────────────────────┘
                                │           │
                         ┌──────┘           └──────┐
                         │   SQLite DB     │  Prometheus │
                         │   (5 tables)    │  /metrics   │
                         └─────────────────┴────────────┘
```

- **Frontend** calls backend API with auth headers, polls with backoff
- **Backend** scans OpenClaw, scores risks (policy-aware), applies fixes with backup
- **SQLite** stores scans, activity, settings, backups, and policies
- **Scheduler** runs background scans, updates metrics, triggers notifications
- **Docker Compose** orchestrates with health checks, resource limits, 4 deployment modes
