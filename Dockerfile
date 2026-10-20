# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /backend

COPY requirement.txt .

# Install dependencies into a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r requirement.txt


# Stage 2: Runtime image
FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd appuser

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Set ownership
RUN chown -R appuser:appuser /backend

USER appuser

CMD ["flask", "--app", "my_app.py", "run", "--host=0.0.0.0"]
