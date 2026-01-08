FROM python:3.11-slim

# Install Tkinter + X11 runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk tk \
    libx11-6 libxext6 libxrender1 libxtst6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Create runtime dirs (also created by ensure_directories, but nice for Docker)
RUN mkdir -p /app/Archive /app/Errors /app/temp

# Default env (you can override via docker run / compose)
ENV DISPLAY=host.docker.internal:0.0

CMD ["python", "main.py"]
