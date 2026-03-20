.PHONY: setup migrate seed dev-backend dev-frontend test build

setup:
	docker compose up -d db
	@echo "Waiting for database..."
	@sleep 3
	$(MAKE) migrate
	$(MAKE) seed
	@echo "✅ Setup complete! Run 'make dev-backend' to start."

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python scripts/seed_db.py

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -v

build:
	docker compose build
