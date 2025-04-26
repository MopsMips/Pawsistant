# Dockerfile

# Leichtgewichtiger Python-Image für ARM (Raspberry Pi)
FROM python:3.11-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Benötigte Dateien kopieren
COPY . /app

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# .env Datei wird erwartet (kann über docker-compose bereitgestellt werden)

# Bot starten
CMD ["python", "bot.py"]
