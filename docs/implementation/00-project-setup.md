# Phase 0: Project Setup

Goal: Scaffold the repository, set up CI, and create a working Docker dev environment.

## Tasks

### 0.1 Backend Scaffold
- [ ] Initialize `backend/` with FastAPI project structure
- [ ] Create `app/main.py` with health check endpoint (`GET /api/v1/health`)
- [ ] Set up `requirements.txt` (fastapi, uvicorn, pydantic, pyyaml, sqlite-utils)
- [ ] Add `backend/Dockerfile` (Python 3.12 slim)
- [ ] Configure ruff for linting

### 0.2 Frontend Scaffold
- [ ] Initialize `frontend/` with Next.js + TypeScript (`create-next-app`)
- [ ] Set up Tailwind CSS with design token CSS custom properties
- [ ] Create basic app layout shell (sidebar nav + content area)
- [ ] Add API client utility (`lib/api.ts`) pointing to backend
- [ ] Configure Vitest + React Testing Library

### 0.3 Docker Compose
- [ ] Create root `docker-compose.yml` with backend + frontend services
- [ ] Add volume mounts for local dev (hot reload)
- [ ] Create `docker-compose.home.yml` overlay (localhost-only, no extra ports)
- [ ] Create `docker-compose.smb.yml` overlay (metrics port, log volume)

### 0.4 CI / Quality
- [ ] Add GitHub Actions workflow: lint + test on PR
- [ ] Add pre-commit config (ruff, eslint, prettier)
- [ ] Create `.env.example` with documented variables

### 0.5 Policy Scaffold
- [ ] Create `policies/` directory with example YAML files
- [ ] `policies/default.yaml` - secure defaults
- [ ] `policies/example-home.yaml` - home user example
- [ ] `policies/example-smb.yaml` - SMB example

## Acceptance Criteria

- `docker compose up` starts both backend and frontend
- Backend responds to `/api/v1/health`
- Frontend renders the layout shell at `localhost:3000`
- CI passes lint and test checks
