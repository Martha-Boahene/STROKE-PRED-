# Base image
FROM python:3.12-slim

# Update system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the app and models
COPY ./app ./app
COPY ./models ./models

# Optional: create non-root user (ensure access to /code)
RUN useradd -m myuser && chown -R myuser:myuser /code
USER myuser

# Expose default Cloud Run port
EXPOSE 8080

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
