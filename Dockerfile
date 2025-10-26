# ---------- Stage 1: Builder ----------
FROM python:3.11-bullseye AS builder

WORKDIR /app

# Install full build toolchain and headers for aiohttp
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
