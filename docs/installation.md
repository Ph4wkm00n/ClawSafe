# Installation Guide

## Requirements

- Linux host (Debian/Ubuntu recommended)
- Docker and Docker Compose installed
- An existing OpenClaw instance (optional — ClawSafe can set one up)

## Quick Start with Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/your-org/clawsafe.git
cd clawsafe
```

### 2. Copy environment config

```bash
cp .env.example .env
```

Edit `.env` if you need to change ports or paths.

### 3. Start ClawSafe

**Home user (localhost only):**
```bash
docker compose -f docker-compose.yml -f docker-compose.home.yml up --build -d
```

**Small business (with metrics):**
```bash
docker compose -f docker-compose.yml -f docker-compose.smb.yml up --build -d
```

**Default:**
```bash
docker compose up --build -d
```

### 4. Open the dashboard

Navigate to [http://localhost:3000](http://localhost:3000) in your browser.

The onboarding wizard will guide you through initial setup.

## Manual Setup (Development)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Updating

Pull the latest images and restart:

```bash
git pull
docker compose down
docker compose up --build -d
```

## Troubleshooting

- **Port conflict:** Change `CLAWSAFE_PORT` in `.env`
- **Database reset:** Delete `clawsafe.db` and restart
- **Logs:** `docker compose logs -f backend`
