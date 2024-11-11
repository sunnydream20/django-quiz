# Use the official Python 3.8 image from Docker Hub
FROM python:3.8-slim

# Set environment variables to prevent Python from writing pyc files to disc and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project into the container
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Command to run the application
CMD ["gunicorn", "quiz_system.wsgi:application", "--bind", "0.0.0.0:8000"]

# Expose the port the app runs on
EXPOSE 8000
