FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ make libffi-dev libssl-dev python3-dev python3-venv \
    python3-setuptools python3-wheel python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
