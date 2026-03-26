# Phase 0: Project Setup

Goal: Scaffold the repository, set up CI, and create a working Docker dev environment.

## Tasks

### 0.1 Backend Scaffold
- [x] Initialize `backend/` with FastAPI project structure
- [x] Create `app/main.py` with health check endpoint (`GET /api/v1/health`)
- [x] Set up `requirements.txt` (fastapi, uvicorn, pydantic, pyyaml, sqlite-utils)
- [x] Add `backend/Dockerfile` (Python 3.12 slim)
- [x] Configure ruff for linting

### 0.2 Frontend Scaffold
- [x] Initialize `frontend/` with Next.js + TypeScript (`create-next-app`)
- [x] Set up Tailwind CSS with design token CSS custom properties
- [x] Create basic app layout shell (sidebar nav + content area)
- [x] Add API client utility (`lib/api.ts`) pointing to backend
- [x] Configure Vitest + React Testing Library

### 0.3 Docker Compose
- [x] Create root `docker-compose.yml` with backend + frontend services
- [x] Add volume mounts for local dev (hot reload)
- [x] Create `docker-compose.home.yml` overlay (localhost-only, no extra ports)
- [x] Create `docker-compose.smb.yml` overlay (metrics port, log volume)

### 0.4 CI / Quality
- [x] Add GitHub Actions workflow: lint + test on PR
- [x] Add pre-commit config (ruff, eslint, prettier)
- [x] Create `.env.example` with documented variables

### 0.5 Policy Scaffold
- [x] Create `policies/` directory with example YAML files
- [x] `policies/default.yaml` - secure defaults
- [x] `policies/example-home.yaml` - home user example
- [x] `policies/example-smb.yaml` - SMB example

## Acceptance Criteria

- `docker compose up` starts both backend and frontend
- Backend responds to `/api/v1/health`
- Frontend renders the layout shell at `localhost:3000`
- CI passes lint and test checks
