# Use an official Python image as the base image
FROM python:3.11-slim

# Set the working directory within the container
WORKDIR /app

# Copy your Python project files into the container
COPY alembic-build/requirements.txt .
COPY modules/models.py ./modules/models.py
COPY modules/database.py ./modules/database.py
COPY alembic.ini .
COPY check-port-alembic.py .
COPY alembic ./alembic

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Run Alembic migrations when the container starts
CMD ["python3", "check-port-alembic.py"]
