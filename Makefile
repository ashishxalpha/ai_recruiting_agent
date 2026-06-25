.PHONY: help setup dev build test lint format clean seed reset coverage demo docs migrate

help:
	@echo "AI Recruiting Platform Developer Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make setup      - Install all dependencies (backend/frontend)"
	@echo "  make dev        - Run both backend and frontend locally using docker-compose"
	@echo "  make build      - Build all docker images"
	@echo "  make test       - Run all tests (backend/frontend)"
	@echo "  make lint       - Run linter checks"
	@echo "  make format     - Run code formatters"
	@echo "  make clean      - Clean up cache, pyc files, and node_modules"
	@echo "  make seed       - Seed the database with sample data"
	@echo "  make reset      - Drop database and re-run migrations"
	@echo "  make migrate    - Run database migrations"
	@echo "  make coverage   - Run tests and generate coverage report"
	@echo "  make demo       - Start the full platform with seeded data for demonstration"
	@echo "  make docs       - Serve MkDocs locally (if installed)"

setup:
	@echo "Installing Backend Dependencies..."
	cd backend && pip install -r requirements.txt || uv pip install -r requirements.txt
	@echo "Installing Frontend Dependencies..."
	cd frontend && npm install

dev:
	docker-compose up --build

build:
	docker-compose build

test:
	cd backend && pytest
	cd frontend && npm test

lint:
	cd backend && flake8 src tests
	cd frontend && npm run lint

format:
	cd backend && black src tests && isort src tests
	cd frontend && npm run format

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.pytest_cache
	rm -rf backend/.coverage
	rm -rf backend/htmlcov
	rm -rf frontend/node_modules
	rm -rf frontend/.next

seed:
	@echo "Seeding the database..."
	# Run the seed script inside the backend
	# docker-compose exec backend python scripts/seed.py

reset:
	@echo "Resetting database..."
	# docker-compose exec backend python scripts/reset_db.py

migrate:
	cd backend && alembic upgrade head

coverage:
	cd backend && pytest --cov=src --cov-report=html
	@echo "Coverage report generated in backend/htmlcov/index.html"

demo: reset seed dev
	@echo "Demo environment running!"

docs:
	@echo "Starting docs server..."
	# mkdocs serve
