FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio (optional, for future use)
RUN apt-get update && apt-get install -y \
    gcc \
    libsdl2-dev \
    libsdl2-mixer-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]