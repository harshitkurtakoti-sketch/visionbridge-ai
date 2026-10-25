# VisionBridge AI - Docker Container
# Compatible with AWS App Runner, ECS, Render, Hugging Face Spaces & GCP Cloud Run
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies for OpenCV and Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Expose default Streamlit port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch application
CMD ["streamlit", "run", "VisionBridgeAI/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
