.PHONY: install dev test lint build prod clean migrate seed

install: ## Install dependencies for local development
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev: ## Start backend and frontend in development mode
	@echo "Starting backend on :8000 and frontend on :3000..."
	cd backend && uvicorn app.main:app --reload --port 8000 &
	cd frontend && npm run dev &
	@echo "ClawSafe running at http://localhost:3000"

test: ## Run all tests
	cd backend && python -m pytest tests/ -v
	cd frontend && npm test

lint: ## Run linters
	cd backend && ruff check .
	cd frontend && npm run lint

build: ## Build Docker images
	docker compose build

up: ## Start with Docker Compose
	docker compose up -d

down: ## Stop Docker Compose
	docker compose down

prod: ## Start production mode (with HTTPS via Caddy)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

home: ## Start in home user mode (localhost only)
	docker compose -f docker-compose.yml -f docker-compose.home.yml up -d

smb: ## Start in SMB mode (with metrics)
	docker compose -f docker-compose.yml -f docker-compose.smb.yml up -d

migrate: ## Run database migrations manually
	cd backend && python -c "import asyncio; from app.db.database import get_db; asyncio.run(get_db()); print('Migrations applied.')"

seed: ## Seed demo data for development
	cd backend && CLAWSAFE_DEMO_MODE=true python -c "import asyncio; from app.db.database import get_db; from app.services.activity import seed_demo_activity; asyncio.run(get_db()); asyncio.run(seed_demo_activity()); print('Demo data seeded.')"

clean: ## Remove containers, volumes, and build artifacts
	docker compose down -v
	rm -rf backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/.next frontend/node_modules

helm-install: ## Install ClawSafe via Helm
	helm install clawsafe ./helm/clawsafe

helm-upgrade: ## Upgrade ClawSafe Helm release
	helm upgrade clawsafe ./helm/clawsafe

helm-template: ## Render Helm templates (dry-run)
	helm template clawsafe ./helm/clawsafe

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
