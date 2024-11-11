# Start with a lightweight Python image based on Alpine
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install dependencies for psycopg2 and other libraries that require system packages
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        postgresql-dev \
        libffi-dev \
        openssl-dev && \
    apk add --no-cache libpq

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Remove build dependencies to keep the image light
RUN apk del .build-deps
