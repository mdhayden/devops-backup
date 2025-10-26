# ✅ Multi-stage Docker build for Alpaca Trading Bot

# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages (fixes aiohttp build)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Copy only the clean production requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt


# ---------- Stage 2: Production ----------
FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash botuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/botuser/.local

# Copy application code
COPY . .

# Change ownership to botuser
RUN chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Make sure user's local bin is in PATH
ENV PATH=/home/botuser/.local/bin:$PATH

# Create necessary directories
RUN mkdir -p tick_data

# Expose port for dashboard
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/api/status')" || exit 1

# Default command to launch dashboard
CMD ["python", "localhost_dashboard.py"]
