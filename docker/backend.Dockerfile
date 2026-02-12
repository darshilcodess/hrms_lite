# backend.Dockerfile - FastAPI app
FROM python:3.12-slim

WORKDIR /app

# Install system deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for better layer caching
COPY server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ .

# Run as non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
