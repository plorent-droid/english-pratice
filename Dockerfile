# HF Spaces (Docker) exécute le conteneur et attend un service sur le port 7860.
FROM python:3.11-slim

# Dépendances système nécessaires à faster-whisper (ffmpeg) et à la compilation de llama-cpp-python
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

# HF Spaces exige un utilisateur non-root et un HOME inscriptible pour le cache HF
RUN useradd -m -u 1000 hfuser
ENV HOME=/home/hfuser
ENV HF_HOME=/home/hfuser/.cache/huggingface
RUN mkdir -p $HF_HOME && chown -R hfuser:hfuser /code /home/hfuser
USER hfuser

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]