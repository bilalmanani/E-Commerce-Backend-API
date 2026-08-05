# ==========================================
# Stage 1: Builder Stage (Install Dependencies)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files & enable unbuffered stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies manifest
COPY requirements.txt .

# Install Python packages into a virtual environment in /app/venv
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Final Production Stage (Minimal Image)
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

# Install lightweight runtime PostgreSQL C-libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /app/venv /app/venv

# Copy application source code
COPY . .

# Expose FastAPI application port
EXPOSE 8000

# Command to run Uvicorn production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
