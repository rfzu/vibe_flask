# Yandex Cloud / Container Registry
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8080

# Yandex Serverless Containers часто используют PORT=8080
ENV PORT=8080
CMD exec gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 2 --timeout 60 wsgi:app
