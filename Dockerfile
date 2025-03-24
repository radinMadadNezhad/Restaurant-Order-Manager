FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USE_POSTGRES=True
ENV PORT=8080

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run using Procfile with buffering settings
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn restaurant_management.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 60 --access-logfile - --log-level warning"] 