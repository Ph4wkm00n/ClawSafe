# Contributing to ClawSafe

We welcome contributions! Here's how to get started.

## Development Setup

1. Clone the repo and create a branch:
   ```bash
   git clone https://github.com/your-org/clawsafe.git
   cd clawsafe
   git checkout -b feat/your-feature
   ```

2. Install dependencies and start development:
   ```bash
   make install   # Install backend + frontend deps
   make dev       # Start both in dev mode (hot reload)
   ```

   Or manually:
   ```bash
   cd backend && pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   # In another terminal:
   cd frontend && npm install && npm run dev
   ```

## Code Style

- **Python:** PEP 8, type hints, `ruff check .` must pass
- **TypeScript:** Strict mode, `npm run lint` must pass
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- **Security:** Use `Depends(require_auth)` on write endpoints. Validate all user input.

## Running Tests

```bash
make test     # Run all tests (65 total)
make lint     # Run all linters
```

Or manually:
```bash
cd backend && pytest -v          # 41 backend tests
cd frontend && npm test          # 24 frontend tests
```

## Pull Request Guidelines

1. Keep PRs focused on a single change
2. Include tests for new functionality
3. All user-facing text must use the i18n system (`t("key")`)
4. Every risk/alert must include a suggested next action
5. Write endpoints must use `Depends(require_auth)` from `app.core.auth`
6. Validate action IDs with `validate_action_id()` and webhook URLs with `validate_webhook_url()`
7. Ensure both Playful and Minimal themes render correctly in light and dark modes
8. Use `useToast()` for save/error feedback in settings components

## Architecture

```
Frontend (Next.js) → API Client (with auth) → Backend (FastAPI) → SQLite
                                                    ↓
                                              Scanner → Scoring (policy-aware) → Status
                                              Scheduler → Metrics → Prometheus
                                              Fixer → Backup → Undo
```

## Key Files to Know

- `backend/app/core/auth.py` — API key auth dependency + input validation
- `backend/app/core/config.py` — All settings (env vars with `CLAWSAFE_` prefix)
- `backend/app/services/scoring.py` — Risk scoring logic (policy-aware)
- `frontend/src/hooks/useSettings.ts` — Theme management, localStorage persistence
- `frontend/src/i18n/en.ts` — All 130+ externalized strings

See [CLAUDE.md](../CLAUDE.md) for the full repository structure and all patterns.
