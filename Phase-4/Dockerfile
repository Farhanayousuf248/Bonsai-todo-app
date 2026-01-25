# syntax=docker/dockerfile:1.6
###############################
# Stage 1: Dependency Builder #
###############################
FROM python:3.11-slim AS builder

# Ensure consistent, reproducible builds
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build essentials only when needed to keep final image slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifests first to leverage Docker layer caching
COPY Phase-3/requirements.txt ./requirements.txt

# Install dependencies into user space to avoid polluting system site-packages
RUN pip install --user --no-cache-dir -r requirements.txt

####################################
# Stage 2: Runtime (non-root image) #
####################################
FROM python:3.11-slim

# Security & runtime optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/todouser/.local/bin:$PATH"

# Install only the minimal runtime packages required (curl for healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with fixed UID/GID for Kubernetes securityContext compatibility
RUN useradd -m -u 1001 -s /bin/bash todouser

WORKDIR /app

# Copy installed dependencies from builder image
COPY --from=builder /root/.local /home/todouser/.local

# Copy application source code (phase 3 implementation reused for API work)
COPY Phase-3/src ./src
COPY Phase-3/specs ./specs
COPY Phase-3/README.md ./README.md

# Set ownership to non-root user for all app files
RUN chown -R todouser:todouser /app

USER todouser

# Expose the default API port (adjust via env var if needed)
EXPOSE 8080

# Healthcheck endpoint will be implemented by Phase-4 API service
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Default command launches the Phase-3 CLI entry point (will evolve to API service)
CMD ["python", "-m", "src.main"]
