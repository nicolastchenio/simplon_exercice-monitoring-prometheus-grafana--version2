FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# On copie d'abord les fichiers de configuration de uv
COPY pyproject.toml .

# On installe les dépendances avec uv
RUN uv sync --no-dev

# On copie le reste du code
COPY app.py .

# On crée le dossier de logs mentionné dans le README
RUN mkdir /logs

# On expose le port 8501
EXPOSE 8501

# On lance l'application via uv
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
