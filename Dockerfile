FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


FROM base AS scraper

COPY --from=builder /install /usr/local

# Install Playwright browsers (Chromium only — saves ~1 GB vs all)
RUN playwright install chromium \
    && playwright install-deps chromium

COPY scrapy/ ./scrapy/
COPY scrapy.cfg .

HEALTHCHECK --interval=60s --timeout=10s --retries=3 \
    CMD scrapy version || exit 1

ENTRYPOINT ["scrapy", "crawl"]
CMD ["indeed"]

FROM base AS api

COPY --from=builder /install /usr/local

COPY api/ ./api/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY .env.example .env

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]


FROM base AS worker

COPY --from=builder /install /usr/local

COPY worker/ ./worker/
COPY scrapy/ ./scrapy/
COPY scrapy.cfg .

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD celery -A worker.celery_app inspect ping || exit 1

CMD ["celery", "-A", "worker.celery_app", "worker", \
     "--loglevel=info", "--concurrency=4", "-Q", "scraping,default"]


FROM base AS beat

COPY --from=builder /install /usr/local

COPY worker/ ./worker/

CMD ["celery", "-A", "worker.celery_app", "beat", \
     "--loglevel=info", "--scheduler", "celery.beat:PersistentScheduler"]