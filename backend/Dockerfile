FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy dependency metadata and application source
COPY pyproject.toml .
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini .

# Install after copying the package so pip can build it.
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir .

# ACA should run the application without root privileges.
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
	&& mkdir -p /storage/resumes /storage/documents /storage/temp \
	&& chown -R appuser:appuser /app /storage
USER appuser

# Expose port and start
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
