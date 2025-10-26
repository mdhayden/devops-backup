# ---------- Stage 1: Builder ----------
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install build dependencies for aiohttp and pandas
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    python3-dev \
    python3-venv \
    python3-setuptools \
    python3-wheel \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: Production ----------
FROM python:3.11-slim-bullseye

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash botuser
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code
COPY . .

# Change ownership and permissions
RUN chown -R botuser:botuser /app
USER botuser

# Ensure correct PATH
ENV PATH="/usr/local/bin:$PATH"

# Optional: create runtime data directory
RUN mkdir -p tick_data

# Expose Cloud Run port
EXPOSE 8080

# Health check (Cloud Run friendly)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/api/status')" || exit 1

# Start the dashboard
CMD ["python", "localhost_dashboard.py"]
