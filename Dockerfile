# Use an official lightweight Python runtime as a parent image.
# 3.13 matches the interpreter the pinned requirements.txt was frozen from (.venv = 3.13.7).
FROM python:3.13-slim

# Unbuffered logs for `docker logs`; no .pyc clutter; no pip cache in layers
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Set the working directory in the container
WORKDIR /app

# Install dependencies first for optimal Docker layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Non-root runtime user; pre-create the state directories (mounted as volumes by
# docker-compose.yml) so they are owned by that user.
RUN useradd --create-home --uid 10001 integra \
    && mkdir -p /app/kernel_memory /app/local_dbs /app/The_Hoard \
    && chown -R integra:integra /app

# Copy the rest of the application (filtered by .dockerignore — secrets/state/assets excluded)
COPY --chown=integra:integra . .

USER integra

# Expose port (Render services bind to 8000 or the PORT env var)
EXPOSE 8000

# Genesis Kernel liveness probe — GET / returns the kernel status JSON
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/' % os.environ.get('PORT','8000'), timeout=4)" || exit 1

# Start FastAPI application via Uvicorn (exec so SIGTERM reaches uvicorn for graceful shutdown)
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
