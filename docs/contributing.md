# Contributing to ClawSafe

We welcome contributions! Here's how to get started.

## Development Setup

1. Clone the repo and create a branch:
   ```bash
   git clone https://github.com/your-org/clawsafe.git
   cd clawsafe
   git checkout -b feat/your-feature
   ```

2. Start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

3. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Code Style

- **Python:** PEP 8, type hints, `ruff check .` must pass
- **TypeScript:** Strict mode, `npm run lint` must pass
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)

## Running Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

## Pull Request Guidelines

1. Keep PRs focused on a single change
2. Include tests for new functionality
3. All user-facing text must use the i18n system (`t("key")`)
4. Every risk/alert must include a suggested next action
5. Ensure both Playful and Minimal themes render correctly

## Project Structure

See [CLAUDE.md](../CLAUDE.md) for the full repository structure and patterns.
