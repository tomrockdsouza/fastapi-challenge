# Use an official Python image as the base image
FROM python:3.11-slim

# Set the working directory within the container
WORKDIR /app

# Copy your Python project files into the container
COPY fastapi-build/requirements.txt .
COPY main.py .
COPY modules ./modules
COPY index.html .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Run FastApi when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80","--workers","4"]
