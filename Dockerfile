# syntax=docker/dockerfile:1
FROM python:3.12-slim

# No .pyc files, unbuffered logs (so `docker logs` shows output immediately)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /srv

# Install dependencies first so this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ ./app/

# Run as a non-root user
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# Container reports healthy only when /health answers (uses stdlib, no curl needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/health', timeout=2)" || exit 1

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 app.app:app"]
