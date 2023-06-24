# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project
COPY . .

# Set environment variables for PostgreSQL and Redis
ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV SECRET_KEY=${SECRET_KEY}

# Run migrations and start Gunicorn
CMD python manage.py migrate && gunicorn <bank>.wsgi:application --bind 0.0.0.0:8000