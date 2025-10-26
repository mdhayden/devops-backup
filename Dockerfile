FROM python:3.10-slim-bullseye

WORKDIR /app

# Install dependencies required to build aiohttp, pandas, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run the dashboard
CMD ["python", "localhost_dashboard.py"]
