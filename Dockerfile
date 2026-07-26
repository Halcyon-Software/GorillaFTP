FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PyQt6 display
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxkbcommon0 \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application with display support
CMD ["python", "main.pyw"]
