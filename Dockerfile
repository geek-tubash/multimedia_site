# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables to ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for PostgreSQL and compiling some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies (using --no-cache-dir to reduce image size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project into the container
COPY . /app/

# Set up static files handling via WhiteNoise (to serve static files in production)
# This command runs 'collectstatic' to gather static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 to make the application accessible outside the container
EXPOSE 8000

# Command to run Gunicorn to serve the Django application (binding it to port 8000)
CMD ["gunicorn", "multimedia_project.wsgi:application", "--bind", "0.0.0.0:8000"]
