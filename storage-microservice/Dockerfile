FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps needed for common Python wheels (e.g., Pillow)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libjpeg62-turbo-dev \
      zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy storage microservice source
COPY ./storage_microservice /app

# Add entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8001

CMD ["/app/entrypoint.sh"]