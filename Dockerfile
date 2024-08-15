# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory and copy requirements
WORKDIR /app
COPY ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# Copy the Django project
COPY ./app /app

# Expose the port
EXPOSE 8888

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
