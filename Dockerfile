# ---------- Stage 1: Builder ----------
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ make libffi-dev libssl-dev python3-dev python3-venv \
    python3-setuptools python3-wheel python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: Final ----------
FROM python:3.10-slim-bullseye

WORKDIR /app

# Copy installed site-packages from builder
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

# Copy your app source code
COPY . .

# Expose Cloud Run port
EXPOSE 8080

# Start your dashboard server
CMD ["python", "app.py"]
