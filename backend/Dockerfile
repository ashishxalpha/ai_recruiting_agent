FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy pyproject.toml and install dependencies first (caching)
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

# Copy application source
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini .

# Expose port and start
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
