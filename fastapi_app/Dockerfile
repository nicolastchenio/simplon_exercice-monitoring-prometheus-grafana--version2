FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# On copie d'abord les fichiers de configuration de uv
COPY pyproject.toml .

# On installe les dépendances avec uv
RUN uv sync --no-dev

# On copie le reste du code
COPY main.py .

# On crée le dossier de logs mentionné dans le README
RUN mkdir /logs

# On expose le port 8080
EXPOSE 8080

# On lance l'application via uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
