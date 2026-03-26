# ClawSafe - Claude Code Guidelines

## Project Overview

ClawSafe is a self-hosted security sidecar for OpenClaw. It helps home users and
small businesses secure, monitor, and understand their OpenClaw instances through
a friendly, non-technical dashboard with advanced options for power users.

**Status:** v1.1.0 — fully implemented with production hardening.

## Tech Stack

- **Backend:** Python 3.12 (FastAPI) with async SQLite, Pydantic models, structured JSON logging
- **Frontend:** Next.js 15 (React 19) with TypeScript, Tailwind CSS, CSS custom properties
- **Styling:** Design token system (playful/minimal themes, light/dark modes, localStorage persistence)
- **Packaging:** Docker images + Docker Compose (with home, SMB, and production overlays)
- **Config:** YAML policy files validated via API, environment variables with `CLAWSAFE_` prefix
- **Database:** SQLite (local) for scans, activity, settings, backups, and policies
- **Auth:** API key authentication on all write endpoints (`CLAWSAFE_API_KEY`)
- **Monitoring:** Prometheus metrics (`/metrics`), structured JSON logging, scheduled background scans
- **Testing:** pytest (backend, 41 tests), Vitest + React Testing Library (frontend, 24 tests)
- **CI:** GitHub Actions (lint, test, coverage, Docker build, Trivy security scan)

## Repository Structure

```
ClawSafe/
├── CLAUDE.md                      # This file
├── README.md                      # Project readme
├── CHANGELOG.md                   # Version history
├── Makefile                       # Build/dev/test commands
├── Caddyfile                      # Reverse proxy config (production)
├── .env.example                   # Environment variables reference
├── docs/                          # Documentation
│   ├── installation.md            # Docker & manual install guide
│   ├── configuration.md           # Env vars, policy YAML format
│   ├── api-reference.md           # All API endpoints
│   ├── security.md                # Auth, HTTPS, SSRF protection
│   ├── operations.md              # Backup, upgrade, monitoring, troubleshooting
│   ├── contributing.md            # Development setup & guidelines
│   ├── implementation/            # Implementation plan (historical, by phase)
│   └── ui-ux/                     # UI/UX design specs (by screen/component)
├── backend/                       # FastAPI backend
│   ├── app/
│   │   ├── main.py                # App entrypoint, middleware, lifespan
│   │   ├── api/                   # 12 API route modules
│   │   │   ├── health.py          # Real health check (DB + scheduler)
│   │   │   ├── status.py          # Safety status (policy-aware scoring)
│   │   │   ├── recommendations.py # Actionable fix recommendations
│   │   │   ├── activity.py        # Activity event log
│   │   │   ├── scans.py           # Scan history
│   │   │   ├── settings.py        # User preferences (auth required for PUT)
│   │   │   ├── fixer.py           # Auto-fix with backup (auth + input validation)
│   │   │   ├── policy.py          # Policy CRUD (auth required for PUT)
│   │   │   ├── notifications.py   # Webhook config (auth + URL validation)
│   │   │   ├── skill.py           # OpenClaw skill interface
│   │   │   └── metrics.py         # Prometheus endpoint
│   │   ├── core/                  # Config, auth, structured logging
│   │   ├── models/                # Pydantic models (15+ schemas)
│   │   ├── services/              # Scanner, scorer, fixer, scheduler, notifications, metrics
│   │   └── db/                    # SQLite with asyncio.Lock, health check, 5 tables
│   ├── tests/                     # 15 test files, 41 tests
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile                 # Non-root user, health check
├── frontend/                      # Next.js frontend
│   ├── src/
│   │   ├── app/                   # 6 pages + error boundary
│   │   ├── components/            # 20+ components (ui, dashboard, onboarding, settings, layout)
│   │   ├── hooks/                 # useStatus, useActivity, useSettings (with backoff)
│   │   ├── lib/                   # API client (with auth), TypeScript types
│   │   ├── styles/                # Design tokens (4 theme combos)
│   │   └── i18n/                  # 130+ externalized strings
│   ├── package.json
│   └── Dockerfile                 # Non-root user, health check
├── skill/                         # OpenClaw skill reference implementation
│   └── clawsafe_skill.py
├── docker-compose.yml             # Base deployment (health checks, resource limits)
├── docker-compose.home.yml        # Home user overlay (localhost only)
├── docker-compose.smb.yml         # SMB overlay (metrics + logging)
├── docker-compose.prod.yml        # Production overlay (Caddy HTTPS)
├── .github/workflows/ci.yml       # CI: lint, test, coverage, Docker, Trivy
└── policies/                      # Example YAML policy files
    ├── default.yaml               # Secure defaults
    ├── example-home.yaml          # Home user preset
    └── example-smb.yaml           # SMB preset
```

## Key Design Decisions

- **Two personas:** "Anna" (non-technical home user) and "Ben" (tech-savvy SMB/DevOps).
  Default UX targets Anna; Advanced Settings targets Ben.
- **Theme system:** Playful (default, mascot + gradients) and Minimal (flat, no mascot).
  Both share the same information architecture. Use CSS custom properties for tokens.
  Theme persisted in localStorage (flash prevention) and backend settings.
- **Safety Status:** Three levels — Safe (green), Needs Attention (amber), At Risk (red).
  Backed by an internal numeric risk score (0-100). Policy-aware scoring adjusts weights.
- **Policy-as-code:** YAML files in `/policies/`. Validated and enforced via backend API.
  Active policy affects risk scoring in real-time.
- **API authentication:** Write endpoints require `Authorization: Bearer <key>` when
  `CLAWSAFE_API_KEY` is set. Read endpoints are always open. Disabled in dev by default.
- **No telemetry** without explicit opt-in.
- **Strings externalized** from day one for future localization.

## Development Commands

```bash
# All-in-one (via Makefile)
make install      # Install backend + frontend dependencies
make dev          # Start both in dev mode (hot reload)
make test         # Run all tests (pytest + vitest)
make lint         # Run all linters (ruff + eslint)

# Docker
make build        # Build images
make up           # Start containers
make down         # Stop containers
make prod         # Start with Caddy HTTPS
make home         # Start in home mode (localhost only)
make smb          # Start in SMB mode (with metrics)

# Manual
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
cd frontend && npm install && npm run dev
```

## Code Style

- **Python:** Follow PEP 8. Use type hints. Use ruff for linting. Wrap file I/O in try-except.
- **TypeScript:** Strict mode. Prefer functional components with hooks.
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- **Naming:** snake_case for Python, camelCase for TypeScript variables,
  PascalCase for React components and TypeScript types.
- **Security:** Validate all user input (action IDs, webhook URLs). Use auth dependency on write endpoints.

## Important Patterns

- All user-facing text must go through the i18n string system (no hardcoded strings in components).
- Every risk/alert must include a suggested next action (never show a problem without a solution).
- API endpoints are prefixed with `/api/v1/` (except `/metrics`).
- Write endpoints require `Depends(require_auth)` from `app.core.auth`.
- Action IDs must be validated with `validate_action_id()` before use.
- Webhook URLs must be validated with `validate_webhook_url()` before sending.
- Auto-fix operations must create a backup first, log changes, and support undo.
- Polling hooks use exponential backoff on API failures (30s → 300s).
- Theme changes save to localStorage (flash prevention) and backend settings.
- Use `useToast()` hook for save/error feedback.

## Documentation

- `docs/installation.md` — Docker & development setup guide
- `docs/configuration.md` — Environment variables, policy YAML format
- `docs/api-reference.md` — All API endpoints with auth requirements
- `docs/security.md` — Authentication, HTTPS, input validation, container security
- `docs/operations.md` — Backup/restore, upgrades, monitoring, troubleshooting
- `docs/contributing.md` — Development setup, code style, PR guidelines
