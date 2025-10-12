FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps for psycopg2 and netcat for startup wait
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY ./StarGo/requirements.txt /app/requirements.txt
# Upgrade pip/setuptools/wheel and prefer binary wheels for faster installs
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r /app/requirements.txt

# Copy app source
COPY ./StarGo /app

# Add entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]