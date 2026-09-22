FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

# Create virtual environment and install dependencies
RUN python -m pip install --upgrade pip && \
    pip install flask pillow gunicorn redis celery

# Create necessary directories
RUN mkdir -p /app/output/videos \
    /app/output/scenes \
    /app/uploads \
    /app/logs

# Expose ports
EXPOSE 5000 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
