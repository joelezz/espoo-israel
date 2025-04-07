# Stage 1: Build dependencies
FROM python:3-alpine AS builder

WORKDIR /app

# Create virtual environment
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Run the app
FROM python:3-alpine AS runner

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/venv venv

# Copy app files (e.g., app.py, templates, static)
COPY app.py app.py
COPY templates/ templates/
COPY static/ static/

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app.py

# Expose port 8080 (for production) and use Gunicorn
EXPOSE 8080

# Run Gunicorn with 2 workers
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
