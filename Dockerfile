# Use a full Python base that includes headers
FROM python:3.11-bullseye

WORKDIR /app

# Install everything required to build aiohttp and pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and copy dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel

# Install dependencies (use prebuilt aiohttp wheel)
RUN pip install --no-cache-dir aiohttp==3.9.5
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Default command to run
CMD ["python", "startup.py"]
