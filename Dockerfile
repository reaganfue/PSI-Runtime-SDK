# Multi-stage build for enterprise-grade PSI Runtime SDK
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash psi

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml setup.py ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PATH="/home/psi/.local/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash psi

# Switch to non-root user
USER psi
WORKDIR /home/psi

# Copy installed packages from builder
COPY --from=builder --chown=psi:psi /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder --chown=psi:psi /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=psi:psi . /home/psi/app

# Set work directory to app
WORKDIR /home/psi/app

# Install the package for the user
RUN pip install --user -e .

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5000}/api/model/status || exit 1

# Expose port
EXPOSE 5000

# Default command
CMD ["python", "app.py"]