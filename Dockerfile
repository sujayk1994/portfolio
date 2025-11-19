# Multi-stage Dockerfile for Windows XP Portfolio (Next.js + Flask)

###########
# BUILDER - Frontend (Next.js)
###########
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production && npm install

# Copy frontend source
COPY src ./src
COPY public ./public
COPY components ./components
COPY assets ./assets
COPY fonts ./fonts
COPY next.config.js tsconfig.json ./

# Build Next.js for static export
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

###########
# BUILDER - Python Dependencies
###########
FROM python:3.11-slim AS python-builder

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy Python dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

###########
# FINAL - Production Runtime
###########
FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python virtual environment from builder
COPY --from=python-builder /app/.venv /app/.venv

# Copy Next.js build from frontend builder
COPY --from=frontend-builder /app/frontend/out ./out

# Copy backend application and configuration
COPY backend ./backend
COPY gunicorn_config.py ./
COPY wsgi.py ./
COPY start.sh ./

# Create upload directory
RUN mkdir -p backend/app/static/uploads && \
    chown -R appuser:appuser /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=backend/app.py \
    FLASK_ENV=production

# Expose port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/projects').read()" || exit 1

# Run with Gunicorn for production
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
