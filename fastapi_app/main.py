import psutil
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from loguru import logger
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from starlette.responses import Response

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

app = FastAPI(title="API Monitoring Simplon", version="1.0.0")

# --- Configuration Prometheus ---
# Un Counter ne fait qu'augmenter (nombre total de requêtes)
REQUEST_COUNT = Counter("app_requests_total", "Nombre total de requêtes reçues", ["method", "endpoint"])
# Un Gauge peut monter ou descendre (mesure instantanée comme le CPU)
CPU_USAGE = Gauge("system_cpu_usage", "Pourcentage d'utilisation instantanée du CPU")

# --- Configuration Loguru ---
# On configure le logger pour écrire dans le dossier partagé /logs monté via Docker
logger.add("/logs/api.log", rotation="500 MB", level="INFO", backtrace=True, diagnose=True)

@app.get("/")
async def root():
    """Point d'entrée racine pour tester si l'API est en ligne.
    
    Returns:
        dict: Un dictionnaire indiquant le statut de l'API.
    """
    # On incrémente le compteur pour chaque appel sur la racine
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    logger.info("Accès à la racine de l'API")
    return {"status": "up"}

@app.post("/predict")
async def predict(data: str = Form(...)):
    """Simule une prédiction et enregistre l'appel dans les métriques.

    Args:
        data (str): La donnée brute reçue via un formulaire (python-multipart).

    Returns:
        dict: Un résultat de prédiction simulé.
    """
    # Crucial pour le monitoring : on compte l'appel à l'endpoint /predict
    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()
    logger.info(f"Requête de prédiction reçue. Donnée : {data}")
    return {"prediction": "Valeur prédite", "value": 450}

@app.get("/metrics")
async def metrics():
    """Endpoint exposé pour que Prometheus vienne 'scraper' les données.

    Cet endpoint transforme les mesures internes en format texte compréhensible par Prometheus.

    Returns:
        Response: Une réponse au format OpenMetrics (CONTENT_TYPE_LATEST).
    """
    # Mise à jour de la jauge CPU juste avant l'exposition des métriques
    CPU_USAGE.set(psutil.cpu_percent())
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health_check():
    logger.debug("Sonde uptime kuma")
    return {"status":"ok", "message":"ok"}
