# Run from project root. Requires Docker Compose and (for alembic) backend image.

.PHONY: up down build logs shell alembic-up alembic-revision alembic-current alembic-history

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

shell:
	docker-compose run --rm backend bash

# Alembic: run inside backend container (uses DATABASE_URL from compose)
alembic-up:
	docker-compose run --rm backend alembic upgrade head

# Usage: make alembic-revision msg="add users table"
alembic-revision:
	docker-compose run --rm backend alembic revision -m "$(msg)"

alembic-current:
	docker-compose run --rm backend alembic current

alembic-history:
	docker-compose run --rm backend alembic history
