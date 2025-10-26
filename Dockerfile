# ---------- Stage 1: Builder ----------
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install lightweight build deps only
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade essential build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies to system (not user dir)
RUN pip install --no-cache-dir -r requirements.txt
