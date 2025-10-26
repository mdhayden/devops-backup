# ---------- Stage 1: Builder ----------
FROM python:3.11-bullseye AS builder

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Stage 2: Production ----------
FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash botuser
WORKDIR /app

# Copy dependencies
COPY --from=builder /root/.local /home/botuser/.local
COPY . .

# Permissions
RUN chown -R botuser:botuser /app
USER botuser

ENV PATH=/home/botuser/.local/bin:$PATH
RUN mkdir -p tick_data

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/api/status')" || exit 1

CMD ["python", "localhost_dashboard.py"]
