# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disc
# - PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
# - PORT: Default port for the Flask service (overridable, e.g., on Cloud Run)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory inside the container
WORKDIR /app

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source code and seed data
COPY app.py .
COPY data/ ./data/

# Expose the default application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

