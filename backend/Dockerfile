# MLForge backend — production image
FROM python:3.12-slim

WORKDIR /app

# System deps: none required for our pure-Python stack (scikit-learn,
# pandas, matplotlib, reportlab, shap all ship manylinux wheels), but
# build-essential is kept as a safety net for any package that needs to
# compile from source on an unusual platform.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Persisted at runtime via a mounted volume (see docker-compose.yml) so
# uploads, trained models, and the SQLite DB survive container restarts.
RUN mkdir -p /app/data/uploads /app/data/saved_models

ENV UPLOAD_DIR=/app/data/uploads \
    SAVED_MODELS_DIR=/app/data/saved_models \
    DATABASE_URL=sqlite:////app/data/mlforge.db \
    ENVIRONMENT=production \
    PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
