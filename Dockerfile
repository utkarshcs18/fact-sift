# ============================================================
# Fact-Sift  –  Multi-stage Dockerfile
# ============================================================
# Build:   docker build -t fact-sift .
# Run:     docker run -p 8000:8000 fact-sift
# ============================================================

# ---- Stage 1: builder ----
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: runtime ----
FROM python:3.12-slim

LABEL maintainer="fact-sift"
LABEL description="Evidence-based claim verification system"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY backend/ ./backend/
COPY src/ ./src/

# Expose the API port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
