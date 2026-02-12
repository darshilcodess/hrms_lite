# HRMS Lite

FastAPI backend + PostgreSQL, with Docker and Alembic.

## Prerequisites

- Docker and Docker Compose
- For local dev (optional): Python 3.12+, copy `env_example.txt` to `.env`

## Quick start with Docker

1. **Copy env and start services**

   ```bash
   copy env_example.txt .env
   docker-compose up -d
   ```

2. **Run migrations** (first time or after adding migrations)

   From project root:

   ```bash
   docker-compose run --rm backend alembic upgrade head
   ```

3. **Try the API**

   - Hello: http://localhost:8000/
   - Health: http://localhost:8000/health
   - DB check: http://localhost:8000/health/db

## Alembic commands

Run these **inside the backend container** (so `DATABASE_URL` points at Postgres) or from **`server/`** with a local `.env` and Postgres running.

From project root (using container):

```bash
# Apply all migrations
docker-compose run --rm backend alembic upgrade head

# Create a new migration after changing models
docker-compose run --rm backend alembic revision -m "add users table"

# Roll back one revision
docker-compose run --rm backend alembic downgrade -1

# Show current revision
docker-compose run --rm backend alembic current

# Show migration history
docker-compose run --rm backend alembic history
```

From `server/` (local Python + Postgres):

```bash
cd server
# Ensure .env has DATABASE_URL=postgresql://hrms:hrms_secret@localhost:5432/hrms_lite
alembic upgrade head
alembic revision -m "add users table"
alembic downgrade -1
alembic current
alembic history
```

## Project layout

- `server/` – FastAPI app
  - `app/main.py` – app entry, hello and health routes
  - `app/core/config.py` – settings (env)
  - `app/core/database.py` – SQLAlchemy engine and session
  - `alembic/` – migrations
- `docker/` – Dockerfiles
- `docker-compose.yml` – backend + Postgres
