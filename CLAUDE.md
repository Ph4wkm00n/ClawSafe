# ClawSafe - Claude Code Guidelines

## Project Overview

ClawSafe is a self-hosted security sidecar for OpenClaw. It helps home users and
small businesses secure, monitor, and understand their OpenClaw instances through
a friendly, non-technical dashboard with advanced options for power users.

**Status:** Pre-release (v0.1) - greenfield project, implementation starting.

## Tech Stack

- **Backend:** Python (FastAPI) - lightweight API server
- **Frontend:** Next.js (React) with TypeScript
- **Styling:** Tailwind CSS with a design token system (playful/minimal themes, light/dark modes)
- **Packaging:** Docker images + Docker Compose
- **Config:** YAML files for policies and settings
- **Database:** SQLite (local, lightweight) for activity logs and state
- **Testing:** pytest (backend), Vitest + React Testing Library (frontend)

## Repository Structure

```
ClawSafe/
├── CLAUDE.md                  # This file
├── README.md                  # Project readme
├── docs/                      # Documentation
│   ├── implementation/        # Implementation plan (split by phase)
│   └── ui-ux/                 # UI/UX design specs (split by screen)
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py            # App entrypoint
│   │   ├── api/               # API route modules
│   │   ├── core/              # Config, security, constants
│   │   ├── models/            # Pydantic models
│   │   ├── services/          # Business logic (scanner, fixer, etc.)
│   │   └── db/                # SQLite models and migrations
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js app router pages
│   │   ├── components/        # Reusable UI components
│   │   ├── lib/               # Utilities, API client, hooks
│   │   ├── styles/            # Theme tokens, globals
│   │   └── i18n/              # String externalization (for future l10n)
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml         # Default secure deployment
├── docker-compose.home.yml    # Home user overlay
├── docker-compose.smb.yml     # SMB overlay
└── policies/                  # Example YAML policy files
```

## Key Design Decisions

- **Two personas:** "Anna" (non-technical home user) and "Ben" (tech-savvy SMB/DevOps).
  Default UX targets Anna; Advanced Settings targets Ben.
- **Theme system:** Playful (default, mascot + gradients) and Minimal (flat, no mascot).
  Both share the same information architecture. Use CSS custom properties for tokens.
- **Safety Status:** Three levels - Safe (green), Needs Attention (amber), At Risk (red).
  Backed by an internal numeric risk score.
- **Policy-as-code:** YAML files in `/policies/` directory. Validated via backend API.
- **No telemetry** without explicit opt-in.
- **Strings externalized** from day one for future localization.

## Development Commands

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install
npm run dev    # starts on port 3000

# Docker (full stack)
docker compose up --build

# Tests
cd backend && pytest
cd frontend && npm test

# Linting
cd backend && ruff check .
cd frontend && npm run lint
```

## Code Style

- **Python:** Follow PEP 8. Use type hints. Use ruff for linting.
- **TypeScript:** Strict mode. Prefer functional components with hooks.
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- **Naming:** snake_case for Python, camelCase for TypeScript variables,
  PascalCase for React components and TypeScript types.

## Important Patterns

- All user-facing text must go through the i18n string system (no hardcoded strings in components).
- Every risk/alert must include a suggested next action (never show a problem without a solution).
- API endpoints are prefixed with `/api/v1/`.
- Use plain language in all user-facing copy. Avoid jargon; when technical terms are needed, include a short explanation.
- Auto-fix operations must log changes and support undo where feasible.

## Documentation

- `docs/implementation/` - Implementation plan split by milestone
- `docs/ui-ux/` - UI/UX design specs split by screen/component
- PRD: `ClawSafe – Product Requirements Document (PRD).md`
- Original UI spec: `ClawSafe – UI - UX Design.md`
