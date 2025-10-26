# ---------- Stage 1: Builder ----------
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install system dependencies for aiohttp build
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

# Copy requirements
COPY requirements.txt .

# Upgrade pip & wheel
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
