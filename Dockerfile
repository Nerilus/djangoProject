FROM python:3.9-slim

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for OpenSSL
ENV LDFLAGS="-L/usr/local/opt/openssl/lib"
ENV CPPFLAGS="-I/usr/local/opt/openssl/include"
ENV PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

COPY django.sh /app/

# Make the entrypoint script executable
RUN chmod +x /app/django.sh

# Expose port
EXPOSE 8000

# Use the script as the entrypoint
ENTRYPOINT ["/app/django.sh"]
