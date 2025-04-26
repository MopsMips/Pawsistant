# Dockerfile

# Leichtgewichtiger Python-Image für ARM (Raspberry Pi)
FROM python:3.11-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Projektdateien kopieren
COPY . /app

# Python-Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Startbefehl
CMD ["python", "bot.py"]
