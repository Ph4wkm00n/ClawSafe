# Installation Guide

## Requirements

- Linux host (Debian/Ubuntu recommended)
- Docker and Docker Compose installed
- An existing OpenClaw instance (optional — ClawSafe works in demo mode without one)

## Quick Start with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
```

### 2. Copy and configure environment

```bash
cp .env.example .env
```

Edit `.env` to configure:
- `CLAWSAFE_API_KEY` — set a secret key for production (leave empty for development)
- `CLAWSAFE_DEMO_MODE` — set to `false` in production
- `CLAWSAFE_PORT` — change backend port if needed (default: 8000)

### 3. Start ClawSafe

**Using the Makefile (recommended):**

```bash
make up        # Default mode
make home      # Home user (localhost only)
make smb       # Small business (with Prometheus metrics)
make prod      # Production (Caddy reverse proxy with HTTPS)
```

**Or with Docker Compose directly:**

```bash
# Default
docker compose up --build -d

# Home user (localhost only)
docker compose -f docker-compose.yml -f docker-compose.home.yml up --build -d

# Small business (with metrics)
docker compose -f docker-compose.yml -f docker-compose.smb.yml up --build -d

# Production (with Caddy HTTPS)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### 4. Open the dashboard

Navigate to [http://localhost:3000](http://localhost:3000) in your browser.

The onboarding wizard will guide you through initial setup on first visit.

### 5. Verify health

```bash
curl http://localhost:8000/api/v1/health
```

Should return:
```json
{"status": "ok", "version": "1.0.0", "checks": {"database": "ok", "scheduler": "ok"}}
```

## Production Deployment

For production, set these in `.env`:

```bash
CLAWSAFE_API_KEY=your-secure-random-key
CLAWSAFE_DEMO_MODE=false
```

Then use the production overlay with Caddy for automatic HTTPS:

```bash
make prod
```

Edit `Caddyfile` to set your domain name (replace `:80` with `clawsafe.yourdomain.com`).

See the [Security Guide](security.md) for full production hardening.

## Manual Setup (Development)

**Using the Makefile:**
```bash
make install   # Install all dependencies
make dev       # Start backend + frontend (hot reload)
make test      # Run all tests
make lint      # Run linters
```

**Or manually:**

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Updating

```bash
git pull
docker compose down
docker compose up --build -d
```

See the [Operations Guide](operations.md) for detailed upgrade and backup procedures.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port conflict | Change `CLAWSAFE_PORT` in `.env` |
| Database reset | Delete `clawsafe.db` and restart |
| Backend won't start | Check `docker compose logs -f backend` |
| Frontend can't reach backend | Verify `NEXT_PUBLIC_API_URL` in `.env` |
| Settings not saving | Verify `CLAWSAFE_API_KEY` matches `NEXT_PUBLIC_API_KEY` |
| Health check failing | Ensure database path is writable |

See the [Operations Guide](operations.md) for more troubleshooting tips.
